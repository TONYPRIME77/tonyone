#!/usr/bin/env python3
"""
WHITE MADRID — Ethical Hacking AI Terminal
Developer : TONYPRIME
Version   : v4.0 — JARVIS Edition
Platform  : Termux / Linux / macOS
API       : OpenRouter
"""

import os, sys, json, time, datetime, subprocess
import urllib.request, urllib.error
import readline, textwrap, re, shutil, threading, random

# ══════════════════════════════════════════════════════════════════════
#  COLORS
# ══════════════════════════════════════════════════════════════════════
class C:
    RESET   = "\033[0m";  BOLD    = "\033[1m";  DIM    = "\033[2m"
    RED     = "\033[91m"; GREEN   = "\033[92m"; YELLOW = "\033[93m"
    BLUE    = "\033[94m"; MAGENTA = "\033[95m"; CYAN   = "\033[96m"
    WHITE   = "\033[97m"; GRAY    = "\033[90m"; DRED   = "\033[31m"
    DGREEN  = "\033[32m"; DCYAN   = "\033[36m"

TTY = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
def c(col, txt): return f"{col}{txt}{C.RESET}" if TTY else txt
def twidth():
    try:    return min(os.get_terminal_size().columns, 110)
    except: return 88

# ══════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════
VERSION       = "v4.0"
DEVELOPER     = "TONYPRIME"
CODENAME      = "JARVIS Edition"
API_URL       = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-sonnet-4-5"
HISTORY_FILE  = os.path.expanduser("~/.whitemadrid_history")
CONFIG_FILE   = os.path.expanduser("~/.whitemadrid_config")
LOG_FILE      = os.path.expanduser("~/.whitemadrid_session.log")

BANNER = r"""
 ██╗    ██╗██╗  ██╗██╗████████╗███████╗
 ██║    ██║██║  ██║██║╚══██╔══╝██╔════╝
 ██║ █╗ ██║███████║██║   ██║   █████╗
 ██║███╗██║██╔══██║██║   ██║   ██╔══╝
 ╚███╔███╔╝██║  ██║██║   ██║   ███████╗
  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝
 ███╗   ███╗ █████╗ ██████╗ ██████╗ ██╗██████╗
 ████╗ ████║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗
 ██╔████╔██║███████║██║  ██║██████╔╝██║██║  ██║
 ██║╚██╔╝██║██╔══██║██║  ██║██╔══██╗██║██║  ██║
 ██║ ╚═╝ ██║██║  ██║██████╔╝██║  ██║██║██████╔╝
 ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝"""

# ══════════════════════════════════════════════════════════════════════
#  JARVIS SYSTEM PROMPT  — full personality + intelligence
# ══════════════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """You are WHITE MADRID, an advanced AI cybersecurity assistant — think JARVIS from Iron Man, built for ethical hacking. You were created by TONYPRIME. You are not just a tool; you are an intelligent companion who thinks ahead, notices patterns, and guides the operator like a seasoned co-pilot.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PERSONALITY & COMMUNICATION STYLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Speak like JARVIS: confident, precise, slightly witty, always professional
- Address the operator as "sir", "boss", or by context — never robotic
- Be proactive: after answering, suggest the NEXT logical step
- Show intelligence: notice what phase of an engagement the operator is in and adapt
- Use short acknowledgment lines: "Understood.", "On it.", "Interesting approach."
- Occasionally show personality: dry humor, brief observations, hacker wisdom
- Never just dump info — narrate it like a briefing: context → action → outcome
- If something is risky or needs authorization, say so firmly but briefly — don't lecture

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTELLIGENCE MODES  (auto-detect from context)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[RECON MODE]     — Mapping targets, OSINT, enumeration. Be thorough and methodical.
[EXPLOIT MODE]   — Vulnerability analysis, payload crafting. Be precise, step-by-step.
[STEALTH MODE]   — Evasion, obfuscation, AV bypass. Think like an adversary.
[CTF MODE]       — Challenge solving. Think creatively, cover all angles.
[LEARNING MODE]  — Teaching concepts. Use analogies, explain the "why", not just "how".
[DEFENSE MODE]   — Blue team, hardening, detection. Flip perspective to defender.
[CRISIS MODE]    — Active incident, under time pressure. Be fast, prioritized, direct.

Detect the mode from what the operator says and announce it briefly if switching.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROACTIVE INTELLIGENCE  (JARVIS behavior)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- After each answer, add a "▸ NEXT STEP:" suggestion for what to do next
- If operator seems stuck, offer 2-3 alternative approaches
- Notice repeated patterns: "You've asked about privilege escalation twice — want me to run through the full Linux privesc checklist?"
- Warn proactively: "Before you run that, make sure your listener is ready on port 4444"
- Offer tool recommendations: "Given what you described, gobuster would be faster than dirb here"
- Remember context within the session and refer back to it naturally

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEEP EXPERTISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recon & OSINT:
  Nmap, Masscan, theHarvester, Shodan, Maltego, Recon-ng, FOCA, SpiderFoot, Amass, Subfinder

Web Application:
  SQLi (error/blind/time/UNION), XSS (stored/reflected/DOM), SSRF, LFI/RFI, IDOR,
  RCE, XXE, SSTI, CORS misconfig, JWT attacks, OAuth abuse, GraphQL injection,
  HTTP request smuggling, WebSocket attacks, CSRF, clickjacking, path traversal

Exploitation:
  Metasploit framework (msfconsole, msfvenom, auxiliary modules), Exploit-DB,
  searchsploit, CVE research, PoC development, buffer overflows (x86/x64),
  format string bugs, use-after-free, heap spray, ROP chains

Password & Auth:
  Hashcat (all modes: wordlist, brute, combinator, mask, hybrid),
  John the Ripper, Hydra, Medusa, CeWL, Cupp, Crunchwrap,
  credential stuffing, password spraying, rainbow tables

Privilege Escalation — Linux:
  SUID/SGID binaries, sudo misconfigs, cron job hijacking, PATH injection,
  writable /etc/passwd, kernel exploits (DirtyPipe, PwnKit, etc.),
  Docker escape, LXC/LXD abuse, capabilities, NFS no_root_squash

Privilege Escalation — Windows:
  Token impersonation, SeImpersonatePrivilege (Potato attacks),
  Unquoted service paths, weak registry ACLs, AlwaysInstallElevated,
  DLL hijacking, scheduled tasks, UAC bypass, credential dumping

