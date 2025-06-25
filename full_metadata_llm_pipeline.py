import pandas as pd
import requests
import time
from datetime import datetime

# === Start the timer for the entire script ===
start_time = time.time()
start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"🚀 Description generation started at: {start_timestamp}")

# === File setup ===
input_file = "metadata_with_descriptions.csv"  # Change if needed
output_file = "final_output_with_timestamps.csv"
model_name = "mistral"

try:
    df = pd.read_csv(input_file)
    print(f"📄 Loaded {len(df)} rows from '{input_file}'")
except Exception as e:
    print(f"❌ Error reading file: {e}")
    exit()

# === Function to generate description with duration and timestamp ===
def generate_row_description(row):
    prompt = f"""
Generate a simple, clear description for the following metadata field:
- Table Name: {row['Table_Name']}
- Field Name: {row['Field_Name']}
- Field Datatype: {row['Field_Datatype']}
- Sample Values: {row['Samples_from_field']}

Respond in one sentence.
"""
    try:
        row_start = time.time()
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model_name, "prompt": prompt, "stream": False}
        )
        row_end = time.time()
        result = response.json()
        description = result.get("response", "").strip()
        duration = round(row_end - row_start, 2)
    except Exception as e:
        description = f"⚠️ Error generating description: {e}"
        duration = -1  # Indicates failure

    row["Row_Description"] = description
    row["Generated_At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row["Duration_Seconds"] = duration
    return row

# === Apply function row by row with progress ===
df = df.apply(generate_row_description, axis=1)

# === Save updated file ===
df.to_csv(output_file, index=False)
print(f"\n✅ Output saved to: {output_file}")

# === End timer for the script ===
end_time = time.time()
end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
total_duration = round(end_time - start_time, 2)

print(f"🏁 Description generation ended at: {end_timestamp}")
print(f"⏱️ Total time taken: {total_duration} seconds")
