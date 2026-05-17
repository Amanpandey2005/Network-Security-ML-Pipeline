import threading
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from collections import Counter

# ==============================
# PATH SETUP
# ==============================

current_dir = os.path.dirname(__file__)

project_root = os.path.abspath(
    os.path.join(current_dir, "..")
)

src_path = os.path.join(project_root, "src")

sys.path.append(src_path)

# ==============================
# IMPORTS
# ==============================

from predict import predict

from realtime_capture import (
    start_sniffing,
    get_live_data
)

from Email_alert import send_alert

from mongodb_logger import log_threat

from auto_retrain import auto_retrain

from block_ip import block_ip

# ==============================
# STREAMLIT CONFIG
# ==============================

st.set_page_config(
    page_title="AI Network IDS",
    layout="wide"
)

st.title(
    "🛡 AI-Based Network Intrusion Detection System"
)

st.markdown("---")

# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("⚙ Control Panel")

mode = st.sidebar.radio(
    "Select Mode",
    [
        "CSV Detection",
        "Real-Time Monitoring"
    ]
)

# ==============================
# EMAIL ALERTS
# ==============================

st.sidebar.subheader("📧 Email Alerts")

email_alert = st.sidebar.checkbox(
    "Enable Email Alerts",
    value=True
)

receiver_email = st.sidebar.text_input(
    "Receiver Email",
    "amanpandey.code@gmail.com"
)

# ==============================
# AUTO BLOCK OPTION
# ==============================

auto_block = st.sidebar.checkbox(
    "Enable Auto IP Blocking",
    value=False
)

# =========================================================
# CSV DETECTION MODE
# =========================================================

if mode == "CSV Detection":

    st.header("📂 CSV Upload Detection")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.subheader("📄 Uploaded Dataset")

        st.write(
            f"Total Rows Uploaded: {len(df)}"
        )

        st.dataframe(
            df.head(50)
        )

        predictions = []

        progress = st.progress(0)

        total_rows = len(df)

        # ==============================
        # PREDICTION LOOP
        # ==============================

        for i, (_, row) in enumerate(
            df.iterrows()
        ):

            try:

                pred = predict(
                    row.to_dict()
                )

            except Exception as e:

                st.error(
                    f"Prediction Error at row {i}: {e}"
                )

                pred = "ERROR"

            predictions.append(pred)

            progress.progress(
                (i + 1) / total_rows
            )

            # ==============================
            # EMAIL ALERT
            # ==============================

            if (
                email_alert and
                pred != "BENIGN"
            ):

                try:

                    send_alert(
                        pred,
                        row.to_dict(),
                        receiver_email
                    )

                except Exception as e:

                    st.warning(
                        f"Email Error: {e}"
                    )

        # ==============================
        # ADD PREDICTIONS
        # ==============================

        df["Prediction"] = predictions

        st.success(
            "✅ Prediction Completed"
        )

        # ==============================
        # METRICS
        # ==============================

        prediction_counts = Counter(
            predictions
        )

        chart_df = pd.DataFrame({

            "Attack Type":
                list(
                    prediction_counts.keys()
                ),

            "Count":
                list(
                    prediction_counts.values()
                )
        })

        col1, col2, col3 = st.columns(3)

        malicious_count = len(
            df[
                df["Prediction"] != "BENIGN"
            ]
        )

        col1.metric(
            "Total Packets",
            len(df)
        )

        col2.metric(
            "Attack Types",
            len(chart_df)
        )

        col3.metric(
            "Malicious Traffic",
            malicious_count
        )

        st.markdown("---")

        # ==============================
        # PIE CHART
        # ==============================

        st.subheader(
            "🥧 Attack Distribution"
        )

        fig1 = px.pie(
            chart_df,
            names="Attack Type",
            values="Count"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True,
            key="csv_pie"
        )

        # ==============================
        # BAR CHART
        # ==============================

        st.subheader(
            "📈 Attack Count"
        )

        fig2 = px.bar(
            chart_df,
            x="Attack Type",
            y="Count",
            color="Attack Type"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
            key="csv_bar"
        )

        # ==============================
        # RESULTS
        # ==============================

        st.subheader(
            "📊 Prediction Results"
        )

        st.dataframe(df)

        # ==============================
        # THREATS
        # ==============================

        threats = df[
            df["Prediction"] != "BENIGN"
        ]

        st.subheader(
            "🚨 Threat Alerts"
        )

        if len(threats) > 0:

            st.error(
                f"{len(threats)} malicious packets detected!"
            )

            st.dataframe(
                threats.head(20)
            )

        else:

            st.success(
                "✅ No threats detected"
            )

        # ==============================
        # DOWNLOAD
        # ==============================

        st.download_button(
            label="⬇ Download Results",
            data=df.to_csv(index=False),
            file_name="prediction_results.csv",
            mime="text/csv"
        )

