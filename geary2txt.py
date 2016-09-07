#!/usr/bin/python

'''

geary2txt.py

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

Set 'geary_db_file' and 'dir_to_export' below where:

geary_db_file - geary database file e.g. '/home/USER/.local/share/geary/EMAIL@EMAIL.COM/geary.db'
dir_to_export - a folder to save messages e.g. '/home/USER/backup_emails' - no trailing slash

## HOW TO USE

Run geary2txt.py from terminal to see all Geary folders you can export messages from:
`geary2txt.py`

Run geary2txt.py from terminal with folder IDs as arguments to export messages as txt files:
`geary2txt.py 2 5 12`

'''

# Settings
geary_db_file = '/home/USER/.local/share/geary/EMAIL@EMAIL.COM/geary.db';
dir_to_export = '/home/USER/backup_emails'; # no trailing slash
fileextension = 'txt'; # eml or txt


import sys, re, datetime, sqlite3, os.path

print ''

# check if db file exists
if os.path.isfile(geary_db_file) : print ' -- Database file OK: ', geary_db_file
else : print '-- Database file does not exists, check your settings! --\n'; exit()

# check if dir to export exists
if os.path.isdir(dir_to_export) : print ' -- Backup directory OK: ', dir_to_export
else : print '-- Backup directory does not exists, check your settings! --\n'; exit()

# connect to the database
con = sqlite3.connect(geary_db_file)
cur = con.cursor()


# list and print all geary mail folders

cur.execute("SELECT id,name,last_seen_total FROM FolderTable")

print ''
print 'Geary mail folders'
print '--------------------------------------'

for row in cur:
    n0=str(row[0]); n1=str(row[1]); n2=str(row[2])
    print 'ID: '+n0+' Name: '+n1+' Messages: '+n2

print '--------------------------------------'


# prepare SQL IN(FOLDERS) based on the passed arguments

folders2process=[]

for arg in sys.argv:
    if arg.isdigit(): folders2process.append(arg)

if len(folders2process)<1 : 
    print 'No messages processed.'
    print 'Call this script with the IDs of the mail folders you want to backup messages from:'
    print 'geary2txt.py 1 5 12\n'
    cur.close(); con.close(); exit()

folders2sql = ','.join(folders2process)
folders2lst = ' '.join(folders2process)

print 'Folder IDs to backup messages from:',folders2lst;


# prepare a list of messages to backup

message_ids=[]
cur.execute('SELECT DISTINCT(message_id) FROM MessageLocationTable WHERE folder_id IN('+folders2sql+')')

for row in cur: 
    message_ids.append(str(row[0]))
message_ids = ','.join(message_ids)


# select the messages

cur.execute('SELECT from_field,date_time_t,subject,header,body FROM MessageTable WHERE id IN('+message_ids+') AND header IS NOT NULL AND body IS NOT NULL')

counter=0


# process the messages in a loop
for row in cur: 
# extract sender email from 'sender' field
    ematch = re.search('([\w.-]+)@([\w.-]+)', row[0])
    sender = ematch.group()
# get date/time from unix timestamp of the message
    mdatetime=datetime.datetime.fromtimestamp(row[1]).strftime('%Y-%m-%d %H:%M:%S')
# get subject, 50 chars only
    subject=row[2]; subject=subject[:50]
# prepare filename: dateime | sender | subject.extension
    mfilename=dir_to_export+'/'+mdatetime+' | '+sender+' | '+subject+'.'+fileextension
# message: header+body
    mfiledata=row[3]+row[4];
# save file
    if not os.path.isfile(mfilename) : f = open(mfilename, 'w'); f.write(mfiledata); f.close(); counter+=1

print counter , 'messages processed...'
print '--------------------------------------'
cur.close(); con.close(); exit()
