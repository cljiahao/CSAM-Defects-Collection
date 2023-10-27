import React from "react";

const Info = ({ data, info }) => {
  return (
    <ul className="info_list_cont">
      <li className="info_list">
        <h1 className="info_head">Lot Number:</h1>
        <div className="info_desc">{data.lot_no}</div>
      </li>
      <li className="info_list">
        <h1 className="info_head">Plate Number:</h1>
        <div className="info_desc">{data.plate_no}</div>
      </li>
      {/* <li className="info_list">
                <h1 className="info_head">Predicted chips:</h1>
                <div className="info_desc">{} <span className="info_unit">pcs</span> </div>
            </li> */}
      <li className="info_list">
        <h1 className="info_head">Selected chips:</h1>
        <div className="info_desc">
          {info.no_of_ng + info.no_of_others}
          <span className="info_unit">pcs</span>
        </div>
      </li>
    </ul>
  );
};

export default Info;
