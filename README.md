# Financial Fraud Detection System

An end-to-end machine learning based financial fraud detection system that identifies potentially fraudulent transactions, evaluates fraud risk, performs SQL-based transaction analytics, and provides an interactive Streamlit dashboard with automatic fraud alert generation.

---

## 📌 Project Overview

Financial fraud detection is a classification problem where the objective is to identify suspicious transactions while minimizing incorrect classifications.

This project develops an end-to-end fraud detection pipeline covering:

- Exploratory Data Analysis
- Data preprocessing
- Class imbalance handling using SMOTE
- Feature engineering
- Multiple machine learning models
- Model evaluation and threshold analysis
- Final model packaging
- SQLite-based transaction analytics
- Interactive Streamlit dashboard
- Real-time transaction risk prediction
- Automatic fraud alert generation
- Fraud alert status management

The project uses a structured financial transaction dataset containing transaction, customer, behavioral, payment, device, location, and fraud-related attributes.

---

## 🎯 Objectives

The main objectives of the project are:

1. Understand transaction patterns associated with fraudulent activity.
2. Prepare and preprocess transaction data for machine learning.
3. Handle class imbalance using SMOTE.
4. Train and compare multiple classification algorithms.
5. Select a final model using fraud-detection-oriented evaluation metrics.
6. Package the final model for application use.
7. Perform SQL-based fraud analytics using SQLite.
8. Build an interactive fraud monitoring dashboard.
9. Predict the fraud probability of new transactions.
10. Automatically generate alerts for high-risk transactions.
11. Provide alert lifecycle management through Open, Investigating, and Resolved states.

---

## 📊 Dataset

The primary dataset used in this project is:

`financial_fraud_detection_dataset.csv`

Dataset characteristics:

- Records: 5,000
- Features: 14
- Missing values: 0
- Duplicate records: 0
- Fraudulent transactions: 482
- Normal transactions: 4,518
- Fraud rate: 9.64%

### Main Features

| Feature | Description |
|---|---|
| Transaction_ID | Unique transaction identifier |
| Customer_ID | Customer identifier |
| Transaction_Date | Transaction date and time |
| Transaction_Amount | Transaction amount |
| Merchant_Category | Merchant category |
| Payment_Method | Payment method |
| Device_Type | Device used for transaction |
| Location | Transaction location |
| Is_International | Indicates international transaction |
| Previous_Transactions | Number of previous transactions |
| Average_Spend | Customer's average spending |
| Account_Age_Days | Customer account age |
| Suspicious_Keyword | Suspicious keyword indicator |
| Fraudulent | Target variable |

---

## 🔎 Exploratory Data Analysis

The dataset was analyzed to understand transaction distributions and fraud patterns.

### Key Findings

- Fraudulent transactions represent approximately **9.64%** of the dataset.
- International transactions showed a substantially higher observed fraud rate than domestic transactions.
- Transactions with a suspicious keyword showed a substantially higher observed fraud rate than transactions without one.
- Fraud rates were also analyzed across merchant categories, payment methods, and device types.
- Transaction amount distribution and numerical feature relationships were examined during EDA.

### Observed Fraud Rates

#### International Transactions

| Transaction Type | Observed Fraud Rate |
|---|---:|
| International | 36.96% |
| Domestic | 7.00% |

#### Suspicious Keyword

| Suspicious Keyword | Observed Fraud Rate |
|---|---:|
| Yes | 47.31% |
| No | 7.57% |

These are descriptive statistics from this dataset and are not intended to establish causal relationships.

---

## ⚙️ Data Preprocessing

The preprocessing pipeline includes:

1. Parsing `Transaction_Date`
2. Removing identifier and date fields from model inputs
3. Separating features and target
4. Train-test split
5. StandardScaler for numerical features
6. OneHotEncoder for categorical features
7. Handling unseen categorical values using `handle_unknown="ignore"`

### Dataset Split

