import os
import subprocess
import time

def auto_retrain(threat_count):

    try:

        # Retrain after every 50 threats
        if threat_count % 50 == 0 and threat_count != 0:

            print("Auto Retraining Started...")

            subprocess.run(

                ["python", "src/train_model.py"]

            )

            print("Retraining Completed")

    except Exception as e:

        print("Retrain Error:", e)