# #import streamlit as st
# #
# #st.set_page_config(
#     #page_title="Financial Fraud Detection",
#     #page_icon="🔍",
#     #layout="wide"
# #)
# #
# #st.title("🔍 Financial Fraud Detection Dashboard")
# #st.write("Streamlit dashboard is working successfully.")




# import streamlit as st
# import pandas as pd

# from data_loader import (
#     get_fraud_summary,
#     fraud_by_merchant,
#     fraud_by_payment,
#     fraud_by_international,
#     fraud_by_keyword,
#     fraud_by_device
# )


# # --------------------------------------------------
# # Page Configuration
# # --------------------------------------------------

# st.set_page_config(
#     page_title="Financial Fraud Detection",
#     page_icon="🔍",
#     layout="wide"
# )


# # --------------------------------------------------
# # Title
# # --------------------------------------------------

# st.title("🔍 Financial Fraud Detection Dashboard")

# st.markdown(
#     """
#     **ML-powered financial transaction monitoring and fraud analytics**
#     """
# )


# # --------------------------------------------------
# # Load Summary
# # --------------------------------------------------

# summary = get_fraud_summary()

# total_transactions = int(summary.loc[0, "total_transactions"])
# fraud_transactions = int(summary.loc[0, "fraud_transactions"])
# normal_transactions = int(summary.loc[0, "normal_transactions"])
# fraud_rate = float(summary.loc[0, "fraud_rate"])
# fraud_amount = float(summary.loc[0, "fraud_amount"])


# # --------------------------------------------------
# # KPI Cards
# # --------------------------------------------------

# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.metric(
#         "Total Transactions",
#         f"{total_transactions:,}"
#     )

# with col2:
#     st.metric(
#         "Fraud Transactions",
#         f"{fraud_transactions:,}"
#     )

# with col3:
#     st.metric(
#         "Fraud Rate",
#         f"{fraud_rate:.2f}%"
#     )

# with col4:
#     st.metric(
#         "Fraud Amount",
#         f"₹{fraud_amount:,.2f}"
#     )


# # --------------------------------------------------
# # Overview
# # --------------------------------------------------

# st.divider()

# st.subheader("📊 Fraud Overview")

# col1, col2 = st.columns(2)

# with col1:

#     merchant_df = fraud_by_merchant()

#     st.write("### Fraud by Merchant Category")

#     st.bar_chart(
#         merchant_df.set_index("Merchant_Category")["fraud_rate"]
#     )


# with col2:

#     payment_df = fraud_by_payment()

#     st.write("### Fraud by Payment Method")

#     st.bar_chart(
#         payment_df.set_index("Payment_Method")["fraud_rate"]
#     )


# # --------------------------------------------------
# # Additional Analytics
# # --------------------------------------------------

# col1, col2 = st.columns(2)

# with col1:

#     international_df = fraud_by_international()

#     st.write("### International vs Domestic")

#     st.bar_chart(
#         international_df.set_index("transaction_type")["fraud_rate"]
#     )


# with col2:

#     keyword_df = fraud_by_keyword()

#     st.write("### Suspicious Keyword Analysis")

#     st.bar_chart(
#         keyword_df.set_index("Suspicious_Keyword")["fraud_rate"]
#     )


# # --------------------------------------------------
# # Device Analysis
# # --------------------------------------------------

# st.divider()

# st.subheader("💻 Fraud by Device")

# device_df = fraud_by_device()

# st.bar_chart(
#     device_df.set_index("Device_Type")["fraud_rate"]
# )




import streamlit as st
import pandas as pd
import plotly.express as px

#from data_loader import load_transactions

from data_loader import (
    load_transactions,
    load_fraud_alerts,
    get_alert_summary,
    update_alert_status,
    create_fraud_alert
)
from model_predictor import predict_transaction


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Financial Fraud Detection",
    page_icon="🔍",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #9ca3af;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

df = load_transactions()


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.markdown(
    "Filter transactions to dynamically update the dashboard."
)

