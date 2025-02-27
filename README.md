# SONICS: Synthetic Or Not - Identifying Counterfeit Songs

[![Paper](https://img.shields.io/badge/ICLR-2025-blue)](https://openreview.net/forum?id=PY7KSh29Z8)  [![Paper](https://img.shields.io/badge/ArXiv-Paper-red)](https://arxiv.org/abs/2408.14080)  [![Hugging Face](https://img.shields.io/badge/HuggingFace-Model-yellow)](https://huggingface.co/collections/awsaf49/sonics-spectttra-67bb6517b3920fd18e409013)  [![Hugging Face Dataset](https://img.shields.io/badge/HuggingFace-Dataset-orange)](https://huggingface.co/datasets/awsaf49/sonics)  [![Kaggle Dataset](https://img.shields.io/badge/Kaggle-Dataset-blue?logo=kaggle)](https://www.kaggle.com/datasets/awsaf49/sonics-dataset)  [![Hugging Face Demo](https://img.shields.io/badge/HuggingFace-Demo-blue)](https://huggingface.co/spaces/awsaf49/sonics-fake-song-detection)  [![License](https://img.shields.io/badge/License-MIT%20License-blue)](https://opensource.org/licenses/MIT)

This repository contains the official source code for our paper **SONICS: Synthetic Or Not - Identifying Counterfeit Songs**.


## 📌 **Abstract**
The recent surge in AI-generated songs presents exciting possibilities and challenges. These innovations necessitate the ability to distinguish between human-composed and synthetic songs to safeguard artistic integrity and protect human musical artistry. Existing research and datasets in fake song detection only focus on singing voice deepfake detection (SVDD), where the vocals are AI-generated
but the instrumental music is sourced from real songs. However, these approaches are inadequate for detecting contemporary end-to-end artificial songs where all components (vocals, music, lyrics, and style) could be AI-generated. Additionally, existing datasets lack music-lyrics diversity, long-duration songs, and open-access fake songs. To address these gaps, we introduce SONICS, a novel dataset
for end-to-end Synthetic Song Detection (SSD), comprising over 97k songs (4,751 hours) with over 49k synthetic songs from popular platforms like Suno and Udio. Furthermore, we highlight the importance of modeling long-range temporal dependencies in songs for effective authenticity detection, an aspect entirely overlooked in existing methods. To utilize long-range patterns, we introduce SpecTTTra, a novel architecture that significantly improves time and memory efficiency over conventional CNN and Transformer-based models. For long songs, our top-performing variant outperforms ViT by 8% in F1 score, is 38% faster, and uses 26% less memory, while also surpassing ConvNeXt with a 1% F1 score gain, 20% speed boost, and 67% memory reduction.

## Spectro Temporal Tokenizer
![Model Architecture](sonics-specttra-v2.jpg)





## System Configuration

- Disk Space: 150GB
- GPU Memory: 48GB
- RAM: 32GB
- Python Version: 3.10
- OS: Ubuntu 20.04
- CUDA Version: 12.4

## Installation

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Dataset 

You can download the dataset either from Huggingface or Kaggle. To download it from Huggingface, run the following code snippet,

```
from huggingface_hub import snapshot_download

snapshot_download(repo_id="awsaf49/sonics", repo_type="dataset", local_dir="you_local_folder")
```

To download it from Kaggle, you can either do it manually or do it via Kaggle API. For using Kaggle API, first you need to set it up following [this documentation](https://www.kaggle.com/docs/api?utm_me...=). Afterwards, run the following command

```
kaggle datasets download -d awsaf49/sonics-dataset --unzip
```

After downloading the dataset, the folder structure should look like following:

```
parentFolder
│
├──sonics
│
├──dataset
│       ├──real_songs  
│       │   └──xxx.mp3 
│       ├──fake_songs
│       │   └──yyy.mp3
│       ├──real_songs.csv
│       └──fake_songs.csv
```

## Metadata Properties
The first metadata file (`real_songs.csv`) contains the following information,

`filename`: Name of the file 

`title`: Title of the song

`artist`: name of the artist

`year`: song release year

`lyrics`: lyrics of the song 

`duration`: total duration of the song (in seconds)

`youtube_id`: Youtube ID of the real song. We do not provide the real songs in mp3 format.

`label`: real/fake. For this file all labels are "real"

`artist_overlap`: does test and train split contains this same artist.

`target`: 0/1. For real songs the target is 0.

`skip_time`: the amount of time for start (in seconds) that contain only instrumental.

`no_vocal`: True/False. Is the songs fully instrumental with no vocal components.

`split`: train/test split

Apart from these, the second metadata file (`fake_songs.csv`) contains the following additional fields- 

`id`: file ID

`algorithm`: the algorithm used to generate the fake song. chirp variants are from suno.

`style`: characteristics of the song. Might include information about male or female voices, instrumental details, and setting of the song.

`bit_rate`: Bit Rate of the generated song. Initially, it can vary. But before training, the bitrate of a song gets downscaled to a unique number.

`source`: Was the song generated from Suno or Udio.

`lyrics_features`: short description about the lyrics

`topic`: The topic of the song. e.g., star trek, pokemon etc.

`genre`: song genre. e.g., salsa, grunge etc.

`mood`: mood of the song. e.g., mournful, tense etc.



## Data Split 

To split it into train, val, and test set, we will need to run the following command from the parent folder

```shell
python data_split.py
```

> **Note:** The `real_songs.csv` and `fake_songs.csv` contain the metadata for the songs including filepath, duration, split, etc and config file contains path of the metadata.

> **Note:** Output files including checkpoints, model predictions will be saved in `./output/<experiment_name>/` folder.

## Training

Choose any of the config from `config` folder and run the following

```shell
python train.py --config <path to the config file>
```

## Testing

Choose any of the config from `config` folder and run the following

```shell
python test.py --config <path to the config file> --ckpt_path <path to the checkpoint file>
```

## Model Profiling

Choose any of the config from `config` folder and run the following
```shell
python model_profile.py --config <path to the config file> --batch_size 12
```

## 📊 Model Performance Comparison

| Model Name                     | HF Link | Variant        | Duration | f_clip | t_clip | F1  | Sensitivity | Specificity | Speed (A/S) | FLOPs (G) | Mem. (GB) | # Act. (M) | # Param. (M) |
|--------------------------------|---------|---------------|----------|--------|--------|-----|-------------|-------------|-------------|-----------|-----------|------------|-------------|
| `sonics-spectttra-alpha-5s`   | <a class="hf-button" href="https://huggingface.co/awsaf49/sonics-spectttra-alpha-5s"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg">HF</a>  | SpecTTTra-α   | 5s       | 1      | 3      | 0.78 | 0.69        | 0.94        | 148         | 2.9       | 0.5       | 6          | 17          |
| `sonics-spectttra-beta-5s`    | <a class="hf-button" href="https://huggingface.co/awsaf49/sonics-spectttra-beta-5s"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg">HF</a>  | SpecTTTra-β   | 5s       | 3      | 5      | 0.78 | 0.69        | 0.94        | 152         | 1.1       | 0.2       | 5          | 17          |
| `sonics-spectttra-gamma-5s`   | <a class="hf-button" href="https://huggingface.co/awsaf49/sonics-spectttra-gamma-5s"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg">HF</a>  | SpecTTTra-γ   | 5s       | 5      | 7      | 0.76 | 0.66        | 0.92        | 154         | 0.7       | 0.1       | 2          | 17          |
| `sonics-spectttra-alpha-120s` | <a class="hf-button" href="https://huggingface.co/awsaf49/sonics-spectttra-alpha-120s"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg">HF</a>  | SpecTTTra-α   | 120s     | 1      | 3      | 0.97 | 0.96        | 0.99        | 47          | 23.7      | 3.9       | 50         | 19          |
| `sonics-spectttra-beta-120s`  | <a class="hf-button" href="https://huggingface.co/awsaf49/sonics-spectttra-beta-120s"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg">HF</a>  | SpecTTTra-β   | 120s     | 3      | 5      | 0.92 | 0.86        | 0.99        | 80          | 14.0      | 2.3       | 29         | 17          |
| `sonics-spectttra-gamma-120s` | <a class="hf-button" href="https://huggingface.co/awsaf49/sonics-spectttra-gamma-120s"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg">HF</a>  | SpecTTTra-γ   | 120s     | 5      | 7      | 0.97 | 0.96        | 0.99        | 97          | 10.1      | 1.6       | 138        | 22          |

## Acknowledgement

We have utilized the code and models provided in the following repository:

- [Pytorch Image Models](https://github.com/huggingface/pytorch-image-models)

## License

This project is licensed under the MIT License for code and checkpoints/models, and the CC BY-NC 4.0 License for the dataset. See the [LICENSE](./LICENSE) file for more details.