- Training set: 4,000 records
- Test set: 1,000 records

After preprocessing:

- Input features: 30
- Training matrix: 4,000 × 30
- Test matrix: 1,000 × 30

The fitted preprocessing pipeline is saved as:

`models/preprocessor.pkl`

---

## ⚖️ Class Imbalance Handling

The training dataset contains significantly fewer fraudulent transactions than normal transactions.

SMOTE (Synthetic Minority Over-sampling Technique) was applied to the training data.

### Before SMOTE

| Class | Records |
|---|---:|
| Normal | 3,614 |
| Fraud | 386 |

### After SMOTE

| Class | Records |
|---|---:|
| Normal | 3,614 |
| Fraud | 3,614 |

The test set remained unchanged to preserve an independent evaluation distribution.

---

## 🧠 Feature Engineering

Additional analytical features were created from the raw transaction data:

- `Transaction_Hour`
- `Transaction_Day`
- `Transaction_Month`
- `Amount_Deviation`
- `High_Amount_Flag`
- `Account_Age_Years`
- `Transactions_Per_Account_Year`

These features were generated as part of the feature-engineering analysis workflow.

---

## 🤖 Machine Learning Models

Five classification models were trained and evaluated:

1. Logistic Regression
2. Decision Tree
3. Random Forest
4. K-Nearest Neighbors
5. Support Vector Classifier

The evaluation considered:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix
- ROC Curve

---

## 📈 Model Evaluation

### Baseline Model Results

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 87.00% | 39.38% | 65.63% | 49.22% | 79.95% |
| Decision Tree | 88.60% | 41.82% | 47.92% | 44.66% | 70.16% |
| Random Forest | 89.40% | 45.19% | 48.96% | 47.00% | 79.94% |
| KNN | 73.70% | 19.64% | 56.25% | 29.11% | 70.22% |
| SVC | 88.10% | 38.83% | 41.67% | 40.20% | 72.92% |

---

## 🎯 Final Model Selection

Threshold analysis was performed to evaluate the effect of changing the classification threshold.

The final model selected for deployment was:

**Logistic Regression**

with a decision threshold of:

**0.70**

At this threshold, the final test-set metrics were:

| Metric | Result |
|---|---:|
| Accuracy | 88.50% |
| Precision | 43.17% |
| Recall | 62.50% |
| F1 Score | 51.06% |
| ROC-AUC | 79.95% |

The selection was based on the F1-score criterion used during the model-selection stage.

The final model is stored as:

`models/final_fraud_model.pkl`

The threshold is stored in:

`models/final_model_threshold.csv`

Model metadata is stored in:

`models/final_model_metadata.json`

---

## 🗃️ SQL Analytics with SQLite

A SQLite database was created to support transaction analytics and fraud alert management.

Database:

`database/fraud_detection.db`

Main transaction table:

`transactions`

The database contains 5,000 transaction records.

SQL analytics include:

- Total transactions
- Fraud transactions
- Normal transactions
- Fraud rate
- Fraud amount
- Fraud by merchant category
- Fraud by payment method
- Fraud by device type
- Domestic vs international fraud
- Suspicious keyword analysis

---

## 📊 Streamlit Dashboard

An interactive Streamlit dashboard was developed for fraud monitoring and analysis.

### Dashboard Features

- Sidebar transaction filters
- KPI cards
- Fraud-rate analysis
- Merchant category analysis
- Payment method analysis
- Device analysis
- International/domestic analysis
- Suspicious keyword analysis
- Recent transaction table
- New transaction risk prediction
- Fraud probability display
- Decision threshold display
- Fraud alert center
- Alert status management

### Dashboard Flow

```text
Transaction Data
       ↓
SQLite Database
       ↓
SQL Analytics
       ↓
Streamlit Dashboard
       ↓
Transaction Risk Prediction
       ↓
Fraud Probability
       ↓
Decision Threshold
       ↓
Fraud / Normal