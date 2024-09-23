## Python Based RAT to exploit users on same network

Developed a RAT to explore socket programming in Python, capable of accessing the file system and camera of compromised machines. 

The RAT auto-activates on installation, disguises itself as a system software, which makes it hard to be detected via Task Manager.

Compiled into an executable package, with a separate controller which is used by attacker to control victim machines on same network. 

Integrated Google Sheets API to log affected systems' IP addresses and usernames. This helps to keep track of victim even when their IP changes on local network.
