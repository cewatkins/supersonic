from huggingface_hub import snapshot_download

# Download the full dataset with reduced concurrency to avoid hanging
snapshot_download(
    repo_id="awsaf49/sonics", 
    repo_type="dataset", 
    local_dir="dataset",
    max_workers=2,  # Reduce concurrent downloads from default (8) to 2
    resume_download=True,  # Resume interrupted downloads
    force_download=False  # Don't re-download existing files
)

print("Full dataset downloaded to dataset/")