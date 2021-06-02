<! --Displays a list of links to any files in the videos/ directory of the server -->
<! --Che Morrow -->
<?php
    $dir = "videos/";
    # Sorted newest to oldest
    $display = scandir($dir,1);
    echo "<h1>List of Available Recordings</h1>";
    # Iterates through all files in the directory
    foreach($display as &$file) {
        if($file != "." && $file != "..") {
            echo "<br>";
            $url = "/videos/" . $file;
            echo "<a href =" . $url . " download>" .$file . "</a>";
            echo "<br>";
        }
    }
    unset($file);
 ?>
