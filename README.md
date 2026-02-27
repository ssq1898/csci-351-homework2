# csci-351-homework2
Homework 2 (Ping and Traceroute) assignment for CSCI-351

How to run my_ping.py:
1. Make sure you are in the directory where the the project is located.
2. Activate a virtual environment.
3. Run the program from the command line.
    usage: my_ping [-h] HOSTNAME [-c C] [-i I] [-s S] [-t T]

Command-line usage examples:
    python my_ping.py google.com
    python my_ping.py google.com -c 5
    python my_ping.py google.com -i 3
    python my_ping.py google.com -s 64
    python my_ping.py google.com -t 20

How to run my_traceroute.py:
1. Make sure you are in the directory where the the project is located.
2. Activate a virtual environment.
3. Run the program from the command line.
    usage: my_traceroute [-h] HOSTNAME [-n] [-q Q] [-S]

Command-line usage examples:
    python my_traceroute.py google.com
    python my_traceroute.py google.com -n
    python my_traceroute.py google.com -q 5
    python my_traceroute.py google.com -S
