import os
import cv2
from datetime import datetime
from shutil import copyfileobj, rmtree, copyfile

from db.repository.csam_ratio import get_ratio


def create_border_img(image, save_dir):

    #shutil.copyfileobj() method to copy the contents of source file-like object to destination file-like object
    tempFile = "tmp/temp.png"
    with open(tempFile, "wb") as buffer: copyfileobj(image.file, buffer)

    ori_dir = os.path.join(save_dir,"original")
    if not os.path.exists(ori_dir): 
        os.makedirs(ori_dir)
        copyfile("tmp/temp.png",os.path.join(ori_dir,image.filename))
    else:
        no_of_files = len(os.listdir(ori_dir))
        new_fname = f"{image.filename.split('.')[0]}_{no_of_files}.png"
        os.rename(os.path.join(ori_dir,image.filename),os.path.join(ori_dir,new_fname))
        copyfile("tmp/temp.png",os.path.join(ori_dir,image.filename))

    image = cv2.imread(tempFile)
    h, w, z = image.shape
    border_img = cv2.copyMakeBorder(image,20,20,20,20,cv2.BORDER_REPLICATE)

    return border_img, [w,h]


def check_dir(image, lot_no, db):
    
    plate_no = image.filename.split(".")[0]

    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    lot_dir = os.path.join(backend_dir,'images',datetime.now().strftime("%b%y"),lot_no)
    save_dir = os.path.join(lot_dir,plate_no)
    temp_dir = os.path.join(save_dir,"temp")
    real_dir = os.path.join(save_dir,"real")
    others_dir = os.path.join(save_dir,"others")

    item_dict = {}
    no_of_batches,no_of_chips = 0,0
    if lot_no.lower()[:4] == "test" and os.path.isdir(lot_dir): rmtree(lot_dir)                 # Testing directory to be remove every testing
    if os.path.isdir(temp_dir) and any(os.scandir(temp_dir)):
        try:
            ratio = get_ratio(lot_no=lot_no, plate_no=plate_no, db=db)                              # Pull data from database for caching
            no_of_batches = ratio.no_of_batches
            no_of_chips = ratio.no_of_chips
            for i in range(no_of_batches): item_dict[f"Batch {i+1}"] = []
            item_dict = caching(temp_dir,item_dict,0)
            if os.path.isdir(real_dir) and any(os.scandir(real_dir)): item_dict = caching(real_dir,item_dict,1)
            if os.path.isdir(others_dir) and any(os.scandir(others_dir)): item_dict = caching(others_dir,item_dict,2)
        except:
            if os.path.isdir(save_dir): rmtree(save_dir) 
            os.makedirs(temp_dir)
    else:
        if os.path.isdir(save_dir): rmtree(save_dir) 
        os.makedirs(temp_dir)

    return no_of_chips, no_of_batches, item_dict, save_dir, temp_dir


def caching(directory,chips,class_type):

    for file in os.listdir(directory):
        if file.split(".")[-1] == "png":
            file = f"{class_type}{file[1:]}"
            if int(file.split("_")[1]) != 0: chips[f"Batch {file.split('_')[1]}"].append(file)
            elif "Stray" in chips.keys(): chips["Stray"].append(file)
            else: chips["Stray"] = []

    return chips