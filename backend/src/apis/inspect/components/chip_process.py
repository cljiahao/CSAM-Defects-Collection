import cv2
import numpy as np

from core.config import settings
from apis.inspect.components.batch_process import find_batch_no


def chips(border_img, batch_data) -> dict:
    """
    Main function to call sub functions for retrieiving chip data

    Parameters
    ----------
    border_img : MatLike
        Directory to check if files exists
    batch_data : list
        An array of each batches coordinate found in the form of
        [{index: int, x1: double, y1: double, x2: double, y2: double}...]

    Returns
    -------
    no_of_chips : int
        Number of chips
    hold_dict : dict
        Images stored in dictionary to be send back to frontend
    """
    no_of_chips = 0
    hold_dict = {}

    mask = mask_chips(border_img.copy())
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Average contour area of the chips
    cArea = np.median(
        [cv2.contourArea(x) for x in contours if cv2.contourArea(x) > 100]
    )
    lower_chip_area = cArea * 0.15
    upper_chip_area = cArea * 3

    for cnt in contours:
        ((xc, yc), (w, h), theta) = cv2.minAreaRect(cnt)
        chip_area = cv2.contourArea(cnt)

        if lower_chip_area < chip_area < upper_chip_area:
            no_of_chips += 1
            batch = find_batch_no(xc, yc, batch_data)
            # 0 first element of name is to indicate image not selected yet
            # xc, yc - 20 to remove the the added borders previously
            fName = "{}_{}_{}_{}_{}.png".format(
                0, batch, no_of_chips, int(xc - 20), int(yc - 20)
            )
            src_pts = cv2.boxPoints(((xc, yc), settings.IMAGESIZE, theta))
            rotated_img = rotate_chips(border_img, h, w, src_pts)

            hold_dict[fName] = rotated_img

    return no_of_chips, hold_dict


def mask_chips(img):
    """
    Parameters
    ----------
    img : numpy array
        Image to mask out background

    Returns
    -------
    mask : MatLike
        A masked image of individual chips
    """
    # Mask for background and convert all to 255 for easier threshold (remove background)
    background = np.where(
        (img[:, :, 0] >= 130) & (img[:, :, 1] >= 130) & (img[:, :, 2] >= 130)
    )
    img[background] = (255, 255, 255)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, ret = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    morph = cv2.morphologyEx(ret, cv2.MORPH_CLOSE, (3, 3))
    mask = cv2.erode(morph, np.ones((7, 7), np.uint8))

    return mask


def rotate_chips(img, height, width, src_pts):
    """
    Parameters
    ----------
    img : numpy array
        Image to mask out background
    height : int
        Height of reference point
    width : int
        Width of reference point
    src_pts : MatLike
        Reference point to rotate from

    Returns
    -------
    rot_img
        Rotated image based on reference point (src_pts and dst_pts)
    """
    vert, hori = settings.IMAGESIZE

    # If-Else condition required as AI does not differentiate height from width.Height & width are interchangeable
    dst_pts = (
        np.array([[vert, 0], [0, 0], [0, hori], [vert, hori]], dtype="float32")
        if width > height
        else np.array([[0, hori], [0, 0], [vert, 0], [vert, hori]], dtype="float32")
    )

    # Fix skewed perspectives (3D->2D)
    A = cv2.getPerspectiveTransform(src_pts, dst_pts)
    rot_img = cv2.warpPerspective(img, A, (vert, hori), flags=cv2.INTER_AREA)

    return rot_img
