import os
import requests
from fastapi import Depends
from shutil import move, copyfile
from sqlalchemy.orm import Session
from datetime import datetime as dt

from core.config import settings
from schemas.ratio import CreateBaseData
from db.session import get_db
from db.models.csam_ratio import CSAM_RATIO


def selected(directory,chip_dict):

    for i,key in enumerate(chip_dict.keys()):
        temp_dir = os.path.join(directory,"temp")
        move_to_dir = os.path.join(directory,key)
        if not os.path.isdir(move_to_dir): os.makedirs(move_to_dir)

        to_move_back = list(set(chip_dict[key]).symmetric_difference(set(os.listdir(move_to_dir))))
        move_files(to_move_back,move_to_dir,temp_dir,str(i+1),"0")
        move_files(chip_dict[key],temp_dir,move_to_dir,"0",str(i+1))


def move_files(files,src,dest,code_from,code_to):

    for fname in files:
        if fname.split(".")[-1] == "png" and fname[0] == code_from:
            if os.path.isfile(os.path.join(src,fname)):
                move(os.path.join(src,fname),os.path.join(dest,code_to+fname[1:]),copy_function=copyfile)


def get_ratio(lot_no: str, plate_no: str, db: Session):

    ratio = db.query(CSAM_RATIO).filter(CSAM_RATIO.lot_no == lot_no, CSAM_RATIO.plate_no == plate_no).first()
    
    return ratio


def create_csv(ratio, directory):

    data = ",,,"
    for k in range(len(ratio)): data += f"{ratio[k]},"
    file_name = f"{settings.TABLEID}_{dt.now().strftime('%d%m%y')}_{dt.now().strftime('%H%M%S')}.csv"
    file_path = os.path.join(directory,file_name)
    with open(file_path, 'w') as f: f.write(data[:-1])

    return file_path


def create_base_data(ratio: CreateBaseData, db: Session = Depends(get_db)):
    
    ratio_dict = ratio.model_dump()

    directory = ratio_dict.pop('directory')
    ng_list = ratio_dict.pop('ng_list')
    others_list = ratio_dict.pop('others_list')
    chip_dict = {"real":ng_list, "others": others_list}
    selected(directory=directory, chip_dict=chip_dict)

    no_of_chips = ratio_dict['no_of_chips']
    no_of_ng = ratio_dict['no_of_ng']
    no_of_others = ratio_dict['no_of_others']
    ng_ratio = round(no_of_ng/no_of_chips*100,2)
    other_ratio = round(no_of_others/no_of_chips*100,2)

    print(f"Previous Lot Number: {ratio_dict['lot_no']} \
            Real NG: {no_of_ng} NG Ratio: {ng_ratio}% \
            Others: {no_of_others} Other Ratio: {other_ratio}%")

    ratio = CSAM_RATIO(
        **ratio_dict, ng_ratio=str(ng_ratio), other_ratio=str(other_ratio)
    )
    
    db.add(ratio)
    db.commit()
    db.refresh(ratio)

    # To Send via HTTP (To REALTIMEDB)
    # file_path = create_csv(ratio, directory)
    # files = {'file': open(file_path, 'rb')}
    # resp = requests.post(settings.REALTIMEDB, files=files)
    # print(f"fileSize: {int(resp.content)}")
    # if int(resp.content) == os.stat(file_path).st_size: os.remove(file_path)

    return ratio


def get_db_data(db: Session):

    ratio = db.query(CSAM_RATIO).first()
    print(ratio)

    return ratio