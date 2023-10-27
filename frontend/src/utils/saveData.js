import Swal from "sweetalert2";

const API = process.env.REACT_APP_API;

const saveData = async (array, data, info) => {
  const send_data = {
    lot_no: data.lot_no,
    plate_no: data.plate_no,
    ng_list: Object.values(array.ng),
    others_list: Object.values(array.others),
    no_of_batches: info.no_of_batches,
    no_of_chips: info.no_of_chips,
    no_of_ng: info.no_of_ng,
    no_of_others: info.no_of_others,
    directory: data.directory,
    chip_type: data.chip_type,
  };

  const resp = await fetch(`${API}/save_images`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(send_data),
  });

  const alert = await resp.json();

  Swal.fire({
    title: alert.title,
    text: alert.text,
    icon: alert.icon,
    confirmButtonText: alert.confirmButtonText,
  });
};

export default saveData;
