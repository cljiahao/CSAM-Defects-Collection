import os
import cv2
import time

from apis.inspect.components.batch_process import mask
from apis.inspect.components.chip_process import chips
from apis.inspect.components.initialize import check_dir, create_border_img


def time_print(time_dict) -> None:
    """
    Parameters
    ----------
    time_dict : dict
        Time recording stored in dictionary
    """
    del time_dict["Start"]
    for i, j in time_dict.items():
        print(f"{i} took: {round(j,2)} secs")


def inspect(image, lot_no, db):
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
    chips_dict: dict
        Key: batch, value: predicted NG's file name
    save_dir : str
        Directory of where the images are saved
    img_shape : list
        Image height and width
    no_of_batches : int
        Number of batches found
    no_of_chips : int
        Number of chips found
    """
    time_dict = {}
    time_dict["Start"] = time.time()
    no_of_chips, no_of_batches, chips_dict, save_dir, pred_dir = check_dir(
        image, lot_no, db
    )
    time_dict["Directory Checking"] = time.time() - time_dict["Start"]
    border_img, img_shape = create_border_img(image, save_dir)
    if any(chips_dict.values()):
        # If exists, return to quicken retrieval (caching)
        return (
            chips_dict,
            save_dir,
            img_shape,
            no_of_batches,
            no_of_chips,
        )

    batch_data = mask(border_img, img_shape)
    no_of_chips, hold_dict = chips(border_img, batch_data)
    time_dict["Chip Masking and Processing"] = time.time() - sum(time_dict.values())

    no_of_batches = len(batch_data)
    chips_dict = {}
    for i in range(no_of_batches):
        chips_dict[f"Batch {i+1}"] = []

    for key, value in hold_dict.items():
        # Writing NG images into directory
        cv2.imwrite(os.path.join(pred_dir, key), value)

        if int(key.split("_")[1]) != 0:
            chips_dict["Batch " + key.split("_")[1]].append(key)
        elif "Stray" in chips_dict.keys():
            chips_dict["Stray"].append(key)
        else:
            chips_dict["Stray"] = []

    time_dict["Write and return individual chips"] = time.time() - sum(
        time_dict.values()
    )

    time_print(time_dict)

    return chips_dict, save_dir, img_shape, no_of_batches, no_of_chips