# =========================================================
# REAL-TIME MONITORING MODE
# =========================================================

elif mode == "Real-Time Monitoring":

    st.header(
        "📡 Real-Time Network Monitoring"
    )

    st.success(
        "✅ Live Monitoring Started"
    )

    # ==============================
    # START SNIFFER
    # ==============================

    if "sniffer_started" not in st.session_state:

        thread = threading.Thread(
            target=start_sniffing,
            daemon=True
        )

        thread.start()

        st.session_state.sniffer_started = True

    # ==============================
    # PLACEHOLDERS
    # ==============================

    metric1, metric2, metric3 = st.columns(3)

    total_placeholder = metric1.empty()

    attack_placeholder = metric2.empty()

    benign_placeholder = metric3.empty()

    chart_placeholder = st.empty()

    table_placeholder = st.empty()

    threat_placeholder = st.empty()

    # ==============================
    # LIVE LOOP
    # ==============================

    status_placeholder = st.empty()

    while True:

        try:

            live_df = get_live_data()

            if live_df.empty:

                status_placeholder.info(
                    "Waiting for packets..."
                )

                time.sleep(2)

                continue

            else:
                status_placeholder.empty()

            # ==============================
            # PREDICTIONS
            # ==============================

            predictions = []

            for _, row in live_df.iterrows():

                try:

                    pred = predict(
                        row.to_dict()
                    )

                except:

                    pred = "BENIGN"

                predictions.append(pred)

            # Fix prediction mismatch issue
            if len(predictions) != len(live_df):

                predictions = (
                    predictions[:len(live_df)]
                )

            live_df["Prediction"] = predictions

            # ==============================
            # COUNTS
            # ==============================

            total_packets = len(live_df)

            malicious_packets = len(
                live_df[
                    live_df["Prediction"] != "BENIGN"
                ]
            )

            benign_packets = (
                total_packets -
                malicious_packets
            )

            # ==============================
            # METRICS
            # ==============================

            total_placeholder.metric(
                "Total Packets",
                total_packets
            )

            attack_placeholder.metric(
                "Malicious Traffic",
                malicious_packets
            )

            benign_placeholder.metric(
                "Benign Traffic",
                benign_packets
            )

            # ==============================
            # CHART
            # ==============================

            chart_df = pd.DataFrame({

                "Type": [
                    "BENIGN",
                    "ATTACK"
                ],

                "Count": [
                    benign_packets,
                    malicious_packets
                ]
            })

            fig = px.bar(
                chart_df,
                x="Type",
                y="Count",
                color="Type",
                title="Live Traffic Analysis"
            )

            chart_placeholder.plotly_chart(
                fig,
                use_container_width=True,
                key=f"live_chart_{time.time()}"
            )

            # ==============================
            # LIVE TABLE
            # ==============================

            table_placeholder.dataframe(
                live_df.tail(20),
                use_container_width=True
            )

            # ==============================
            # THREAT ALERTS
            # ==============================

            threats = live_df[
                live_df["Prediction"] != "BENIGN"
            ]

            if len(threats) > 0:

                latest_threat = threats.iloc[-1]

                threat_placeholder.error(

                    f"⚠ Threat Detected: "
                    f"{latest_threat['Prediction']}"
                )

                # ==============================
                # EMAIL ALERT
                # ==============================

                if email_alert:

                    try:

                        send_alert(
                            latest_threat["Prediction"],
                            latest_threat.to_dict(),
                            receiver_email
                        )

                    except Exception as e:

                        st.warning(
                            f"Email Error: {e}"
                        )

                # ==============================
                # MONGODB LOGGING
                # ==============================

                try:

                    log_threat(
                        latest_threat.to_dict()
                    )

                except Exception as e:

                    st.warning(
                        f"MongoDB Error: {e}"
                    )

                # ==============================
                # AUTO RETRAIN
                # ==============================

                auto_retrain(
                    malicious_packets
                )

                # ==============================
                # AUTO BLOCK IP
                # ==============================

                if auto_block:

                    try:

                        attacker_ip = (
                            latest_threat.get(
                                "Source IP",
                                None
                            )
                        )

                        if attacker_ip:

                            block_ip(
                                attacker_ip
                            )

                            st.error(
                                f"🚫 Blocked IP: "
                                f"{attacker_ip}"
                            )

                    except Exception as e:

                        st.warning(
                            f"Blocking Error: {e}"
                        )

            else:

                threat_placeholder.success(
                    "✅ Network Safe"
                )

            time.sleep(3)

        except Exception as e:

            st.error(
                f"Real-Time Error: {e}"
            )

            time.sleep(2)
