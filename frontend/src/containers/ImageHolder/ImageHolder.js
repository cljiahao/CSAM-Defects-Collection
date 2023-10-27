import React, { useContext } from "react";
import { AppContext } from "../../contexts/context";
import PanAndZoom from "./components/PanAndZoom";
import "./ImageHolder.css";

const ImageHolder = ({ highlight }) => {
  const { state } = useContext(AppContext);
  return (
    <div className="imageholder">
      {state.image.src ? (
        <PanAndZoom highlight={highlight} />
      ) : (
        <div className="placeholder" />
      )}
    </div>
  );
};

export default ImageHolder;
