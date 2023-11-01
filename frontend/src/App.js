import React, { useEffect, useState } from "react";
import "./App.css";
import {
  initialArray,
  initialData,
  initialFocus,
  initialInfo,
  initialState,
} from "./ini";

import { AppContext } from "./contexts/context";
import { InfoBar, ImageHolder, Gallery } from "./containers";
import saveData from "./utils/saveData";
import changeColour from "./utils/changeColour";

function App() {
  // Deep copy / clone initial states to prevent overlapping
  const [array, setArray] = useState(structuredClone(initialArray));
  const [data, setData] = useState(structuredClone(initialData));
  const [focus, setFocus] = useState(structuredClone(initialFocus));
  const [info, setInfo] = useState(structuredClone(initialInfo));
  const [state, setState] = useState(structuredClone(initialState));

  useEffect(() => {
    const load = () => {
      save();
    };
    window.addEventListener("beforeunload", load);
    return () => {
      window.removeEventListener("beforeunload", load);
    };
  }, [array]);

  const save = () => {
    if (
      !state.error &&
      data.lot_no &&
      (Object.values(array.ng).length > 0 ||
        Object.values(array.others).length > 0)
    )
      saveData(array, data, info);
  };

  // const insert_db = () => {
  //   if (!state.error && data.lot_no) insertDB(array, data, info);
  // };

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
          <InfoBar save={save} />
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
