  

## Description:

(Work in progress)

Repository was created for experiments with [Penn-Fudan Database for Pedestrian Detection and Segmentation](https://www.cis.upenn.edu/~jshi/ped_html/) as small target sample and a few open person datasets as a sources for custom selecting images similar to ones in the target sample.

Selecting is be based on a few attributes, such as objects scales, IOU distributions (typical occlusions), keypoints distribution (to check popular poses). Later a few models will be trained to evaluatean approach. 

  
  

  

## To start

  

`python3.6 -m venv venv`

`source venv/bin/activate`

`pip install -U pip setuptools wheel`

`pip install -r requirements.txt`

  

  

- download Penn-Fudan dataset

`./download.sh`

- convert annotation to json

`/datasets/convert_pfp_to_json.py`

  

  

- explore

  

`/datasets/datasets_eda.ipynb`


  

At the moment selection was tested for Wider dataset. Script to select and save custom categories from COCO:

`/datasets/COCO_person/download_person_dataset.ipynb`

  


  
