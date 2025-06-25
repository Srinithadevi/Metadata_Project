import pandas as pd
import requests
from datetime import datetime
import time

# === Load the metadata file ===
df = pd.read_csv("final_output_with_timestamps.csv")

# === Ask user for a question ===
question = input("❓ Ask a question about your metadata: ")

# === Build metadata string with progress ===
table_str = ""
total_rows = len(df)

print(f"\n📊 Starting to format metadata from {total_rows} rows...\n")

for i, row in df.iterrows():
    print(f"🔁 Processing row {i + 1} of {total_rows}")
    table_str += (
        f"Table: {row['Table_Name']} | "
        f"Field: {row['Field_Name']} | "
        f"Description: {row['Row_Description']} | "
        f"Generated At: {row['Generated_At']}\n"
    )

print("\n✅ Finished formatting metadata. Sending to LLM...\n")

# === Build prompt to LLM ===
prompt = f"""
You are a helpful assistant for understanding metadata. Below is a list of metadata fields, their descriptions, and when they were generated:

{table_str}

Now answer the following question based on the above metadata:
{question}
"""

# === Start time for response tracking ===
start_dt = datetime.now()
start_time = time.time()
print(f"\n🚀 LLM Request Start Time: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}")

# === Call local LLM via Ollama ===
try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    end_dt = datetime.now()
    end_time = time.time()
    duration = round(end_time - start_time, 2)

    # === Get answer and show output ===
    answer = response.json().get("response", "").strip()
    print("\n🧠 LLM Answer:\n" + answer)

    # === Print end time and duration ===
    print(f"\n🏁 LLM Request End Time: {end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️ Total Time Taken: {duration} seconds")

except Exception as e:
    print("⚠️ Error contacting LLM:", e)
