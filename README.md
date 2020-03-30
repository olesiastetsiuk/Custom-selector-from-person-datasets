  

## Description:

  

It is a typical situation when we have only a relatively small sample of the data expected later. How could we benefit from open datasets to augment our sample to train baseline model which will be better than already available pretrained?

  

Repository was created for experiments with [Penn-Fudan Database for Pedestrian Detection and Segmentation](https://www.cis.upenn.edu/~jshi/ped_html/) as target sample and a few open  person datasets as a sources for custom selecting images similar to ones in the target sample. 

  

## To start

  

- download dataset

- explore

- select  

## To optimise

  - convert

## To test performance

  - run

|  model name|speed  |
|--|--|
|  |  |


**Next steps ideas:**

- from tf api switch to [nmdetection](https://github.com/open-mmlab/mmdetection) for baseline prototyping (for conversion pytorch -> onnx -> tensorrt)

- test [augmentation libraries](https://github.com/albumentations-team/albumentations)

- test [uda](https://github.com/vfdev-5/UDA-pytorch)

- test [Siamese Mask R-CNN from](https://github.com/bethgelab/siamese-mask-rcnn) [One-Shot Instance Segmentation](https://arxiv.org/abs/1811.11507)