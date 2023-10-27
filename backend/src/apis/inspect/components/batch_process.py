import cv2
import numpy as np


def mask(border_img, img_shape) -> list:
    """ Main function to call sub functions """
    mask = mask_batch(border_img.copy())
    contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    batch_data = find_batch(contours, img_shape)

    return batch_data


def mask_batch(img):
    """
    Parameters
    ----------
    img : numpy array
        Image to mask out background

    Returns
    -------
    morph
        A masked image of non background
    """
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(27,27))
    th, ret = cv2.threshold(blur,150,255,cv2.THRESH_BINARY_INV)
    morph = cv2.morphologyEx(ret,cv2.MORPH_CLOSE,np.ones((11,35),np.uint8))     # Merge neighbouring chips to form a huge blob mask
    morph = cv2.morphologyEx(morph,cv2.MORPH_ERODE,np.ones((3,3),np.uint8))     # Erode to prevent merging between batches

    return morph


def find_batch(contours, img_shape) -> list:
    """
    Parameters
    ----------
    contours : numpy array
        Contours of non background
    img_shape : array
        Image Height and Width in a list

    Returns
    -------
    batch_data
        An array of each batches coordinate found in the form of 
        [{index: int, x1: double, y1: double, x2: double, y2: double}...]
    """
    img_height, img_width = img_shape
    thres_area = img_height*img_width * 0.01                                    # Use to remove noises (Stray Chips / Dirt)

    batch_data = []

    for cnt in contours:

        ((cx, cy), (wi, he), thet) = cv2.minAreaRect(cnt)
        blob_area = wi*he

        if blob_area > thres_area:
            x, y, w, h = cv2.boundingRect(cnt)
            xc, yc = x + w/2, y + h/2

            factor = -(-img_height//1000)*1000                                  # Factor depends on the size of image (RoundUp)
            index = round(yc/factor, 1) * factor**2 + xc
            data = {
                'index': index,
                'x1': x,
                'y1': y,
                'x2': x+w,
                'y2': y+h
            }
            batch_data.append(data)

    batch_data = sorted(batch_data, key=lambda x: x['index'])

    return batch_data


def find_batch_no(x,y,batch_data):
    """
    Parameters
    ----------
    x : float
        x coordinate of interest point
    y : float
        y coordinate of interest point
    batch_data : list
        An array of each batches coordinate found in the form of 
        [{index: int, x1: double, y1: double, x2: double, y2: double}...]

    Returns
    -------
    batch_no
        The batch number the interest is associated with
    """
    batch_no = 0
    for i,coor in enumerate(batch_data):
        if x<=coor['x2'] and x>=coor['x1'] and y<=coor['y2'] and y>=coor['y1']: batch_no = i+1

    return batch_no