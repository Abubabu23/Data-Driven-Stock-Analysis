import os
import yaml
import pandas as pd


def load_and_process_data(yml_folder_path):
    all_data = []
    yaml_record_count = 0
    error_files = []

    
    for root, dirs, files in os.walk(yml_folder_path):
        for file in files:
            if file.lower().endswith((".yml", ".yaml")):
                file_path = os.path.join(root, file)

               
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = yaml.safe_load(f)
                except Exception as e:
                    error_files.append((file_path, f"YAML read failure: {e}"))
                    continue

               
                if isinstance(content, dict):
                    records = [content]
                elif isinstance(content, list):
                    records = content
                else:
                    error_files.append((file_path, "Invalid structure"))
                    continue

        
                for record in records:
                    if not isinstance(record, dict):
                        error_files.append((file_path, "Non-dict record in list"))
                        continue

                    
                    record = {str(k).lower(): v for k, v in record.items()}

                    df = pd.DataFrame([record])

                    # Rename columns
                    df.rename(columns={
                        'ticker': 'Stock',
                        'date': 'Date',
                        'open': 'Open',
                        'close': 'Close',
                        'high': 'High',
                        'low': 'Low',
                        'volume': 'Volume'
                    }, inplace=True)

                    all_data.append(df)
                    yaml_record_count += len(df)

    # If no data found
    if not all_data:
        raise ValueError("❌ No valid YAML records found.")

    # Combine all data
    final_df = pd.concat(all_data, ignore_index=True)

    # Data cleaning
    final_df['Date'] = pd.to_datetime(final_df['Date'], errors='coerce')
    final_df.sort_values(by=['Stock', 'Date'], inplace=True)
    final_df.reset_index(drop=True, inplace=True)

    # Save error log if exists
    if error_files:
        os.makedirs("csv", exist_ok=True)
        error_df = pd.DataFrame(error_files, columns=["File_Path", "Error_Reason"])
        error_df.to_csv("csv/error_files.csv", index=False)
        print("⚠️ Errors logged to csv/error_files.csv")

    return final_df, yaml_record_count


if __name__ == "__main__":
    

    yml_folder = r"C:\Users\Abuthahir\project\Stock_Analysis\Raw_data"
    
    output_folder = "csv"
    os.makedirs(output_folder, exist_ok=True)

   
    final_data, yaml_record_count = load_and_process_data(yml_folder)

    
    output_path = os.path.join(output_folder, "cleaned_stock_data.csv")
    final_data.to_csv(output_path, index=False)

   
    print("\n===== DATA SUMMARY =====")
    print(f"📄 Total YAML Records Processed : {yaml_record_count}")
    print(f"🧾 Total Final CSV Rows        : {len(final_data)}")
    print("=========================")
    print(f"✅ Cleaned CSV Saved To: {output_path}\n")