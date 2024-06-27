import os
import json

# Define the path to the directory containing the JSON files
json_dir = r"C:\Users\hamza\OneDrive - University of Manitoba\Documents\HISHAM\Computer Science\Laptop Scraper\JSON-files\Dell"

# Define the path for the output merged JSON file
output_file = r"C:\Users\hamza\OneDrive - University of Manitoba\Documents\HISHAM\Computer Science\Laptop Scraper\merged_dell_laptops.json"

# List to store the merged content
merged_data = []

# Iterate over each file in the directory
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(json_dir, filename)
        
        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Check if the data is a list
            if isinstance(data, list):
                for entry in data:
                    if 'link' in entry and not entry['link'].startswith('http'):
                        entry['link'] = 'https://' + entry['link']
                merged_data.extend(data)
            else:
                if 'link' in data and not data['link'].startswith('http'):
                    data['link'] = 'https://' + data['link']
                merged_data.append(data)

# Write the merged data to the output file
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(merged_data, outfile, indent=4)

print(f"Successfully merged {len(os.listdir(json_dir))} files into {output_file}")
