# import sqlite3
# import pandas as pd
# import streamlit as st


# # --------------------------------------------------
# # Database Path
# # --------------------------------------------------

# DB_PATH = "database/fraud_detection.db"


# # --------------------------------------------------
# # Load Complete Transactions
# # --------------------------------------------------

# @st.cache_data
# def load_transactions():
#     conn = sqlite3.connect(DB_PATH)

#     query = """
#     SELECT *
#     FROM transactions
#     """

#     df = pd.read_sql_query(query, conn)

#     conn.close()

#     return df


# # --------------------------------------------------
# # Overall Fraud Summary
# # --------------------------------------------------

# @st.cache_data
# def get_fraud_summary():

#     conn = sqlite3.connect(DB_PATH)

#     query = """
#     SELECT
#         COUNT(*) AS total_transactions,
#         SUM(CASE WHEN Fraudulent = 1 THEN 1 ELSE 0 END) AS fraud_transactions,
#         SUM(CASE WHEN Fraudulent = 0 THEN 1 ELSE 0 END) AS normal_transactions,
#         ROUND(
#             100.0 * SUM(CASE WHEN Fraudulent = 1 THEN 1 ELSE 0 END)
#             / COUNT(*),
#             2
#         ) AS fraud_rate,
#         ROUND(
#             SUM(
#                 CASE
#                     WHEN Fraudulent = 1
#                     THEN Transaction_Amount
#                     ELSE 0
#                 END
#             ),
#             2
#         ) AS fraud_amount
#     FROM transactions
#     """

#     result = pd.read_sql_query(query, conn)

#     conn.close()

#     return result


# # --------------------------------------------------
# # Fraud by Merchant Category
# # --------------------------------------------------

# @st.cache_data
# def fraud_by_merchant():

#     conn = sqlite3.connect(DB_PATH)

#     query = """
#     SELECT
#         Merchant_Category,
#         COUNT(*) AS total_transactions,
#         SUM(CASE WHEN Fraudulent = 1 THEN 1 ELSE 0 END) AS fraud_transactions,
#         ROUND(
#             100.0 * SUM(CASE WHEN Fraudulent = 1 THEN 1 ELSE 0 END)
#             / COUNT(*),
#             2
#         ) AS fraud_rate
#     FROM transactions
#     GROUP BY Merchant_Category
#     ORDER BY fraud_rate DESC
#     """

#     result = pd.read_sql_query(query, conn)

#     conn.close()

#     return result


# # --------------------------------------------------
# # Fraud by Payment Method
# # --------------------------------------------------

# @st.cache_data
# def fraud_by_payment():

#     conn = sqlite3.connect(DB_PATH)

#     query = """
#     SELECT
#         Payment_Method,
#         COUNT(*) AS total_transactions,
#         SUM(CASE WHEN Fraudulent = 1 THEN 1 ELSE 0 END) AS fraud_transactions,
#         ROUND(
#             100.0 * SUM(CASE WHEN Fraudulent = 1 THEN 1 ELSE 0 END)
#             / COUNT(*),
#             2
#         ) AS fraud_rate
#     FROM transactions
#     GROUP BY Payment_Method
#     ORDER BY fraud_rate DESC
#     """

#     result = pd.read_sql_query(query, conn)

#     conn.close()

#     return result


# # --------------------------------------------------
# # Fraud by International Transactions
# # --------------------------------------------------

# @st.cache_data
# def fraud_by_international():

#     conn = sqlite3.connect(DB_PATH)

#     query = """
#     SELECT
#         CASE
#             WHEN Is_International = 1
#             THEN 'International'
#             ELSE 'Domestic'
#         END AS transaction_type,

#         COUNT(*) AS total_transactions,

#         SUM(
#             CASE
#                 WHEN Fraudulent = 1
#                 THEN 1
#                 ELSE 0
#             END
#         ) AS fraud_transactions,

#         ROUND(
#             100.0 *
#             SUM(
#                 CASE
#                     WHEN Fraudulent = 1
#                     THEN 1
#                     ELSE 0
#                 END
#             ) / COUNT(*),
#             2
#         ) AS fraud_rate

#     FROM transactions

#     GROUP BY Is_International

#     ORDER BY fraud_rate DESC
#     """

#     result = pd.read_sql_query(query, conn)

#     conn.close()

#     return result


# # --------------------------------------------------
# # Fraud by Suspicious Keyword
# # --------------------------------------------------

# @st.cache_data
# def fraud_by_keyword():

#     conn = sqlite3.connect(DB_PATH)

