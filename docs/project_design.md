# Clinical Trial Opportunity Radar

## Project Scope

### Business Problem

Clinical trial development requires strategic decisions about which therapeutic areas, indications and countries offer attractive opportunities for conducting clinical research. These decisions involve multiple factors, including patient population, unmet medical need, existing trial competition and operational feasibility.

Evaluating these factors independently can make it difficult to compare potential opportunities consistently and identify markets that warrant further investigation.

### Project Objective

Develop an interactive analytics tool to identify, compare and prioritize country–indication combinations for clinical trial development.
The tool will combine clinical research indicators into an interpretable opportunity score and provide visualizations that help users understand both the relative attractiveness of each opportunity and the factors driving its ranking.


### Key Business Questions
1. Which country–indication combinations present the most attractive clinical research opportunities?
2. Where does potential patient demand appear relatively high compared with existing trial competition?
3. How do opportunities differ across countries and therapeutic areas?
4. Which factors contribute most to an opportunity's overall score?
5. How sensitive are the rankings to changes in assumptions and scoring weights?

### Limitations

Focused on country-level opportunity assessment rather than individual site selection, detailed patient recruitment forecasting or drug development portfolio valuation.
The model will initially use synthetic data to develop and test the analytical methodology.
The opportunity score will support exploratory decision-making. It will not be interpreted as proof of commercial attractiveness, clinical trial success or actual patient recruitment feasibility.




## Project Design
### Countries
Latam
Arg Argentina
BRA Brasil
CHL Chile
COL Colombia
ECU Ecuador
MEX Mexico
PRY Paraguay
VEN Venezuela



### TA/ Indications
- Neurology: Multiple Sclerosis (MS), Parkinsons disease, Amylotrophic lateral sclerosis (ALS)
- Rheumatology: Rheumatoid arthritis (RA), Systemic lupus erythematosus (SLE), Axial spondyloarthritis (axSpA)
-Oncology: Non-small cell lung cancer (NSCLC)
-Respiratory: Asthma, Chronic obstructive pulmonary disease (COPD), Idiopathic pulmonary fibrosis (IPF)
-Dermatology: Atopic dermatitis, Plaque psoriasis, Acne vulgaris 


### Variables

country      | Cat | Country being evaluated
therap_area  | Cat | Therapeutic area associated with the indication
indication   | Cat | Clinical disease or indication
patient_pop  | Num | Estimated size of the potential patient population (cont- thousands of people)
unmet_need   | Num | Level of unmet medical need (Scale: 1–100)
trial_compet | Num | Intensity of competition from other clinical trials (discrete count)
op_feas      | Num | Estimated feasibility of conducting a clinical trial in the country for the given indication (Scale: 1–100)
reg_env      | Num | Favorability of the regulatory environment for conducting clinical trials in the country (Scale: 1–100)