    // get points data from data-attribute
    const container = document.querySelector("#map");
    const data = container.getAttribute("data-points");
    const points = JSON.parse(data);
    const attribution = new ol.control.Attribution({
        collapsible: false
    });
    const iconStyles = new ol.style.Style({
        image: new ol.style.Icon({
          anchor: [0.5, 1],
          src: 'static/blue.png',
        })
    });
    const vectorSource = new ol.source.Vector();
    const markers = [];
    const setMarker = (longitude, latitude) => {
        return new ol.Feature({
            geometry: new ol.geom.Point(
                ol.proj.fromLonLat([longitude, latitude])
            ),
            type: 'v-icon'
        });
    }
    points.forEach(function(point){
        point = Array.from(point);
        /** @params longitude and latitude
          * longitude = Number(point[3]) and latitude = Number(point[2])
          */
        const marker = setMarker(Number(point[3]),Number(point[2]))
        markers.push(marker)
    })
    // console.log('Markers', markers)
    vectorSource.addFeatures(Array.from(markers))
    const vectorLayer = new ol.layer.Vector({
        source: vectorSource,
        style: iconStyles,
        updateWhileAnimating: true,
        updateWhileInteracting: true
    })
    const map = new ol.Map({
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
