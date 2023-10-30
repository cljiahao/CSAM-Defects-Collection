import React, { useEffect, useState } from "react";
import "./App.css";
import {
  initialArray,
  initialData,
  initialFocus,
  initialInfo,
  initialState,
} from "./ini";

import saveData from "./utils/saveData";
import { AppContext } from "./contexts/context";
import { InfoBar, ImageHolder, Gallery } from "./containers";

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
          <InfoBar initialize={initialize} save={save} />
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
