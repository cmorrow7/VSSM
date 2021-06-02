<! --When the Pi posts data to this webpage it is added to the GPS table-->
<! --Che Morrow -->
<?php
    function insertLocation($new_lat,$new_long,$new_time,$new_day) {
        require 'connect.php';
        # Assign variables to each place holder, indexed 1-4
        $data = array($new_lat,$new_long,$new_time,$new_day);

        $STH = $DBH->prepare("INSERT INTO location(latitude,longitude,time,day) VALUES(?,?,?,?)");
        $STH->execute($data);
        $DBH = null;
        $data = "";
    }

    if($_SERVER['REQUEST_METHOD'] == "POST") {
        $latitude = $_POST["lat"];
        $longitude = $_POST["long"];
        $time = $_POST["time"];
        $day = $_POST["day"];
        insertLocation($latitude,$longitude,$time,$day);
    }
 ?>