Active Directory:
  BloodHound/SharpHound, Impacket (secretsdump, psexec, smbclient),
  CrackMapExec, Rubeus (Kerberoasting, AS-REP roasting, pass-the-ticket),
  Mimikatz, LDAP enumeration, ACL abuse, DCSync, Golden/Silver tickets,
  PrintNightmare, ZeroLogon, PetitPotam, ADCS ESC attacks

Network:
  Wireshark, tcpdump, tshark, Zeek/Bro, ARP spoofing, MITM (Ettercap, Bettercap),
  network pivoting (SSH tunnels, Chisel, ligolo-ng), packet crafting (Scapy, hping3)

Wireless:
  Aircrack-ng suite, Kismet, Wifite, evil twin (hostapd-wpe), WPS attacks (Reaver),
  PMKID attack, deauth attacks, WEP/WPA/WPA2/WPA3 analysis

Reverse Shells & Payloads:
  Bash, Python, PHP, Perl, Ruby, PowerShell, socat, netcat, rlwrap,
  msfvenom (all formats: exe/elf/apk/war/jar), staged vs stageless,
  shell stabilization techniques, encrypted shells (openssl)

Evasion & Stealth:
  AV bypass (AMSI patching, signature mutation, packing), OPSEC,
  living-off-the-land (LOLBins), obfuscation (PowerShell, Python),
  traffic blending, timestomping, log clearing, memory-only payloads

Forensics & CTF:
  Volatility (memory forensics), binwalk, steghide, stegsolve,
  file carving, hex analysis, Ghidra/IDA (reversing), pwntools (pwn),
  cryptography (RSA, AES, XOR, base encodings), PCAP analysis

Mobile & Android (Termux):
  APK decompilation (apktool, jadx), Frida (dynamic instrumentation),
  objection, ADB exploitation, SSL pinning bypass, Android pentest setup in Termux

Certifications:
  OSCP — methodology, report writing, 24h exam strategy
  CEH, PNPT, eJPT, CPTS, CPPT — exam tips and prep paths
  HTB, TryHackMe, PG Practice machine writeup help

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESPONSE FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Lead with a brief acknowledgment line (1 sentence max)
- Use [MODE: X] tag when switching intelligence modes
- Structure: Context → Commands → Explanation → Next Step
- Use [+] success/tip  [-] error/risk  [*] info  [!] critical warning
- All commands in triple-backtick code blocks with language tag
- End every response with:
  ▸ NEXT STEP: <specific actionable suggestion>
  OR
  ▸ WANT MORE?: <offer to go deeper on a subtopic>
