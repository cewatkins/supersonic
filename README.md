# SONICS: Synthetic Or Not - Identifying Counterfeit Songs

This repository contains the official source code for our paper **SONICS: Synthetic Or Not - Identifying Counterfeit Songs**.


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

[As a part of our submission, we are not providing our dataset. It will be published after the final decision.]

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

After downloading the dataset, to split it into train, val, and test set, we will need to run the following part from the parent folder

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

## Acknowledgement

We have utilized the code and models provided in the following repository:

- [Pytorch Image Models](https://github.com/huggingface/pytorch-image-models)