st.sidebar.divider()


# Merchant filter
merchant_options = sorted(
    df["Merchant_Category"].dropna().unique().tolist()
)

selected_merchants = st.sidebar.multiselect(
    "Merchant Category",
    options=merchant_options,
    default=merchant_options
)


# Payment filter
payment_options = sorted(
    df["Payment_Method"].dropna().unique().tolist()
)

selected_payments = st.sidebar.multiselect(
    "Payment Method",
    options=payment_options,
    default=payment_options
)


# Device filter
device_options = sorted(
    df["Device_Type"].dropna().unique().tolist()
)

selected_devices = st.sidebar.multiselect(
    "Device Type",
    options=device_options,
    default=device_options
)


# International filter
international_options = ["Domestic", "International"]

selected_international = st.sidebar.multiselect(
    "Transaction Type",
    options=international_options,
    default=international_options
)


# Suspicious keyword filter
keyword_options = sorted(
    df["Suspicious_Keyword"].dropna().unique().tolist()
)

selected_keywords = st.sidebar.multiselect(
    "Suspicious Keyword",
    options=keyword_options,
    default=keyword_options
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


filtered_df = filtered_df[
    filtered_df["Merchant_Category"].isin(selected_merchants)
]


filtered_df = filtered_df[
    filtered_df["Payment_Method"].isin(selected_payments)
]


filtered_df = filtered_df[
    filtered_df["Device_Type"].isin(selected_devices)
]


if "International" in selected_international and \
   "Domestic" not in selected_international:

    filtered_df = filtered_df[
        filtered_df["Is_International"] == 1
    ]

elif "Domestic" in selected_international and \
     "International" not in selected_international:

    filtered_df = filtered_df[
        filtered_df["Is_International"] == 0
    ]


filtered_df = filtered_df[
    filtered_df["Suspicious_Keyword"].isin(selected_keywords)
]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🔍 Financial Fraud Detection Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'ML-powered financial transaction monitoring and fraud analytics'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_transactions = len(filtered_df)

fraud_transactions = int(
    filtered_df["Fraudulent"].sum()
)

normal_transactions = (
    total_transactions - fraud_transactions
)

if total_transactions > 0:
    fraud_rate = (
        fraud_transactions / total_transactions
    ) * 100
else:
    fraud_rate = 0


fraud_amount = filtered_df.loc[
    filtered_df["Fraudulent"] == 1,
    "Transaction_Amount"
].sum()


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Transactions",
        f"{total_transactions:,}"
    )


with col2:

    st.metric(
        "Fraud Transactions",
        f"{fraud_transactions:,}"
    )


with col3:

    st.metric(
        "Fraud Rate",
        f"{fraud_rate:.2f}%"
    )


with col4:

    st.metric(
        "Fraud Amount",
        f"₹{fraud_amount:,.2f}"
    )


st.divider()


# =========================================================
# FRAUD OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">📊 Fraud Analytics</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# =========================================================
# MERCHANT ANALYSIS
# =========================================================

