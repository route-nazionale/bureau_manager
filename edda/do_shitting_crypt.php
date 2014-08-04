#!/usr/bin/php5
<?php

include('Crypt/AES.php');

$testo = $argv[1];
$b64key = $argv[2];
$b64iv = $argv[3];

$publicKey = base64_decode($b64key);
$iv = base64_decode($b64iv);

$cipher = new Crypt_AES(CRYPT_AES_MODE_CBC);

$cipher->setKey($publicKey);
$cipher->setIV($iv);

$encoded = $cipher->encrypt($testo);

$crypt_text = base64_encode($encoded);

echo $crypt_text;

?>
