# 📊 Detailed Analysis Operations by Dataset

This document explains **exactly what is calculated** for each dataset in each analysis operation.

---

## 📋 Dataset Schemas

### 1. **Financial Data** (`financial_data.csv`)
**Columns:**
- `transaction_amount` - Amount of transaction (numeric)
- `account_balance` - Current account balance (numeric)
- `transaction_type` - Type of transaction: 1=Deposit, 2=Withdrawal, 3=Transfer (numeric)
- `fraud_flag` - Fraud indicator: 0=Normal, 1=Fraud (numeric)

### 2. **Medical Data** (`medical_data.csv`)
**Columns:**
- `age` - Patient age in years (numeric)
- `blood_pressure` - Blood pressure reading (numeric)
- `cholesterol` - Cholesterol level (numeric)
- `has_disease` - Disease indicator: 0=No disease, 1=Has disease (numeric)

### 3. **Housing Data** (`housing_data.csv`)
**Columns:**
- `area` - House area in square feet (numeric)
- `bedrooms` - Number of bedrooms (numeric)
- `age` - House age in years (numeric)
- `price` - House price in thousands (numeric)

### 4. **Student Scores Data** (`student_scores.csv`)
**Columns:**
- `hours_studied` - Hours studied per week (numeric)
- `previous_score` - Previous exam score (numeric)
- `sleep_hours` - Average hours of sleep (numeric)
- `final_score` - Final exam score (numeric)

---

## 🧮 Statistical Operations

**IMPORTANT:** Statistical operations are performed **column-wise**. Each row is encrypted as a vector containing all numeric columns, but operations compute statistics for a **specific column** across all rows.

**Column Selection:** Use `column_index` (0-based) or `column_name` in the API request to specify which column to analyze. If neither is specified, the operation works across all columns.

### 📊 **AVERAGE** (`/compute/average`)

Calculates the **mean** across all rows for each dataset. Each encrypted vector contains all columns, so the average is computed for the entire dataset.

#### Financial Data:
- **What's calculated:** Average across all 50 rows
  - Average `transaction_amount`
  - Average `account_balance`
  - Average `transaction_type`
  - Average `fraud_flag`
- **Result:** Single average value representing the mean of all numeric fields across all transactions
- **Use case:** Average transaction amount, average account balance

#### Medical Data:
- **What's calculated:** Average across all 50 rows
  - Average `age`
  - Average `blood_pressure`
  - Average `cholesterol`
  - Average `has_disease` (proportion of patients with disease)
- **Result:** Mean values for all medical parameters
- **Use case:** Average patient age, average blood pressure, disease prevalence rate

#### Housing Data:
- **What's calculated:** Average across all 50 rows
  - Average `area`
  - Average `bedrooms`
  - Average `age` (house age)
  - Average `price`
- **Result:** Mean values for all housing attributes
- **Use case:** Average house size, average price, average number of bedrooms

#### Student Scores Data:
- **What's calculated:** Average across all 50 rows
  - Average `hours_studied`
  - Average `previous_score`
  - Average `sleep_hours`
  - Average `final_score`
- **Result:** Mean values for all student metrics
- **Use case:** Average study hours, average scores, average sleep hours

---

### ➕ **SUM** (`/compute/sum`)

Calculates the **total sum** across all rows for each dataset.

#### Financial Data:
- **What's calculated:** Sum across all 50 rows
  - Total `transaction_amount` (sum of all transactions)
  - Total `account_balance` (sum of all balances - less meaningful)
  - Total `transaction_type` (sum of transaction types)
  - Total `fraud_flag` (total number of fraud cases)
- **Result:** Aggregate totals for all numeric fields
- **Use case:** Total transaction volume, total fraud count

#### Medical Data:
- **What's calculated:** Sum across all 50 rows
  - Total `age` (sum of all ages)
  - Total `blood_pressure` (sum of all BP readings)
  - Total `cholesterol` (sum of all cholesterol levels)
  - Total `has_disease` (total number of diseased patients)
- **Result:** Aggregate totals for all medical parameters
- **Use case:** Total patient age sum, total disease count

#### Housing Data:
- **What's calculated:** Sum across all 50 rows
  - Total `area` (total square footage)
  - Total `bedrooms` (total number of bedrooms)
  - Total `age` (total house age - less meaningful)
  - Total `price` (total property value)
- **Result:** Aggregate totals for all housing attributes
- **Use case:** Total property value, total square footage

