"""
Python translation of METH_BSousa_v11.R (MeTHODICAL v11)
Converted by GitHub Copilot.

Usage: functions accept numpy arrays or nested lists. Columns are 0-based in Python.
"""

import numpy as np
import pandas as pd

# This is to avoid zeros and then divisions by 0 
MINSUM_TOPSIS = 1e-99

def aux_step03_weight_of_norm_matrix(in_matrix, in_weight):
    arr = np.array(in_matrix, dtype=float)
    out = arr.copy()
    nrows, ncols = arr.shape
    iMcalc = arr[:, 1:]
    aMmul = np.tile(np.array(in_weight, dtype=float), (nrows, 1))
    auxCalc = iMcalc * aMmul
    out[:, 1:] = auxCalc
    return out


def aux_step02_VEC_Normalization(in_matrix):
    arr = np.array(in_matrix, dtype=float)
    nrows, ncols = arr.shape
    iMcalc = arr[:, 1:]

    auxSum = np.sum(iMcalc ** 2, axis=0) + MINSUM_TOPSIS
    auxCalc = iMcalc / np.sqrt(auxSum)

    out = arr.copy()
    out[:, 1:] = auxCalc
    return out


def calcRscorev10(inM, alpha=0.5, omega=0.5):
    arr = np.array(inM, dtype=float)
    # expecting columns: id, benDist, costDist
    ids = arr[:, 0]
    ben = arr[:, 1]
    cost = arr[:, 2]
    rscore = np.sqrt(ben + cost)
    return np.column_stack((ids, rscore))


def calcDist_METHODICALv10b(in_matrix, in_ideal, in_min, in_max, BenCriteria=True, ign_first_col=True):
    arr = np.array(in_matrix, dtype=float)
    nrows, _ = arr.shape

    if ign_first_col:
        iMcalc = arr[:, 1:]
    else:
        iMcalc = arr.copy()

    def fCalcAux(column_values):
        auxMean = np.mean(column_values)
        auxSD = np.var(column_values, ddof=1)
        if BenCriteria:
            SDMean = auxMean + auxSD
        else:
            SDMean = auxMean - auxSD
        return SDMean

    SDMean = np.apply_along_axis(fCalcAux, 0, iMcalc)

    mSDMean = np.tile(SDMean, (nrows, 1))
    mIdeal = np.tile(np.array(in_ideal, dtype=float), (nrows, 1))
    mMax = np.tile(np.array(in_max, dtype=float), (nrows, 1))
    mMin = np.tile(np.array(in_min, dtype=float), (nrows, 1))

    Yaux = (iMcalc - mIdeal) ** 2
    auxDeno = np.abs(mIdeal - mSDMean) + 0.001

    auxCalcM = Yaux / auxDeno
    auxCalcM = np.nan_to_num(auxCalcM, nan=0.0, posinf=0.0, neginf=0.0)

    auxCalc = auxCalcM.sum(axis=1)

    outMat = np.empty((nrows, 2), dtype=float)
    outMat[:, 0] = arr[:, 0]
    outMat[:, 1] = auxCalc
    return outMat


