# 🛡 AI-Based Network Intrusion Detection System (AI-NIDS)

## 📌 Project Overview

The AI-Based Network Intrusion Detection System (AI-NIDS) is a Machine Learning powered cybersecurity application that detects malicious network traffic in real-time and through uploaded CSV datasets.

The project combines:

* Machine Learning based attack detection
* Real-time packet monitoring using Scapy
* Streamlit interactive dashboard
* Email alert system
* MongoDB threat logging
* Auto-retraining architecture support
* Future firewall blocking support

The system helps identify suspicious traffic such as:

* DDoS attacks
* Brute force attacks
* Botnet traffic
* Port scanning
* Malicious packets
* Other abnormal traffic patterns

---

# 🚀 Features

## ✅ CSV Detection Mode

Upload a CSV dataset and perform attack prediction on network packets.

### Features:

* CSV Upload
* Batch Prediction
* Attack Visualization
* Threat Reports
* Download Prediction Results
* Email Alert Support

---

## ✅ Real-Time Monitoring

Monitor live network traffic directly from the machine.

### Features:

* Live Packet Sniffing
* Real-Time Predictions
* Live Threat Detection
* Dynamic Charts
* Packet Logs
* Real-Time Metrics
* Threat Notifications

---

## ✅ Email Alerts

Whenever a malicious packet is detected:

* Email alerts are automatically sent
* Threat details are included
* Receiver email is configurable from dashboard

---

## ✅ MongoDB Threat Logging

Detected threats are automatically stored inside MongoDB.

### Stored Information:

* Timestamp
* Threat Type
* Packet Information
* Source IP
* Destination IP
* Protocol

---

## ✅ Auto Retraining Support

Future retraining support allows:

* Continuous learning
* Updating models with new attack data
* Improved accuracy over time

---

## ✅ Future Firewall Blocking Support

The system architecture supports:

* IP blocking
* Firewall integration
* Permission-based malicious host blocking

---

# 🧠 Machine Learning Workflow

## Training Pipeline

1. Dataset Collection
2. Data Cleaning
3. Feature Engineering
4. Scaling
5. Label Encoding
6. Model Training
7. Model Saving
8. Deployment

---

# 🏗 System Architecture

```text
                +------------------+
                | Network Traffic |
                +--------+---------+
                         |
                         v
                +------------------+
                | Packet Sniffing |
                |     (Scapy)     |
                +--------+---------+
                         |
                         v
                +------------------+
                | Feature Extract. |
                +--------+---------+
                         |
                         v
                +------------------+
                | ML Prediction    |
                |  (Trained Model) |
                +--------+---------+
                         |
          +--------------+--------------+
          |                             |
          v                             v
+------------------+        +-------------------+
| Streamlit UI     |        | MongoDB Logging   |
+------------------+        +-------------------+
          |
          v
+------------------+
| Email Alerts     |
+------------------+
```

---

# 🧩 Technologies Used

| Technology   | Purpose              |
| ------------ | -------------------- |
| Python       | Core Development     |
| Streamlit    | Dashboard UI         |
| Scikit-learn | Machine Learning     |
| Scapy        | Packet Sniffing      |
| MongoDB      | Threat Logging       |
| Plotly       | Visualization        |
| Pandas       | Data Processing      |
| NumPy        | Numerical Operations |
| Joblib       | Model Loading        |
| SMTP         | Email Alerts         |

---

# 📂 Project Structure

```text
Network Security ML Pipeline/
│
├── Dashboard/
│   └── dashboard.py
│
├── src/
│   ├── predict.py
│   ├── realtime_capture.py
│   ├── Email_alert.py
│   ├── mongodb_logger.py
│   ├── auto_retrain.py
│   └── block_ip.py
│
├── models/
│   ├── model.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── feature_names.pkl
│
├── dataset/
│
├── requirements.txt
│
└── README.md
```

---

# ⚙ Installation Guide

## Step 1: Clone Repository

```bash
git clone <repository-link>
```

---

## Step 2: Open Project Folder

```bash
cd "Network Security ML Pipeline"
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Install Npcap (Windows Only)

Required for real-time packet sniffing.

Download:

[https://npcap.com/#download](https://npcap.com/#download)

During installation:

✅ Enable WinPcap Compatibility Mode

---

## Step 5: Install MongoDB

Download:

[https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)

Install MongoDB Compass:

[https://www.mongodb.com/products/compass](https://www.mongodb.com/products/compass)

---

## Step 6: Start MongoDB

```bash
net start MongoDB
```

---

## Step 7: Run Streamlit Dashboard

```bash
python -m streamlit run Dashboard/dashboard.py
```

---

# 📧 Email Alert Configuration

Configure inside dashboard sidebar.

## Sender Email

Configure in:

```text
src/Email_alert.py
```

## Receiver Email

Can be entered directly from dashboard.

---

# 🗃 MongoDB Database Structure

## Database:

```text
network_ids
```

## Collection:

```text
threat_logs
```

---

# 📊 Dashboard Modules

## CSV Detection Dashboard

### Displays:

* Uploaded dataset
* Prediction results
* Attack distribution
* Threat table
* Downloadable CSV

---

## Real-Time Monitoring Dashboard

### Displays:

* Total Packets
* Malicious Packets
* Benign Packets
* Live Packet Logs
* Live Attack Distribution
* Real-Time Alerts

---

# 🔐 Security Features

* Real-time packet inspection
* Threat classification
* Alert notification system
* Threat database logging
* Attack visualization
* Future firewall blocking integration

---

# 🧪 Model Files

| File              | Purpose           |
| ----------------- | ----------------- |
| model.pkl         | Trained ML Model  |
| scaler.pkl        | Feature Scaling   |
| label_encoder.pkl | Label Decoding    |
| feature_names.pkl | Feature Alignment |

---

# 📈 Future Improvements

## Planned Features

* Deep Learning Models
* Hybrid IDS
* Firewall Automation
* Cloud Deployment
* Threat Heatmaps
* SIEM Integration
* User Authentication
* PDF Report Generation
* API Support
* Threat Severity Scores

---

# ☁ Deployment Notes

## Local Deployment

Fully Supported:

* CSV Detection
* Real-Time Monitoring
* Packet Sniffing
* MongoDB Logging
* Email Alerts

---

## Streamlit Cloud Deployment

Supported:

* CSV Detection
* Dashboard Visualization

Not Supported:

* Real-time packet sniffing
* Local firewall blocking
* localhost MongoDB

For cloud deployment:

* Use MongoDB Atlas
* Replace live sniffing with APIs

---

# 🧾 Requirements

```txt
streamlit
streamlit-autorefresh
pandas
numpy
scikit-learn
joblib
plotly
scapy
pymongo
dnspython
matplotlib
scipy
```

---

# 👨‍💻 Author

Developed as an AI-powered cybersecurity and machine learning project for intelligent network threat detection.
Aman Pandey
---

# 📜 License

This project is intended for educational and research purposes.

Use responsibly and ethically.
