import os,sys

scriptName=r'"FBA Label Printer.py"'
hooker='--additional-hooks-dir=.'
solo="--onefile"
noTrash="--clean"
iconname="printerico.ico"
iconstring="--icon="+iconname+""
noConsole="--noconsole"
bundleIcon='--add-data printer.png;.'
option=[hooker,solo,noTrash,
        iconstring,noConsole,bundleIcon,scriptName]
command='pyinstaller '
for i in option:
    command+=i+' '
##command+=solo
##command+=noTrash
##command+=iconstring
##command+=noConsole
##command+=bundleIcon
##command+=scriptName
os.system(command)
print(command)
