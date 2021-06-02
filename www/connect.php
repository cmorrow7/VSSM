<! --Create database handler using stored credentials -->
<! --Username and password should be stored securely in the future -->
<! --Che Morrow -->
<?php
$servername = "localhost";
$dbname = "vssm";
$username = "root";
$password = "";

try {
    $DBH = new PDO("mysql:host=$servername;dbname=$dbname",$username,$password);
    $DBH->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}

return $DBH;
?>
