#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

geary2txt.py 
version 0.2 / 2016-09-15

A cmd tool in Python to export / backup Geary and Pantheon-mail messages as source: TXT, EML or MHT files.

https://github.com/uuencode/geary2txt


HOW TO INSTALL

- Make this file executable

- Set 'geary_db_file' and 'dir_to_export' below where:

  geary_db_file - geary database file e.g. '/home/USER/.local/share/ geary-OR-pantheon-mail /EMAIL@EMAIL.COM/geary.db'
  dir_to_export - a folder to save messages e.g. '/home/USER/backup_emails' - no trailing slash

- Make sure that you have permissions to read 'geary_db_file' and permissions to create files in 'dir_to_export' 


HOW TO USE

Run geary2txt.py from terminal:
`PATH-TO/geary2txt.py`

Run geary2txt.py from terminal with folder IDs as arguments to export messages as source files without prompt:
`PATH-TO/geary2txt.py 2 5 12`

'''

# Settings
geary_db_file = '/home/USER/.local/share/ geary-OR-pantheon-mail /EMAIL@EMAIL.COM/geary.db';
dir_to_export = '/home/USER/backup_emails'; # no trailing slash
fileextension = 'eml'; # eml, txt or mht or whatever you wish

# ----------


import sys, os, re, datetime, sqlite3

hr=' --------------------------------------'

# colors for printing
class clr:
 ppl='\033[95m'
 blu='\033[94m'
 gre='\033[92m'
 yel='\033[93m'
 red='\033[91m'
 bld='\033[1m'
 end='\033[0m'

# create nice table output + colors
def niceprint(a,b,c,d):
# a=string; b=spaces to align right; c=length; d=color
# r=result; x=calc spaces (left); y=calc spaces to length
 r=''; x=''; y=''
 if len(a)<b: x=b-len(a); x=x*' '
 r=x+a
 if len(r)<c: y=c-len(r); y=y*' '
 r=r+y
 if d!=0: r=d+r+clr.end
 return r

# clear the screen
os.system('clear')

print ''
print clr.bld+' geary2txt'+clr.end+' (Export/backup Geary mail messages as source files)'
print ''

# check if db file exists or die
if os.path.isfile(geary_db_file): print clr.gre+' Database file OK: '+clr.end, geary_db_file
else: print clr.red+' Database file does NOT exist, check your settings!\n'+clr.end; exit()

# check if dir to export exists or die
if os.path.isdir(dir_to_export): print clr.gre+' Backup directory OK: '+clr.end, dir_to_export
else: print clr.red+' Backup directory does NOT exist, check your settings!\n'+clr.end; exit()

# print help
print '\n This script can be called with the IDs of the folders you want to backup messages from:'
print clr.blu+' geary2txt.py 1 5 12'+clr.end

# connect to the database
con=sqlite3.connect(geary_db_file)
cur=con.cursor()

# Geary mail folders

print ''
print clr.yel+' Geary folders'+clr.end+' ( where messages > 0 )'

print hr
print ' id    Folder                Messages'
print hr

# put folder names in a dictionary
gfolders={}
cur.execute("SELECT id,name FROM FolderTable ORDER BY id")
for row in cur:
 gfolders[row[0]]=row[1]

# list folders and count messages since Geary counting is unreliable
cur.execute("SELECT folder_id, COUNT(message_id) FROM MessageLocationTable GROUP BY folder_id")

atleastone=0

for row in cur:
 n0=niceprint(str(row[0]),2,6,0) # folder id
 n1=gfolders[row[0]]; n1=n1[:20]; n1=niceprint(n1,0,25,0) # folder name
 n2=niceprint(str(row[1]),5,7,clr.red+clr.bld) # message count
 line=' '+n0+n1+n2; atleastone+=1
 print line

if atleastone<1: 
 cur.close(); con.close()
 print ' No folders with messages!'
 print hr
 print '\n Bye bye!\n'; exit()

print hr

# prepare SQL IN(FOLDERS) based on the passed arguments
 
folders2process=[]

# use sys.argv first
for arg in sys.argv:
 if arg.isdigit(): folders2process.append(arg)

# if no sys.argv show input
if len(folders2process)<1: 
 passids=raw_input(" Folder IDs to export messages from or (n) to exit: ")
 passids=passids.split()
 for entry in passids:
  if entry.isdigit(): folders2process.append(entry)

# if still no valid arguments die
if len(folders2process)<1:
 print '\n No valid folder IDs.\n Bye bye!\n'; cur.close(); con.close(); exit()

folders2sql=','.join(folders2process)
folders2lst=' '.join(folders2process)

print '\n Exporting messages from folders:',folders2lst

# prepare a list of messages to backup

message_ids=[]
cur.execute('SELECT DISTINCT(message_id) FROM MessageLocationTable WHERE folder_id IN('+folders2sql+')')

for row in cur: 
 message_ids.append(str(row[0]))
message_ids=','.join(message_ids)


# select the messages
cur.execute('SELECT from_field,date_time_t,subject,header,body FROM MessageTable WHERE id IN('+message_ids+')')

skippedcounter=0; successcounter=0; failedocounter=0; successlog=[]; failedolog=[]

# process the messages in a loop
for row in cur: 
 mfiledata=''

 # extract sender email from 'sender' field
 ematch=re.search('([\w.-]+)@([\w.-]+)', row[0])
 sender=ematch.group()

 # get date/time from unix timestamp of the message
 mdatetime=datetime.datetime.fromtimestamp(row[1]).strftime('%Y-%m-%d %H:%M:%S')

 # get subject, 50 chars only
 subject=row[2]
 subject=re.sub(r'[^a-zA-Z0-9 ]','',subject)
 subject=subject[:50]

 # prepare log entry name and filename: dateime | sender | subject.extension
 nametolog=' '+mdatetime+' | '+sender+' | '+subject
 mfilename=dir_to_export+'/'+mdatetime+' | '+sender+' | '+subject+'.'+fileextension

 # message: header+body and save file (skip if exists)
 if(row[3] is not None and row[4] is not None): mfiledata=row[3]+row[4]
 else: failedocounter+=1; failedolog.append(nametolog)
 
 if os.path.isfile(mfilename): skippedcounter+=1
 elif len(mfiledata)>0: successlog.append(nametolog); f=open(mfilename, 'w'); f.write(mfiledata); f.close(); successcounter+=1

# close db connection
cur.close(); con.close()

print hr

# bold result numbers
successn=niceprint(str(successcounter),3,0,clr.bld)
skippedn=niceprint(str(skippedcounter),3,0,clr.bld)
failedon=niceprint(str(failedocounter),3,0,clr.bld)

# print result
print ' '+successn+clr.gre+' messages processed successfully...'+clr.end
print ' '+skippedn+clr.blu+' messages skipped (previously processed)...'+clr.end
print ' '+failedon+clr.red+' messages failed due to a missing header or body...'+clr.end
print hr+'\n'

# if no messages in the selected folders simply die
if(successcounter+failedocounter)<1: print ' Bye bye!\n'; exit()

# show log
showlog=raw_input(' Would like to see a log (y) or (n): ')
if(showlog!='y'): print ' Bye bye!\n'; exit()

successlog='\n'.join(successlog)
failedolog='\n'.join(failedolog)

print ''
print clr.gre+successlog+clr.end
print clr.red+failedolog+clr.end

print ' Bye bye!\n'
exit()
