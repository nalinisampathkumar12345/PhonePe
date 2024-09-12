import subprocess
import os
import json
import pandas as pd

# URL of the GitHub repository
repo_url = "https://github.com/PhonePe/pulse.git"
repo_dir = "pulse"

# Clone the repository if it doesn't already exist
if not os.path.exists(repo_dir):
    subprocess.run(["git", "clone", repo_url])
else:
    print(f"Repository '{repo_dir}' already exists. Skipping clone.")

# Directory where the data is expected
data_dir = os.path.join(repo_dir, "data")

# List to store file paths
data_files = []

# Walk through the data directory to find JSON files
for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith(".json"):
            data_files.append(os.path.join(root, file))

# List to hold the data loaded from JSON files
data = []

# Load the data from each JSON file into the list
for file in data_files:
    with open(file, 'r') as f:
        json_data = json.load(f)
        # Handle the case where JSON data is a list of dictionaries
        if isinstance(json_data, list):
            data.extend(json_data)
        else:
            data.append(json_data)

# Normalize the list of dictionaries into a pandas DataFrame
df = pd.json_normalize(data)

# Display DataFrame information
df.info()

# Print the DataFrame (optional)
print(df)
