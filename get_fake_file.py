import sys
import csv
import os
import shutil
import kagglehub

def get_fake_file(real_id):
    """
    Given a real song ID like 'real_04742', find the corresponding fake song filename from fake_songs.csv,
    download the full dataset using KaggleHub, and copy the specific file to dataset/.
    """
    if not real_id.startswith("real_") or not real_id.split("_")[1].isdigit():
        raise ValueError("Invalid real_id format. Expected 'real_XXXXX' where XXXXX is digits")
    
    # Extract the number part and remove leading zeros
    number = real_id.split("_")[1].lstrip('0')
    id_to_find = int(number)
    
    # Read fake_songs.csv to find the filename for the ID
    csv_file_path = 'dataset/fake_songs.csv'
    filename = None
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row['id']) == id_to_find:
                filename = row['filename']
                break
    
    if filename is None:
        raise ValueError(f"ID {id_to_find} not found in fake_songs.csv")
    
    # Download the full dataset using KaggleHub
    dataset_path = kagglehub.dataset_download("awsaf49/sonics-dataset")
    
    # Construct the source path
    source_path = os.path.join(dataset_path, 'fake_songs', filename)
    
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"File {source_path} not found in downloaded dataset")
    
    # Copy the file to dataset/
    dest_path = os.path.join('dataset', filename)
    shutil.copy(source_path, dest_path)
    
    print(f"Downloaded dataset and copied {filename} to dataset/")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_fake_file.py <real_id>")
        print("Example: python get_fake_file.py real_04742")
        sys.exit(1)
    
    real_id = sys.argv[1]
    try:
        get_fake_file(real_id)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)