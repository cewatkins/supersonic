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
    
    # List of large files that commonly have download issues
    large_files = [
        "fake_songs/part_01.zip",
        "fake_songs/part_02.zip", 
        "fake_songs/part_03.zip",
        "fake_songs/part_04.zip",
        "fake_songs/part_05.zip",
        "fake_songs/part_06.zip",
        "fake_songs/part_07.zip",
        "fake_songs/part_08.zip",
        "fake_songs/part_09.zip",
        "fake_songs/part_10.zip"
    ]
    
    print("🔧 Alternative download methods for large files")
    print("📦 Available files:")
    
    # Show file status
    for i, filename in enumerate(large_files, 1):
        file_path = os.path.join(local_dir, filename)
        status = "✅" if os.path.exists(file_path) else "❌"
        print(f"  {i:2d}. {status} {filename}")
    
    print(f"\n🎯 Options:")
    print("11. Download all missing files sequentially")
    print("12. Show direct download URL for a file")
    print("13. Cancel")
    
    choice = input(f"\nEnter your choice (1-{len(large_files)} for specific file, 11-13 for options): ").strip()
    
    try:
        choice_num = int(choice)
        
        if 1 <= choice_num <= len(large_files):
            filename = large_files[choice_num - 1]
            file_path = os.path.join(local_dir, filename)
            
            if os.path.exists(file_path):
                print(f"✅ File {filename} already exists!")
                overwrite = input("🔄 Download anyway? (y/n): ").strip().lower()
                if overwrite != 'y':
                    return
            
            print(f"🎯 Selected: {filename}")
            
            # Choose download method
            print("\n📥 Download method:")
            print("1. wget (with resume)")
            print("2. curl (with resume)")
            
            method = input("Choose method (1-2): ").strip()
            
            if method == "1":
                try:
                    subprocess.run(["wget", "--version"], capture_output=True, check=True)
                    download_with_wget(repo_id, filename, local_dir)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("❌ wget not found. Please install it: sudo pacman -S wget")
            
            elif method == "2":
                try:
                    subprocess.run(["curl", "--version"], capture_output=True, check=True)
                    download_with_curl(repo_id, filename, local_dir)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("❌ curl not found. Please install it: sudo pacman -S curl")
            else:
                print("❌ Invalid method choice")
        
        elif choice_num == 11:
            # Download all missing files
            missing_files = [f for f in large_files if not os.path.exists(os.path.join(local_dir, f))]
            
            if not missing_files:
                print("✅ All files already downloaded!")
                return
            
            print(f"📥 Found {len(missing_files)} missing files")
            method = input("Choose download method for all (1=wget, 2=curl): ").strip()
            
            for i, filename in enumerate(missing_files, 1):
                print(f"\n📥 Downloading file {i}/{len(missing_files)}: {filename}")
                
                if method == "1":
                    success = download_with_wget(repo_id, filename, local_dir)
                elif method == "2":
                    success = download_with_curl(repo_id, filename, local_dir)
                else:
                    print("❌ Invalid method")
                    return
                
                if not success:
                    cont = input(f"❌ Failed to download {filename}. Continue? (y/n): ")
                    if cont.lower() != 'y':
                        break
        
        elif choice_num == 12:
            # Show URL for a file
            file_choice = input(f"Which file URL to show (1-{len(large_files)})? ").strip()
            try:
                file_num = int(file_choice)
                if 1 <= file_num <= len(large_files):
                    filename = large_files[file_num - 1]
                    url = hf_hub_url(repo_id=repo_id, filename=filename, repo_type="dataset")
                    print(f"\n🔗 Direct download URL for {filename}:")
                    print(f"{url}")
                    print(f"\n💡 You can use this URL with any download manager")
                else:
                    print("❌ Invalid file number")
            except ValueError:
                print("❌ Invalid input")
            except Exception as e:
                print(f"❌ Error getting URL: {e}")
        
        elif choice_num == 13:
            print("👋 Cancelled")
        
        else:
            print("❌ Invalid choice")
            
    except ValueError:
        print("❌ Invalid input - please enter a number")

if __name__ == "__main__":
    main()