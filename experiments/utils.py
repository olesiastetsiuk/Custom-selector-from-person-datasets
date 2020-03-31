import cv2
import numpy as np
from PIL import Image, ImageDraw


def resize_keeping_aspect_ratio(image, min_dimension, max_dimension=None):

    height, width, _ = image.shape
    original_min_dim = min(height, width)
    scale_factor1 = min_dimension / original_min_dim
    height1 = np.round(height * scale_factor1)
    width1 = np.round(width * scale_factor1)
    new_height, new_width = height1, width1

    if max_dimension is not None:

        if max(height1, width1) < max_dimension:
            new_height, new_width = height1, width1
        else:
            original_max_dim = max(height, width)
            scale_factor2 = max_dimension / original_max_dim
            height2 = np.round(height * scale_factor2)
            width2 = np.round(width * scale_factor2)
            new_height, new_width = height2, width2

    image = cv2.resize(image, (int(new_width), int(new_height)), cv2.INTER_NEAREST)
    return image


def visualize(image_array, boxes, scores, labels):

    colors = {1: 'blue'}
    image = Image.fromarray(image_array.copy())
    draw = ImageDraw.Draw(image)

    width, height = image.size
    scaler = np.array([height, width, height, width], dtype='float32')
    boxes = scaler * boxes.copy()

    for i in range(len(boxes)):

        color = colors[labels[i]]
        text = '{:.3f}'.format(scores[i])

        ymin, xmin, ymax, xmax = boxes[i]
        draw.rectangle(
            [(xmin, ymin), (xmax, ymax)], outline=color
        )
        draw.text((xmin, ymin), text, fill=color)

    return image