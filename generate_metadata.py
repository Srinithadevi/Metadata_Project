import pandas as pd
import os

def detect_datatype(series):
    if pd.api.types.is_string_dtype(series):
        return "String"
    elif pd.api.types.is_numeric_dtype(series):
        return "Numeric"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "Datetime"
    else:
        return "Unknown"

def generate_metadata_for_folder(folder_path, output_file="metadata.xlsx"):
    metadata_rows = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            table_name = os.path.splitext(filename)[0].capitalize()
            df = pd.read_csv(file_path)

            for column in df.columns:
                field_name = column
                field_data = df[column]
                field_datatype = detect_datatype(field_data)
                non_null_count = field_data.count()
                total_count = len(df)
                occ_percent = round((non_null_count / total_count) * 100, 2)
                samples = field_data.dropna().astype(str).unique()[:3]
                sample_str = " | ".join(samples)

                metadata_rows.append({
                    "Table_Name": table_name,
                    "Field_Name": field_name,
                    "Field_Datatype": field_datatype,
                    "Occurance (number)": non_null_count,
                    "Occurance (Percentage)": f"{occ_percent}%",
                    "Samples_from_field": sample_str,
                    "Description_table": f"This {table_name.lower()} table is about the {table_name.lower()} of cycle"
                })

    metadata_df = pd.DataFrame(metadata_rows)
    metadata_df.to_excel(output_file, index=False)
    print(f"Metadata written to {output_file}")

# Use this path directly
folder_path = "C:/Users/srini/Metadata_Project"
generate_metadata_for_folder(folder_path)
