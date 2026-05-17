import os
import time

from src.preprocess import preprocess
from src.train import train

# =====================================
# PROJECT HEADER
# =====================================

print("\n====================================")

print("🚀 AI NETWORK INTRUSION DETECTION")

print("====================================\n")

time.sleep(1)

# =====================================
# CREATE REQUIRED FOLDERS
# =====================================

folders = [

    "models",

    "logs",

    "reports",

    "data/processed"
]

for folder in folders:

    os.makedirs(
        folder,
        exist_ok=True
    )

print("✅ Required folders checked")

time.sleep(1)

# =====================================
# STEP 1 — PREPROCESSING
# =====================================

print("\n====================================")

print("📦 STEP 1 — DATA PREPROCESSING")

print("====================================\n")

time.sleep(1)

preprocess()

print("\n✅ Preprocessing Completed")

time.sleep(1)

# =====================================
# STEP 2 — MODEL TRAINING
# =====================================

print("\n====================================")

print("🧠 STEP 2 — MODEL TRAINING")

print("====================================\n")

time.sleep(1)

train()

print("\n✅ Training Completed")

time.sleep(1)

# =====================================
# FINAL MESSAGE
# =====================================

print("\n====================================")

print("🎉 PROJECT COMPLETED SUCCESSFULLY")

print("====================================\n")

print("Generated Files:")

print("\n📁 Models Saved → models/")

print("📁 Reports Saved → reports/")

print("📁 Logs Saved → logs/")

print("\n🚀 Ready For Dashboard & Live Detection")