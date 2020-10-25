import json
import os
from pathlib import Path

result_dir = "vis/"
result_file = result_dir + "vis.json"

def predict(file_name):
   
    os.system("th eval.lua -model model_id1-501-1448236541.t7 -image_folder images -num_images 1")
    with open(result_file) as json_file:
        data = json.load(json_file)
    caption = []
    for items in data:
        caption.append(items["caption"])
    
    response = " ".join(caption)

    os.remove(file_name)
    os.remove(result_dir + "imgs/img1.jpg")
    os.remove(result_file)

    return response
