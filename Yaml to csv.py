import os
import yaml
import pandas as pd
from collections import defaultdict

# Paths
BASE_DIR = r"C:\Users\Abuthahir\project\Stock_Analysis\Raw_data"
OUTPUT_DIR = r"C:\Users\Abuthahir\project\Stock_Analysis\Csv_data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

merged_records = []
symbol_records = defaultdict(list)

# Walk through all date folders & yaml files
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if not file.endswith((".yaml", ".yml")):
            continue

        file_path = os.path.join(root, file)
        date = os.path.splitext(file)[0]  # safer than replace

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        # Case 1: YAML as dict (symbol -> values)
        if isinstance(data, dict):
            for symbol, values in data.items():
                if not isinstance(values, dict):
                    continue

                record = {
                    "date": date,
                    "symbol": symbol
                }
                record.update(values)

                merged_records.append(record)
                symbol_records[symbol].append(record)

        # Case 2: YAML as list of records
        elif isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue

                symbol = item.get("symbol") or item.get("Ticker")
                if not symbol:
                    continue

                record = {
                    "date": date,
                    "symbol": symbol
                }

                for k, v in item.items():
                    if k not in ["symbol", "Ticker"]:
                        record[k] = v

                merged_records.append(record)
                symbol_records[symbol].append(record)

# ---- Company-wise CSV ----
for symbol, records in symbol_records.items():
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.sort_values("date", inplace=True)

    df.to_csv(
        os.path.join(OUTPUT_DIR, f"{symbol}.csv"),
        index=False
    )

# ---- Overall merged CSV ----
df_merged = pd.DataFrame(merged_records)
df_merged["date"] = pd.to_datetime(df_merged["date"], errors="coerce")
df_merged.sort_values(["symbol", "date"], inplace=True)

merged_path = os.path.join(OUTPUT_DIR, "all_stocks_merged.csv")
df_merged.to_csv(merged_path, index=False)

print("✅ 50 individual company CSVs + 1 merged CSV created successfully")
