<! --Takes in a date from the user, then exports related locational data-->
<! --to an XML document for Maps API use-->
<! --Che Morrow -->
<!DOCTYPE HTML>
<html>
    <head>
        <style>
            .error {color: #FF0000;}
        </style>
    </head>
    <body>
    <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $day = $_POST["day"];
            createXML($day);
            header("Location: map.php");
        }
        function createXML($day) {
            # Needs the DBH created in the connect file
            require 'connect.php';
            # Forms a mySQL query and sends it to the database
            $query = "SELECT * from location WHERE day = '".$day."'";
            $STH = $DBH->query($query);
            # Saves current day to use in the maps file for future queries
            $SAVE = fopen("day.txt","w");
            fwrite($SAVE,$day);
            fclose($SAVE);
            # Setting the fetch mode
            $STH->setFetchMode(PDO::FETCH_ASSOC);
            # Creates XML file with location data, following Maps API documentation
            $XML = fopen("pins.xml","w");
            $i = 1;
            fwrite($XML,"<markers>\n");
            while($row = $STH->fetch()) {
                fwrite($XML,'<marker id="');
                fwrite($XML,$i);
                $i = $i + 1;
                fwrite($XML,'" lat="');
                fwrite($XML,$row['latitude']);
                fwrite($XML,'" lng="');
                fwrite($XML,$row['longitude']);
                fwrite($XML,'" time="');
                fwrite($XML,$row['time']);
                fwrite($XML,'" />');
                fwrite($XML,"\n");
            }
            fwrite($XML,"</markers>");
            fclose($XML);
            $DBH = null;
        }
    ?>
    <h2>Display Positional Data</h2>
    <p>Enter a date in the form year-month-day, e.g. 2021-02-14</p>
    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
        Enter Date: <input type="text" name="day" value="">
        <input type="submit" name="submit" value="Submit">
    </form>
    <br>
    <a href = "download.php">View Uploaded Recordings</a>
    </body>
</html>