- Keep it tight — no filler, no padding, no unnecessary caveats
- Note root/sudo and Termux compatibility where relevant
- Legal reminder: one brief line only if genuinely needed, never repeat it"""

# ══════════════════════════════════════════════════════════════════════
#  BOOT MESSAGES  (JARVIS-style startup lines)
# ══════════════════════════════════════════════════════════════════════
BOOT_LINES = [
    "Good evening. All systems operational.",
    "Online and ready. What are we hunting today?",
    "Initializing threat intelligence modules... done.",
    "WHITE MADRID standing by. The network awaits.",
    "Systems nominal. I've missed you, boss.",
    "All modules loaded. Let's get to work.",
    "Ready when you are. I've pre-loaded your tool catalogue.",
]

EXIT_LINES = [
    "Powering down. Stay sharp out there.",
    "Session terminated. Nice work today.",
    "Going dark. Until next time, boss.",
    "All logs secured. Stay ethical.",
    "WHITE MADRID offline. — TONYPRIME",
]

THINK_LINES = [
    "Analyzing...",
    "Processing threat data...",
    "Running intelligence modules...",
    "Cross-referencing databases...",
    "Calculating optimal approach...",
    "Scanning knowledge base...",
    "Compiling response...",
    "Running deep analysis...",
]

# ══════════════════════════════════════════════════════════════════════
#  TOOL CATALOGUE
# ══════════════════════════════════════════════════════════════════════
TOOL_CATALOGUE = {
    "nmap":        ("nmap",                 "recon",     "Network port scanner & service detection",   "nmap --version"),
    "masscan":     ("masscan",              "recon",     "High-speed internet port scanner",           "masscan --version"),
    "dnsrecon":    ("dnsrecon",             "recon",     "DNS enumeration & zone transfer testing",    "dnsrecon --help"),
    "whois":       ("whois",                "recon",     "Domain registration lookup",                 "whois --version"),
    "curl":        ("curl",                 "recon",     "HTTP request tool & web interaction",        "curl --version"),
    "wget":        ("wget",                 "recon",     "File download & web crawling",               "wget --version"),
    "amass":       ("amass",                "recon",     "Subdomain enumeration & OSINT",              "amass -version"),
    "nikto":       ("nikto",                "web",       "Web server vulnerability scanner",           "nikto -Version"),
    "sqlmap":      ("sqlmap",               "web",       "Automated SQL injection exploitation",       "sqlmap --version"),
    "gobuster":    ("gobuster",             "web",       "Fast dir/DNS/vhost brute-forcer",            "gobuster version"),
    "ffuf":        ("ffuf",                 "web",       "Fast web fuzzer — dirs, params, headers",    "ffuf -V"),
    "dirb":        ("dirb",                 "web",       "Web directory brute-forcer",                 "dirb"),
    "hydra":       ("hydra",                "password",  "Online brute-force (SSH/FTP/HTTP/etc)",      "hydra -h"),
    "john":        ("john",                 "password",  "John the Ripper — offline hash cracker",     "john --list=formats"),
    "hashcat":     ("hashcat",              "password",  "GPU-accelerated hash cracking",              "hashcat --version"),
    "crunch":      ("crunch",               "password",  "Custom wordlist generator",                  "crunch --help"),
    "netcat":      ("netcat-openbsd",       "network",   "TCP/UDP Swiss army knife",                   "nc -h"),
    "socat":       ("socat",                "network",   "Advanced relay — shells, pivoting, tunnels", "socat -V"),
    "tcpdump":     ("tcpdump",              "network",   "Packet capture & traffic analysis",          "tcpdump --version"),
    "tshark":      ("tshark",               "network",   "Wireshark CLI — deep packet inspection",     "tshark --version"),
    "hping3":      ("hping3",               "network",   "Custom TCP/IP packet crafting",              "hping3 --version"),
    "iperf3":      ("iperf3",               "network",   "Network bandwidth & throughput testing",     "iperf3 --version"),
    "traceroute":  ("traceroute",           "network",   "Network path tracing",                       "traceroute --version"),
    "metasploit":  ("metasploit",           "exploit",   "Full exploitation framework (MSF)",          "msfconsole --version"),
    "exploitdb":   ("exploitdb",            "exploit",   "Exploit-DB local copy + searchsploit",       "searchsploit --version"),
    "aircrack-ng": ("aircrack-ng",          "wireless",  "WEP/WPA wireless auditing suite",            "aircrack-ng --version"),
    "bettercap":   ("bettercap",            "wireless",  "Network attacks & MITM framework",           "bettercap -v"),
    "binwalk":     ("binwalk",              "forensics", "Firmware & binary analysis / extraction",    "binwalk --help"),
    "steghide":    ("steghide",             "forensics", "Steganography hide/extract tool",            "steghide --version"),
    "foremost":    ("foremost",             "forensics", "File carving & data recovery",               "foremost -h"),
    "exiftool":    ("libimage-exiftool-perl","forensics","Metadata reader/writer for files",           "exiftool -ver"),
    "python":      ("python",               "utility",   "Python 3 runtime",                           "python3 --version"),
    "git":         ("git",                  "utility",   "Version control — clone exploit repos",      "git --version"),
    "tmux":        ("tmux",                 "utility",   "Terminal multiplexer",                       "tmux -V"),
    "openssh":     ("openssh",              "utility",   "SSH client & server",                        "ssh -V"),
    "openssl":     ("openssl",              "utility",   "Crypto toolkit — certs, hashing, TLS",       "openssl version"),
    "chisel":      ("chisel",               "utility",   "Fast TCP/UDP tunnel over HTTP (pivoting)",   "chisel --version"),
}

CATEGORIES = {
    "recon":    ("🔍", C.CYAN,    "Reconnaissance & OSINT"),
    "web":      ("🌐", C.BLUE,    "Web Application Testing"),
    "password": ("🔑", C.YELLOW,  "Password Attacks"),
    "network":  ("📡", C.GREEN,   "Network Tools"),
    "exploit":  ("💥", C.RED,     "Exploitation Frameworks"),
    "wireless": ("📶", C.MAGENTA, "Wireless Security"),
    "forensics":("🔬", C.DCYAN,   "Forensics & Crypto"),
    "utility":  ("⚙️ ", C.GRAY,   "Utilities & Dev Tools"),
}

# ══════════════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════════════
def load_config():
    cfg = {"api_key": "", "model": DEFAULT_MODEL, "operator": "Operator", "session_count": 0}
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f: cfg.update(json.load(f))
    except: pass
    return cfg

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f: json.dump(cfg, f, indent=2)

def get_api_key(cfg):
    return cfg.get("api_key") or os.environ.get("OPENROUTER_API_KEY", "")

# ══════════════════════════════════════════════════════════════════════
#  SPINNER  (JARVIS style)
# ══════════════════════════════════════════════════════════════════════
class Spinner:
    FRAMES = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    def __init__(self, msg=""):
        self.msg   = msg
        self._stop = threading.Event()
        self._t    = threading.Thread(target=self._run, daemon=True)
    def _run(self):
        i = 0
        while not self._stop.is_set():
            f = self.FRAMES[i % len(self.FRAMES)]
            sys.stdout.write(f"\r  {c(C.CYAN,f)} {c(C.GRAY, self.msg)}   ")
            sys.stdout.flush()
            time.sleep(0.08); i += 1
    def start(self): self._t.start()
    def stop(self):
        self._stop.set(); self._t.join()
        sys.stdout.write("\r" + " "*55 + "\r")
        sys.stdout.flush()

# ══════════════════════════════════════════════════════════════════════
#  SYSTEM INFO
# ══════════════════════════════════════════════════════════════════════
def now_str():  return datetime.datetime.now().strftime("%H:%M:%S")
def date_str(): return datetime.datetime.now().strftime("%Y-%m-%d")

def sysinfo():
    info = {}
    try: info["user"] = os.environ.get("USER", os.environ.get("LOGNAME","user"))
    except: info["user"] = "user"
    try: info["host"] = os.uname().nodename
    except: info["host"] = "device"
    try:
        r = subprocess.run(["uname","-r"], capture_output=True, text=True, timeout=3)
        info["kernel"] = r.stdout.strip()[:22]
    except: info["kernel"] = "unknown"
    try:
        r = subprocess.run(["uname","-m"], capture_output=True, text=True, timeout=3)
        info["arch"] = r.stdout.strip()
    except: info["arch"] = ""
    info["termux"] = is_termux()
    return info

def is_termux():
    return "com.termux" in os.environ.get("PREFIX","") or os.path.exists("/data/data/com.termux")

def detect_pkg_manager():
    if is_termux():            return "pkg"
    if shutil.which("apt"):    return "apt"
    if shutil.which("pacman"): return "pacman"
    if shutil.which("dnf"):    return "dnf"
    return None

# ══════════════════════════════════════════════════════════════════════
#  BOOT SEQUENCE  (JARVIS style)
# ══════════════════════════════════════════════════════════════════════
def clr(): os.system("clear" if os.name != "nt" else "cls")

def boot_sequence(cfg):
    clr()
    si = sysinfo()
    w  = twidth()

    # Banner
    print(c(C.WHITE + C.BOLD, BANNER))
    print()

    # Animated boot lines
    boot_items = [
        ("Initializing AI core",        C.CYAN),
        ("Loading exploit database",     C.CYAN),
        ("Mounting tool catalogue",      C.CYAN),
        ("Establishing API link",        C.CYAN),
        ("Calibrating threat modules",   C.CYAN),
        ("All systems operational",      C.GREEN),
    ]
    for label, col in boot_items:
        dots = "." * random.randint(2, 5)
        sys.stdout.write(f"  {c(C.GRAY,'[')}  {c(col, label)}{c(C.GRAY, dots)}  {c(C.GREEN,'OK')}{c(C.GRAY,']')}\n")
        sys.stdout.flush()
        time.sleep(0.08)

    print()
    # Status bar
    platform = c(C.YELLOW, "Termux/Android") if si["termux"] else c(C.YELLOW, si.get("host","?"))
    print(c(C.GRAY, "  " + "═"*(w-4)))
    print(
        f"  {c(C.MAGENTA+C.BOLD,'WHITE MADRID')} {c(C.GRAY, VERSION)} {c(C.GRAY,'·')} "
        f"{c(C.GRAY, CODENAME)}  "
        f"{c(C.GRAY,'·')} {c(C.GRAY, 'DEV:')} {c(C.CYAN+C.BOLD, DEVELOPER)}"
    )
    print(
        f"  {c(C.GRAY,'HOST:')} {platform}  "
        f"{c(C.GRAY,'KERNEL:')} {c(C.GRAY, si.get('kernel','?'))}  "
        f"{c(C.GRAY,'ARCH:')} {c(C.GRAY, si.get('arch','?'))}  "
        f"{c(C.GRAY,'TIME:')} {c(C.GRAY, date_str())} {c(C.GRAY, now_str())}"
    )
    print(c(C.GRAY, "  " + "═"*(w-4)))
    print()

    # JARVIS greeting
    sessions = cfg.get("session_count", 0)
    if sessions == 0:
        greeting = f"  {c(C.CYAN+C.BOLD,'[WM]')} First boot detected. Welcome, {c(C.WHITE+C.BOLD, cfg.get('operator','Operator'))}. I am WHITE MADRID."
    else:
        greeting = f"  {c(C.CYAN+C.BOLD,'[WM]')} {random.choice(BOOT_LINES)} Session #{sessions+1}."
    print(greeting)
    print(f"  {c(C.GRAY,'[WM]')} {c(C.GRAY, 'Type your query naturally, or use a command. Try: ')}'{c(C.GREEN, 'help')}'")
    print(f"  {c(C.YELLOW,'[WM]')} {c(C.YELLOW, 'Authorized security research only. Ensure you have written scope.')}")
    print()

    cfg["session_count"] = sessions + 1
    save_config(cfg)

# ══════════════════════════════════════════════════════════════════════
#  DISPLAY HELPERS
# ══════════════════════════════════════════════════════════════════════
def print_help():
    w = twidth()
    B = C.CYAN + C.BOLD
    print()
    print(c(B, "  ╔" + "═"*(w-4) + "╗"))
    title = "WHITE MADRID v4.0 — Command Reference"
    print(c(B,"  ║") + c(C.WHITE+C.BOLD, title.center(w-4)) + c(B,"║"))
    print(c(B, "  ╠" + "═"*(w-4) + "╣"))

    sections = [
        ("AI & CONVERSATION", [
            ("ask anything",       "Just type naturally — WHITE MADRID responds like JARVIS"),
            ("mode <name>",        "Switch AI mode: recon/exploit/stealth/ctf/learn/defend/crisis"),
            ("recap",              "Summarize what we've covered this session"),
            ("suggest",            "Get proactive next-step suggestions from the AI"),
            ("explain <topic>",    "Deep-dive explanation of any security concept"),
        ]),
        ("TERMINAL COMMANDS", [
            ("help",               "Show this reference"),
            ("clear",              "Clear screen & redraw banner"),
            ("about",              "Developer & system info"),
            ("history",            "Show session query log"),
            ("log",                "Save session to file"),
            ("topics",             "Example queries by category"),
            ("model",              "View / switch AI model"),
            ("setkey",             "Update OpenRouter API key"),
            ("operator <name>",    "Set your operator name"),
            ("exit / q",           "Quit WHITE MADRID"),
        ]),
        ("TOOL MANAGER", [
            ("tools",              "List all 35+ pentest tools with install status"),
            ("install",            "Interactive installer — by category or individual"),
            ("install <name>",     "Install a specific tool directly"),
            ("check",              "Scan & show tool coverage with progress bar"),
        ]),
        ("NETWORK TESTING  ⚠ auth required", [
            ("stress",             "Network resilience testing tools & commands"),
        ]),
        ("SHELL", [
            ("!<cmd>",             "Run shell command directly  e.g. !nmap -sV 10.0.0.1"),
            ("!cd <path>",         "Change working directory"),
        ]),
    ]

    for section, cmds in sections:
        pad = w - 4 - len(section) - 2
        print(c(B,"  ║"))
        print(c(B,"  ║") + c(C.YELLOW+C.BOLD, f"  {section}") + " "*max(0,pad) + c(B,"║"))
        for cmd, desc in cmds:
            rpad = max(0, w - 6 - len(cmd) - len(desc) - 5)
            print(c(B,"  ║") + f"    {c(C.GREEN+C.BOLD, cmd):<30} {c(C.GRAY, desc)}" + " "*rpad + c(B,"║"))

    print(c(B,"  ║"))
    print(c(B, "  ╚" + "═"*(w-4) + "╝"))
    print()

def print_about(cfg):
    w = min(twidth(), 68)
    B = C.MAGENTA
    si = sysinfo()
    print()
    print(c(B,"  ╔" + "═"*(w-4) + "╗"))
    print(c(B,"  ║") + c(C.WHITE+C.BOLD,"  WHITE MADRID — System Information".center(w-4)) + c(B,"║"))
    print(c(B,"  ╠" + "═"*(w-4) + "╣"))
    rows = [
        ("AI Name",     "WHITE MADRID",              C.CYAN),
        ("Version",     f"{VERSION} — {CODENAME}",   C.GREEN),
        ("Developer",   DEVELOPER,                   C.CYAN),
        ("API",         "OpenRouter",                C.YELLOW),
        ("Model",       cfg.get("model", DEFAULT_MODEL)[:36], C.YELLOW),
        ("Operator",    cfg.get("operator","Unknown"), C.WHITE),
        ("Sessions",    str(cfg.get("session_count","?")), C.GRAY),
        ("Platform",    "Termux/Android" if si["termux"] else "Linux/macOS", C.GRAY),
        ("Host",        si.get("host","?"),           C.GRAY),
        ("Kernel",      si.get("kernel","?"),         C.GRAY),
        ("Date",        date_str(),                   C.GRAY),
        ("Codename",    "JARVIS Edition",             C.MAGENTA),
    ]
    for label, val, vc in rows:
        ll = len(label) + len(val) + 8
        pad = max(0, w - 4 - ll)
        print(c(B,"  ║") + f"  {c(C.GRAY+C.BOLD, label+':')}  {c(vc, val)}" + " "*pad + c(B,"║"))
    print(c(B,"  ╚" + "═"*(w-4) + "╝"))
    print()

def print_topics():
    cats = [
        ("🔍 Recon", C.CYAN, [
            "Scan 192.168.1.0/24 with nmap, find all open ports and services",
            "Enumerate subdomains of target.com using amass and theHarvester",
            "Run a DNS zone transfer attack against a domain",
            "Use Shodan to find exposed services on my target IP",
        ]),
        ("🌐 Web", C.BLUE, [
            "Test a login form for SQL injection with sqlmap, bypass WAF",
            "Perform directory brute-forcing with gobuster on port 8080",
            "Explain how to find and exploit an SSRF vulnerability",
            "How do I test for JWT algorithm confusion attacks?",
        ]),
        ("💥 Exploit", C.RED, [
            "Set up a Metasploit reverse shell handler for a Windows target",
            "Generate a msfvenom payload for Android APK",
            "How do I exploit EternalBlue (MS17-010) manually?",
            "Create a Python reverse shell with encryption",
        ]),
        ("🔑 Passwords", C.YELLOW, [
            "Crack this hash: 5f4dcc3b5aa765d61d8327deb882cf99",
            "Perform password spraying against an RDP service with Hydra",
            "Generate a targeted wordlist from a company website using CeWL",
            "Kerberoasting — explain the attack and how to perform it",
        ]),
        ("⬆ PrivEsc", C.GREEN, [
            "Give me a full Linux privilege escalation checklist",
            "Find all SUID binaries on this box and exploit one",
            "Windows token impersonation with PrintSpoofer or GodPotato",
            "How do I abuse a writable /etc/crontab for root?",
        ]),
        ("🏁 CTF", C.MAGENTA, [
            "I found a jpg file in a CTF, how do I check for steganography?",
            "Decode this cipher and identify the type: WkdWemRHNXZaRzVo",
            "I have a .pcap file, walk me through analyzing it for credentials",
            "RSA CTF challenge — n, e, c given. How do I decrypt?",
        ]),
        ("🛡 Defense", C.DCYAN, [
            "How do I detect Mimikatz usage on a Windows system?",
            "Set up fail2ban on Termux/Linux to block SSH brute-force",
            "What logs should I monitor to detect lateral movement?",
            "Harden my SSH config against brute-force and key attacks",
        ]),
    ]
    print()
    print(c(C.CYAN+C.BOLD, "  [WM] Example queries — just type these directly:\n"))
    for cat, col, items in cats:
        print(c(col+C.BOLD, f"  {cat}"))
        for item in items:
            print(f"    {c(C.GRAY,'›')} {item}")
        print()

def print_models():
    models = [
        ("anthropic/claude-sonnet-4-5",       "Claude Sonnet 4.5",    "Best overall — recommended"),
        ("anthropic/claude-haiku-4-5",         "Claude Haiku 4.5",     "Fast & cheap"),
        ("openai/gpt-4o",                      "GPT-4o",               "Strong reasoning"),
        ("openai/gpt-4o-mini",                 "GPT-4o Mini",          "Very fast"),
        ("google/gemini-pro-1.5",              "Gemini Pro 1.5",       "Long context"),
        ("meta-llama/llama-3.1-70b-instruct",  "Llama 3.1 70B",        "Open source"),
        ("mistralai/mistral-7b-instruct",      "Mistral 7B",           "Lightweight"),
        ("deepseek/deepseek-coder",            "DeepSeek Coder",       "Code-focused"),
        ("nousresearch/hermes-3-llama-3.1-70b","Hermes 3 70B",         "Instruction tuned"),
    ]
    print()
    print(c(C.CYAN+C.BOLD, "  [WM] Available OpenRouter models:\n"))
    for mid, name, note in models:
        print(f"  {c(C.GREEN+C.BOLD, mid):<58} {c(C.GRAY, note)}")
    print()

# ══════════════════════════════════════════════════════════════════════
#  TOOL MANAGER
# ══════════════════════════════════════════════════════════════════════
def tool_installed(vcmd):
    try:
        r = subprocess.run(vcmd.split(), capture_output=True, timeout=5)
        return r.returncode in (0, 1)
    except: return False

def install_tool(tool_key):
    if tool_key not in TOOL_CATALOGUE:
        print(c(C.RED, f"\n  [WM] I don't have '{tool_key}' in my catalogue. Try 'tools' to see all options."))
        return False
    pkg_name, cat, desc, verify = TOOL_CATALOGUE[tool_key]
    pm = detect_pkg_manager()
    if not pm:
        print(c(C.RED, "\n  [WM] No supported package manager detected."))
        return False

    print(c(C.CYAN, f"\n  [WM] Installing {c(C.WHITE+C.BOLD, tool_key)} — {desc}"))

    cmds = {
        "pkg":    f"pkg install -y {pkg_name}",
        "apt":    f"sudo apt install -y {pkg_name}",
        "pacman": f"sudo pacman -S --noconfirm {pkg_name}",
        "dnf":    f"sudo dnf install -y {pkg_name}",
    }
    cmd = cmds.get(pm, f"sudo apt install -y {pkg_name}")

    # Special handling
    specials = {
        ("metasploit", "pkg"):  "pkg install unstable-repo -y && pkg install metasploit -y",
        ("gobuster",   "pkg"):  "pkg install golang -y && go install github.com/OJ/gobuster/v3@latest",
        ("ffuf",       "pkg"):  "pkg install golang -y && go install github.com/ffuf/ffuf/v2@latest",
        ("chisel",     "pkg"):  "pkg install golang -y && go install github.com/jpillora/chisel@latest",
        ("amass",      "pkg"):  "pkg install golang -y && go install github.com/owasp-amass/amass/v4/...@latest",
        ("bettercap",  "pkg"):  "pkg install bettercap -y",
    }
    cmd = specials.get((tool_key, pm), cmd)
    if tool_key == "sqlmap":
        cmd = f"pip install sqlmap --break-system-packages 2>/dev/null || {cmd}"

    ret = os.system(cmd)
    if ret == 0:
        print(c(C.GREEN, f"  [WM] {tool_key} installed successfully. Good to go."))
        return True
    else:
        print(c(C.RED,  f"  [WM] Install returned exit code {ret}. Manual command:"))
        print(c(C.GRAY, f"       {cmd}"))
        return False

def print_tool_list():
    w = twidth()
    print()
    print(c(C.CYAN+C.BOLD, f"  {'TOOL':<18} {'STATUS':<14} DESCRIPTION"))
    print(c(C.GRAY, "  " + "─"*(w-4)))
    for cat_id, (icon, col, cat_name) in CATEGORIES.items():
        shown = False
        for key, (pkg, cat, desc, vcmd) in TOOL_CATALOGUE.items():
            if cat != cat_id: continue
            if not shown:
                print(c(col+C.BOLD, f"\n  {icon} {cat_name}"))
                shown = True
            ok = tool_installed(vcmd)
            st = c(C.GREEN, "✔ installed") if ok else c(C.GRAY, "· available")
            print(f"  {c(C.WHITE+C.BOLD, key):<26}{st:<22}{c(C.GRAY, desc)}")
    print()
    print(c(C.GRAY, "  'install <name>' or 'install' for interactive menu"))
    print()

def check_tools():
    print(f"\n  {c(C.CYAN+C.BOLD,'[WM]')} Scanning tool inventory...\n")
    ok_list, miss_list = [], []
    for key, (pkg, cat, desc, vcmd) in TOOL_CATALOGUE.items():
        if tool_installed(vcmd): ok_list.append(key)
        else: miss_list.append(key)
    n = len(TOOL_CATALOGUE)
    pct = int(len(ok_list)/n*100)

    print(c(C.GREEN,  f"  [+] Installed ({len(ok_list)}/{n}):"))
    line = "  "
    for t in ok_list:
        if len(line) + len(t) > twidth() - 4:
            print(c(C.GREEN, line)); line = "  "
        line += c(C.GREEN, t) + "  "
    if line.strip(): print(c(C.GREEN, line))

    print(c(C.GRAY, f"\n  [-] Missing ({len(miss_list)}):"))
    line = "  "
    for t in miss_list:
        if len(line) + len(t) > twidth() - 4:
            print(c(C.GRAY, line)); line = "  "
        line += c(C.GRAY, t) + "  "
    if line.strip(): print(c(C.GRAY, line))

    blen  = min(50, twidth()-20)
    filled = int(blen * pct / 100)
    bar    = c(C.GREEN,"█"*filled) + c(C.GRAY,"░"*(blen-filled))
    col    = C.GREEN if pct>=80 else C.YELLOW if pct>=40 else C.RED
    print(f"\n  {c(C.GRAY,'Coverage')} [{bar}] {c(col+C.BOLD, str(pct)+'%')}")
    if pct < 100:
        print(c(C.GRAY, f"\n  [WM] Run 'install' to bring your arsenal up to speed."))
    else:
        print(c(C.GREEN, f"\n  [WM] Full arsenal loaded. You're ready for anything."))
    print()

def interactive_installer():
    print()
    print(c(C.CYAN+C.BOLD, "  ╔══════════════════════════════════════════════╗"))
    print(c(C.CYAN+C.BOLD, "  ║      WHITE MADRID — Arsenal Installer       ║"))
    print(c(C.CYAN+C.BOLD, "  ╚══════════════════════════════════════════════╝\n"))
    options = [
        ("1", "Full arsenal — install everything",         list(TOOL_CATALOGUE.keys())),
        ("2", "Recon & OSINT suite",                       [k for k,v in TOOL_CATALOGUE.items() if v[1]=="recon"]),
        ("3", "Web application testing suite",             [k for k,v in TOOL_CATALOGUE.items() if v[1]=="web"]),
        ("4", "Password attack suite",                     [k for k,v in TOOL_CATALOGUE.items() if v[1]=="password"]),
        ("5", "Network tools suite",                       [k for k,v in TOOL_CATALOGUE.items() if v[1]=="network"]),
        ("6", "Exploitation frameworks",                   [k for k,v in TOOL_CATALOGUE.items() if v[1]=="exploit"]),
        ("7", "Forensics & crypto tools",                  [k for k,v in TOOL_CATALOGUE.items() if v[1]=="forensics"]),
        ("8", "Utilities & dev tools",                     [k for k,v in TOOL_CATALOGUE.items() if v[1]=="utility"]),
        ("9", "Choose individual tool",                    []),
        ("0", "Cancel",                                    []),
    ]
    for num, label, tools in options:
        col = C.RED if num=="1" else C.GRAY if num=="0" else C.CYAN
        count = f" ({len(tools)} tools)" if tools else ""
        print(f"  {c(col+C.BOLD,'['+num+']')} {label}{c(C.GRAY, count)}")
    print()
    try:    choice = input(c(C.WHITE+C.BOLD, "  [WM] Select: ")).strip()
    except: print(); return

    targets = []
    for num, label, tools in options:
        if choice == num:
            if num == "0": return
            if num == "9":
                print()
                try:    t = input(c(C.WHITE, "  Tool name: ")).strip().lower()
                except: print(); return
                if t in TOOL_CATALOGUE: targets = [t]
                else:
                    print(c(C.RED, f"  [WM] '{t}' not found. Use 'tools' to browse the catalogue."))
                    return
            else: targets = tools
            break

    if not targets:
        print(c(C.YELLOW, "\n  [WM] Nothing selected.\n")); return

    print(c(C.YELLOW, f"\n  [WM] Queued {len(targets)} tool(s): {', '.join(targets)}"))
    try:    confirm = input(c(C.WHITE, "  Confirm install? [y/N]: ")).strip().lower()
    except: print(); return
    if confirm != "y":
        print(c(C.GRAY, "  [WM] Aborted.\n")); return

    ok, fail = 0, 0
    for tool in targets:
        if install_tool(tool): ok += 1
        else: fail += 1

    print(f"\n  {c(C.CYAN+C.BOLD,'[WM] Install complete.')}")
    print(f"  {c(C.GREEN,'[+]')} Success: {ok}   {c(C.RED,'[-]')} Failed: {fail}\n")

def print_stress_tools():
    tools = [
        ("hping3",  "TCP/UDP/ICMP packet crafting",
         "hping3 -S -p 80 --flood <target>   # SYN flood test\nhping3 -A -p 80 <target>            # ACK probe"),
        ("iperf3",  "Bandwidth / throughput test",
         "iperf3 -s                           # server mode\niperf3 -c <target> -t 30 -P 4       # 30s, 4 threads"),
        ("ab",      "HTTP request rate benchmark",
         "ab -n 10000 -c 100 http://<target>/"),
        ("wrk",     "Modern HTTP load testing",
         "wrk -t4 -c200 -d30s http://<target>/"),
        ("siege",   "Multi-user HTTP simulation",
         "siege -c50 -t60S --log=/tmp/siege.log http://<target>/"),
        ("netperf", "TCP/UDP performance measurement",
         "netperf -H <target> -t TCP_STREAM -l 30"),
    ]
    print()
    print(c(C.RED+C.BOLD, "  ╔══════════════════════════════════════════════════════╗"))
    print(c(C.RED+C.BOLD, "  ║   ⚠  AUTHORIZED NETWORK STRESS TESTING ONLY  ⚠     ║"))
    print(c(C.RED+C.BOLD, "  ║   Written scope required. Own infrastructure only.   ║"))
    print(c(C.RED+C.BOLD, "  ╚══════════════════════════════════════════════════════╝\n"))
    for i, (name, desc, cmds) in enumerate(tools, 1):
        print(c(C.YELLOW+C.BOLD, f"  [{i}] {name}") + c(C.GRAY, f"  —  {desc}"))
        for line in cmds.strip().split("\n"):
            if "#" in line:
                code, comment = line.split("#", 1)
                print(c(C.CYAN, f"       $ {code.strip()}") + c(C.GRAY, f"  # {comment.strip()}"))
            else:
                print(c(C.CYAN, f"       $ {line}"))
        print()
    print(c(C.GRAY, "  Ask WHITE MADRID for tuning, timing, and evasion advice.\n"))

# ══════════════════════════════════════════════════════════════════════
#  RESPONSE FORMATTER
# ══════════════════════════════════════════════════════════════════════
def format_response(text, operator="Operator"):
    w = twidth()
    lines = text.split("\n")
    in_code = False
    code_buf = []
    lang = "shell"
    out = []

    for line in lines:
        # Code block
        if line.startswith("```"):
            if not in_code:
                in_code = True
                lang = line[3:].strip() or "shell"
                code_buf = []
            else:
                hdr = f"  ┌─[{c(C.YELLOW,lang)}]" + c(C.GRAY,"─"*max(0, w-10-len(lang)))
                ftr = c(C.GRAY, "  └" + "─"*(w-5))
                out.append(hdr)
                for cl in code_buf:
                    # highlight $ prompt lines
                    if cl.startswith("$") or cl.startswith("#"):
                        out.append(c(C.GRAY,"  │ ") + c(C.GREEN, cl))
                    else:
                        out.append(c(C.GRAY,"  │ ") + c(C.WHITE, cl))
                out.append(ftr)
                in_code = False; code_buf = []
            continue

        if in_code:
            code_buf.append(line); continue

        s = line.strip()
        if not s: out.append(""); continue

        # Prefix tags
        if s.startswith("[+]"):
            out.append(f"  {c(C.GREEN+C.BOLD,'[+]')}{c(C.GREEN, s[3:])}")
        elif s.startswith("[-]"):
            out.append(f"  {c(C.RED+C.BOLD,'[-]')}{c(C.RED, s[3:])}")
        elif s.startswith("[!]"):
            out.append(f"  {c(C.YELLOW+C.BOLD,'[!]')}{c(C.YELLOW, s[3:])}")
        elif s.startswith("[*]"):
            out.append(f"  {c(C.BLUE+C.BOLD,'[*]')}{c(C.BLUE, s[3:])}")

        # JARVIS next-step callout
        elif s.startswith("▸ NEXT STEP:") or s.startswith("▸ WANT MORE?"):
            key, _, rest = s.partition(":")
            out.append(f"\n  {c(C.MAGENTA+C.BOLD, key+':')} {c(C.WHITE, rest.strip())}")

        # Mode tag
        elif re.match(r'^\[MODE:', s):
            out.append(f"\n  {c(C.CYAN+C.BOLD, s)}")

        # Headings
        elif re.match(r'^#{1,3} ', s):
            h = re.sub(r'^#{1,3} ', '', s)
            sep = c(C.CYAN, "━"*(w-4))
            out.append(f"\n  {sep}")
            out.append(f"  {c(C.WHITE+C.BOLD, '▶ '+h)}")
            out.append(f"  {sep}")

        # Bullet points
        elif s.startswith(("- ","* ","• ")):
            out.append(f"    {c(C.CYAN,'›')} {s[2:]}")

        # Numbered lists
        elif re.match(r'^\d+\.', s):
            num, _, rest = s.partition(".")
            out.append(f"    {c(C.YELLOW+C.BOLD, num+'.')} {rest.strip()}")

        # Normal text
        else:
            wrapped = textwrap.fill(line, width=w-4, initial_indent="  ", subsequent_indent="  ")
            wrapped = re.sub(r'`([^`]+)`', lambda m: c(C.YELLOW, m.group(1)), wrapped)
            # Bold **text**
            wrapped = re.sub(r'\*\*([^*]+)\*\*', lambda m: c(C.WHITE+C.BOLD, m.group(1)), wrapped)
            out.append(wrapped)

    return "\n".join(out)

# ══════════════════════════════════════════════════════════════════════
#  API
# ══════════════════════════════════════════════════════════════════════
def query_ai(prompt, api_key, model, history, cfg):
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer":  "https://github.com/tonyprime/whitemadrid",
        "X-Title":       "WHITE MADRID by TONYPRIME",
    }
    # Inject operator context into system
    operator = cfg.get("operator", "Operator")
    sys_msg  = SYSTEM_PROMPT + f"\n\nCurrent operator: {operator}. Address them naturally."

    messages = [{"role": "system", "content": sys_msg}]
    messages += history[-20:]
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({"model": model, "max_tokens": 2000, "messages": messages,
                          "temperature": 0.7}).encode()
    req = urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read().decode())
            return data["choices"][0]["message"]["content"], None
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body).get("error", {})
            return "", err.get("message", body) if isinstance(err, dict) else str(err)
        except: return "", body
    except urllib.error.URLError as e:
        return "", f"Network error: {e.reason}"
    except Exception as e:
        return "", str(e)

# ══════════════════════════════════════════════════════════════════════
#  SESSION LOG
# ══════════════════════════════════════════════════════════════════════
def save_session_log(session):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"\n\n{'='*60}\n")
            f.write(f"WHITE MADRID Session — {date_str()} {now_str()}\n")
            f.write(f"{'='*60}\n")
            for role, text in session:
                f.write(f"\n[{role.upper()}]\n{text}\n")
        print(c(C.GREEN, f"  [WM] Session saved to {LOG_FILE}"))
    except Exception as e:
        print(c(C.RED, f"  [WM] Could not save log: {e}"))

# ══════════════════════════════════════════════════════════════════════
#  READLINE
# ══════════════════════════════════════════════════════════════════════
def setup_readline():
    try: readline.read_history_file(HISTORY_FILE)
    except FileNotFoundError: pass
    readline.set_history_length(2000)

def save_readline():
    try: readline.write_history_file(HISTORY_FILE)
    except: pass

# ══════════════════════════════════════════════════════════════════════
#  PROMPT
# ══════════════════════════════════════════════════════════════════════
def build_prompt(cfg, mode=""):
    t = now_str()
    op = cfg.get("operator","OP")[:10]
    mode_tag = f"─[{c(C.YELLOW, mode)}]" if mode else ""
    return (
        c(C.GRAY, "\n  ╭─[") + c(C.WHITE+C.BOLD,"WM") + c(C.GRAY,"]─[") +
        c(C.CYAN, op) + c(C.GRAY, "]") + mode_tag +
        c(C.GRAY, "─[") + c(C.GRAY, t) + c(C.GRAY, "]\n  ╰─") +
        c(C.GREEN+C.BOLD, "▶ ")
    ) if TTY else "\n[WM]> "

# ══════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════
def main():
    cfg     = load_config()
    api_key = get_api_key(cfg)
    model   = cfg.get("model", DEFAULT_MODEL)

    boot_sequence(cfg)

    if not api_key:
        print(c(C.YELLOW, "  [WM] I need your OpenRouter API key to come online."))
        print(c(C.GRAY,   "       Get one free at: https://openrouter.ai/keys\n"))
        try:    key = input(c(C.GREEN+C.BOLD, "  ▶ API key: ")).strip()
        except: print(); sys.exit(0)
        if not key:
            print(c(C.RED, "  [WM] No key provided. Shutting down.")); sys.exit(1)
        cfg["api_key"] = key; save_config(cfg); api_key = key
        print(c(C.GREEN, "  [WM] Key secured. Coming online...\n"))
        time.sleep(0.5)

    print(c(C.GREEN, f"  [WM] Connected  ·  Model: {c(C.CYAN, model)}"))
    print(c(C.BLUE,  "  [WM] Ask me anything. Commands: help · tools · install · check"))
    print()

    setup_readline()
    ai_history = []   # for API
    session    = []   # for log (role, text) pairs
    full_log   = []   # (query, response) for recap
    mode       = ""   # current intelligence mode
    cwd        = os.getcwd()

    while True:
        try:
            raw = input(build_prompt(cfg, mode)).strip()
        except KeyboardInterrupt:
            print(c(C.GRAY, "\n  [WM] ^C — say 'exit' to shut down.")); continue
        except EOFError:
            print(c(C.GRAY, "\n  [WM] " + random.choice(EXIT_LINES))); break

        if not raw: continue
        cmd = raw.lower().strip()

        # ── Shell passthrough ─────────────────────────────
        if raw.startswith("!"):
            shell_cmd = raw[1:].strip()
            if shell_cmd.startswith("cd "):
                try:
                    newdir = shell_cmd[3:].strip()
                    os.chdir(os.path.expanduser(newdir))
                    cwd = os.getcwd()
                    print(c(C.GREEN, f"  [WM] Now in {cwd}"))
                except Exception as e:
                    print(c(C.RED, f"  [WM] {e}"))
            else:
                os.system(shell_cmd)
            continue

        # ── Built-in commands ─────────────────────────────
        if cmd in ("exit","quit","q","bye","shutdown"):
            print(c(C.GREEN+C.BOLD, f"\n  [WM] {random.choice(EXIT_LINES)} — {DEVELOPER}\n"))
            save_readline(); break

        elif cmd == "clear":
            clr(); boot_sequence(cfg); continue

        elif cmd == "help":           print_help(); continue
        elif cmd == "about":          print_about(cfg); continue
        elif cmd == "topics":         print_topics(); continue
        elif cmd == "stress":         print_stress_tools(); continue
        elif cmd == "tools":          print_tool_list(); continue
        elif cmd == "check":          check_tools(); continue
        elif cmd == "install":        interactive_installer(); continue
        elif cmd.startswith("install "):
            install_tool(cmd.split("install ",1)[1].strip()); continue

        elif cmd.startswith("operator "):
            name = raw.split("operator ",1)[1].strip()
            cfg["operator"] = name; save_config(cfg)
            print(c(C.GREEN, f"  [WM] Operator name set to '{name}'.")); continue

        elif cmd.startswith("mode "):
            mode = cmd.split("mode ",1)[1].strip().upper()
            print(c(C.CYAN, f"  [WM] Switching to [{mode} MODE].")); continue

        elif cmd == "model":
            print_models()
            try:    nm = input(c(C.WHITE, f"  Current [{model}]  New model (Enter=keep): ")).strip()
            except: print(); continue
            if nm: model = nm; cfg["model"] = nm; save_config(cfg)
            print(c(C.GREEN, f"  [WM] Model → {model}\n")); continue

        elif cmd == "setkey":
            try:    k = input(c(C.WHITE, "  New API key: ")).strip()
            except: print(); continue
            if k:
                cfg["api_key"] = k; save_config(cfg); api_key = k
                print(c(C.GREEN, "  [WM] Key updated and saved.")); continue
            continue

        elif cmd == "history":
            if not session:
                print(c(C.GRAY, "\n  [WM] No queries logged yet this session.\n"))
            else:
                print(c(C.CYAN, f"\n  [WM] Session log ({len(full_log)} queries):\n"))
                for i, (q, _) in enumerate(full_log, 1):
                    print(f"  {c(C.GRAY, str(i).rjust(3)+'.')} {q}")
                print()
            continue

        elif cmd == "log":
            save_session_log(session); continue

        elif cmd == "recap":
            if not full_log:
                print(c(C.GRAY, "\n  [WM] Nothing to recap yet.\n")); continue
            topics = "\n".join(f"- {q}" for q, _ in full_log[-10:])
            raw = f"Give me a quick briefing recap of what we've covered so far in this session. Topics: {topics}"

        elif cmd == "suggest":
            if full_log:
                last_q = full_log[-1][0]
                raw = f"Based on our last topic '{last_q}', proactively suggest the 3 best next steps I should take in this engagement."
            else:
                raw = "I'm starting a new penetration test engagement. As WHITE MADRID, proactively suggest an optimal workflow and what I should do first."

        elif cmd.startswith("explain "):
            topic = raw.split("explain ",1)[1].strip()
            raw = f"Give me a thorough but tight explanation of '{topic}' — cover what it is, why it matters in pentesting, how it works technically, and a practical example with commands."

        # ── AI Query ──────────────────────────────────────
        think_msg = random.choice(THINK_LINES)
        sp = Spinner(think_msg)
        sp.start()
        response, error = query_ai(raw, api_key, model, ai_history, cfg)
        sp.stop()

        if error:
            print(c(C.RED, f"\n  [WM] API Error: {error}"))
            if "401" in str(error) or "auth" in str(error).lower():
                print(c(C.YELLOW, "  [WM] Check your API key with 'setkey'"))
            print()
            continue

        # Update history
        ai_history.append({"role":"user",      "content": raw})
        ai_history.append({"role":"assistant", "content": response})
        if len(ai_history) > 30: ai_history = ai_history[-30:]

        session.append(("user",      raw))
        session.append(("assistant", response))
        full_log.append((raw, response))

        # Detect mode changes in response
        mode_match = re.search(r'\[MODE:\s*([A-Z]+)', response)
        if mode_match: mode = mode_match.group(1)

        # Render
        w = twidth()
        print()
        print(c(C.GRAY, "  " + "━"*(w-4)))
        print(format_response(response, cfg.get("operator","Operator")))
        print(c(C.GRAY, "  " + "━"*(w-4)))
        print()

    save_readline()

if __name__ == "__main__":
    main()
