import { API } from "../ini";

const insertDB = async (array, data, info) => {
  const send_data = {
    lot_no: data.lot_no,
    plate_no: data.plate_no,
    ng_list: Object.values(array.ng),
    others_list: Object.values(array.others),
    no_of_batches: info.no_of_batches,
    no_of_chips: info.no_of_chips,
    no_of_pred: info.no_of_pred,
    no_of_ng: info.no_of_ng,
    no_of_others: info.no_of_others,
    directory: data.directory,
    chip_type: data.chip_type,
  };

  await fetch(`${API}/insert_db`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(send_data),
  });
};

export default insertDB;
