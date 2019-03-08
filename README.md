# pyfiles

This python app requires bottle and some other less significant imports

It uses python2 in order to remain compatible with standard (ubuntu) apache WGSI (if you choose to use that).

This program lists file in a directory declared in pyfiles.py - see the global variables section
The default dir is /data/share/dlfiles.
It will only list files in that directory that have an associated description file
This description file must be a hidden file (starts with a ".") followed by the basename with extension and then followed by ".nts"
So if, for example if you want to include a file called app.py then you need a file associated with it called .app.py.nts
THe first line will be used as a description of the file in the downloadable file listing
so if you want to to include /data/share/dlfiles/app.py 
then add a file with a description as the first line eg:

```
cat /data/share/dlfiles/.app.py.nts 
This file [app.py] will plan your camping trip and prepare your dinner menu for every night you are camping.
```

Now if you also want to keep count of the times the file was invoked for download then add this as the second line

```
<description>
[cnt]:
```

With that second line a count will be kept of all the attempted downloads.
After 10 attempted downloads your description notes file would look like this

```
cat /data/share/dlfiles/.app.py.nts 
This file [app.py] will plan your camping trip and prepare your dinner menu for every night you are camping.
[cnt]: 10
```

Enjoy
geoff.mcnamara@gmail.com

------- README.md -------
    
Created on: 20190308-1745
Created by: geoffm
    
----- Last Code Changes -----
    
Modified on: 20190308-1809
Modified by: geoffm
   
------- README.md -------
" vim: set syntax=none nospell:
