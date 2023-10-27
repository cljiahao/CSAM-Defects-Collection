import React, { useContext } from "react";
import { AppContext } from "../../contexts/context";
import "./Gallery.css";

import BatchZones from "./components/BatchZones";

const Gallery = ({ highlight }) => {
  const { array } = useContext(AppContext);

  return (
    <div className="gallery">
      {array.chips && (
        <BatchZones highlight={highlight} batches={array.chips} />
      )}
    </div>
  );
};

export default Gallery;
