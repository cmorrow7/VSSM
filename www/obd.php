<! --When the Pi posts data to this webpage it is added to the OBD table-->
<! --Che Morrow -->
<?php
    # Adds a new entry to the OBD table
    function insertOBD($new_code,$new_day) {
        require 'connect.php';
        # Assign variables to each place holder, indexed 1-4
        $data = array($new_code,$new_day);

        $STH = $DBH->prepare("INSERT INTO obd(code,day) VALUES(?,?)");
        $STH->execute($data);
        $DBH = null;
        $data = "";
    }

    if($_SERVER['REQUEST_METHOD'] == "POST") {
        $code = $_POST["code"];
        $day = $_POST["day"];
        insertOBD($code,$day);
    }
 ?>
