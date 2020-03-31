  

## Description:

  

It is a typical situation when we have only a relatively small sample of the data expected later. How could we benefit from open datasets to augment our sample to train baseline model which will be better than already available pretrained?

  

Repository was created for experiments with [Penn-Fudan Database for Pedestrian Detection and Segmentation](https://www.cis.upenn.edu/~jshi/ped_html/) as target sample and a few open  person datasets as a sources for custom selecting images similar to ones in the target sample. 
Selecting could be based on a few attributes, such as objects scales, IOU distributions (typical occlusions), keypoints distribution (to check popular poses). 


  

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

- with pd. Dataframe we could select  images, combine datasets to create .csv to be converted to tf.records for training, this is our filter for datasets. 

At the moment selection was tested for Wider dataset. Script to select and save custom categories from COCO:
`/datasets/COCO_person/download_person_dataset.ipynb`

## To optimise

  - `/experiments/convert_to_tensorrt.ipynb`

## To test performance

  - `/experiments/performance.ipynb`
  
[ssd_resnet_50_fpn_coco](http://download.tensorflow.org/models/object_detection/ssd_resnet50_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03.tar.gz) was chosen as a baseline model, it was trained on a part of Wider validation dataset with the scales similar to target dataset.

|model| speed on CPU |
|--|--|
| ssd_resnet_50_fpn | 1.906570651170706 2.242779171540924 |



**Next steps ideas:**

- from tf api switch to [nmdetection](https://github.com/open-mmlab/mmdetection) for baseline prototyping (for conversion pytorch -> onnx -> tensorrt)

- test [augmentation libraries](https://github.com/albumentations-team/albumentations)

- test [uda](https://github.com/vfdev-5/UDA-pytorch)

- test [Siamese Mask R-CNN from](https://github.com/bethgelab/siamese-mask-rcnn) [One-Shot Instance Segmentation](https://arxiv.org/abs/1811.11507)