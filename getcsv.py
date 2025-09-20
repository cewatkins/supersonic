from huggingface_hub import hf_hub_download

# Download real_songs.csv
hf_hub_download(
    repo_id="awsaf49/sonics",
    filename="real_songs.csv",
    repo_type="dataset",
    local_dir="dataset"
)

# Download fake_songs.csv
hf_hub_download(
    repo_id="awsaf49/sonics",
    filename="fake_songs.csv",
    repo_type="dataset",
    local_dir="dataset"
)