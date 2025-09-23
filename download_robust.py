#!/usr/bin/env python3
"""
Robust dataset downloader with retry logic and individual file handling.
"""
import os
import time
from huggingface_hub import hf_hub_download, list_repo_files
from tqdm import tqdm

def download_file_with_retry(repo_id, filename, local_dir, max_retries=3):
    """Download a single file with retry logic."""
    for attempt in range(max_retries):
        try:
            print(f"\nAttempting to download {filename} (attempt {attempt + 1}/{max_retries})")
            
            # Download to local directory
            downloaded_path = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                repo_type="dataset",
                local_dir=local_dir,
                force_download=False,  # Resume if file exists
                local_files_only=False
            )
            
            print(f"✅ Successfully downloaded: {filename}")
            return downloaded_path
            
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed for {filename}: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print(f"🚫 Failed to download {filename} after {max_retries} attempts")
                return None

def main():
    repo_id = "awsaf49/sonics"
    local_dir = "dataset"
    
    print(f"🔍 Listing files in repository: {repo_id}")
    
    try:
        # Get list of all files in the repository
        all_files = list_repo_files(repo_id=repo_id, repo_type="dataset")
        print(f"📁 Found {len(all_files)} files to download")
        
        # Create local directory if it doesn't exist
        os.makedirs(local_dir, exist_ok=True)
        
        # Sort files by size (smaller files first, then large zip files)
        def file_priority(filename):
            if filename.endswith('.zip'):
                return 1  # Large zip files last
            else:
                return 0  # Small files first
        
        sorted_files = sorted(all_files, key=file_priority)
        
        # Download each file individually
        successful_downloads = 0
        failed_downloads = []
        
        for i, filename in enumerate(tqdm(sorted_files, desc="Downloading files")):
            print(f"\n📥 Processing file {i+1}/{len(sorted_files)}: {filename}")
            
            # Check if file already exists and is complete
            local_path = os.path.join(local_dir, filename)
            if os.path.exists(local_path):
                print(f"✅ File already exists: {filename}")
                successful_downloads += 1
                continue
            
            # Download the file
            result = download_file_with_retry(repo_id, filename, local_dir)
            
            if result:
                successful_downloads += 1
            else:
                failed_downloads.append(filename)
                # Ask user if they want to continue or stop
                response = input(f"\n❓ Failed to download {filename}. Continue with remaining files? (y/n): ")
                if response.lower() != 'y':
                    break
        
        # Summary
        print(f"\n📊 Download Summary:")
        print(f"✅ Successful: {successful_downloads}/{len(sorted_files)}")
        print(f"❌ Failed: {len(failed_downloads)}")
        
        if failed_downloads:
            print(f"🚫 Failed files: {failed_downloads}")
        else:
            print(f"🎉 All files downloaded successfully!")
            
    except Exception as e:
        print(f"💥 Error listing repository files: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())