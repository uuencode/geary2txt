# geary2txt

A cmd tool in Python to export / backup Geary and Pantheon-mail messages as source: TXT, EML or MHT files.

https://github.com/uuencode/geary2txt

* this tool does NOT change anything in the Geary database
* messages removed from Geary are NOT removed from backup
* previously exported messages are skipped
* messages that are visible in the Geary mail list but not yet downloaded (no header+body in the database) are not processed, (info provided instead)


![Alt text](/geary2txt.gif "screencast GIF")


## HOW TO INSTALL

* Download and save 'geary2txt.py' and make it executable
* Set 'geary_db_file' and 'dir_to_export' at the beginning of geary2txt.py where:
 * geary_db_file - geary database file e.g. '/home/USER/.local/share/ geary-OR-pantheon-mail /EMAIL@EMAIL.COM/geary.db'
 * dir_to_export - a folder to save messages e.g. '/home/USER/backup_emails' - no trailing slash
* Make sure that you have permissions to read 'geary_db_file' and permissions to create files in 'dir_to_export' 


## HOW TO USE

Run geary2txt from terminal:

`PATH-TO/geary2txt.py`

Run geary2txt.py from terminal with folder IDs as arguments to export messages as source files without prompt:

`PATH-TO/geary2txt.py 2 5 12`


## WHAT TO DO WITH THE FILES

* messages can be displayed or imported from any email program that supports EML/MHT files e.g. Thunderbird
* there is a Firefox extension that opens EML and MHT files: UnMHT
* there is a Chrome extension to open and extract EML/MHT files: MHT Viewer
* a cmd tool called mpack extracts the content of EML/MHT files with the following command: munpack file
* a gtk/webkit based app on GitHub called ohwgiles/wemed claims to open & edit EML files

## HISTORY

* version 0.2 / 2016-09-15

 * fancy colors
 * Geary folders with no messages are not displayed
 * log: skipped, failed and processed messages + details
 * interactive options to choose folders and display log
 * messages are counted internally since Geary db records seem to be unreliable
 * messages without header & body in the database are marked as 'failed' and not processed
 * php version removed

* version 0.1 / 2016-09-07 - initial release 


## KNOWN ISSUES
 
There seems to be no easy and reliable way to convert the email subject to utf8 from the various encoding methods that are used. Now geary2txt simply removes any non-ascii symbol to create the subject part of the filename.
