import React, { useContext } from "react";
import { AppContext } from "../../contexts/context";
import "./InfoBar.css";

import Info from "./components/Info";
import Input from "./components/Input";
import Button from "./components/Button";

const InfoBar = ({ process, save }) => {
  const { data, info } = useContext(AppContext);
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
