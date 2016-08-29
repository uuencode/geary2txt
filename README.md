# geary2txt

A cmd tool to export/backup Geary email messages as TXT/EML files. Requires php with pdo_sqlite extension.

https://github.com/uuencode/geary2txt

- this tool would NOT change anything in the Geary database
- messages removed from Geary are NOT removed from backup
- previously exported messages are skipped
- messages can be displayed or imported from any email program that supports eml files

## REQUIREMENTS
php with pdo_sqlite extension

## HOW TO INSTALL
Put geary2txt in /usr/local/bin and make it executable

Set '$geary_db_file' and '$dir_to_export' at the beginning of geary2txt where:

$geary_db_file - geary database file e.g. '/home/USER/.local/share/geary/EMAIL@EMAIL.COM/geary.db'

$dir_to_export - a folder to save messages e.g. '/home/USER/backup_emails' - no trailing slash

## HOW TO USE
Run geary2txt from terminal to see all Geary folders you can export messages from:

`php /usr/local/bin/geary2txt`

Run geary2txt from terminal with folder IDs as arguments to export messages as txt files:

`php /usr/local/bin/geary2txt 2 5 12`

## SCREENSHOT
![Alt text](/screenshot.png "void")

## SCREENCAST

https://youtu.be/p5bfxWthEOg
