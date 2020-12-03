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
          src: 'http://maps.google.com/mapfiles/ms/micons/blue.png',
        })
        /*image: new ol.style.Circle({
          radius: 7,
          fill: new ol.style.Fill({color: 'green'}),
          stroke: new ol.style.Stroke({
            color: 'white',
            width: 2,
          })
        })*/
    });
    var markerLasalle = new ol.Feature({
      geometry: new ol.geom.Point(
        ol.proj.fromLonLat([-73.63, 45.43])
      ),
      type: 'icon'
    });
    var vectorSource = new ol.source.Vector();
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
    vectorSource.addFeatures([markerCenter, markerLasalle])
