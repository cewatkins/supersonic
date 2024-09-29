# SONICS: Synthetic Or Not - Identifying Counterfeit Songs

This repository contains the official source code for our paper:

SONICS: SYNTHETIC OR NOT - IDENTIFYING COUNTERFEIT SONGS


## System Configuration

- Disk Space: 150GB
- GPU Memory: 48GB

## Installation

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Dataset 

[As a part of our submission, we are not providing our dataset. It will be published after the final decision about acceptance.]

After downloading the dataset, the folder structure should look like following:

```
parentFolder
│
├──sonics
│
├──dataset
│       ├──real  
│       │   └── xxx.mp3 
│       ├──fake_songs
│       │   └──yyy.mp3
│       ├──real_songs.csv
│       └──fake_songs.csv
```

After downloading the dataset, to split it into train, val, and test set, we will need to run the following part from the parent folder

```
python data_split.py
```

## Training

Choose any of the config from `config` folder and run the following

```
python train.py --config ./configs/convnext-5s.yaml
```

## Acknowledgement

We have utilized the code and models provided in the following repository:

- [Pytorch Image Models](https://github.com/huggingface/pytorch-image-models)



