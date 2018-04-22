mapboxgl.accessToken = 'pk.eyJ1IjoiY2Fwcmlwb3QiLCJhIjoiY2pjMDJqcDhsMDQ2MzJ4bW85MTR0YXBzYiJ9.Ag9mIZTDONNN9JdN2kW76g';
var map = new mapboxgl.Map({
  container: 'map',
  maxZoom: 5.5,
  minZoom: 1.8,
  style: 'mapbox://styles/mapbox/light-v9',
  center: [-115.36957574368233, 40],
  zoom: 2
});

var firstSymbolId;

map.on('load', function () {

  var layers = map.getStyle().layers;

  // Find the index of the first symbol layer in the map style
  for (var i = 0; i < layers.length; i++) {
      if (layers[i].type === 'symbol') {
          firstSymbolId = layers[i].id;
          break;
      }
  }

  map.addSource('us-data', { type: 'geojson', data: statesData });

  doAddStatesLayer();

});

map.on('click', 'us-states', function(e) {
  var coordinates = almostFlatten(e.features[0].geometry.coordinates);
  var bounds = new mapboxgl.LngLatBounds(coordinates[0], coordinates[0]);
  coordinates.forEach(function(coord) {
    bounds.extend(coord);
  });

  map.fitBounds(bounds, { padding: 100 });
});


function doAddStatesLayer() {
  /* Add the us-states layer to the map. */

  map.addLayer({
    'id': 'us-states',
    'type': 'fill',
    'source': 'us-data',
    'paint': {
      'fill-color': {
        property: 'density',
        stops: [
            [0, '#EEE'],
            [10, '#56D7FF'],
            [20, '#3DBEFF'],
            [50, '#23A4FF'],
            [100, '#0A8BE6'],
            [200, '#0071CC'],
            [500, '#0058B3'],
            [800, '#003E99']
        ]
      },
      'fill-opacity': 0.75
    }
  }, firstSymbolId);

} // end doAddStatesLayer


function almostFlatten(arr) {
  return arr.reduce(function (flat, toFlatten) {
    return flat.concat(Array.isArray(toFlatten[0]) ? almostFlatten(toFlatten) : [toFlatten]);
  }, []);
}


function updateMap() {
  /* Refreshes data source with updated data. */

  map.getSource('us-data').setData(statesData);

} // end updateMap


function updateDensities(count, events) {
    /* Updates the densities (ie incident count) in statesData. */

    let densities = {};
    let i, state;

    for ( i = 0; i < count; i++ ) {
        state = events[i].state;
        densities[state] = pyGet(densities, state, 0) + 1;
    } // end for

    for ( i = 0; i < statesData.features.length; i++ ) {
        state = statesData.features[i].properties.name;
        statesData.features[i].properties.density = pyGet(densities, state, 0);
    } // end for

} // end updateDensities