#     query = """
#     SELECT
#         Suspicious_Keyword,
#         COUNT(*) AS total_transactions,

#         SUM(
#             CASE
#                 WHEN Fraudulent = 1
#                 THEN 1
#                 ELSE 0
#             END
#         ) AS fraud_transactions,

#         ROUND(
#             100.0 *
#             SUM(
#                 CASE
#                     WHEN Fraudulent = 1
#                     THEN 1
#                     ELSE 0
#                 END
#             ) / COUNT(*),
#             2
#         ) AS fraud_rate

#     FROM transactions

#     GROUP BY Suspicious_Keyword

#     ORDER BY fraud_rate DESC
#     """

#     result = pd.read_sql_query(query, conn)

#     conn.close()

#     return result


# # --------------------------------------------------
# # Fraud by Device
# # --------------------------------------------------

# @st.cache_data
# def fraud_by_device():

#     conn = sqlite3.connect(DB_PATH)

#     query = """
#     SELECT
#         Device_Type,
#         COUNT(*) AS total_transactions,

#         SUM(
#             CASE
#                 WHEN Fraudulent = 1
#                 THEN 1
#                 ELSE 0
#             END
#         ) AS fraud_transactions,

#         ROUND(
#             100.0 *
#             SUM(
#                 CASE
#                     WHEN Fraudulent = 1
#                     THEN 1
#                     ELSE 0
#                 END
#             ) / COUNT(*),
#             2
#         ) AS fraud_rate

#     FROM transactions

#     GROUP BY Device_Type

#     ORDER BY fraud_rate DESC
#     """

#     result = pd.read_sql_query(query, conn)

#     conn.close()

#     return result









import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


# Project root
BASE_DIR = Path(__file__).resolve().parents[1]

# Database path
DB_PATH = BASE_DIR / "database" / "fraud_detection.db"


@st.cache_data
def load_transactions():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM transactions
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    df["Transaction_Date"] = pd.to_datetime(
        df["Transaction_Date"],
        errors="coerce"
    )

    return df 





@st.cache_data
def load_fraud_alerts():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        alert_id,
        created_at,
        transaction_amount,
        merchant_category,
        payment_method,
        device_type,
        location,
        is_international,
        suspicious_keyword,
        fraud_probability,
        decision_threshold,
        prediction,
        status
    FROM fraud_alerts
    ORDER BY alert_id DESC
    """

    alerts = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return alerts 
















@st.cache_data
def get_alert_summary():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        COUNT(*) AS total_alerts,

        SUM(
            CASE
                WHEN status = 'Open'
                THEN 1
                ELSE 0
            END
        ) AS open_alerts,

        SUM(
            CASE
                WHEN status = 'Investigating'
                THEN 1
                ELSE 0
            END
        ) AS investigating_alerts,

        SUM(
            CASE
                WHEN status = 'Resolved'
                THEN 1
                ELSE 0
            END
        ) AS resolved_alerts,

        ROUND(
            AVG(fraud_probability) * 100,
            2
        ) AS average_risk

    FROM fraud_alerts
    """

    result = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return result





@st.cache_data
def update_alert_status(alert_id, new_status):
    conn = sqlite3.connect(DB_PATH)

    query = """
    UPDATE fraud_alerts
    SET status = ?
    WHERE alert_id = ?
    """

    conn.execute(
        query,
        (new_status, alert_id)
    )

    conn.commit()
    conn.close()

    # Refresh cached data
    load_fraud_alerts.clear()
    get_alert_summary.clear()

    return True


def create_fraud_alert(
    transaction_amount,
    merchant_category,
    payment_method,
    device_type,
    location,
    is_international,
    suspicious_keyword,
    fraud_probability,
    decision_threshold,
    prediction
):
    conn = sqlite3.connect(DB_PATH)

    query = """
    INSERT INTO fraud_alerts (
        created_at,
        transaction_amount,
        merchant_category,
        payment_method,
        device_type,
        location,
        is_international,
        suspicious_keyword,
        fraud_probability,
        decision_threshold,
        prediction,
        status
    )
    VALUES (
        datetime('now'),
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        'Open'
    )
    """

    conn.execute(
        query,
        (
            transaction_amount,
            merchant_category,
            payment_method,
            device_type,
            location,
            is_international,
            suspicious_keyword,
            fraud_probability,
            decision_threshold,
            prediction
        )
    )

    conn.commit()
    conn.close()

    load_fraud_alerts.clear()
    get_alert_summary.clear()

    return True