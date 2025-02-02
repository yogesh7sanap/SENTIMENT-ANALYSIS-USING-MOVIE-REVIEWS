import json
import pandas as pd
import glob
import csv

# Step1:
# Load multiple json files

json_files=glob.glob('*.json')  #Assuming all json files are in current directory

all_data=[]

# for file in json_files:
#   with open(file,"r") as f1:
#     data=json.load(f1) # load Json data
#     all_data.append(data) #Append data to the list

# Loop through each file
for json_file in json_files:
    with open(json_file, 'r') as file:
        data = json.load(file)
        all_data.extend(data)  # Combine all data from all files

# Now we need to get all possible keys from the JSON files
all_keys = set()
for entry in all_data:
    all_keys.update(entry.keys())

# Convert set to list for consistent ordering
all_keys = list(all_keys)

# Open a new CSV file to write the combined data
with open('IMDB_movie_review_dataset.csv', 'w', newline='', encoding='utf-8') as csv_file:
    # Initialize the CSV writer
    csv_writer = csv.DictWriter(csv_file, fieldnames=all_keys)

    # Write the header using the keys
    csv_writer.writeheader()

    # Write each row of data to the CSV
    for row in all_data:
        csv_writer.writerow(row)

print("Multiple JSON files have been successfully converted to a single CSV file!")
