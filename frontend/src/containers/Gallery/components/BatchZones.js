import React from "react";
import Thumbnails from "./Thumbnails";

const BatchZones = ({ highlight, batches }) => {
  return (
    <div className="batchzone-cont">
      {Object.keys(batches).map((zone, index) => (
        <div className="zone-cont" key={index}>
          <div className="zone">{zone}</div>
          {batches[zone] && <Thumbnails highlight={highlight} zone={zone} />}
        </div>
      ))}
    </div>
  );
};

export default BatchZones;
