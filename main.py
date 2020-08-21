from fastapi import FastAPI, File, UploadFile
import json
import subprocess
import os

app = FastAPI()


result_dir = "vis/"
result_file = result_dir + "vis.json"

@app.post("/uploadfile/")
def create_upload_file(file: UploadFile = File(...)):
    file_path = "images/" + file.filename
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    os.system("th eval.lua -model model_id1-501-1448236541.t7 -image_folder images -num_images 1")
    with open(result_file) as json_file:
        data = json.load(json_file)
    caption = []
    for items in data:
        caption.append(items["caption"])
    response = {
        "captions" : caption,
    }
    os.remove(file_path)
    os.remove(result_dir + "imgs/img1.jpg")
    os.remove(result_file)
    return response
