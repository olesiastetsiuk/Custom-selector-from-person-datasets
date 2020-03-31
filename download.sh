#!/bin/sh

mkdir ./PennFudanPed                                                                 && \
cd ./PennFudanPed                                                                    && \
curl -sS https://www.cis.upenn.edu/~jshi/ped_html/PennFudanPed.zip > file.zip        && \
unzip file.zip                                                                       && \
rm file.zip
echo Downloaded Penn-Fudan Database for Pedestrian Detection and Segmentation