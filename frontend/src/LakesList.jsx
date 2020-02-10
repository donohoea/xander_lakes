import React, { useState, useEffect } from "react";
import "./LakeList.css";

const LakeList = props => {
  const [list, setList] = useState(null);

  useEffect(function loadLakeList() {
    async function fetchLakeListData() {
      try {
        const response = await fetch("/lakes/list");
        if (response.ok) {
          const jsonResponse = await response.json();
          setList(jsonResponse);
        }
      } catch (error) {
        console.log(error);
      }
    }
    fetchLakeListData();
  }, []);
  if (!list) {
    return (
      <div id="accordion">
        <div className="card" key="loading">
          <div className="card-header p-0" id="loading">
            <button className="btn btn-dark btn-block">Loading Lakes...</button>
          </div>
        </div>
      </div>
    );
  }
  return (
    <div id="accordion">
      <div>
        <button
          className="btn btn-dark btn-block m-0"
          onClick={() => props.onClick(null)}
        >
          All Lakes
        </button>
      </div>
      {list.map(card => (
        <div className="card" key={card[1]}>
          <div className="card-header p-0" id={`heading${card[1]}`}>
            <button
              className="btn btn-dark btn-block collapsed m-0"
              data-toggle="collapse"
              data-target={`#collapse${card[1]}`}
              aria-expanded="false"
              aria-controls={`collapse${card[1]}`}
            >
              {card[1]}
            </button>
          </div>
          <div
            id={`collapse${card[1]}`}
            className="collapse"
            aria-labelledby={`heading${card[1]}`}
            data-parent="#accordion"
          >
            <div className="card-body p-0">
              <ul className="no-bullet p-0">
                {card[0].map(lake => (
                  <li key={lake[0]}>
                    <button
                      className="btn btn-light btn-block"
                      onClick={() => props.onClick(lake[0])}
                    >
                      {lake[1]}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default LakeList;
