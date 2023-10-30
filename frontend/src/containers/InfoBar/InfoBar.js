import React, { useContext } from "react";
import { AppContext } from "../../contexts/context";
import "./InfoBar.css";
import { API } from "../../ini";

import dataProcess from "../../utils/dataProcess";
import loadImage from "../../utils/loadImage";

import Info from "./components/Info";
import Input from "./components/Input";
import Button from "./components/Button";

const InfoBar = ({ initialize, save }) => {
  const {
    array,
    data,
    focus,
    info,
    state,
    setArray,
    setData,
    setFocus,
    setInfo,
    setState,
  } = useContext(AppContext);

  const errorHandling = async (res) => {
    if (res.status === "404") {
      setState({
        error: true,
        image: {
          src: "Error/Error_Lot_Num.png",
          alt: "Error_Lot_Num.png",
        },
      });
      return false;
    } else if (res.status === "400") {
      setState({
        error: true,
        image: { src: "Error/Error.png", alt: "Error.png" },
      });
      return false;
    } else {
      const json = await res.json();
      return json;
    }
  };

  const process = async (e) => {
    e.preventDefault();
    initialize();

    if (data.lot_no === "" || data.lot_no === null || state.error) {
      data.lot_no = prompt("Please Scan or Input Lot Number.");
    }
    const file = e.target.files[0];
    if (file) {
      setState({
        ...state,
        image: { src: "Error/Loading.gif", alt: "Loading.gif" },
      });
      const res = await loadImage(file, data);
      if (res) {
        const json = await errorHandling(res);
        if (json) {
          const [array_dict, data_dict, focus_dict, info_dict] = dataProcess(
            json,
            array,
            data,
            focus,
            info
          );
          setArray(array_dict);
          setData(data_dict);
          setFocus(focus_dict);
          setInfo(info_dict);
          setState({
            error: false,
            image: {
              src: `${API}${data_dict.directory.split("backend")[1]}/Original/${
                file.name
              }`,
              alt: file.name,
            },
          });
        }
      }
    }
  };

  return (
    <div className="infobar">
      <Info data={data} info={info} />
      <div className="button_cont">
        <Input text="Upload Image" onChange={process} />
        <Button text="Submit" onClick={save} />
      </div>
    </div>
  );
};

export default InfoBar;
