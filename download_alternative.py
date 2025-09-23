#!/usr/bin/env python3
"""
Alternative downloader using direct URLs and external tools
"""
import subprocess
import os
from huggingface_hub import get_hf_file_metadata, hf_hub_url

def download_with_wget(repo_id, filename, local_dir):
    """Download using wget with resume capability"""
    try:
        # Get the direct download URL
        url = hf_hub_url(repo_id=repo_id, filename=filename, repo_type="dataset")
        
        # Create directory structure
        file_path = os.path.join(local_dir, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Use wget with continue and timeout options
        cmd = [
            "wget", 
            "--continue",  # Resume partial downloads
            "--timeout=30",  # 30 second timeout
            "--tries=3",  # 3 retry attempts
            "--progress=bar",  # Show progress
            "-O", file_path,  # Output file
            url
        ]
        
        print(f"📥 Downloading {filename} using wget...")
        print(f"💡 Command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully downloaded: {filename}")
            return True
        else:
            print(f"❌ wget failed with return code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def download_with_curl(repo_id, filename, local_dir):
    """Download using curl with resume capability"""
    try:
        # Get the direct download URL
        url = hf_hub_url(repo_id=repo_id, filename=filename, repo_type="dataset")
        
        # Create directory structure
        file_path = os.path.join(local_dir, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Use curl with continue and timeout options
        cmd = [
            "curl",
            "-C", "-",  # Resume from where it left off
            "--connect-timeout", "30",  # 30 second connection timeout
            "--max-time", "3600",  # 1 hour max total time
            "--retry", "3",  # 3 retry attempts
            "--retry-delay", "5",  # 5 second delay between retries
            "--progress-bar",  # Show progress bar
            "-L",  # Follow redirects
            "-o", file_path,  # Output file
            url
        ]
        
        print(f"📥 Downloading {filename} using curl...")
        print(f"💡 Command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully downloaded: {filename}")
            return True
        else:
            print(f"❌ curl failed with return code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    repo_id = "awsaf49/sonics"
    local_dir = "dataset"
    filename = "fake_songs/part_01.zip"
    
    print("🔧 Alternative download methods for problematic files")
    print(f"🎯 Target: {filename}")
    
    print("\n🎯 Options:")
    print("1. Try wget (with resume)")
    print("2. Try curl (with resume)")
    print("3. Show direct download URL")
    print("4. Cancel")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Check if wget is available
        try:
            subprocess.run(["wget", "--version"], capture_output=True, check=True)
            download_with_wget(repo_id, filename, local_dir)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ wget not found. Please install it: sudo pacman -S wget")
    
    elif choice == "2":
        # Check if curl is available
        try:
            subprocess.run(["curl", "--version"], capture_output=True, check=True)
            download_with_curl(repo_id, filename, local_dir)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ curl not found. Please install it: sudo pacman -S curl")
    
    elif choice == "3":
        try:
            url = hf_hub_url(repo_id=repo_id, filename=filename, repo_type="dataset")
            print(f"\n🔗 Direct download URL:")
            print(f"{url}")
            print(f"\n💡 You can use this URL with any download manager")
        except Exception as e:
            print(f"❌ Error getting URL: {e}")
    
    elif choice == "4":
        print("👋 Cancelled")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()