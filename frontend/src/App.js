import React, { props, useState, useEffect } from "react";
import Map from "./Map";
import LakesList from "./LakesList";
import logo from "./xander.png"
import "./App.css";


function App() {
  const [lakeName, setLakeName] = useState(null);
  const [lakePK, setLakePK] = useState(null);
  const [delayed, setDelayed] = useState(true);

  useEffect(() => {
    const timeout = setTimeout(() => setDelayed(false), 4000);
    return () => clearTimeout(timeout);
  }, []);

  return (delayed ? <div class="container">
                      <div class="buffer"></div>
                      <img src={logo} class="center"/>
                      <h1 class='title'>Xander's Lakes</h1>
                      <div class="buffer"></div>
                    </div> : 
    <div className="row">
      <div className="col-3 scrollable p-0" >
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