#### Student Scores Data:
- **What's calculated:** Sum across all 50 rows
  - Total `hours_studied` (total study hours)
  - Total `previous_score` (sum of all previous scores)
  - Total `sleep_hours` (total sleep hours)
  - Total `final_score` (sum of all final scores)
- **Result:** Aggregate totals for all student metrics
- **Use case:** Total study hours, total score sum

---

### 📈 **VARIANCE** (`/compute/variance`)

Calculates the **statistical variance** (spread/dispersion) across all rows for each dataset.

#### Financial Data:
- **What's calculated:** Variance across all 50 rows
  - Variance of `transaction_amount` (variability in transaction sizes)
  - Variance of `account_balance` (variability in balances)
  - Variance of `transaction_type` (variability in transaction types)
  - Variance of `fraud_flag` (variance in fraud occurrence)
- **Result:** Variance values showing data spread for all fields
- **Use case:** Understanding transaction amount variability, fraud pattern spread

#### Medical Data:
- **What's calculated:** Variance across all 50 rows
  - Variance of `age` (age distribution spread)
  - Variance of `blood_pressure` (BP variability)
  - Variance of `cholesterol` (cholesterol level variability)
  - Variance of `has_disease` (disease distribution variance)
- **Result:** Variance values for all medical parameters
- **Use case:** Understanding patient age distribution, cholesterol variability

#### Housing Data:
- **What's calculated:** Variance across all 50 rows
  - Variance of `area` (size variability)
  - Variance of `bedrooms` (bedroom count spread)
  - Variance of `age` (house age variability)
  - Variance of `price` (price variability)
- **Result:** Variance values for all housing attributes
- **Use case:** Understanding price spread, size distribution

#### Student Scores Data:
- **What's calculated:** Variance across all 50 rows
  - Variance of `hours_studied` (study hours variability)
  - Variance of `previous_score` (previous score spread)
  - Variance of `sleep_hours` (sleep pattern variability)
  - Variance of `final_score` (final score spread)
- **Result:** Variance values for all student metrics
- **Use case:** Understanding score distribution, study pattern variability

---

### 🔢 **COUNT** (`/compute/count`)

Counts the **number of records** (rows) in each dataset.

#### Financial Data:
- **What's calculated:** Total number of transactions
- **Result:** 50 (total number of financial records)
- **Use case:** Transaction count, record count

#### Medical Data:
- **What's calculated:** Total number of patient records
- **Result:** 50 (total number of medical records)
- **Use case:** Patient count, medical record count

#### Housing Data:
- **What's calculated:** Total number of property listings
- **Result:** 50 (total number of housing records)
- **Use case:** Property count, listing count

#### Student Scores Data:
- **What's calculated:** Total number of student records
- **Result:** 50 (total number of student records)
- **Use case:** Student count, exam record count

---

## 🤖 Machine Learning Predictions

**⚠️ IMPORTANT:** ML predictions **ONLY work with Medical Data**. The system validates the dataset type and will reject non-medical datasets.

### 🏥 **LOGISTIC REGRESSION** (`/model/predict/logistic_regression`)

**Purpose:** Binary classification (e.g., disease prediction)

**Dataset Requirement:** ✅ **MEDICAL DATA ONLY**

**Model Features Used:**
- `age` (Age)
- `blood_pressure` (Blood Pressure)
- `cholesterol` (Cholesterol Level)
- Bias term

**Model Weights:**
```
weights: [0.2, -0.1, 0.3, 0.15]
intercept: -2.5
```

**For Each Dataset:**

#### Financial Data:
- **❌ Not Applicable** - Financial data doesn't have age, blood_pressure, cholesterol
- **Available columns:** transaction_amount, account_balance, transaction_type, fraud_flag
- **Note:** Would need a different model trained on financial features

#### Medical Data:
- **✅ Applicable** - Uses medical features
- **Input features:** `age`, `blood_pressure`, `cholesterol`
- **Output:** Disease prediction probability (0-1)
- **What's predicted:** Probability that a patient has a disease based on:
  - Age (positive weight: 0.2 - older age increases disease risk)
  - Blood pressure (negative weight: -0.1 - lower BP increases disease risk)
  - Cholesterol (positive weight: 0.3 - higher cholesterol increases disease risk)
- **Use case:** Predict disease probability for new patients

