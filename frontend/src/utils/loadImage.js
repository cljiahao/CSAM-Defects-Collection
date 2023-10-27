import { API } from "../ini";

const uploadImage = async (file, data) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("lot_no", data.lot_no);

  const res = await fetch(`${API}/upload_file`, {
    method: "POST",
    headers: {
      Accept: "application/json",
    },
    body: formData,
  });
  return res;
};

export default uploadImage;
