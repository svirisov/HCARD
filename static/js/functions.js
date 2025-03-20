jQuery(function(){
    var socket = io.connect('http://192.168.22.253:5000');

    var regions = ['#region1', '#region2', '#region3'];
    
    socket.on('update_zone', function(msg) {
        /* reset all regions as blank slate */
        $.each(regions, function(index, value) {
            $(value).css("opacity", "0%");
        });
        /* select and enable region of interest */
        zone = parseInt(msg.data);
        $(regions[zone]).css("opacity","80%"); 
    });

    socket.on('after_connect', function() {
        /* set all regions to transparent by default */
        $.each(regions, function(index, value) {
            $(value).css("opacity", "0%");
        });
    });

    /* theme control */
    const checkbox = document.getElementById("theme");
    checkbox.addEventListener("change", () => {
        document.body.classList.toggle("dark")
    });
});