import os
import json
import xml.etree.ElementTree as ET

# val_txt_path = 'datasets/kaist-rgbt/val.txt'
val_txt_path = 'datasets/kaist-rgbt/val_random.txt'
annotations_dir = 'datasets/kaist-rgbt/train/labels-xml'
# json_output_path = 'KAIST_annotation.json'
json_output_path = 'KAIST_annotation_random.json'

with open(val_txt_path, 'r') as f:
    lines = f.readlines()

kaist_annotation = {
    "info": {
        "dataset": "KAIST Multispectral Pedestrian Benchmark",
        "url": "https://soonminhwang.github.io/rgbt-ped-detection/",
        "related_project_url": "http://multispectral.kaist.ac.kr",
        "publish": "CVPR 2015"
    },
    "info_improved": {
        "sanitized_annotation": {
            "publish": "BMVC 2018",
            "url": "https://li-chengyang.github.io/home/MSDS-RCNN/",
            "target": "files in train-all-02.txt (set00-set05)"
        },
        "improved_annotation": {
            "url": "https://github.com/denny1108/multispectral-pedestrian-py-faster-rcnn",
            "publish": "BMVC 2016",
            "target": "files in test-all-20.txt (set06-set11)"
        }
    },
    "images": [],
    "annotations": [],
    "categories": [
        {"id": 0, "name": "person"},
        {"id": 1, "name": "cyclist"},
        {"id": 2, "name": "people"},
        {"id": 3, "name": "person?"}
    ]
}

image_id = 0
annotation_id = 0

for line in lines:
    image_path = line.strip()
    image_name = image_path.split('/')[-1].replace('.jpg', '')
    annotation_file = os.path.join(annotations_dir, image_name + '.xml')

    kaist_annotation['images'].append({
        "id": image_id,
        "im_name": image_name + '.jpg',
        "height": 512,
        "width": 640
    })
    
    if os.path.exists(annotation_file):
        tree = ET.parse(annotation_file)
        root = tree.getroot()
        
        for obj in root.findall('object'):
            category_name = obj.find('name').text
            category_id = next((item['id'] for item in \
                                kaist_annotation['categories'] if item["name"] == category_name), None)
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('x').text)
            ymin = int(bbox.find('y').text)
            width = int(bbox.find('w').text)
            height = int(bbox.find('h').text)
            occlusion = int(obj.find('occlusion').text)
            ignore = int(obj.find('difficult').text)
            
            kaist_annotation['annotations'].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "bbox": [xmin, ymin, width, height],
                "height": height,
                "occlusion": occlusion,
                "ignore": ignore
            })
            
            annotation_id += 1
    
    image_id += 1

with open(json_output_path, 'w') as f:
    json.dump(kaist_annotation, f, indent=4)
