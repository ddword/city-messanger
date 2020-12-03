    var attribution = new ol.control.Attribution({
         collapsible: false
    });
    var markerCenter = new ol.Feature({
      geometry: new ol.geom.Point(
        ol.proj.fromLonLat([-73.65269, 45.48858])
      ),
      type: 'icon'
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
    /*var markerCenter = new ol.Feature({
      geometry: new ol.geom.Point(
        ol.proj.fromLonLat([-73.65269, 45.48858])
      ),
      type: 'icon'
    });
    var markerVectorLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
          features: [markerCenter]
        })
    });
    var markerLasalle = new ol.feature.Vector({
      geometry: new ol.geom.Point(
        ol.proj.fromLonLat([-74, 42])
      ),
      type: 'icon'
    });
    map.addLayer(markerVectorLayer);
    markerVectorLayer.addFeature(markerLasalle);
    */