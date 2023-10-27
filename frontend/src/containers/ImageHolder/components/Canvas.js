import React, { useContext } from "react";
import { AppContext } from "../../../contexts/context";

const ChipMarker = ({ moved, display, highlight }) => {
  const { array, focus } = useContext(AppContext);
  return (
    <svg
      className="marker"
      style={{ position: "absolute" }}
      width={display.width}
      height={display.height}
    >
      {Object.keys(array.chips).map((key, index) => {
        return Object.keys(array.chips[key]).map((k, i) => {
          const { class_type, x, y, color, fname, marker_radius, border } =
            array.chips[key][k];
          const cx = (x * display.width) / focus.img_shape.width;
          const cy = (y * display.height) / focus.img_shape.height;
          return (
            <circle
              key={k}
              cx={cx}
              cy={cy}
              r={marker_radius}
              stroke={color}
              strokeWidth="2"
              fillOpacity="0"
              onClick={() => {
                moved && highlight(key, k);
              }}
            />
          );
        });
      })}
    </svg>
  );
};

export default ChipMarker;
