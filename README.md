# PiFmPSRT
Script for PiFmRds.  
You can create the amount of PS and RT, and so that it changes through the seconds that you indicated, as well as use the modes and change the position of the text.  
Management via rds_ctl.  

# Installation
**1.** Choose a version of PiFmPSRT and drag to the PiFmRds Directory.  
**2.** Create in the directory PiFmRds -> mkfifo rds_ctl  
**3.** In one console we run -> sudo ./pi_fm_rds -ctl rds_ctl  
and in another console we run -> python3 psrtv(ver).py  
**4.** After the PiFmRds -> Change ps.txt and rt.txt directory. Without closing the script, you can change PS and RT by saving a text file  

# Registers for V4
Gaps and any other symbols are also taken into account, including |.  
r||text -> ___|text  
If you put the gaps, the text will move. It works both in PS and RT.  
⠀text -> _ text ___  
⠀⠀text -> __ text __  

**Standart mode:**  
text - normal mode, starting on the left, switching for 5 seconds  
text|2 - Switching in 2 seconds  
l|text - Indication of the position on the left -> text____  
c|text - Indication of the position on the centre -> __ text __  
r|text - Indication of the position on the right -> ____text  

**Scroll mode:**  
s|hellotext - Scroll of letters -> hellotex [or] ellotext  
s|hellotext|5 - Scroll of letters 5 seconds -> hellotex (5s) [or] ellotext (5s)  

**Transfer mode:**  
t|hellotext - Transfer of text -> hellotex [or] t_______  
t|hellotext|5 - Transfer of text 5 seconds -> hellotex (5s) [or] t_______ (5s)  
t6|hellotext - Transfer of text only 6 characters -> hellot__ [or] ext_____  
t4|hellotext - Transfer of text only 4 characters -> hell____ [or] otex____ [or] t_______  
lt|hellotext - Transfer of text on the left -> hellotex [or] t_______  
ct|text - Transfer of text on the centre -> hellotex [or] ___ t ____  
rt|text - Transfer of text on the right -> hellotex [or] _______t  
ct6|hellotext - Transfer of text in the centre of only 6 characters -> _ hellot _ [or] __ ext ___  

# Version
**V1** - To change only in Python File (psrtv1.py)  
**V2** - You can in real time change PS and RT in files (ps.txt and rt.txt)  
**V3** - Support for seconds (PS | Seconds) is added and taken into account the characters (gaps) PS and RT. If seconds are not exhibited, by default, what is written in the script (psrtv3.py) is placed    
**V4** - Support for transferring text, scrolling by letter, position of the word (left, center, right)  
**V4.1** - One code is divided into several files for convenience. It is launched through main.py, all files in the PIFMPSRT folder (including ps.txt and rt.txt)
