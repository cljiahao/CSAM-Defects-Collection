import os
import cv2
from datetime import datetime
from shutil import copyfileobj, rmtree, copyfile

from db.repository.csam_ratio import get_ratio


def create_border_img(image, save_dir):
    """
    Parameters
    ----------
    image :
        Image file from frontend
    save_dir :
        Directory to save folder and files to

    Returns
    -------
    border_img : MatLike
        Border added image
    [w,h] : list
        Width and height of the image
    """
    # shutil.copyfileobj() method to copy the contents of source file-like object to destination file-like object
    tempFile = "tmp/temp.png"
    with open(tempFile, "wb") as buffer:
        copyfileobj(image.file, buffer)

    ori_dir = os.path.join(save_dir, "original")
    if not os.path.exists(ori_dir):
        os.makedirs(ori_dir)
        copyfile("tmp/temp.png", os.path.join(ori_dir, image.filename))
    else:
        no_of_files = len(os.listdir(ori_dir))
        new_fname = f"{image.filename.split('.')[0]}_{no_of_files}.png"
        os.rename(
            os.path.join(ori_dir, image.filename), os.path.join(ori_dir, new_fname)
        )
        copyfile("tmp/temp.png", os.path.join(ori_dir, image.filename))

    image = cv2.imread(tempFile)
    h, w, z = image.shape
    # Added border to include chips near the edge of images,
    # allowing better cropping of chips later on
    border_img = cv2.copyMakeBorder(image, 20, 20, 20, 20, cv2.BORDER_REPLICATE)

    return border_img, [w, h]


def check_dir(image, lot_no, db):
    """
    Parameters
    ----------
    image : numpy array
        Image to mask out background
    lot_no : str
        Lot number associated
    db : Session
        Database session

    Returns
    -------
    no_of_chips : int
        Number of chips
    no_of_batches : int
        Number of batches
    chips_dict : dict
        Chip filename saved in dictionary by batches
    save_dir :
        Directory to save folder and files to
    temp_dir :
        Temporary Directory to save temp files to
    """
    plate_no = image.filename.split(".")[0]

    backend_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )
    lot_dir = os.path.join(
        backend_dir, "images", datetime.now().strftime("%b%y"), lot_no
    )
    save_dir = os.path.join(lot_dir, plate_no)
    temp_dir = os.path.join(save_dir, "temp")
    real_dir = os.path.join(save_dir, "real")
    others_dir = os.path.join(save_dir, "others")

    chips_dict = {}
    no_of_batches, no_of_chips = 0, 0
    # Testing directory to be remove every testing
    if lot_no.lower()[:4] == "test" and os.path.isdir(lot_dir):
        rmtree(lot_dir)
    if os.path.isdir(temp_dir) and any(os.scandir(temp_dir)):
        try:
            # Pull data from database for caching
            ratio = get_ratio(lot_no=lot_no, plate_no=plate_no, db=db)
            no_of_batches = ratio.no_of_batches
            no_of_chips = ratio.no_of_chips
            for i in range(no_of_batches):
                chips_dict[f"Batch {i+1}"] = []
            chips_dict = caching(temp_dir, chips_dict)
            if os.path.isdir(real_dir) and any(os.scandir(real_dir)):
                chips_dict = caching(real_dir, chips_dict)
            if os.path.isdir(others_dir) and any(os.scandir(others_dir)):
                chips_dict = caching(others_dir, chips_dict)
        except:
            # If no data is found in database
            if os.path.isdir(save_dir):
                rmtree(save_dir)
            os.makedirs(temp_dir)
    else:
        if os.path.isdir(save_dir):
            rmtree(save_dir)
        os.makedirs(temp_dir)

    return no_of_chips, no_of_batches, chips_dict, save_dir, temp_dir


def caching(directory, chips):
    """
    Parameters
    ----------
    directory : str
        Directory to check if files exists
    chips : dict
        Chip filename saved in dictionary by batches

    Returns
    -------
    chips : dict
        Chip filename saved in dictionary by batches
    """
    for file in os.listdir(directory):
        if file.split(".")[-1] == "png":
            if int(file.split("_")[1]) != 0:
                chips[f"Batch {file.split('_')[1]}"].append(file)
            elif "Stray" in chips.keys():
                chips["Stray"].append(file)
            else:
                chips["Stray"] = []

    return chips
