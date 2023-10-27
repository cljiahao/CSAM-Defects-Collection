const dataProcess = (json, array, data, focus, info) => {
  const chips = json.chips;

  let no_of_ng = 0;
  let no_of_others = 0;

  Object.keys(chips).map((key, index) => {
    return (chips[key] = Object.assign(
      {},
      ...json.chips[key].map((filename) => {
        const img_name = filename.split(".")[0];
        const [class_type, , id, x, y] = img_name.split("_");
        const fname = filename;

        let color = null;
        let marker_radius = 3;
        let border = null;

        if (class_type === "1") {
          color = "yellow";
          marker_radius = 1;
          border = "2px solid red";
          no_of_ng += 1;
          array.ng[id] = fname;
        } else if (class_type === "2") {
          color = "aqua";
          marker_radius = 1;
          border = "2px solid red";
          no_of_others += 1;
          array.others[id] = fname;
        }
        return {
          [id]: { class_type, x, y, color, fname, marker_radius, border },
        };
      })
    ));
  });
  array.chips = chips;

  data.plate_no = json.plate_no;
  data.directory = json.directory;
  data.chip_type = json.chip_type;

  const img_shape = json.img_shape;
  focus.img_shape = { width: img_shape[0], height: img_shape[1] };

  info.no_of_batches = json.no_of_batches;
  info.no_of_chips = json.no_of_chips;
  info.no_of_ng = no_of_ng;
  info.no_of_others = no_of_others;
  //   const ng_count = json.ng_count;

  if (
    data.plate_no.slice(0, 3)[0].toLowerCase() === "end" ||
    data.lot_no === null
  )
    data.lot_no = "";

  return [array, data, focus, info];
};

export default dataProcess;
