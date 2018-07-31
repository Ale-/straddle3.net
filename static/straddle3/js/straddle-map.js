!(function($){
  $(document).ready( function(){
    $.ajax({
        url    : "/api/map",
        context: document.body
    }).done(function(response) {
        var map = L.map('straddle-map', {
            zoomControl : false,
            scrollWheelZoom: false,
        }).setView([36.4115, -23.7076], 12);
        var zc = L.control.zoom({ 'position' : 'topright' }).addTo(map);
        L.tileLayer('https://api.mapbox.com/styles/v1/ale/cj3rpgd2n00142slekpjya98f/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWxlIiwiYSI6ImpKQ2dnekEifQ.GjyY2X3Wa6pgoHTPOrUBdA', {
          attribution: '<a href="https://www.mapbox.com/about/maps/" target="_blank">© Mapbox</a> <a href="http://www.openstreetmap.org/about/" target="_blank">© OpenStreetMap</a>'
        }).addTo(map);

        // Marker icon
        var icon = L.icon({
            iconUrl      : '/static/straddle3/img/s3-marker.svg',
            iconSize     : [30, 45],
            iconAnchor   : [15, 45],
            popupAnchor  : [0, -30],
            shadowUrl    : '/static/straddle3/img/s3-marker--shadow.svg',
            shadowSize   : [20, 25],
            shadowAnchor : [0, 25]
        });
        var markers = [];
        // Populate map
        for(var i in response){
            var m = response[i];
            var popup_content = "";
            if(m.pos){
                if(m.cat){
                  popup_content += "<p class='marker-cat'>" + m.cat + "</p>";
                }
                if(m.img){
                  popup_content += "<img class='marker-img' src='" + m.img + "'/>";
                }
                popup_content += "<h4 class='marker-name'><a href='" + m.url + "'>" + m.name + "</a></h4>";
                if(m.subtitle){
                  popup_content += "<h5 class='marker-subtitle'>" + m.subtitle + "</h5>";
                }

                var popup = document.createElement('div');
                popup.innerHTML = popup_content;

                markers.push(L.marker([m.pos.coordinates[1], m.pos.coordinates[0], -0.09], { icon : icon }).bindPopup(popup));
            }
        }
        var group = new L.featureGroup(markers).addTo(map);
        map.fitBounds(group.getBounds());
    });
})})(jQuery);
