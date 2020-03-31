import json
from pathlib import Path

import statistics
import PIL.Image
import pandas as pd

import IPython.display
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def explore(root: str, ann_path_mask:str) -> pd.DataFrame:
    """Explore dataset annotations"""

    mean_box_sizes_per_img = []
    box_counter_per_img = []

    files = list(Path(root).glob(ann_path_mask))    
    file_jsons = (json.loads(file.read_text()) for file in files)
    ann_data = [data for data in file_jsons]

    def get_size(box):
        widht = box[2] - box[0]
        height = box[3] - box[1]
        return (widht, height)

    for ann in ann_data:
        sizes = []
        counter = 0
        for key, value in ann.items():
            counter =+ len(value)
            for box in value:                
                sizes.append(get_size(box))
        mean_box_sizes_per_img.append((statistics.mean([size[0] for size in sizes]),statistics.mean([size[1] for size in sizes])))
        box_counter_per_img.append(counter)


    return pd.DataFrame(data={
        'name': [f.name.split('.')[0] for f in files],
        'rects_num': box_counter_per_img,
        'mean_width':[item[0] for item in mean_box_sizes_per_img],
        'mean_height': [item[1] for item in mean_box_sizes_per_img],
        'path': [str(f) for f in files],
    })


def show_hist(dataset: pd.DataFrame, ds_name: str):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f'Number of rects / image',
            f'Mean rects height / image',
            f'Mean rects width / image'
        ),
        y_title="count"
    )

    fig.append_trace(
        go.Histogram(
            x=dataset['rects_num']
        ),
        row=1, col=1)
        
    fig.append_trace(
        go.Histogram(
            x=dataset[dataset['mean_height'] > 0]['mean_height']
        ),
        row=1, col=2)

    fig.append_trace(
        go.Histogram(
            x=dataset[dataset['mean_width'] > 0]['mean_width']
        ),
        row=2, col=1)

    fig.update_layout(
        title=f'{ds_name} ({dataset["name"].count()} images)',
        showlegend=False,
        height=1200
    )

    fig.show()


def show_samples(dataset: pd.DataFrame, samples: int = 10, scale: float = 0.5):
    for row, path in enumerate(dataset['path'].sample(n=samples), start=0):
        img_path = path.replace('/annotations/', '/images/').replace('.json', '')
        if not Path(img_path).suffix:
            img_path = Path(img_path).with_suffix('.png')

        img = PIL.Image.open(img_path)

        new_size = int(img.width * scale), int(img.height * scale)
        img = img.resize(new_size)

        IPython.display.display(img)


def parse_pfd_to_csv(root: str, ann_path_mask:str)-> pd.DataFrame:
    
    files = list(Path(root).glob(ann_path_mask))    
    file_jsons = (json.loads(file.read_text()) for file in files)
    ann_data = [data for data in file_jsons]

    boxes = []
    box_counter_per_img = []

    for ann in ann_data:
        counter = 0       
        for key, value in ann.items():
            counter += len(value)     
            for box in value:
                boxes.append(box)
        box_counter_per_img.append(counter)

    unique_pathes = list(zip([str(f) for f in files], box_counter_per_img))
    pathes = [path[0] for path in unique_pathes for i in range(path[1])]
    img_pathes = [path.replace('/annotations/', '/images/').replace('.json', '') for path in pathes]
    img_sizes = [(PIL. Image. open(Path(path).with_suffix('.png')).size) for path in img_pathes]
                

    
    return pd.DataFrame(data={
        'filename': [img_path.split('/')[-1]+'.png' for img_path in img_pathes],
        'widht': [size[0] for size in img_sizes],
        'height': [size[1] for size in img_sizes],
        'class': 'person',
        'xmin': [box[0] for box in boxes],
        'ymin': [box[1] for box in boxes],
        'xmax': [box[2] for box in boxes],
        'ymax': [box[3] for box in boxes],
    })

def parse_wider_to_csv(root: str, ann_path_mask:str, class_name:int=1)-> pd.DataFrame:

    mapping = {1: 'person', 2: 'riders', 3: 'partially-visible persons', 4: 'ignore regions', 5: 'crowd'}

    files = list(Path(root).glob(ann_path_mask))

    ann = []

    for fl in files:
        df = pd.read_csv(fl, skiprows=1, names = ['class', 'xmin', 'ymin', 'xmax', 'ymax'], delim_whitespace=True)
        filename = str(fl).replace('/Annotations/', '/Images/').replace('.txt', '')
        df['filename'] = filename.split('/')[-1]
        df['width'], df['height'] = PIL. Image.open(Path(filename)).size 
        ann.append(df)
    
    ann = pd.concat(ann)   
    ann = ann.loc[ann['class'] == class_name]
    ann['class'] = mapping[class_name]

    return ann

#TODO: add IOU distribution, add explore for other open pedestrian datasets, refactor iterating/get rid of df double usage 