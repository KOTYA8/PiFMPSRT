# PiFMPSRT
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀Script for [PiFmRds](https://github.com/ChristopheJacquet/PiFmRds) and [PiFMX](https://github.com/KOTYA8/PiFMX).  
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ You can create the amount of **PS** and **RT**,  
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀and so that it changes through the seconds that you indicated,  
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀as well as use the modes and change the position of the text.  
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Management via **rds_ctl**.  

# Installation
**1.** In the terminal we write -> `git clone https://github.com/KOTYA8/PiFMPSRT/`  
**2.** Next, transfer the `pifmpsrt` and `psrt.py` to the PiFmRds or PiFMX Directory.  
**3.** Create in the directory PiFmRds or PiFMX -> `mkfifo rds_ctl`  
**4.** In one console we run -> `sudo ./pi_fm_rds -ctl rds_ctl` or `sudo ./pi_fm_x -ctl rds_ctl`  
and in another console we run: `python3 psrt.py`  
**5.** After the PiFmRds or PiFMX -> pifmpsrt -> `Change ps.txt and rt.txt directory`. Without closing the script, you can change PS and RT by saving a text file. 

# Future Functions

* **Scroll (modes)** - ❌ not realized  
* **Scroll (RT)** - ❌ not realized  
* **Transfer along with (-)** - ❌ not realized  
* **Source (file)** - ❌ not realized  
* **Clock** - ❌ not realized  
* **Date** - ❌ not realized  

# Registers
### **GLOBAL Mode**  
Gaps and any other symbols are also taken into account, including |.  
r||text -> `___|text`  

If you put the gaps, the text will move. It works both in PS and RT.  
⠀text -> `_text ___`  
⠀⠀text -> `__text__`  

### **PS Mode** 
**Standart mode:**  
text - normal mode, starting on the left, switching for 5 seconds -> `text____`  
text|2 - Switching in 2 seconds  
l|text - Indication of the position on the left -> `text____`  
c|text - Indication of the position on the centre -> `__text__`  
r|text - Indication of the position on the right -> `____text`  

**Scroll mode:**  
s|hellotext - Scroll of letters -> `hellotex [or] ellotext`  
s|hellotext|5 - Scroll of letters 5 seconds -> `hellotex (5s) [or] ellotext (5s)`  
s|hellotext|5/2 - Scroll of letters 5/2 seconds -> `hellotex (5s) [or] ellotext (2s)`  

**Transfer mode:**  
t|hellotext - Transfer of text -> `hellotex [or] t_______`  
t|hellotext|5 - Transfer of text 5 seconds -> `hellotex (5s) [or] t_______ (5s)`  
t|hellotext|5/2 - Transfer of text 5/2 seconds -> `hellotex (5s) [or] t_______ (2s)`  
t1|hellotext - Transfer of text only 1 characters -> `h_______ [or] e_______ [or] l_______ (...)`  
t2|hellotext - Transfer of text only 2 characters -> `he______ [or] ll______ [or] ot______ (...)`  
t3|hellotext - Transfer of text only 3 characters -> `hel_____ [or] lot_____ [or] ext_____ `  
t4|hellotext - Transfer of text only 4 characters -> `hell____ [or] otex____ [or] t_______`  
t5|hellotext - Transfer of text only 5 characters -> `hello___ [or] text____`  
t6|hellotext - Transfer of text only 6 characters -> `hellot__ [or] ext_____`  
t7|hellotext - Transfer of text only 7 characters -> `hellote_ [or] xt______`  
lt|hellotext - Transfer of text on the left -> `hellotex [or] t_______ `  
ct|text - Transfer of text on the centre -> `hellotex [or] ___ t ____`  
rt|text - Transfer of text on the right -> `hellotex [or] _______t`  
ct6|hellotext - Transfer of text in the centre of only 6 characters -> `_hellot_ [or] __ext___`  

### **RT Mode** 
text - Normal mode -> `text____(...)`  

l|text - Indication of the position on the left -> `text____(...)`  
c|text - Indication of the position on the centre -> `__text__`  
r|text - Indication of the position on the right -> `(...)____text` 

# Changelog
All previous versions are available in the repository: [PiFMPSRT_VER](https://github.com/KOTYA8/PiFMPSRT_VER) 

### **Currently**  
* **V5** - The name main.py on psrt.py. Automatic definition has been added when the ps.txt and rt.txt file is saved. Added support for seconds for transfer and scroll (s/s). Added position support for RT (l, c, r). Support for the readings of 1.2.3.5.7 characters are added.  
