!(function($){$(document).ready( function(){
    $.ajax({
        url    : "/api/map",
        context: document.body
    }).done(function(response) {
        var map = L.map('straddle-map', {
            zoomControl : false,
            scrollWheelZoom: false,
        }).setView([40.4115, -3.7076], 5);
        var zc = L.control.zoom({ 'position' : 'topright' }).addTo(map);
        L.tileLayer('https://api.mapbox.com/styles/v1/ale/cj3rpgd2n00142slekpjya98f/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWxlIiwiYSI6ImpKQ2dnekEifQ.GjyY2X3Wa6pgoHTPOrUBdA', {
          attribution: '<a href="https://www.mapbox.com/about/maps/" target="_blank">© Mapbox</a> <a href="http://www.openstreetmap.org/about/" target="_blank">© OpenStreetMap</a>'
        }).addTo(map);

        for(var i in response){
            var m = response[i];
            var popup = "";
            if(m.img){
                popup += "<img class='marker-img' src='" + m.img + "'/>";
            }
            if(m.cat){
                popup += "<p class='marker-cat'><span style='color:" + m.col +"'>■</span> " + m.cat + "</p>";
            }
            popup += "<h4 class='marker-name'>" + m.name + "</h4>";
            if(m.start_date){
                popup += "<p class='marker-date'>" + m.start_date;
            };
            if(m.end_date){
                popup += "—" + m.end_date; + "</p>";
            } else {
                popup += "</p>";
            }
            L.marker([m.pos.coordinates[1], m.pos.coordinates[0], -0.09]).addTo(map)
              .bindPopup(popup);
        }
    });
})})(jQuery);
