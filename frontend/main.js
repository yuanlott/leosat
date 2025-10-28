import * as Cesium from "cesium";
import "cesium/Build/Cesium/Widgets/widgets.css";

const viewer = new Cesium.Viewer("cesiumContainer", {
  terrainProvider: Cesium.createWorldTerrain(),
});

async function loadSimulation() {
  const response = await fetch("http://127.0.0.1:8000/simulate");
  const { simulation } = await response.json();

  // Render satellites
  simulation[0].positions.forEach((sat) => {
    viewer.entities.add({
      position: Cesium.Cartesian3.fromDegrees(sat.lon, sat.lat, sat.alt * 1000),
      point: { pixelSize: 5, color: Cesium.Color.CYAN },
      label: { text: sat.name, font: "10pt sans-serif", pixelOffset: new Cesium.Cartesian2(10, 0) },
    });
  });

  // Draw one routing path
  const path = simulation[0].path.map((p) =>
    Cesium.Cartesian3.fromDegrees(p.lon, p.lat, p.alt * 1000)
  );
  viewer.entities.add({
    polyline: { positions: path, width: 2, material: Cesium.Color.RED },
  });
}

loadSimulation();
