import React, { useRef, useEffect } from "react";
import L from "leaflet";
import "./Map.css";

function Map(props) {
  const mapInstance = useRef();
  const lakeLayers = useRef();

  useEffect(function loadMap() {
    const addGeoJsonLayer = async endpoint => {
      try {
        const response = await fetch(endpoint);
        if (response.ok) {
          const jsonResponse = await response.json();
          L.geoJSON(jsonResponse, {
            style: lakePerimeterStyle,
            onEachFeature: onEachFeature
          }).addTo(mapInstance.current);
        }
      } catch (error) {
        console.log(error);
      }
    };
    const addDepthContours = async endpoint => {
      try {
        const response = await fetch(endpoint);
        if (response.ok) {
          const jsonResponse = await response.json();
          L.geoJSON(jsonResponse, { style: lakeContourStyle }).addTo(
            mapInstance.current
          );
        }
      } catch (error) {
        console.log(error);
      }
    };

    function lakePerimeterStyle(feature) {
      return { weight: "1" };
    }

    function lakeContourStyle(feature) {
      const shade = (115 - feature.properties.calc_dep_m) / 115;
      const color = `rgb(${51 * shade}, ${136 * shade}, ${255 * shade})`;
      return { weight: "0.8", color: color };
    }

    function onEachFeature(feature, layer) {
      lakeLayers.current[feature.properties.pk] = layer;

      //bind click
      layer.on("click", function(e) {
        const pk = e["target"]["feature"]["properties"]["pk"];
        addDepthContours(`/contours/${pk}/geojson`);
        const { _northEast, _southWest } = e["target"]["_bounds"];
        const lakeName = e["target"]["feature"]["properties"]["name"];
        mapInstance.current.fitBounds([
          [_northEast.lat, _northEast.lng],
          [_southWest.lat, _southWest.lng]
        ]);
        props.handleLakeClick(lakeName);
      });
    }

    mapInstance.current = L.map("map").fitBounds([[60, -120], [49, -110]]);
    L.tileLayer(
      "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
      {
        attribution:
          'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: "mapbox/satellite-streets-v11",
        accessToken:
          "pk.eyJ1IjoiZG9ub2hvZWEiLCJhIjoiY2s1bjJuM3IwMHFiejNrcGZkMDdkMjI3cCJ9.tZiSlH78_0M5q-SYuvC4EA"
      }
    ).addTo(mapInstance.current);
    lakeLayers.current = [];
    addGeoJsonLayer("/lakes/geojson");
  }, []);

  useEffect(
    function zoomToLake() {
      if (!props.pk) {
        mapInstance.current.fitBounds([[60, -120], [49, -110]]);
        props.handleLakeClick(null);
      } else {
        lakeLayers.current[props.pk].fire("click");
      }
    },
    [props.pk]
  );

  return <div id="map"></div>;
}

export default Map;
