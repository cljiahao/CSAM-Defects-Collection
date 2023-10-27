import React, { useEffect, useState } from "react";
import "./App.css";
import {
  API,
  initialArray,
  initialData,
  initialFocus,
  initialInfo,
  initialState,
} from "./ini";

import { AppContext } from "./contexts/context";
import { InfoBar, ImageHolder, Gallery } from "./containers";
import saveData from "./utils/saveData";
import dataProcess from "./utils/dataProcess";
import loadImage from "./utils/loadImage";
import changeColour from "./utils/changeColour";

function App() {
  const [array, setArray] = useState(initialArray);
  const [data, setData] = useState(initialData);
  const [focus, setFocus] = useState(initialFocus);
  const [info, setInfo] = useState(initialInfo);
  const [state, setState] = useState(initialState);

  useEffect(() => {
    const load = () => {
      save();
    };
    window.addEventListener("beforeunload", load);
    return () => {
      window.removeEventListener("beforeunload", load);
    };
  }, [array]);

  const initialize = () => {
    setArray(initialArray);
    setData(initialData);
    setFocus(initialFocus);
    setInfo(initialInfo);
    setState(initialState);
  };

  const save = () => {
    if (!state.error && data.lot_no && Object.values(array).length > 0)
      saveData(array, data, info);
  };

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

  const highlight = (zone, key) => {
    const [array_dict, info_dict] = changeColour(zone, key, array, info);
    setArray({
      ...array,
      chips: array_dict.chips,
      ng: array_dict.ng,
      others: array_dict.others,
    });
    setInfo({
      ...info,
      no_of_ng: info_dict.no_of_ng,
      no_of_others: info_dict.no_of_others,
    });
  };

  return (
    <AppContext.Provider
      value={{
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
      }}
    >
      <div className="App">
        <main className="App-main">
          <InfoBar process={process} save={save} />
          <ImageHolder highlight={highlight} />
        </main>
        <aside className="App-side">
          <Gallery highlight={highlight} />
        </aside>
      </div>
    </AppContext.Provider>
  );
}

export default App;
