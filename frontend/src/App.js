import React, { useState } from "react";
import Map from "./Map";
import LakesList from "./LakesList";
import "./App.css";

function App() {
  const [lakeName, setLakeName] = useState(null);
  const [lakePK, setLakePK] = useState(null);
  return (
    <div className="row">
      <div className="col-3 scrollable p-0">
        <LakesList onClick={i => setLakePK(i)} />
      </div>
      <div className="col-9">
        <div className="row">
          <button className="btn btn-dark btn-block">
            {lakeName ? lakeName : "Xander's Lakes"}
          </button>
        </div>
        <div className="row">
          <Map pk={lakePK} handleLakeClick={lake => setLakeName(lake)}></Map>
        </div>
      </div>
    </div>
  );
}

export default App;
