
import pandas as pd
import re
from datetime import datetime

log_path = "../validation_log.txt"

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

try:
    df = pd.read_csv("../data/suis_uav_data.csv")
    log("Started validation of suis_uav_data.csv")

    required_columns = ["mission_id", "timestamp", "location", "altitude_m", "image_path", "threat_level", "operator_id"]
    for col in required_columns:
        if df[col].isnull().any():
            log(f"[ERROR] Missing values in: {col}")
        else:
            log(f"[PASS] {col} - OK")

    pattern = r"\d{2}\.\d{4}[NS] \d{3}\.\d{4}[EW]"
    invalid_locs = df[~df["location"].str.contains(pattern, regex=True)]
    if not invalid_locs.empty:
        log("[ERROR] Invalid GPS location format:")
        log(invalid_locs.to_string())
    else:
        log("[PASS] GPS location format OK")

    valid_levels = {"Low", "Medium", "High"}
    if not df["threat_level"].isin(valid_levels).all():
        log("[ERROR] Invalid threat level detected.")
    else:
        log("[PASS] Threat levels valid")

    log("✅ Validation Complete")

except Exception as e:
    log(f"[EXCEPTION] {str(e)}")
