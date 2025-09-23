#!/usr/bin/env python3
"""
Download only essential files (no large zip files) to get started quickly.
"""
from huggingface_hub import hf_hub_download

def download_essential_files():
    """Download only the essential metadata and CSV files."""
    repo_id = "awsaf49/sonics"
    local_dir = "dataset"
    
    # Essential files (excluding large zip files)
    essential_files = [
        "README.md",
        "metadata.json", 
        "real_songs.csv",
        "fake_songs.csv",
        "train.csv",
        "valid.csv", 
        "test.csv",
        ".gitattributes"
    ]
    
    print("📥 Downloading essential files (excluding large zip files)...")
    
    for filename in essential_files:
        try:
            print(f"⬇️  Downloading {filename}...")
            hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                repo_type="dataset",
                local_dir=local_dir,
                force_download=False
            )
            print(f"✅ Downloaded: {filename}")
        except Exception as e:
            print(f"⚠️  Could not download {filename}: {str(e)}")
    
    print("\n🎉 Essential files downloaded!")
    print("💡 You can now explore the dataset metadata and CSV files.")
    print("🗂️  Large audio zip files can be downloaded later if needed.")

if __name__ == "__main__":
    download_essential_files()