with col1:

    merchant_df = (
        filtered_df
        .groupby("Merchant_Category")
        .agg(
            Transactions=("Fraudulent", "count"),
            Fraud=("Fraudulent", "sum")
        )
        .reset_index()
    )

    merchant_df["Fraud_Rate"] = (
        merchant_df["Fraud"]
        / merchant_df["Transactions"]
    ) * 100

    merchant_df = merchant_df.sort_values(
        "Fraud_Rate",
        ascending=True
    )

    fig = px.bar(
        merchant_df,
        x="Fraud_Rate",
        y="Merchant_Category",
        orientation="h",
        title="Fraud Rate by Merchant Category",
        labels={
            "Fraud_Rate": "Fraud Rate (%)",
            "Merchant_Category": ""
        },
        hover_data=[
            "Transactions",
            "Fraud"
        ],
        text="Fraud_Rate"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PAYMENT METHOD
# =========================================================

with col2:

    payment_df = (
        filtered_df
        .groupby("Payment_Method")
        .agg(
            Transactions=("Fraudulent", "count"),
            Fraud=("Fraudulent", "sum")
        )
        .reset_index()
    )

    payment_df["Fraud_Rate"] = (
        payment_df["Fraud"]
        / payment_df["Transactions"]
    ) * 100

    payment_df = payment_df.sort_values(
        "Fraud_Rate",
        ascending=False
    )

    fig = px.bar(
        payment_df,
        x="Payment_Method",
        y="Fraud_Rate",
        title="Fraud Rate by Payment Method",
        labels={
            "Fraud_Rate": "Fraud Rate (%)",
            "Payment_Method": ""
        },
        hover_data=[
            "Transactions",
            "Fraud"
        ],
        text="Fraud_Rate"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# INTERNATIONAL VS DOMESTIC
# =========================================================

col1, col2 = st.columns(2)


with col1:

    international_df = filtered_df.copy()

    international_df["Transaction_Type"] = (
        international_df["Is_International"]
        .map({
            0: "Domestic",
            1: "International"
        })
    )

    international_df = (
        international_df
        .groupby("Transaction_Type")
        .agg(
            Transactions=("Fraudulent", "count"),
            Fraud=("Fraudulent", "sum")
        )
        .reset_index()
    )

    international_df["Fraud_Rate"] = (
        international_df["Fraud"]
        / international_df["Transactions"]
    ) * 100

    fig = px.bar(
        international_df,
        x="Transaction_Type",
        y="Fraud_Rate",
        title="International vs Domestic Fraud",
        labels={
            "Fraud_Rate": "Fraud Rate (%)",
            "Transaction_Type": ""
        },
        hover_data=[
            "Transactions",
            "Fraud"
        ],
        text="Fraud_Rate"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# SUSPICIOUS KEYWORD
# =========================================================

with col2:

    keyword_df = (
        filtered_df
        .groupby("Suspicious_Keyword")
        .agg(
            Transactions=("Fraudulent", "count"),
            Fraud=("Fraudulent", "sum")
        )
        .reset_index()
    )

    keyword_df["Fraud_Rate"] = (
        keyword_df["Fraud"]
        / keyword_df["Transactions"]
    ) * 100

    fig = px.bar(
        keyword_df,
        x="Suspicious_Keyword",
        y="Fraud_Rate",
        title="Suspicious Keyword Analysis",
        labels={
            "Fraud_Rate": "Fraud Rate (%)",
            "Suspicious_Keyword": "Suspicious Keyword"
        },
        hover_data=[
            "Transactions",
            "Fraud"
        ],
        text="Fraud_Rate"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# DEVICE ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">💻 Fraud by Device</div>',
    unsafe_allow_html=True
)


device_df = (
    filtered_df
    .groupby("Device_Type")
    .agg(
        Transactions=("Fraudulent", "count"),
        Fraud=("Fraudulent", "sum")
    )
    .reset_index()
)

device_df["Fraud_Rate"] = (
    device_df["Fraud"]
    / device_df["Transactions"]
) * 100


fig = px.bar(
    device_df,
    x="Device_Type",
    y="Fraud_Rate",
    title="Fraud Rate by Device Type",
    labels={
        "Fraud_Rate": "Fraud Rate (%)",
        "Device_Type": ""
    },
    hover_data=[
        "Transactions",
        "Fraud"
    ],
    text="Fraud_Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# TRANSACTION RISK SCORING
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🤖 Transaction Risk Scoring'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    "Enter transaction details below to estimate fraud risk "
    "using the trained machine learning model."
)


col1, col2 = st.columns(2)


# =========================================================
# LEFT COLUMN
# =========================================================

with col1:

    transaction_amount = st.number_input(
        "Transaction Amount (₹)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

    merchant_category = st.selectbox(
        "Merchant Category",
        sorted(
            df["Merchant_Category"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    payment_method = st.selectbox(
        "Payment Method",
        sorted(
            df["Payment_Method"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    device_type = st.selectbox(
        "Device Type",
        sorted(
            df["Device_Type"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    location = st.selectbox(
        "Location",
        sorted(
            df["Location"]
            .dropna()
            .unique()
            .tolist()
        )
    )


# =========================================================
# RIGHT COLUMN
# =========================================================

with col2:

    is_international = st.selectbox(
        "Transaction Type",
        ["Domestic", "International"]
    )

    previous_transactions = st.number_input(
        "Previous Transactions",
        min_value=0,
        value=10,
        step=1
    )

    average_spend = st.number_input(
        "Average Spend (₹)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

    account_age_days = st.number_input(
        "Account Age (Days)",
        min_value=0,
        value=365,
        step=1
    )

    suspicious_keyword = st.selectbox(
        "Suspicious Keyword",
        sorted(
            df["Suspicious_Keyword"]
            .dropna()
            .unique()
            .tolist()
        )
    )


# =========================================================
# PREDICT BUTTON
# =========================================================

if st.button(
    "🔍 Predict Fraud Risk",
    use_container_width=True
):

    transaction_data = {

        "Transaction_Amount":
            transaction_amount,

        "Merchant_Category":
            merchant_category,

        "Payment_Method":
            payment_method,

        "Device_Type":
            device_type,

        "Location":
            location,

        "Is_International":
            1 if is_international == "International"
            else 0,

        "Previous_Transactions":
            previous_transactions,

        "Average_Spend":
            average_spend,

        "Account_Age_Days":
            account_age_days,

        "Suspicious_Keyword":
            suspicious_keyword
    }


    # =============================================
    # MODEL PREDICTION
    # =============================================

    result = predict_transaction(
        transaction_data
    )


    prediction = result["prediction"]

    probability = result["fraud_probability"]

    threshold_used = result["threshold"]


    st.divider()

    # =============================================
    # AUTOMATIC FRAUD ALERT CREATION
    # =============================================

    alert_created = False

    if prediction == "Fraud":

        create_fraud_alert(
            transaction_amount=transaction_amount,
            merchant_category=merchant_category,
            payment_method=payment_method,
            device_type=device_type,
            location=location,
            is_international=(
                1 if is_international == "International"
                else 0
            ),
            suspicious_keyword=suspicious_keyword,
            fraud_probability=probability,
            decision_threshold=threshold_used,
            prediction=1
        )

        alert_created = True



    # =============================================
    # RESULT
    # =============================================

    result_col1, result_col2, result_col3 = st.columns(3)


    with result_col1:

        st.metric(
            "Fraud Probability",
            f"{probability * 100:.2f}%"
        )


    with result_col2:

        st.metric(
            "Decision Threshold",
            f"{threshold_used:.2f}"
        )


    with result_col3:

        if prediction == "Fraud":

            st.error(
                "🚨 FRAUD DETECTED"
            )

        else:

            st.success(
                "✅ TRANSACTION NORMAL"
            )


        if alert_created:
            st.success(


                "🚨 Fraud alert automatically created "
                "in the Alert Center."
        )






    # =============================================
    # PROBABILITY BAR
    # =============================================

    st.progress(
        min(
            probability,
            1.0
        )
    )


    if prediction == "Fraud":

        st.warning(
            f"⚠️ This transaction has an estimated "
            f"fraud probability of "
            f"**{probability * 100:.2f}%**, "
            f"which is above the selected "
            f"threshold of **{threshold_used:.2f}**."
        )

    else:

        st.info(
            f"ℹ️ This transaction has an estimated "
            f"fraud probability of "
            f"**{probability * 100:.2f}%**, "
            f"which is below the selected "
            f"threshold of **{threshold_used:.2f}**."
        )


# =========================================================
# FRAUD ALERT CENTER
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🚨 Fraud Alert Center'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    "Monitor high-risk transactions generated by the "
    "machine learning fraud detection system."
)



st.markdown("### 🔄 Update Alert Status")


alerts_df = load_fraud_alerts()

if not alerts_df.empty:

    alert_ids = alerts_df["alert_id"].tolist()

    selected_alert = st.selectbox(
        "Select Alert",
        alert_ids,
        format_func=lambda x: f"Alert #{x}"
    )

    current_status = alerts_df.loc[
        alerts_df["alert_id"] == selected_alert,
        "status"
    ].iloc[0]

    new_status = st.selectbox(
        "New Status",
        ["Open", "Investigating", "Resolved"],
        index=["Open", "Investigating", "Resolved"].index(current_status)
    )

    if st.button(
        "Update Alert Status",
        type="primary",
        use_container_width=True
    ):

        update_alert_status(
            selected_alert,
            new_status
        )

        st.success(
            f"Alert #{selected_alert} status updated to {new_status}."
        )

        st.rerun()















# =========================================================
# LOAD ALERT DATA
# =========================================================

alert_summary = get_alert_summary()
alerts_df = load_fraud_alerts()


total_alerts = int(
    alert_summary.loc[0, "total_alerts"] or 0
)

open_alerts = int(
    alert_summary.loc[0, "open_alerts"] or 0
)

investigating_alerts = int(
    alert_summary.loc[0, "investigating_alerts"] or 0
)

resolved_alerts = int(
    alert_summary.loc[0, "resolved_alerts"] or 0
)

average_risk = float(
    alert_summary.loc[0, "average_risk"] or 0
)


# =========================================================
# ALERT KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Alerts",
        f"{total_alerts:,}"
    )


with col2:

    st.metric(
        "Open Alerts",
        f"{open_alerts:,}"
    )


with col3:

    st.metric(
        "Investigating",
        f"{investigating_alerts:,}"
    )


with col4:

    st.metric(
        "Average Risk",
        f"{average_risk:.2f}%"
    )


# =========================================================
# ALERT TABLE
# =========================================================

if not alerts_df.empty:

    display_alerts = alerts_df.copy()

    display_alerts["fraud_probability"] = (
        display_alerts["fraud_probability"] * 100
    ).round(2)

    display_alerts["prediction"] = (
        display_alerts["prediction"]
        .map({
            0: "Normal",
            1: "Fraud"
        })
    )

    display_alerts = display_alerts.rename(
        columns={
            "alert_id": "Alert ID",
            "created_at": "Created At",
            "transaction_amount": "Amount",
            "merchant_category": "Merchant",
            "payment_method": "Payment",
            "device_type": "Device",
            "location": "Location",
            "fraud_probability": "Risk %",
            "prediction": "Prediction",
            "status": "Status"
        }
    )

    display_alerts = display_alerts[
        [
            "Alert ID",
            "Created At",
            "Amount",
            "Merchant",
            "Payment",
            "Device",
            "Location",
            "Risk %",
            "Prediction",
            "Status"
        ]
    ]

    st.dataframe(
        display_alerts,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No fraud alerts have been generated yet."
    )       


# =========================================================
# RECENT TRANSACTIONS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">💳 Recent Transactions</div>',
    unsafe_allow_html=True
)


display_columns = [
    "Transaction_ID",
    "Customer_ID",
    "Transaction_Date",
    "Transaction_Amount",
    "Merchant_Category",
    "Payment_Method",
    "Device_Type",
    "Location",
    "Is_International",
    "Suspicious_Keyword",
    "Fraudulent"
]


recent_df = (
    filtered_df[
        display_columns
    ]
    .sort_values(
        "Transaction_Date",
        ascending=False
    )
    .head(20)
    .copy()
)


recent_df["Fraudulent"] = (
    recent_df["Fraudulent"]
    .map({
        0: "Normal",
        1: "Fraud"
    })
)


st.dataframe(
    recent_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Financial Fraud Detection | "
    "SQLite + SQL Analytics + Machine Learning + Streamlit"
)