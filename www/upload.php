<! --Allows the Pi to post video files to the website-->
<! --Che Morrow -->
<?php
    if($_SERVER['REQUEST_METHOD'] == "POST") {
        $file_name = $_FILES['vid']['name'];
        $file_tmp = $_FILES['vid']['tmp_name'];
        if(move_uploaded_file($file_tmp,"videos/".$file_name)) {
            print("File Uploaded");
        } else {
            print("Error");
        }
   }
?>
