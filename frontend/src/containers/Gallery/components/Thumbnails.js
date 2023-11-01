import React, { useContext } from "react";
import { AppContext } from "../../../contexts/context";
import { API, FOCUS_SCALE, marker } from "../../../ini";

const Thumbnails = ({ highlight, zone }) => {
  const { array, data, focus, setArray, setFocus } = useContext(AppContext);
  const selected = Object.assign({}, array.ng, array.others);
  const chips = array.chips[zone];

  const focusOnChip = (e, key, zone) => {
    const coords = e.target.alt.split(".")[0];
    const [x, y] = coords.split("_").slice(-2);
    setFocus({ ...focus, state: true, x: x, y: y, scale: FOCUS_SCALE });
    let target = array.chips[zone][key];
    if (target.color == null) {
      target.color = marker.color.zoom;
      target.marker_radius = marker.radius.zoom;
      setArray({ ...array, array: { ...array.chips, [key]: target } });
    }
  };

  const unfocusOnChip = (key, zone) => {
    setFocus({ ...focus, state: false, x: 0, y: 0, scale: 1 });
    let target = array.chips[zone][key];
    if (target.color === "chartreuse") {
      target.color = marker.color.default;
      target.marker_radius = marker.radius.default;
      setArray({ ...array, array: { ...array.chips, [key]: target } });
    }
  };
  // TODO: Caching of images
  // TODO: Lazing Loading or Pagination to improve speed
  return (
    <div className="thumbnail-cont" key={zone}>
      {Object.keys(chips).map((key, i) => {
        return (
          <>
            {key in selected && (
              <img
                key={key}
                className="thumbnail"
                src={`${API}${data.directory.split("backend")[1]}/${
                  chips[key].class_type === "1"
                    ? "real"
                    : chips[key].class_type === "2"
                    ? "others"
                    : "temp"
                }/${chips[key].fname}`}
                alt={chips[key].fname}
                style={{ border: chips[key].border }}
                onClick={() => highlight(zone, key)}
                onMouseEnter={(e) => focusOnChip(e, key, zone)}
                onMouseLeave={() => unfocusOnChip(key, zone)}
              />
            )}
          </>
        );
      })}
    </div>
  );
};

export default Thumbnails;
