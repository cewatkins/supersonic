#!/usr/bin/env python3
"""
Interactive downloader - lets you choose which files to download
"""
from huggingface_hub import list_repo_files, hf_hub_download
import os

def main():
    repo_id = "awsaf49/sonics"
    local_dir = "dataset"
    
    print("🔍 Getting file list from repository...")
    try:
        all_files = list_repo_files(repo_id=repo_id, repo_type="dataset")
    except Exception as e:
        print(f"❌ Error accessing repository: {e}")
        return
    
    # Categorize files
    small_files = []
    large_files = []
    
    for file in all_files:
        if file.endswith('.zip'):
            large_files.append(file)
        else:
            small_files.append(file)
    
    print(f"\n📊 Repository contains:")
    print(f"  📄 Small files: {len(small_files)} (CSV, metadata, etc.)")
    print(f"  📦 Large files: {len(large_files)} (ZIP archives)")
    
    # Check what we already have
    existing_small = []
    existing_large = []
    
    for file in small_files:
        if os.path.exists(os.path.join(local_dir, file)):
            existing_small.append(file)
    
    for file in large_files:
        if os.path.exists(os.path.join(local_dir, file)):
            existing_large.append(file)
    
    print(f"\n✅ Already downloaded:")
    print(f"  📄 Small files: {len(existing_small)}/{len(small_files)}")
    print(f"  📦 Large files: {len(existing_large)}/{len(large_files)}")
    
    # Show options
    print(f"\n🎯 Options:")
    print(f"  1. Skip all downloads (you have the essential files)")
    print(f"  2. Download missing small files only")
    print(f"  3. Try downloading one large file at a time")
    print(f"  4. List all files and their status")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("✅ Skipping downloads. You can work with existing files!")
        return
    
    elif choice == "2":
        missing_small = [f for f in small_files if not os.path.exists(os.path.join(local_dir, f))]
        if not missing_small:
            print("✅ All small files already downloaded!")
            return
        
        print(f"📥 Downloading {len(missing_small)} missing small files...")
        for file in missing_small:
            try:
                print(f"⬇️  {file}")
                hf_hub_download(repo_id=repo_id, filename=file, repo_type="dataset", 
                              local_dir=local_dir, force_download=False)
                print(f"✅ Downloaded: {file}")
            except Exception as e:
                print(f"❌ Failed: {file} - {e}")
    
    elif choice == "3":
        missing_large = [f for f in large_files if not os.path.exists(os.path.join(local_dir, f))]
        if not missing_large:
            print("✅ All large files already downloaded!")
            return
            
        print(f"📦 Found {len(missing_large)} large files to download:")
        for i, file in enumerate(missing_large):
            print(f"  {i+1}. {file}")
        
        try:
            file_num = int(input(f"Which file to download (1-{len(missing_large)}, 0 to cancel)? "))
            if file_num == 0:
                return
            if 1 <= file_num <= len(missing_large):
                file = missing_large[file_num-1]
                print(f"📥 Downloading {file}...")
                print("💡 Press Ctrl+C to cancel if it hangs")
                
                hf_hub_download(repo_id=repo_id, filename=file, repo_type="dataset",
                              local_dir=local_dir, force_download=True)  # Force fresh download
                print(f"✅ Successfully downloaded: {file}")
            else:
                print("❌ Invalid selection")
        except ValueError:
            print("❌ Invalid input")
        except KeyboardInterrupt:
            print("\n⏹️  Download cancelled")
        except Exception as e:
            print(f"❌ Download failed: {e}")
    
    elif choice == "4":
        print(f"\n📄 Small files:")
        for file in small_files:
            status = "✅" if os.path.exists(os.path.join(local_dir, file)) else "❌"
            print(f"  {status} {file}")
        
        print(f"\n📦 Large files:")
        for file in large_files:
            status = "✅" if os.path.exists(os.path.join(local_dir, file)) else "❌"
            print(f"  {status} {file}")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()