import sys
import csv
import os
import zipfile
import glob

def get_fake_file(real_id):
    """
    Given a real song ID like 'real_04742', find the corresponding fake song filename from fake_songs.csv,
    locate it in one of the 10 zip files, and extract just that specific file to dataset/extracted/.
    Will find all versions (e.g., _0.mp3, _1.mp3, etc.) if they exist.
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
    
    print(f"Looking for file: {filename}")
    
    # Create extraction directory
    extract_dir = 'dataset/extracted'
    os.makedirs(extract_dir, exist_ok=True)
    
    # Look for the file in all zip files
    zip_pattern = 'dataset/fake_songs/part_*.zip'
    zip_files = glob.glob(zip_pattern)
    
    if not zip_files:
        raise FileNotFoundError("No zip files found in dataset/fake_songs/. Please download them first.")
    
    print(f"Searching in {len(zip_files)} zip files...")
    
    extracted_files = []
    
    # Search for the file in each zip
    for zip_path in sorted(zip_files):
        print(f"Checking {os.path.basename(zip_path)}...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Get list of files in this zip
                zip_contents = zip_ref.namelist()
                
                # Debug: show first few files in this zip
                print(f"  Sample files in zip: {zip_contents[:3]}...")
                
                # Look for all versions of our target file (base_name_0, base_name_1, etc.)
                # First, get the base name without the number suffix
                if '_' in filename and filename.split('_')[-1].isdigit():
                    # If filename ends with _digit, get the base part
                    base_name = '_'.join(filename.split('_')[:-1])
                else:
                    # If no digit suffix, use the whole filename as base
                    base_name = filename
                
                # Generate patterns for multiple versions (0, 1, 2, 3)
                base_patterns = []
                for i in range(4):  # Check versions 0, 1, 2, 3
                    base_patterns.append(f"{base_name}_{i}")
                
                # Also include the original filename pattern
                base_patterns.append(filename)
                
                print(f"  Looking for patterns: {base_patterns[:3]}...")
                
                for base_pattern in base_patterns:
                    possible_patterns = [
                        base_pattern,  # exact match
                        base_pattern + '.wav',  # with .wav extension
                        base_pattern + '.mp3',  # with .mp3 extension
                        base_pattern + '.flac', # with .flac extension
                        'fake_songs/' + base_pattern,  # in subfolder
                        'fake_songs/' + base_pattern + '.wav',  # in subfolder with extension
                        'fake_songs/' + base_pattern + '.mp3',
                        'fake_songs/' + base_pattern + '.flac'
                    ]
                    
                    for pattern in possible_patterns:
                        for zip_file in zip_contents:
                            if zip_file.endswith(pattern) or zip_file == pattern:
                                print(f"Found {zip_file} in {os.path.basename(zip_path)}")
                                
                                # Extract this file
                                dest_filename = os.path.basename(zip_file)
                                dest_path = os.path.join(extract_dir, dest_filename)
                                
                                # Skip if already extracted
                                if dest_path in extracted_files:
                                    continue
                                
                                # Read the file from zip and write to destination
                                with zip_ref.open(zip_file) as source, open(dest_path, 'wb') as dest:
                                    dest.write(source.read())
                                
                                print(f"Extracted {dest_filename} to {extract_dir}/")
                                extracted_files.append(dest_path)
                    
        except zipfile.BadZipFile:
            print(f"Warning: {os.path.basename(zip_path)} is not a valid zip file or is corrupted")
            continue
        except Exception as e:
            print(f"Error reading {os.path.basename(zip_path)}: {e}")
            continue
    
    if extracted_files:
        print(f"\nSuccessfully extracted {len(extracted_files)} file(s):")
        for file_path in extracted_files:
            print(f"  {file_path}")
        return extracted_files
    
    # If we get here, file wasn't found. Let's show what files ARE available
    print(f"\nFile {filename} not found. Here are some sample files from the zips:")
    for zip_path in sorted(zip_files)[:2]:  # Check first 2 zips
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                contents = zip_ref.namelist()
                print(f"\n{os.path.basename(zip_path)} contains {len(contents)} files. First 10:")
                for i, file in enumerate(contents[:10]):
                    print(f"  {file}")
                if len(contents) > 10:
                    print(f"  ... and {len(contents) - 10} more files")
        except Exception as e:
            print(f"Error reading {zip_path}: {e}")
    
    raise FileNotFoundError(f"File {filename} (or similar patterns) not found in any of the zip files")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_fake_file.py <real_id>")
        print("Example: python get_fake_file.py real_04742")
        sys.exit(1)
    
    real_id = sys.argv[1]
    try:
        result_paths = get_fake_file(real_id)
        if result_paths:
            print(f"\nSuccess! Extracted {len(result_paths)} file(s) to dataset/extracted/")
            for path in result_paths:
                file_size = os.path.getsize(path)
                print(f"  {os.path.basename(path)} ({file_size:,} bytes)")
        else:
            print("No files were extracted.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)