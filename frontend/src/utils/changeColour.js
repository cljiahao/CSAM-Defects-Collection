import { marker } from "../ini";

const changeColour = (zone, key, array, info) => {
  let target = array.chips[zone][key];
  if (target.color === "chartreuse" || target.color == null) {
    target.color = marker.color.highlight;
    target.marker_radius = marker.radius.highlight;
    target.border = marker.border.highlight;
    array.ng[key] = target.fname;
    info.no_of_ng += 1;
  } else if (target.color === "yellow") {
    target.color = marker.color.others;
    delete array.ng[key];
    array.others[key] = target.fname;
    info.no_of_ng -= 1;
    info.no_of_others += 1;
  } else if (target.color === "aqua") {
    target.color = marker.color.default;
    target.marker_radius = marker.radius.default;
    target.border = marker.border.default;
    delete array.others[key];
    info.no_of_others -= 1;
  }
  return [array, info];
};

export default changeColour;
