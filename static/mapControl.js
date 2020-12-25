    // get points data from data-attribute
    var container = document.querySelector("#map");
    var data = container.getAttribute("data-points");
    var points = JSON.parse(data);
    console.log('Points', points);
    var attribution = new ol.control.Attribution({
        collapsible: false
    });
    var markerCenter = new ol.Feature({
      geometry: new ol.geom.Point(
        ol.proj.fromLonLat([-73.65269, 45.48858])
      ),
      type: 'icon'
    });
    var iconStyles = new ol.style.Style({
        image: new ol.style.Icon({
          anchor: [0.5, 1],
          src: 'static/blue.png',
        })
    });
    var markerLasalle = new ol.Feature({
      geometry: new ol.geom.Point(
        ol.proj.fromLonLat([-73.63, 45.43])
      ),
      type: 'icon'
    });
    var vectorSource = new ol.source.Vector();
    /* example of the pattern:*/
    // var coordinate = [lon, lat];
    var markers = [];
    var setMarker = function(lon, lat) {
        return new ol.Feature({
            geometry: new ol.geom.Point(
                ol.proj.fromLonLat([lon, lat])
            ),
            type: 'v-icon'
        });
        // vectorSource.addFeature(marker);
    }
    points.forEach(function(point){
        point = Array.from(point);
        console.log('Mark Points', point, Number(point[2]))
        markers.push(setMarker(Number(point[2]),Number(point[3])))
    })
    console.log('Markers', markers)
    console.log('Compare default markers addFeatures', [markerCenter, markerLasalle])
    // vectorSource.addFeature(markers)
    vectorSource.addFeatures([markerCenter, markerLasalle])
    var vectorLayer = new ol.layer.Vector({
        source: vectorSource,
        style: iconStyles,
        updateWhileAnimating: true,
        updateWhileInteracting: true
    })
    var map = new ol.Map({
         target: 'map',
         view: new ol.View({
             center: ol.proj.fromLonLat([-73.7, 45.5]),
             zoom: 11
         }),
         controls: ol.control.defaults({attribution: false}).extend([attribution]),
         layers: [
             new ol.layer.Tile({
                 preload: 3,
                 source: new ol.source.OSM()
             }),
             vectorLayer,
         ],
         loadTilesWhileAnimating: true,
    });
