
import time
import requests
from fastapi import Form, Depends, File
from fastapi import APIRouter, UploadFile, HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from db.session import get_db
from db.repository.csam_ratio import create_base_data, get_db_data
from schemas.ratio import CreateBaseData
from schemas.ng import ShowNG

from apis.inspect.base import inspect


router = APIRouter()


@router.post("/upload_file", response_model=ShowNG)
def predict_NG_chips(file: UploadFile = File(...), lot_no: str = Form(...), db: Session = Depends(get_db)):

    print("Received file to process, please wait...")
    start = time.time()
    if lot_no.lower()[:4] == "test": chip_type = settings.CHIPTYPE
    else:
        prass = requests.get(settings.PRASS_URL+lot_no).json()
        if prass['noc0027'] == None: 
            raise HTTPException(status_code=404, detail=f"Lot number: {lot_no} not found in database")
        chip_type = prass['cdc0163']
    try:
        item_dict, save_dir, img_shape, no_of_batches, no_of_chips = inspect(file, lot_no, db)
    except:
        raise HTTPException(status_code=400, detail=f"Error while processing uploaded file")

    res = ShowNG(plate_no=file.filename.split(".")[0],
                chips=item_dict,
                img_shape=img_shape,
                no_of_chips=no_of_chips,
                no_of_batches=no_of_batches,
                directory=save_dir,
                chip_type=chip_type)
    
    print(f"Total Time taken: {time.time()-start}")

    return res


@router.post("/save_images")
def save_img(ratio: CreateBaseData, db: Session = Depends(get_db)):
    
    res = create_base_data(ratio=ratio, db=db)
    if res: alert = {'title': 'Images Failed to Save!', 
                     'text': 'Please Try Again', 
                     'icon': 'error', 
                     'confirmButtonText': 'Confirm'}
    alert = {'title': 'Images Saved!', 
             'text': 'Confirm to continue', 
             'icon': 'success', 
             'confirmButtonText': 'Confirm'}

    return alert


@router.get("/read_db")
def read_db(db: Session = Depends(get_db)):
    ratio = get_db_data(db=db)
    return ratio