def METH_METHODICALv11(iM, iVecWei, rngBEN=None, rngCost=None, rngWBen=None, rngWCost=None, MeTHBeta=0.5, MeTHOmega=0.5, itry=1):
    """
    iM: 2D array-like (rows x cols). First column is an identifier.
    iVecWei: 1D weights vector.

    rngBEN, rngCost, rngWBen, rngWCost: zero-based indices or lists of indices.
    Defaults are chosen to reflect the original R defaults (adjusted to 0-based).
    """
    arr = np.array(iM, dtype=float)
    nrows, ncols = arr.shape

    # default ranges (0-based) matching R defaults: rngBEN=1:5 -> cols 0..4 (incl.)
    if rngBEN is None:
        rngBEN = list(range(0, 5))
    if rngCost is None:
        rngCost = 5
    if rngWBen is None:
        rngWBen = list(range(0, 4))
    if rngWCost is None:
        rngWCost = 4

    # ensure rngCost and weight indices are lists
    if isinstance(rngCost, int):
        rngCost_idx = [rngCost]
    else:
        rngCost_idx = list(rngCost)

    if isinstance(rngWBen, int):
        rngWBen_idx = [rngWBen]
    else:
        rngWBen_idx = list(rngWBen)

    if isinstance(rngWCost, int):
        rngWCost_idx = [rngWCost]
    else:
        rngWCost_idx = list(rngWCost)

    # Select benefit and cost matrices
    mBen_Criteria = arr[:, rngBEN]
    # include id (column 0) plus cost columns
    cols_for_cost = [0] + rngCost_idx
    mCost_Criteria = arr[:, cols_for_cost]

    vBen_weight = np.array(iVecWei)[rngWBen_idx]
    vCost_weight = np.array(iVecWei)[rngWCost_idx]

    applyWeight = True
    applyNorm = True
    norm_method = "vector"

    # Step 01: normalization
    MeTHTOPsisBenefits = np.array(mBen_Criteria, dtype=float)
    MeTHTOPsisCosts = np.array(mCost_Criteria, dtype=float)

    if applyNorm:
        if norm_method == "vector":
            MeTHTOPsisBenefits = aux_step02_VEC_Normalization(MeTHTOPsisBenefits)
            MeTHTOPsisCosts = aux_step02_VEC_Normalization(MeTHTOPsisCosts)

    if applyWeight:
        MeTHTOPsisBenefits = aux_step03_weight_of_norm_matrix(MeTHTOPsisBenefits, vBen_weight)
        MeTHTOPsisCosts = aux_step03_weight_of_norm_matrix(MeTHTOPsisCosts, vCost_weight)

    # Step 02: retrieve max/min
    rngBBen = list(range(1, MeTHTOPsisBenefits.shape[1]))
    rngCCost = list(range(1, MeTHTOPsisCosts.shape[1]))

    MeTHMaxIdeal = np.max(MeTHTOPsisBenefits[:, rngBBen], axis=0)
    MeTHBenMin = np.min(MeTHTOPsisBenefits[:, rngBBen], axis=0)
    MeTHBenMax = MeTHMaxIdeal

    MeTHMinIdeal = np.min(MeTHTOPsisCosts[:, rngCCost], axis=0)
    MeTHCostMax = np.max(MeTHTOPsisCosts[:, rngCCost], axis=0)
    MeTHCostMin = MeTHMinIdeal

    MeTHBenDist = calcDist_METHODICALv10b(MeTHTOPsisBenefits, MeTHMaxIdeal, MeTHBenMin, MeTHBenMax, BenCriteria=True)
    MeTHCostDist = calcDist_METHODICALv10b(MeTHTOPsisCosts, MeTHMinIdeal, MeTHCostMin, MeTHCostMax, BenCriteria=False)

    inMatForR = MeTHBenDist
    inMatForR = np.column_stack((inMatForR, MeTHCostDist[:, 1]))

    MeTHRScore = calcRscorev10(inMatForR, MeTHBeta, MeTHOmega)

    orderRet = MeTHRScore[np.argsort(MeTHRScore[:, 1])]
    return orderRet


#if __name__ == "__main__":
    # Quick syntax/test example (not a comprehensive test): create a tiny matrix and run the function
    #sample = np.array([
        #[1, 0.2, 0.3, 0.5, 0.6, 0.7],
        #[2, 0.4, 0.1, 0.8, 0.2, 0.9],
    #])
    #weights = [0.25, 0.25, 0.25, 0.25, 0.0]
    #res = METH_METHODICALv11(sample, weights)
    #print(res)
if __name__ == "__main__":

    import pandas as pd
    import numpy as np

    df = pd.read_csv("iiot_methodical_matrix_table7.csv")

    df = df.rename(columns={
        "Security Strength": "SecurityStrength",
        "Energy Efficiency": "EnergyEfficiency",
        "IoT Suitability": "IIoTSuitability",
        "Memory Cost": "MemoryCost"
    })

    sample = df[
        ["ID", "SecurityStrength", "Standardization",
         "EnergyEfficiency", "IIoTSuitability", "MemoryCost"]
    ].values

    id_to_alg = dict(zip(df["ID"], df["Algorithm"]))

    scenarios = {
        "S0_baseline":          [0.28,0.15,0.22,0.20,0.15],
        "S1_security_first":    [0.45,0.25,0.10,0.15,0.05],
        "S2_constrained_first": [0.05,0.05,0.40,0.25,0.25],
        "S3_deployment_first":  [0.30,0.35,0.10,0.15,0.10],
        "S4_equal_weights":     [0.20,0.20,0.20,0.20,0.20],

    }

    with open("scenario_results.txt", "w", encoding="utf-8") as f:

        for scenario_name, weights in scenarios.items():

            print("Running:", scenario_name)
            f.write("\n===================================\n")
            f.write(f"{scenario_name}\n")
            f.write(f"Weights: {weights}\n")
            f.write("Ranking (lower RScore = better):\n")

            res = METH_METHODICALv11(
                sample,
                weights,
                rngBEN=[0, 1, 2, 3, 4],
                rngCost=[5],
                rngWBen=[0, 1, 2, 3],
                rngWCost=4
            )

            for rank, row in enumerate(res, start=1):
                _id = int(row[0])
                score = float(row[1])
                line = f"Rank {rank}: {_id} - {id_to_alg[_id]} | RScore = {score:.6f}"
                print(line)
                f.write(line + "\n")





        

        

