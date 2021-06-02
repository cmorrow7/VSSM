<! --Code adapted from the Google Maps API Documentation-->
<! --https://developers.google.com/maps/documentation/javascript/overview-->
<! --Adapted by Che Morrow -->
<!DOCTYPE html >
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
<title>VSSM Location</title>
<style>
/* Always set the map height explicitly to define the size of the div
* element that contains the map. */
#map {
height: 100%;
}
/* Optional: Makes the sample page fill the window. */
html, body {
height: 90%;
margin: 0;
padding: 0;
}
</style>
</head>

<html>
    <body>
        <div id="map"></div>
        <script>
            function initMap() {
                var map = new google.maps.Map(document.getElementById('map'), {
                    // Center the map around Chico, CA
                    center: new google.maps.LatLng(39.72962, -121.83737),
                    zoom: 12
                });
                var infoWindow = new google.maps.InfoWindow;

                downloadUrl('pins.xml', function(data) {
                    var xml = data.responseXML;
                    var markers = xml.documentElement.getElementsByTagName('marker');
                    Array.prototype.forEach.call(markers, function(markerElem) {
                        // When the markers are selected the index and time of creation will display
                        var id = markerElem.getAttribute('id');
                        var time = markerElem.getAttribute('time');

                        var point = new google.maps.LatLng(
                        parseFloat(markerElem.getAttribute('lat')),
                        parseFloat(markerElem.getAttribute('lng')));

                        var infowincontent = document.createElement('div');
                        var strong = document.createElement('strong');
                        strong.textContent = id
                        infowincontent.appendChild(strong);
                        infowincontent.appendChild(document.createElement('br'));
                        var icon = "";
                        var text = document.createElement('text');
                        text.textContent = time
                        infowincontent.appendChild(text);
                        var marker = new google.maps.Marker({
                            map: map,
                            position: point,
                            label: icon.label
                        });
                        marker.addListener('click', function() {
                            infoWindow.setContent(infowincontent);
                            infoWindow.open(map, marker);
                        });
                    });
                });
            }

            function downloadUrl(url, callback) {
                var request = window.ActiveXObject ?
                new ActiveXObject('Microsoft.XMLHTTP') :
                new XMLHttpRequest;

                request.onreadystatechange = function() {
                    if (request.readyState == 4) {
                        request.onreadystatechange = doNothing;
                        callback(request, request.status);
                    }
                };
                request.open('GET', url, true);
                request.send(null);
            }
            function doNothing() {}
        </script>
        <script async src=""> </script>
        <br>
        <?php
            # Retrieves data from DTC table and displays under the map
            function printTable() {
                require 'connect.php';
                $CURRENT = fopen("day.txt","r");
                $day = fread($CURRENT,16);
                fclose($CURRENT);
                # STH means "Statement Handle"
                $query = "SELECT code from obd WHERE day = '".$day."'";
                $STH = $DBH->query($query);

                # setting the fetch mode
                $STH->setFetchMode(PDO::FETCH_ASSOC);

                while($row = $STH->fetch()) {
                    echo nl2br($row['code'] . "\n");
                    echo "<br>";
                }
                $DBH = null;
            }
            echo "<h2>Diagnostic Trouble Codes Detected:</h2>";
            printTable();
        ?>
        <a href = "index.php">Return To Homepage</a>
    </body>
</html>
