# PiFmPSRT
Script for PiFmRds.  
You can create the amount of PS and RT, and so that it changes through the seconds you specified.  
Management via rds_ctl.  

# Installation
**1.** Choose a version of PiFmPSRT and drag to the PiFmRds Directory.  
**2.** Create in the directory PiFmRds -> mkfifo rds_ctl  
**3.** In one console we run -> sudo ./pi_fm_rds -ctl rds_ctl,  
and in another console we run -> python3 psrtv(ver).py  

# Version
**V1** - To change only in Python File (psrtv1.py)  
**V2** - You can in real time change PS and RT in files (ps.txt and rt.txt)  
**V3** - Support for seconds (PS | Seconds) is added and taken into account the characters (gaps) PS and RT. If seconds are not exhibited, by default, what is written in the script (psrtv3.py) is placed    