#### Housing Data:
- **❌ Not Applicable** - Housing data has `age` (house age, not patient age), but lacks blood_pressure and cholesterol
- **Available columns:** area, bedrooms, age (house age), price
- **Note:** Would need a different model (e.g., price prediction model)

#### Student Scores Data:
- **❌ Not Applicable** - Student data doesn't have age, blood_pressure, cholesterol
- **Available columns:** hours_studied, previous_score, sleep_hours, final_score
- **Note:** Would need a different model for student performance prediction

---

### 📈 **LINEAR REGRESSION** (`/model/predict/linear_regression`)

**Purpose:** Continuous value prediction

**Dataset Requirement:** ✅ **MEDICAL DATA ONLY**

**Model Features Used:**
- `age` (Age)
- `blood_pressure` (Blood Pressure)
- `cholesterol` (Cholesterol Level)
- Bias term

**Model Weights:**
```
weights: [0.5, 0.3, 0.2, 10.0]
(bias: 10.0)
```

**For Each Dataset:**

#### Financial Data:
- **❌ Not Applicable** - Financial data doesn't have age, blood_pressure, cholesterol
- **Available columns:** transaction_amount, account_balance, transaction_type, fraud_flag
- **Note:** Would need a different model (e.g., fraud probability, transaction amount prediction)

#### Medical Data:
- **✅ Applicable** - Uses medical features
- **Input features:** `age`, `blood_pressure`, `cholesterol`
- **Output:** Continuous numerical prediction (typically 50-150 range)
- **What's predicted:** A continuous value based on:
  - Age (weight: 0.5)
  - Blood pressure (weight: 0.3)
  - Cholesterol (weight: 0.2)
  - Bias: 10.0
- **Use case:** Predict continuous medical metrics (e.g., risk score, predicted lab value)

#### Housing Data:
- **❌ Not Applicable** - Housing data lacks blood_pressure and cholesterol
- **Available columns:** area, bedrooms, age (house age), price
- **Note:** Would need a different model for price prediction using area, bedrooms, age

#### Student Scores Data:
- **❌ Not Applicable** - Student data doesn't have age, blood_pressure, cholesterol
- **Available columns:** hours_studied, previous_score, sleep_hours, final_score
- **Note:** Would need a different model (e.g., predict final_score from hours_studied, previous_score, sleep_hours)

---

## 📝 Summary Table

| Dataset | Average | Sum | Variance | Count | Logistic Regression | Linear Regression |
|---------|---------|-----|----------|-------|---------------------|-------------------|
| **Financial** | ✅ All 4 columns | ✅ All 4 columns | ✅ All 4 columns | ✅ Row count | ❌ Requires different model | ❌ Requires different model |
| **Medical** | ✅ All 4 columns | ✅ All 4 columns | ✅ All 4 columns | ✅ Row count | ✅ Disease probability | ✅ Continuous value |
| **Housing** | ✅ All 4 columns | ✅ All 4 columns | ✅ All 4 columns | ✅ Row count | ❌ Requires different model | ❌ Requires different model |
| **Student** | ✅ All 4 columns | ✅ All 4 columns | ✅ All 4 columns | ✅ Row count | ❌ Requires different model | ❌ Requires different model |

**Legend:**
- ✅ = Works with current implementation
- ❌ = Requires different model/features (not applicable with current ML models)

---

## 🔍 Important Notes

1. **Statistical Operations:** Operations are performed **column-wise**. Use `column_index` or `column_name` to specify which column to analyze. If not specified, operations work across all columns. Each encrypted vector contains all columns from a row, and statistics are computed for a specific column across all rows.

2. **ML Models:** The current logistic and linear regression models are trained specifically for **medical data features** (age, blood_pressure, cholesterol). 
   - ✅ **Medical Data:** Fully compatible
   - ❌ **Other Datasets:** System will reject with an error message
   - The backend validates dataset type and blocks non-medical data from ML predictions
   - To use other datasets, you would need to train new models with appropriate features

3. **Feature Compatibility:**
   - Medical data: ✅ Fully compatible with both ML models
   - Financial data: ❌ Needs fraud prediction or transaction amount prediction model
   - Housing data: ❌ Needs price prediction model (using area, bedrooms, age)
   - Student data: ❌ Needs score prediction model (using hours_studied, previous_score, sleep_hours)

4. **Encryption:** Each row is encrypted as a single vector containing all numeric columns. This means statistical operations aggregate across all columns, and individual column analysis would require separate encryption or column selection in the computation logic.

