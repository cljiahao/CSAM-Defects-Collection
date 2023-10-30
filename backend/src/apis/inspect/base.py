import os
import cv2
import time

from apis.inspect.components.batch_process import mask
from apis.inspect.components.chip_process import chips
from apis.inspect.components.initialize import check_dir, create_border_img


def time_print(time_dict):
    del time_dict["Start"]
    for i,j in time_dict.items():
        print(f"{i} took: {round(j,2)} secs")


def inspect(image, lot_no, db):
    """
    Parameters
    ----------
    image : numpy array
        Image to mask out background
    lot_no : str
        Lot number associated
    chip_type : str
        chip_type associated with lot number
    db : Session
        Database session

    Returns
    -------
    NG
        Dict of key: batch to value: predicted NG's file name
    save_dir
        Directory of where the images are saved
    img_shape
        Image height and width
    no_of_batches
        Number of batches found
    no_of_chips
        Number of chips found
    """
    time_dict = {}
    time_dict["Start"] = time.time()
    no_of_chips, no_of_batches, item_dict, save_dir, pred_dir = check_dir(image, lot_no, db)
    time_dict["Directory Checking"] = time.time() - time_dict["Start"]
    border_img, img_shape = create_border_img(image, save_dir)
    if any(item_dict.values()): return item_dict, save_dir, img_shape, no_of_batches, no_of_chips                # If exists, return to quicken retrieval

    batch_data = mask(border_img, img_shape)
    no_of_chips, pred_dict = chips(border_img, batch_data)
    time_dict["Chip Masking and Processing"] = time.time() - sum(time_dict.values())
    no_of_batches = len(batch_data)
    item_dict = {}
    for i in range(no_of_batches): item_dict[f"Batch {i+1}"] = []

    for key,value in pred_dict.items():

        ng_img=cv2.cvtColor(value,cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(pred_dir,key),ng_img)                                              # Writing NG images into directory

        if int(key.split("_")[1]) != 0 : item_dict["Batch " + key.split("_")[1]].append(key)
        elif "Stray" in item_dict.keys(): item_dict["Stray"].append(key)
        else: item_dict["Stray"] = []
    time_dict["Write and return individual chips"] = time.time() - sum(time_dict.values())

    time_print(time_dict)

    return item_dict, save_dir, img_shape, no_of_batches, no_of_chips