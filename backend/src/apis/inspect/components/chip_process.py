import cv2
import time
import numpy as np

from core.config import settings
from apis.inspect.components.batch_process import find_batch_no


def chips(border_img, batch_data) -> dict:
    """ Main function to call sub functions """
    no_of_chips = 0
    pred_dict = {}

    mask = mask_chips(border_img.copy())
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cArea = np.median([cv2.contourArea(x) for x in contours if cv2.contourArea(x) > 100])
    lower_chip_area = cArea * 0.15
    upper_chip_area = cArea * 3
    
    for cnt in contours:
        ((xc,yc), (w, h), theta) = cv2.minAreaRect(cnt)
        chip_area = cv2.contourArea(cnt)

        if lower_chip_area < chip_area < upper_chip_area:
            # print(f"lowest: {lower_chip_area}, low: {lower_def_area}, area: {chip_area}, high: {upper_def_area}, highest: {upper_chip_area}")

            no_of_chips += 1
            batch = find_batch_no(xc, yc, batch_data)
            fName = "{}_{}_{}_{}_{}.png".format(0,
                                                batch,
                                                no_of_chips,
                                                int(xc-20),
                                                int(yc-20)
                                                )
            src_pts = cv2.boxPoints(((xc,yc), settings.IMAGESIZE, theta))
            rotated_img = rotate_chips(border_img, h, w, src_pts)
            rotated_img = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2RGB)

            pred_dict[fName] = rotated_img
    
    return no_of_chips, pred_dict


def mask_chips(img):

    background = np.where((img[:,:,0]>=130) & (img[:,:,1]>=130) & (img[:,:,2]>=130))
    img[background] = (255,255,255)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    th, ret = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    morph = cv2.morphologyEx(ret,cv2.MORPH_CLOSE,(3,3))
    mask = cv2.erode(morph,np.ones((7,7),np.uint8))

    return mask


def rotate_chips(img, height, width, src_pts):
    vert, hori = settings.IMAGESIZE

    # If-Else condition required as AI does not differentiate height from width.Height & width are interchangeable
    dst_pts = np.array([[vert, 0], [0,0], [0,hori], [vert, hori]], dtype = "float32") if width > height else np.array([[0, hori], [0,0], [vert, 0], [vert, hori]], dtype = "float32")

    # Fix skewed perspectives (3D->2D)
    A = cv2.getPerspectiveTransform(src_pts, dst_pts)
    rot_img = cv2.warpPerspective(img, A, (vert, hori), flags=cv2.INTER_AREA)

    return rot_img

