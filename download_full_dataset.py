from huggingface_hub import snapshot_download

# Download the full dataset
snapshot_download(repo_id="awsaf49/sonics", repo_type="dataset", local_dir="dataset")

print("Full dataset downloaded to dataset/")