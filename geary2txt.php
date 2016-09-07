#!/usr/bin/php
<?php

/*

geary2txt.php

A cmd tool to export/backup Geary email messages as TXT/EML files.

https://github.com/uuencode/geary2txt

- this tool will NOT change anything in the Geary database
- messages removed from Geary are NOT removed from backup
- previously exported messages are skipped
- messages can be displayed or imported from any email program that supports eml files

## REQUIREMENTS

python 2.x

## HOW TO INSTALL

Make this file executable

Set '$geary_db_file' and '$dir_to_export' below where:

$geary_db_file - geary database file e.g. '/home/USER/.local/share/geary/EMAIL@EMAIL.COM/geary.db'
$dir_to_export - a folder to save messages e.g. '/home/USER/backup_emails' - no trailing slash

## HOW TO USE

Run geary2txt.php from terminal to see all Geary folders you can export messages from:
`geary2txt.php`

Run geary2txt.php from terminal with folder IDs as arguments to export messages as txt files:
`geary2txt.php 2 5 12`

*/

// SETTINGS
$geary_db_file = '/home/USER/.local/share/geary/EMAIL@EMAIL.COM/geary.db';
$dir_to_export = '/home/USER/backup_emails'; // no trailing slash
$fileextension = 'eml'; //eml or txt


// -------------------------------------------


// check if db file is readable
if(!is_readable($geary_db_file)){
print "\nGeary database file does not exist / not readable.\nSet a full path to a proper Geary db file at the beginning of this script...\n\n";
die();}


// check if dir to export is writeable
if(!is_writable($dir_to_export)){
print "\nThe directory to save messages does not exist / not writeable.\nSet a full path to a writeable directory at the beginning of this script...\n\n";
die();}


// connect to the Geary database
$dbo = new PDO('sqlite:'.$geary_db_file);


// list and print all geary mail folders
print "\nAll Geary mail folders\n";
print "________________________________\n\n";

$query = 'SELECT id,name,last_seen_total FROM FolderTable';
$query = $dbo -> prepare($query);
$query -> execute();
while($entry = $query -> fetch()){
print 'ID:'.$entry['id'].' Name:'.$entry['name'].' Messages:'.$entry['last_seen_total']."\n";
}

print "________________________________\n";


// prepare SQL IN(FOLDERS) based on the passed arguments
$folders2sql = '';
$folders2lst = '';
if(isset($argv)){
for($i = 0; $i<count($argv); $i++){$argv[$i] = (int)$argv[$i];}
unset($argv[0]);
$folders2lst = implode(' ',$argv);
$folders2sql = implode(',',$argv);
}


// if no arguments were passed print some help and die
if(strlen($folders2sql)<1){
print "\nNo messages processed.\n";
print "Call this script with the IDs of the mail folders you want to export messages from:\n";
print "php geary2txt 1 5 12\n";
print "________________________________\n\n";
die();}


print "\nFolder IDs to export messages from: ".$folders2lst."\n";


// prepare a list of messages to export
$query = "SELECT DISTINCT(message_id) FROM MessageLocationTable WHERE folder_id IN($folders2sql)";
$query = $dbo -> prepare($query);
$query -> execute();
$message_ids = array();
while($entry = $query -> fetch()){$message_ids[] = $entry[0];}
$message_ids = implode(',',$message_ids);


// select the messages
$query = "SELECT from_field,date_time_t,subject,header,body FROM MessageTable WHERE id IN($message_ids)";
$query = $dbo -> prepare($query);
$query -> execute();

$counter = 0;


// process the messages in a loop
while($msg = $query -> fetch()){

// extract sender email from 'sender' field
$pattern = '/[A-Za-z0-9_-]+@[A-Za-z0-9_-]+\.([A-Za-z0-9_-][A-Za-z0-9_]+)/';
preg_match($pattern, $msg['from_field'], $matches);
$sender = $matches[0];

// get date/time from unix timestamp of the message
$datetime = gmdate('Y-m-d H:i:s',$msg['date_time_t']);

// get subject, 50 chars only
$subject = substr($msg['subject'],0,50);

// prepare filename: dateime | sender | subject.extension
$filename = $dir_to_export.'/'.$datetime.' | '.$sender.' | '.$subject.'.'.$fileextension;

// message: header+body
$filedata = $msg['header'].$msg['body'];

// save file
if(!is_file($filename)){
file_put_contents($filename, $filedata);
$counter+ = 1;
}

}

print "$counter messages processed...\n";
print "________________________________\n\n";
