// ============================================================
// STUDY AREA — Chapada dos Veadeiros + 25 km buffer
// VERIFIED definition. Resulting area: 11,934.66 km2
//
// Logic:
//   1. Load protected-area polygons (WDPA).
//   2. Filter by the name 'Cerrado Protected' (returns Chapada + Emas).
//   3. Clip to Goias with an auxiliary rectangle (excludes PARNA das Emas,
//      which was contaminating the selection).
//   4. Apply a 25 km buffer (in meters).
//
// Do NOT confuse 'region_goias' (auxiliary clipping rectangle) with the
// study area. The study area is the RESULT (polygon + buffer).
// ============================================================

var wdpa = ee.FeatureCollection('WCMC/WDPA/current/polygons');

// Auxiliary rectangle, only to clip to Goias and exclude Emas [W, S, E, N]
var region_goias = ee.Geometry.Rectangle([-48.5, -14.8, -46.8, -13.0]);

var chapada = wdpa
  .filter(ee.Filter.stringContains('NAME', 'Cerrado Protected'))
  .filterBounds(region_goias);

var aoi = chapada.geometry()
  .intersection(region_goias, 100)   // clip to Goias (maxError = 100 m)
  .buffer(25000);                    // 25 km buffer, in meters

// -------- Reproducibility control --------
// When run, the printed area must be ~11,934.66 km2.
//   ~2,400   -> forgot the buffer
//   ~150,000 -> grabbed a rectangular bbox by mistake
var area_km2 = aoi.area(100).divide(1e6);
print('AOI area (km2):', area_km2);   // expected: 11934.66

Map.centerObject(aoi, 9);
Map.addLayer(aoi, {color: 'red'}, 'AOI (Chapada + 25 km buffer)');
