# METHODICAL-LWC-IoT-Ranking
METHODICAL: Multi-Criteria Ranking Framework for Lightweight Symmetric Encryption in IoT
1. Overview
This repository provides the reproducible Python implementation of the multi-criteria ranking methodology proposed in the paper: “**Symmetric Encryption for Secure Resource-Constrained Devices**”

The Methodology evaluates and ranks lightweight symmetric encryption algorithms across heterogeneous IoT devices using a structured decision-making approach based on:

1) Security strength
2) Standardization maturity
3) Energy efficiency
4) IoT and IIoT suitability
5) Memory cost
The implementation is a Python translation of the original R-based METHODICAL model and enables transparent, scenario-based ranking of candidate algorithms under different deployment priorities.

2. Repository Structure
METHODICAL-LWC-IoT-Ranking/

src/methodical.py

data/iiot_methodical_matrix_table7.csv

results/scenario_results.txt

requirements.txt

CITATION.cff

LICENSE

README.md

4. Installation
This project requires Python 3.8+.

Step 1: Clone the repository
git clone (https://github.com/Saadk459/METHODICAL-LWC-IoT-Ranking)

cd METHODICAL-LWC-IoT-Ranking

Step 2: Install dependencies

pip install -r requirements.txt

Required libraries:
numpy
pandas

4. How to Run

Ensure that the input dataset file:

iiot_methodical_matrix_table7.csv
is located in the correct directory (or update the path in the script).

Then run:
python src/methodical.py

The script will:
Load the evaluation matrix

Apply normalization

Apply criterion weights

Compute benefit and cost distances

Calculate final RScore values

Rank algorithms for each defined scenario

5. Input and Output Description

Input

The input CSV file must contain the following columns:

1) ID
2) Algorithm
3) Security Strength
4) Standardization
5) Energy Efficiency
6) IoT Suitability
7) Memory Cost
Each row represents one candidate encryption algorithm.

Scenarios

The implementation includes predefined weight scenarios:

S0_baseline

S1_security_first

S2_constrained_first

S3_deployment_first

S4_equal_weights

Each scenario defines a different priority distribution across evaluation criteria.

Output

The script generates:

scenario_results.txt

For each scenario, it prints:

Rank X: ID - Algorithm | RScore = value

Lower RScore values indicate better overall ranking under the selected scenario.

6. Methodological Notes

The implemented process includes:

Vector normalization

Weight application

Ideal solution identification

Benefit and cost distance computation

Final ranking score calculation

The methodology supports benefit and cost criteria simultaneously and enables flexible weight configurations for deployment-specific decision support.

7. Citation

If you use this framework in academic work, please cite:

Saad Khan, Pedro Martins, Vasco Pereira, Bruno Sousa.
"Symmetric Encryption for Secure Resource-Constrained Devices."
(Submitted to Computers & Security, Elsevier, 2026).

Software citation (Zenodo DOI to be added after release):

Khan, S., Martins, P., Pereira, V., Sousa, B. (2026).
METHODICAL: Multi-Criteria Ranking Framework for Lightweight Encryption in IoT (Version 1.0).
Zenodo. DOI: xx.xxxx/zenodo.xxxxxxx
8. License

This project is licensed under the MIT License.
