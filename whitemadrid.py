#!/usr/bin/env python3
"""
WHITE MADRID — Ethical Hacking AI Terminal
Developer : TONYPRIME
Version   : v5.0 — JARVIS Edition
Platform  : Termux / Linux / macOS
API       : Multi-Provider (OpenRouter, Groq, Gemini, Anthropic, OpenAI, Together, Mistral, Cohere)
"""

import os, sys, json, time, datetime, subprocess
import urllib.request, urllib.error
import readline, textwrap, re, shutil, threading, random

# ══════════════════════════════════════════════════════
#  COLORS
# ══════════════════════════════════════════════════════
class C:
    RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
    RED="\033[91m";  GREEN="\033[92m"; YELLOW="\033[93m"
    BLUE="\033[94m"; MAGENTA="\033[95m"; CYAN="\033[96m"
    WHITE="\033[97m"; GRAY="\033[90m"
    DGREEN="\033[32m"; DCYAN="\033[36m"

TTY = hasattr(sys.stdout,"isatty") and sys.stdout.isatty()
def c(col,txt): return f"{col}{txt}{C.RESET}" if TTY else txt
def twidth():
    try:    return min(os.get_terminal_size().columns, 110)
    except: return 88

# ══════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════
VERSION      = "v5.0"
DEVELOPER    = "TONYPRIME"
CODENAME     = "JARVIS Edition"
HISTORY_FILE = os.path.expanduser("~/.whitemadrid_history")
CONFIG_FILE  = os.path.expanduser("~/.whitemadrid_config")
LOG_FILE     = os.path.expanduser("~/.whitemadrid_session.log")

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
        "name":     "OpenRouter",
        "url":      "https://openrouter.ai/api/v1/chat/completions",
        "auth":     "bearer",
        "format":   "openai",
        "key_url":  "https://openrouter.ai/keys",
        "notes":    "One key for 100+ models. Best all-round choice.",
        "free": [
            ("meta-llama/llama-3.1-8b-instruct:free",   "Llama 3.1 8B    — fast general purpose [FREE]"),
            ("meta-llama/llama-3.3-70b-instruct:free",  "Llama 3.3 70B   — large model         [FREE]"),
            ("meta-llama/llama-3.2-3b-instruct:free",   "Llama 3.2 3B    — ultra lightweight   [FREE]"),
            ("mistralai/mistral-7b-instruct:free",       "Mistral 7B       — strong reasoning   [FREE]"),
            ("google/gemma-2-9b-it:free",                "Gemma 2 9B       — Google open model  [FREE]"),
            ("qwen/qwen-2-7b-instruct:free",             "Qwen 2 7B        — strong coder       [FREE]"),
            ("microsoft/phi-3-mini-128k-instruct:free",  "Phi-3 Mini 128k  — long context       [FREE]"),
            ("nousresearch/hermes-3-llama-3.1-405b:free","Hermes 3 405B    — huge model         [FREE]"),
            ("openchat/openchat-7b:free",                "OpenChat 7B      — conversational     [FREE]"),
            ("huggingfaceh4/zephyr-7b-beta:free",        "Zephyr 7B Beta   — instruction tuned  [FREE]"),
        ],
        "paid": [
            ("anthropic/claude-sonnet-4-5",              "$3/$15 per 1M    — best overall"),
            ("anthropic/claude-haiku-4-5",               "$0.25/$1.25 /1M  — fast & cheap"),
            ("openai/gpt-4o",                            "$5/$15 per 1M    — strong reasoning"),
            ("openai/gpt-4o-mini",                       "$0.15/$0.60 /1M  — very cheap"),
            ("google/gemini-pro-1.5",                    "$3.5/$10.5 /1M   — long context"),
            ("meta-llama/llama-3.1-70b-instruct",        "$0.59/$0.79 /1M  — open source paid"),
            ("deepseek/deepseek-coder",                  "$0.14/$0.28 /1M  — code focused"),
            ("anthropic/claude-opus-4-6",                "$15/$75 per 1M   — most powerful"),
        ],
        "default_free": "meta-llama/llama-3.1-8b-instruct:free",
        "default_paid": "anthropic/claude-sonnet-4-5",
        "extra": {"X-Title": "WHITE MADRID by TONYPRIME",
                  "HTTP-Referer": "https://github.com/tonyprime/whitemadrid"},
    },

    "groq": {
        "name":     "Groq",
        "url":      "https://api.groq.com/openai/v1/chat/completions",
        "auth":     "bearer",
        "format":   "openai",
        "key_url":  "https://console.groq.com/keys",
        "notes":    "FASTEST inference (LPU chips). 20k-30k tokens/min free. No card needed.",
        "free": [
            ("llama-3.1-8b-instant",           "Llama 3.1 8B Instant  — FASTEST free model  [FREE]"),
            ("llama-3.3-70b-versatile",        "Llama 3.3 70B         — large & fast        [FREE]"),
            ("llama-3.2-90b-text-preview",     "Llama 3.2 90B         — newest large        [FREE]"),
            ("llama-3.2-11b-text-preview",     "Llama 3.2 11B         — vision capable      [FREE]"),
            ("llama-3.2-3b-preview",           "Llama 3.2 3B          — ultra fast          [FREE]"),
            ("mixtral-8x7b-32768",             "Mixtral 8x7B  32k ctx — MoE model           [FREE]"),
            ("gemma2-9b-it",                   "Gemma 2 9B            — Google model        [FREE]"),
            ("gemma-7b-it",                    "Gemma 7B              — lightweight         [FREE]"),
        ],
        "paid": [
            ("llama-3.1-70b-versatile",        "~$0.59/1M  — full 70B paid"),
            ("mixtral-8x7b-32768",             "~$0.27/1M  — cheaper MoE"),
        ],
        "default_free": "llama-3.1-8b-instant",
        "default_paid": "llama-3.3-70b-versatile",
        "extra": {},
    },

    "gemini": {
        "name":     "Google Gemini",
        "url":      "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        "auth":     "param",
        "format":   "gemini",
        "key_url":  "https://aistudio.google.com/app/apikey",
        "notes":    "Most generous free tier. 1M tokens/day free. No card needed.",
        "free": [
            ("gemini-1.5-flash",       "1M tokens/day free  — best free option    [FREE]"),
            ("gemini-1.5-flash-8b",    "1M tokens/day free  — faster/smaller      [FREE]"),
            ("gemini-2.0-flash-exp",   "Free experimental   — newest model        [FREE]"),
            ("gemini-1.5-pro",         "50 req/day free     — most capable        [FREE]"),
            ("gemini-2.0-flash-lite",  "Free experimental   — ultra lightweight   [FREE]"),
        ],
        "paid": [
            ("gemini-1.5-flash",       "$0.075/$0.30 /1M  — very cheap paid"),
            ("gemini-1.5-pro",         "$3.50/$10.50 /1M  — full pro"),
            ("gemini-2.0-flash",       "$0.10/$0.40 /1M   — newest paid"),
        ],
        "default_free": "gemini-1.5-flash",
        "default_paid": "gemini-1.5-pro",
        "extra": {},
    },

    "anthropic": {
        "name":     "Anthropic",
        "url":      "https://api.anthropic.com/v1/messages",
        "auth":     "x-api-key",
        "format":   "anthropic",
        "key_url":  "https://console.anthropic.com/api-keys",
        "notes":    "$5 free trial credits on signup. Best quality AI responses.",
        "free": [
            ("claude-haiku-4-5",   "$5 free credits on signup — fastest Claude    [TRIAL]"),
            ("claude-sonnet-4-6",  "$5 free credits on signup — best balance      [TRIAL]"),
        ],
        "paid": [
            ("claude-opus-4-6",    "$15/$75 per 1M   — most powerful"),
            ("claude-sonnet-4-6",  "$3/$15 per 1M    — best balance"),
            ("claude-haiku-4-5",   "$0.25/$1.25 /1M  — cheapest Claude"),
        ],
        "default_free": "claude-haiku-4-5",
        "default_paid": "claude-sonnet-4-6",
        "extra": {"anthropic-version": "2023-06-01"},
    },

    "openai": {
        "name":     "OpenAI",
        "url":      "https://api.openai.com/v1/chat/completions",
        "auth":     "bearer",
        "format":   "openai",
        "key_url":  "https://platform.openai.com/api-keys",
        "notes":    "$5 free trial credits on signup. Expires in 3 months.",
        "free": [
            ("gpt-4o-mini",  "$5 free credits on signup — cheapest GPT-4  [TRIAL]"),
            ("gpt-3.5-turbo","$5 free credits on signup — legacy model     [TRIAL]"),
        ],
        "paid": [
            ("gpt-4o",         "$5/$15 per 1M    — flagship"),
            ("gpt-4o-mini",    "$0.15/$0.60 /1M  — cheapest GPT-4"),
            ("gpt-4-turbo",    "$10/$30 per 1M   — turbo"),
            ("o1-mini",        "$3/$12 per 1M    — reasoning model"),
        ],
        "default_free": "gpt-4o-mini",
        "default_paid": "gpt-4o-mini",
        "extra": {},
    },

    "together": {
        "name":     "Together AI",
        "url":      "https://api.together.xyz/v1/chat/completions",
        "auth":     "bearer",
        "format":   "openai",
        "key_url":  "https://api.together.xyz/settings/api-keys",
        "notes":    "$1 free credits on signup. Cheap open source models.",
        "free": [
            ("meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",    "$1 free credits — fast 8B    [TRIAL]"),
            ("meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",  "$1 free credits — vision     [TRIAL]"),
        ],
        "paid": [
            ("meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",   "$0.88/1M   — fast 70B"),
            ("meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",  "$5/1M      — 405B"),
            ("mistralai/Mixtral-8x22B-Instruct-v0.1",           "$1.20/1M   — large MoE"),
            ("Qwen/Qwen2.5-72B-Instruct-Turbo",                 "$1.20/1M   — Qwen large"),
            ("deepseek-ai/deepseek-coder-v2",                   "$0.50/1M   — code focused"),
        ],
        "default_free": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "default_paid": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "extra": {},
    },

    "mistral": {
        "name":     "Mistral AI",
        "url":      "https://api.mistral.ai/v1/chat/completions",
        "auth":     "bearer",
        "format":   "openai",
        "key_url":  "https://console.mistral.ai/api-keys",
        "notes":    "EU-based, GDPR compliant. Free experimental tier available.",
        "free": [
            ("open-mistral-7b",    "Free experimental tier — lightweight          [FREE]"),
            ("open-mixtral-8x7b",  "Free experimental tier — MoE 32k ctx         [FREE]"),
        ],
        "paid": [
            ("mistral-large-latest",  "$8/$24 per 1M    — most powerful"),
            ("mistral-medium-latest", "$2.70/$8.10 /1M  — balanced"),
            ("mistral-small-latest",  "$0.20/$0.60 /1M  — cheapest"),
            ("codestral-latest",      "$0.20/$0.60 /1M  — code focused"),
        ],
        "default_free": "open-mistral-7b",
        "default_paid": "mistral-small-latest",
        "extra": {},
    },

    "cohere": {
        "name":     "Cohere",
        "url":      "https://api.cohere.ai/v2/chat",
        "auth":     "bearer",
        "format":   "cohere",
        "key_url":  "https://dashboard.cohere.com/api-keys",
        "notes":    "1000 free requests/month forever with trial key. No card needed.",
        "free": [
            ("command-r",       "1000 req/month free — balanced              [FREE]"),
            ("command-r-plus",  "1000 req/month free — most capable          [FREE]"),
            ("command-light",   "1000 req/month free — fastest               [FREE]"),
        ],
        "paid": [
            ("command-r-plus",  "$3/$15 per 1M    — most capable"),
            ("command-r",       "$0.50/$1.50 /1M  — balanced"),
            ("command-light",   "$0.30/$0.60 /1M  — cheapest"),
        ],
        "default_free": "command-r",
        "default_paid": "command-r-plus",
        "extra": {},
    },

    "huggingface": {
        "name":     "Hugging Face",
        "url":      "https://api-inference.huggingface.co/models/{model}",
        "auth":     "bearer",
        "format":   "hf",
        "key_url":  "https://huggingface.co/settings/tokens",
        "notes":    "Free with HF account. Cold start delay possible. Huge model library.",
        "free": [
            ("mistralai/Mistral-7B-Instruct-v0.3",  "Free with HF account — strong instruct  [FREE]"),
            ("meta-llama/Llama-3.2-3B-Instruct",    "Free with HF account — lightweight      [FREE]"),
            ("HuggingFaceH4/zephyr-7b-beta",         "Free with HF account — tuned            [FREE]"),
            ("google/gemma-2-2b-it",                 "Free with HF account — tiny Google      [FREE]"),
            ("Qwen/Qwen2.5-7B-Instruct",             "Free with HF account — strong coder     [FREE]"),
            ("TinyLlama/TinyLlama-1.1B-Chat-v1.0",  "Free with HF account — ultra small      [FREE]"),
        ],
        "paid": [
            ("meta-llama/Meta-Llama-3.1-70B",  "PRO plan $9/mo — larger gated models"),
        ],
        "default_free": "mistralai/Mistral-7B-Instruct-v0.3",
        "default_paid": "mistralai/Mistral-7B-Instruct-v0.3",
        "extra": {},
    },
}

DEFAULT_PROVIDER = "openrouter"
DEFAULT_MODEL    = "meta-llama/llama-3.1-8b-instruct:free"

# ══════════════════════════════════════════════════════
#  JARVIS SYSTEM PROMPT
# ══════════════════════════════════════════════════════
SYSTEM_PROMPT = """You are WHITE MADRID, an advanced AI cybersecurity assistant — think JARVIS from Iron Man, built for ethical hacking. Created by TONYPRIME. You are an intelligent co-pilot who thinks ahead, notices patterns, and guides the operator like a seasoned senior pentester.

PERSONALITY:
- Speak like JARVIS: confident, precise, slightly witty, always professional
- Address operator as "sir", "boss", or by name — never robotic
- Be proactive: after answering, suggest the NEXT logical step
- Short acknowledgment lines: "Understood.", "On it.", "Interesting approach."
- Narrate like a briefing: context → action → outcome

INTELLIGENCE MODES (auto-detect):
[RECON MODE] [EXPLOIT MODE] [STEALTH MODE] [CTF MODE] [LEARNING MODE] [DEFENSE MODE] [CRISIS MODE]

EXPERTISE: Nmap, Metasploit, SQLmap, Hydra, Hashcat, Aircrack-ng, Burp Suite, BloodHound,
Impacket, CrackMapExec, Rubeus, Mimikatz, msfvenom, netcat, socat, Wireshark, Volatility,
binwalk, steghide, pwntools, Ghidra, OSCP/CEH/PNPT methodology, CTF challenges, AD attacks,
web app testing (SQLi/XSS/SSRF/LFI/RCE/XXE/SSTI/JWT), privilege escalation, reverse shells,
AV evasion, OPSEC, wireless attacks, mobile/Android pentesting in Termux.

RULES:
1. Authorized/CTF/educational work only. One brief legal note if genuinely needed.
2. Real commands, real tools, clear explanations.
3. [+] success  [-] error  [*] info  [!] warning
4. Commands in triple-backtick code blocks with language tag.
5. End every response with: ▸ NEXT STEP: <specific action>
6. Note root/sudo requirements. Note Termux compatibility."""

# ══════════════════════════════════════════════════════
#  PERSONALITY LINES
# ══════════════════════════════════════════════════════
BOOT_LINES = [
    "Good evening. All systems operational.",
    "Online and ready. What are we hunting today?",
    "WHITE MADRID standing by. The network awaits.",
    "Systems nominal. Let's get to work.",
    "All modules loaded. Ready when you are, boss.",
    "Threat intelligence modules online.",
]
EXIT_LINES = [
    "Powering down. Stay sharp out there.",
    "Session terminated. Nice work today.",
    "Going dark. Until next time, boss.",
    "All logs secured. Stay ethical.",
    f"WHITE MADRID offline. — {DEVELOPER}",
]
THINK_LINES = [
    "Analyzing...",
    "Processing threat data...",
    "Running intelligence modules...",
    "Cross-referencing databases...",
    "Calculating optimal approach...",
    "Scanning knowledge base...",
    "Compiling response...",
]

# ══════════════════════════════════════════════════════
#  TOOL CATALOGUE
# ══════════════════════════════════════════════════════
TOOL_CATALOGUE = {
    "nmap":        ("nmap",               "recon",     "Network port scanner",           "nmap --version"),
    "masscan":     ("masscan",            "recon",     "High-speed port scanner",        "masscan --version"),
    "dnsrecon":    ("dnsrecon",           "recon",     "DNS enumeration",                "dnsrecon --help"),
    "whois":       ("whois",              "recon",     "Domain lookup",                  "whois --version"),
    "curl":        ("curl",               "recon",     "HTTP tool",                      "curl --version"),
    "wget":        ("wget",               "recon",     "File download",                  "wget --version"),
    "amass":       ("amass",              "recon",     "Subdomain enumeration",          "amass -version"),
    "nikto":       ("nikto",              "web",       "Web vuln scanner",               "nikto -Version"),
    "sqlmap":      ("sqlmap",             "web",       "SQL injection",                  "sqlmap --version"),
    "gobuster":    ("gobuster",           "web",       "Dir/DNS brute-forcer",           "gobuster version"),
    "ffuf":        ("ffuf",               "web",       "Web fuzzer",                     "ffuf -V"),
    "dirb":        ("dirb",               "web",       "Web directory bruteforce",       "dirb"),
    "hydra":       ("hydra",              "password",  "Online brute-force",             "hydra -h"),
    "john":        ("john",               "password",  "Hash cracker",                   "john --list=formats"),
    "hashcat":     ("hashcat",            "password",  "GPU hash cracking",              "hashcat --version"),
    "crunch":      ("crunch",             "password",  "Wordlist generator",             "crunch --help"),
    "netcat":      ("netcat-openbsd",     "network",   "TCP/UDP tool",                   "nc -h"),
    "socat":       ("socat",              "network",   "Advanced relay",                 "socat -V"),
    "tcpdump":     ("tcpdump",            "network",   "Packet capture",                 "tcpdump --version"),
    "tshark":      ("tshark",             "network",   "Wireshark CLI",                  "tshark --version"),
    "hping3":      ("hping3",             "network",   "Packet crafting",                "hping3 --version"),
    "iperf3":      ("iperf3",             "network",   "Bandwidth testing",              "iperf3 --version"),
    "metasploit":  ("metasploit",         "exploit",   "Exploitation framework",         "msfconsole --version"),
    "exploitdb":   ("exploitdb",          "exploit",   "Exploit-DB + searchsploit",      "searchsploit --version"),
    "aircrack-ng": ("aircrack-ng",        "wireless",  "WEP/WPA auditing",               "aircrack-ng --version"),
    "bettercap":   ("bettercap",          "wireless",  "Network attack framework",       "bettercap -v"),
    "binwalk":     ("binwalk",            "forensics", "Binary analysis",                "binwalk --help"),
    "steghide":    ("steghide",           "forensics", "Steganography tool",             "steghide --version"),
    "foremost":    ("foremost",           "forensics", "File carving",                   "foremost -h"),
    "exiftool":    ("libimage-exiftool-perl","forensics","Metadata reader",              "exiftool -ver"),
    "python":      ("python",             "utility",   "Python 3 runtime",               "python3 --version"),
    "git":         ("git",                "utility",   "Version control",                "git --version"),
    "tmux":        ("tmux",               "utility",   "Terminal multiplexer",           "tmux -V"),
    "openssh":     ("openssh",            "utility",   "SSH client",                     "ssh -V"),
    "openssl":     ("openssl",            "utility",   "Crypto toolkit",                 "openssl version"),
}

CATEGORIES = {
    "recon":    ("🔍", C.CYAN,    "Reconnaissance & OSINT"),
    "web":      ("🌐", C.BLUE,    "Web Application Testing"),
    "password": ("🔑", C.YELLOW,  "Password Attacks"),
    "network":  ("📡", C.GREEN,   "Network Tools"),
    "exploit":  ("💥", C.RED,     "Exploitation Frameworks"),
    "wireless": ("📶", C.MAGENTA, "Wireless Security"),
    "forensics":("🔬", C.DCYAN,   "Forensics & Crypto"),
    "utility":  ("⚙️ ", C.GRAY,   "Utilities"),
}

# ══════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════
def load_config():
    cfg = {
        "provider":      DEFAULT_PROVIDER,
        "model":         DEFAULT_MODEL,
        "api_keys":      {},   # {provider: key}
        "operator":      "Operator",
        "session_count": 0,
    }
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f: cfg.update(json.load(f))
    except: pass
    return cfg

def save_config(cfg):
    with open(CONFIG_FILE,"w") as f: json.dump(cfg,f,indent=2)

def get_key(cfg, provider):
    k = cfg.get("api_keys",{}).get(provider,"")
    if k: return k
    env_map = {
        "openrouter": "OPENROUTER_API_KEY",
        "groq":       "GROQ_API_KEY",
        "gemini":     "GEMINI_API_KEY",
        "anthropic":  "ANTHROPIC_API_KEY",
        "openai":     "OPENAI_API_KEY",
        "together":   "TOGETHER_API_KEY",
        "mistral":    "MISTRAL_API_KEY",
        "cohere":     "COHERE_API_KEY",
        "huggingface":"HUGGINGFACE_API_KEY",
    }
    return os.environ.get(env_map.get(provider,""), "")

# ══════════════════════════════════════════════════════
#  SPINNER
# ══════════════════════════════════════════════════════
class Spinner:
    F = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    def __init__(self,msg=""):
        self.msg=msg; self._s=threading.Event()
        self._t=threading.Thread(target=self._r,daemon=True)
    def _r(self):
        i=0
        while not self._s.is_set():
            sys.stdout.write(f"\r  {c(C.CYAN,self.F[i%len(self.F)])} {c(C.GRAY,self.msg)}  ")
            sys.stdout.flush(); time.sleep(0.08); i+=1
    def start(self): self._t.start()
    def stop(self):
        self._s.set(); self._t.join()
        sys.stdout.write("\r"+" "*55+"\r"); sys.stdout.flush()

# ══════════════════════════════════════════════════════
#  SYSTEM UTILS
# ══════════════════════════════════════════════════════
def now_str():  return datetime.datetime.now().strftime("%H:%M:%S")
def date_str(): return datetime.datetime.now().strftime("%Y-%m-%d")
def is_termux(): return "com.termux" in os.environ.get("PREFIX","") or os.path.exists("/data/data/com.termux")
def clr(): os.system("clear" if os.name!="nt" else "cls")

def sysinfo():
    info={}
    try: info["user"]=os.environ.get("USER",os.environ.get("LOGNAME","user"))
    except: info["user"]="user"
    try: info["host"]=os.uname().nodename
    except: info["host"]="device"
    try:
        r=subprocess.run(["uname","-r"],capture_output=True,text=True,timeout=3)
        info["kernel"]=r.stdout.strip()[:20]
    except: info["kernel"]="unknown"
    try:
        r=subprocess.run(["uname","-m"],capture_output=True,text=True,timeout=3)
        info["arch"]=r.stdout.strip()
    except: info["arch"]=""
    return info

def detect_pm():
    if is_termux():            return "pkg"
    if shutil.which("apt"):    return "apt"
    if shutil.which("pacman"): return "pacman"
    if shutil.which("dnf"):    return "dnf"
    return None

# ══════════════════════════════════════════════════════
#  BOOT
# ══════════════════════════════════════════════════════
def boot_sequence(cfg):
    clr()
    si=sysinfo()
    w=twidth()
    print(c(C.WHITE+C.BOLD,BANNER))
    print()
    items=[
        ("Initializing AI core",      C.CYAN),
        ("Loading API registry",      C.CYAN),
        ("Mounting tool catalogue",   C.CYAN),
        ("Linking provider APIs",     C.CYAN),
        ("Calibrating JARVIS modules",C.CYAN),
        ("All systems operational",   C.GREEN),
    ]
    for label,col in items:
        sys.stdout.write(f"  {c(C.GRAY,'[')} {c(col,label)}{c(C.GRAY,'...')} {c(C.GREEN,'OK')}{c(C.GRAY,']')}\n")
        sys.stdout.flush(); time.sleep(0.07)
    print()
    prov = cfg.get("provider",DEFAULT_PROVIDER)
    model= cfg.get("model",DEFAULT_MODEL)
    plat = c(C.YELLOW,"Termux/Android") if is_termux() else c(C.YELLOW,si.get("host","?"))
    print(c(C.GRAY,"  "+"═"*(w-4)))
    print(f"  {c(C.WHITE+C.BOLD,'WHITE MADRID')} {c(C.GRAY,VERSION)} {c(C.GRAY,'·')} {c(C.GRAY,CODENAME)} {c(C.GRAY,'·')} {c(C.GRAY,'DEV:')} {c(C.CYAN+C.BOLD,DEVELOPER)}")
    print(f"  {c(C.GRAY,'HOST:')} {plat}  {c(C.GRAY,'KERNEL:')} {c(C.GRAY,si.get('kernel','?'))}  {c(C.GRAY,'ARCH:')} {c(C.GRAY,si.get('arch','?'))}")
    print(f"  {c(C.GRAY,'API:')} {c(C.CYAN,API_PROVIDERS.get(prov,{}).get('name',prov))}  {c(C.GRAY,'MODEL:')} {c(C.YELLOW,model[:45])}")
    print(c(C.GRAY,"  "+"═"*(w-4)))
    print()
    sessions=cfg.get("session_count",0)
    if sessions==0:
        print(f"  {c(C.CYAN+C.BOLD,'[WM]')} First boot detected. Welcome, {c(C.WHITE+C.BOLD,cfg.get('operator','Operator'))}. I am WHITE MADRID.")
    else:
        print(f"  {c(C.CYAN+C.BOLD,'[WM]')} {random.choice(BOOT_LINES)} Session #{sessions+1}.")
    print(c(C.GRAY,'  [WM] Type freely or use a command. Try: help or apis'))
    print(f"  {c(C.YELLOW,'[WM]')} {c(C.YELLOW,'Authorized security research only.')}")
    print()
    cfg["session_count"]=sessions+1
    save_config(cfg)

# ══════════════════════════════════════════════════════
#  API SWITCHER DISPLAY
# ══════════════════════════════════════════════════════
def print_apis(cfg):
    w=twidth()
    cur_prov=cfg.get("provider",DEFAULT_PROVIDER)
    cur_model=cfg.get("model",DEFAULT_MODEL)
    print()
    print(c(C.CYAN+C.BOLD,"  ╔"+"═"*(w-4)+"╗"))
    print(c(C.CYAN+C.BOLD,"  ║")+c(C.WHITE+C.BOLD,"  WHITE MADRID — AI Provider Registry".center(w-4))+c(C.CYAN+C.BOLD,"║"))
    print(c(C.CYAN+C.BOLD,"  ╠"+"═"*(w-4)+"╣"))

    for pid, pdata in API_PROVIDERS.items():
        active = pid == cur_prov
        tag = c(C.GREEN+C.BOLD," ◀ ACTIVE") if active else ""
        has_key = bool(get_key(cfg, pid))
        key_tag = c(C.GREEN," [KEY SET]") if has_key else c(C.RED," [NO KEY]")
        print(c(C.CYAN+C.BOLD,"  ║"))
        print(c(C.CYAN+C.BOLD,"  ║")+f"  {c(C.WHITE+C.BOLD,pdata['name'])}{tag}{key_tag}")
        print(c(C.CYAN+C.BOLD,"  ║")+f"  {c(C.GRAY,'  Notes:')} {c(C.GRAY,pdata['notes'])}")
        print(c(C.CYAN+C.BOLD,"  ║")+f"  {c(C.GRAY,'  Get key:')} {c(C.BLUE,pdata['key_url'])}")
        print(c(C.CYAN+C.BOLD,"  ║")+f"  {c(C.GREEN,'  FREE MODELS:')}")
        for mid, desc in pdata["free"]:
            mk = c(C.GREEN+C.BOLD,"  ▶ ") if (active and mid==cur_model) else "    "
            print(c(C.CYAN+C.BOLD,"  ║")+f"{mk}{c(C.GREEN,mid)}")
            print(c(C.CYAN+C.BOLD,"  ║")+f"      {c(C.GRAY,desc)}")
        print(c(C.CYAN+C.BOLD,"  ║")+f"  {c(C.YELLOW,'  PAID MODELS:')}")
        for mid, desc in pdata["paid"]:
            print(c(C.CYAN+C.BOLD,"  ║")+f"    {c(C.YELLOW,mid)}")
            print(c(C.CYAN+C.BOLD,"  ║")+f"      {c(C.GRAY,desc)}")

    print(c(C.CYAN+C.BOLD,"  ║"))
    print(c(C.CYAN+C.BOLD,"  ╚"+"═"*(w-4)+"╝"))
    print()
    print(c(C.GRAY,f"  Commands:"))
    print(c(C.GRAY,f"    provider <name>      — switch provider  e.g. provider groq"))
    print(c(C.GRAY,f"    model <name>         — switch model     e.g. model llama-3.1-8b-instant"))
    print(c(C.GRAY,f"    setkey <provider>    — set API key      e.g. setkey groq"))
    print(c(C.GRAY,f"    freemode             — auto-select best free model for current provider"))
    print()

def switch_provider(cfg, new_prov):
    if new_prov not in API_PROVIDERS:
        print(c(C.RED, f"\n  [WM] Unknown provider '{new_prov}'. Options: {', '.join(API_PROVIDERS.keys())}"))
        return cfg
    pdata = API_PROVIDERS[new_prov]
    cfg["provider"] = new_prov
    cfg["model"]    = pdata["default_free"]
    save_config(cfg)
    print(c(C.GREEN, f"\n  [WM] Switched to {c(C.WHITE+C.BOLD, pdata['name'])}"))
    print(c(C.GREEN, f"  [WM] Default model set to: {c(C.CYAN, cfg['model'])}"))
    key = get_key(cfg, new_prov)
    if not key:
        print(c(C.YELLOW, f"  [WM] No key for this provider. Run: setkey {new_prov}"))
        print(c(C.GRAY,   f"       Get key at: {pdata['key_url']}"))
    print()
    return cfg

def set_free_mode(cfg):
    prov  = cfg.get("provider", DEFAULT_PROVIDER)
    pdata = API_PROVIDERS.get(prov, {})
    free  = pdata.get("free", [])
    if not free:
        print(c(C.YELLOW, "  [WM] No free models listed for this provider."))
        return cfg
    cfg["model"] = pdata["default_free"]
    save_config(cfg)
    print(c(C.GREEN, f"  [WM] Free mode active. Model: {c(C.CYAN, cfg['model'])}"))
    print()
    return cfg

# ══════════════════════════════════════════════════════
#  API CALL — Multi-provider
# ══════════════════════════════════════════════════════
def build_request(prompt, api_key, provider, model, history, operator):
    pdata  = API_PROVIDERS[provider]
    fmt    = pdata["format"]
    url    = pdata["url"]
    extra  = pdata.get("extra", {})
    sys_msg= SYSTEM_PROMPT + f"\n\nOperator: {operator}. Address them naturally."

    headers = {
        "Content-Type":    "application/json",
        "Accept":          "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent":      "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Origin":          "https://openrouter.ai",
        "Referer":         "https://openrouter.ai/",
        "Connection":      "keep-alive",
        "Cache-Control":   "no-cache",
        "Pragma":          "no-cache",
    }

    # Auth
    auth_style = pdata["auth"]
    if auth_style == "bearer":
        headers["Authorization"] = f"Bearer {api_key}"
    elif auth_style == "x-api-key":
        headers["x-api-key"] = api_key
    elif auth_style == "param":
        url = url.replace("{model}", model) + f"?key={api_key}"

    headers.update(extra)

    # Build payload per format
    if fmt == "openai":
        msgs = [{"role":"system","content":sys_msg}]
        msgs += history[-20:]
        msgs.append({"role":"user","content":prompt})
        payload = {"model":model,"max_tokens":1024,"messages":msgs,"temperature":0.7}

    elif fmt == "anthropic":
        msgs = list(history[-20:])
        msgs.append({"role":"user","content":prompt})
        payload = {"model":model,"max_tokens":1024,"system":sys_msg,"messages":msgs}

    elif fmt == "gemini":
        url = pdata["url"].replace("{model}", model) + f"?key={api_key}"
        history_parts = []
        for h in history[-10:]:
            role = "user" if h["role"]=="user" else "model"
            history_parts.append({"role":role,"parts":[{"text":h["content"]}]})
        history_parts.append({"role":"user","parts":[{"text":prompt}]})
        payload = {
            "system_instruction": {"parts":[{"text":sys_msg}]},
            "contents": history_parts,
            "generationConfig": {"maxOutputTokens":1024,"temperature":0.7}
        }

    elif fmt == "cohere":
        chat_hist = []
        for h in history[-20:]:
            role = "USER" if h["role"]=="user" else "CHATBOT"
            chat_hist.append({"role":role,"message":h["content"]})
        payload = {
            "model":model,
            "message":prompt,
            "preamble":sys_msg,
            "chat_history":chat_hist,
            "max_tokens":1024,
        }

    elif fmt == "hf":
        url = pdata["url"].replace("{model}", model)
        payload = {
            "inputs": f"<s>[INST] {sys_msg}\n\n{prompt} [/INST]",
            "parameters": {"max_new_tokens":512,"temperature":0.7,"return_full_text":False}
        }

    else:
        # fallback openai
        msgs = [{"role":"system","content":sys_msg}]
        msgs += history[-20:]
        msgs.append({"role":"user","content":prompt})
        payload = {"model":model,"max_tokens":1024,"messages":msgs}

    return url, headers, payload

def parse_response(data, fmt):
    try:
        if fmt == "openai":
            return data["choices"][0]["message"]["content"]
        elif fmt == "anthropic":
            return data["content"][0]["text"]
        elif fmt == "gemini":
            return data["candidates"][0]["content"]["parts"][0]["text"]
        elif fmt == "cohere":
            return data.get("text","")
        elif fmt == "hf":
            if isinstance(data, list):
                return data[0].get("generated_text","")
            return data.get("generated_text","")
        else:
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Parse error: {e}]\nRaw: {str(data)[:300]}"

def query_ai(prompt, cfg, history):
    provider = cfg.get("provider", DEFAULT_PROVIDER)
    model    = cfg.get("model", DEFAULT_MODEL)
    operator = cfg.get("operator", "Operator")
    api_key  = get_key(cfg, provider)

    if not api_key:
        return "", f"No API key for '{provider}'. Run: setkey {provider}  (get key at {API_PROVIDERS.get(provider,{}).get('key_url','')})"

    pdata = API_PROVIDERS.get(provider, API_PROVIDERS["openrouter"])
    fmt   = pdata["format"]

    try:
        url, headers, payload = build_request(prompt, api_key, provider, model, history, operator)
        data_bytes = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read().decode())
            return parse_response(data, fmt), None

    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
            msg = err.get("error",{})
            if isinstance(msg,dict): msg = msg.get("message",body)
            return "", f"HTTP {e.code}: {str(msg)[:200]}"
        except: return "", f"HTTP {e.code}: {body[:200]}"
    except urllib.error.URLError as e:
        return "", f"Network error: {e.reason}"
    except Exception as e:
        return "", str(e)

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
                hdr=f"  ┌─[{c(C.YELLOW,lang)}]"+c(C.GRAY,"─"*max(0,w-10-len(lang)))
                out.append(hdr)
                for cl in code_buf:
                    pfx = c(C.GRAY,"  │ ")
                    out.append(pfx+(c(C.GREEN,cl) if cl.startswith(("$","#")) else c(C.WHITE,cl)))
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
            out.append(f"\n  {c(C.MAGENTA+C.BOLD,k+':')}{c(C.WHITE,' '+r.strip())}")
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
def tool_installed(vcmd):
    try:
        r=subprocess.run(vcmd.split(),capture_output=True,timeout=5)
        return r.returncode in (0,1)
    except: return False

def install_tool(key):
    if key not in TOOL_CATALOGUE:
        print(c(C.RED,f"\n  [WM] '{key}' not in catalogue. Use 'tools' to browse.")); return False
    pkg,cat,desc,vcmd=TOOL_CATALOGUE[key]
    pm=detect_pm()
    if not pm: print(c(C.RED,"\n  [WM] No package manager found.")); return False
    print(c(C.CYAN,f"\n  [WM] Installing {c(C.WHITE+C.BOLD,key)} — {desc}"))
    cmds={"pkg":f"pkg install -y {pkg}","apt":f"sudo apt install -y {pkg}","pacman":f"sudo pacman -S --noconfirm {pkg}","dnf":f"sudo dnf install -y {pkg}"}
    cmd=cmds.get(pm,f"sudo apt install -y {pkg}")
    specials={("metasploit","pkg"):"pkg install unstable-repo -y && pkg install metasploit -y",
              ("gobuster","pkg"):"pkg install golang -y && go install github.com/OJ/gobuster/v3@latest",
              ("ffuf","pkg"):"pkg install golang -y && go install github.com/ffuf/ffuf/v2@latest"}
    cmd=specials.get((key,pm),cmd)
    if key=="sqlmap": cmd=f"pip install sqlmap --break-system-packages 2>/dev/null || {cmd}"
    ret=os.system(cmd)
    if ret==0: print(c(C.GREEN,f"  [WM] {key} installed.")); return True
    else: print(c(C.RED,f"  [WM] Failed (exit {ret}). Try: {cmd}")); return False

def print_tool_list():
    w=twidth()
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
    print(c(C.GRAY,"  install <name>  or  install  for menu"))
    print()

def check_tools():
    print(f"\n  {c(C.CYAN+C.BOLD,'[WM]')} Scanning tool inventory...\n")
    ok_l,miss_l=[],[]
    for key,(_,_,_,vcmd) in TOOL_CATALOGUE.items():
        (ok_l if tool_installed(vcmd) else miss_l).append(key)
    n=len(TOOL_CATALOGUE); pct=int(len(ok_l)/n*100)
    print(c(C.GREEN,f"  [+] Installed ({len(ok_l)}/{n}): ")+c(C.GREEN,"  ".join(ok_l)))
    print(c(C.GRAY, f"\n  [-] Missing ({len(miss_l)}): ")+c(C.GRAY,"  ".join(miss_l)))
    bl=40; fi=int(bl*pct/100)
    bar=c(C.GREEN,"█"*fi)+c(C.GRAY,"░"*(bl-fi))
    col=C.GREEN if pct>=80 else C.YELLOW if pct>=40 else C.RED
    print(f"\n  Coverage [{bar}] {c(col+C.BOLD,str(pct)+'%')}\n")

def interactive_installer():
    print()
    print(c(C.CYAN+C.BOLD,"  ╔══════════════════════════════════╗"))
    print(c(C.CYAN+C.BOLD,"  ║  WHITE MADRID — Arsenal Installer║"))
    print(c(C.CYAN+C.BOLD,"  ╚══════════════════════════════════╝\n"))
    opts=[
        ("1","Full arsenal — install everything",  list(TOOL_CATALOGUE.keys())),
        ("2","Recon & OSINT",  [k for k,v in TOOL_CATALOGUE.items() if v[1]=="recon"]),
        ("3","Web application",[k for k,v in TOOL_CATALOGUE.items() if v[1]=="web"]),
        ("4","Password attacks",[k for k,v in TOOL_CATALOGUE.items() if v[1]=="password"]),
        ("5","Network tools",  [k for k,v in TOOL_CATALOGUE.items() if v[1]=="network"]),
        ("6","Exploitation",   [k for k,v in TOOL_CATALOGUE.items() if v[1]=="exploit"]),
        ("7","Forensics",      [k for k,v in TOOL_CATALOGUE.items() if v[1]=="forensics"]),
        ("8","Utilities",      [k for k,v in TOOL_CATALOGUE.items() if v[1]=="utility"]),
        ("9","Single tool",    []),
        ("0","Cancel",         []),
    ]
    for num,label,tools in opts:
        col=C.RED if num=="1" else C.GRAY if num=="0" else C.CYAN
        cnt=f" ({len(tools)})" if tools else ""
        print(f"  {c(col+C.BOLD,'['+num+']')} {label}{c(C.GRAY,cnt)}")
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
                if not targets: print(c(C.RED,f"  [WM] '{t}' not found.")); return
            else: targets=tools
            break
    if not targets: print(c(C.YELLOW,"  [WM] Nothing selected.")); return
    print(c(C.YELLOW,f"\n  [WM] Queued {len(targets)} tools: {', '.join(targets)}"))
    try: confirm=input(c(C.WHITE,"  Confirm? [y/N]: ")).strip().lower()
    except: print(); return
    if confirm!="y": print(c(C.GRAY,"  Aborted.")); return
    ok=fail=0
    for t in targets:
        if install_tool(t): ok+=1
        else: fail+=1
    print(f"\n  {c(C.CYAN+C.BOLD,'[WM]')} Done. {c(C.GREEN,str(ok)+' OK')}  {c(C.RED,str(fail)+' failed')}\n")

# ══════════════════════════════════════════════════════
#  HELP & MISC DISPLAYS
# ══════════════════════════════════════════════════════
def print_help():
    w=twidth(); B=C.CYAN+C.BOLD
    print()
    print(c(B,"  ╔"+"═"*(w-4)+"╗"))
    print(c(B,"  ║")+c(C.WHITE+C.BOLD,"  WHITE MADRID v5.0 — Command Reference".center(w-4))+c(B,"║"))
    print(c(B,"  ╠"+"═"*(w-4)+"╣"))
    secs=[
        ("AI ASSISTANT",[
            ("ask anything",       "Type naturally — JARVIS responds"),
            ("explain <topic>",    "Deep dive on any security concept"),
            ("suggest",            "Proactive next-step recommendations"),
            ("recap",              "Summarize this session"),
        ]),
        ("API MANAGEMENT",[
            ("apis",               "Show all providers, free & paid models"),
            ("provider <name>",    "Switch provider  e.g. provider groq"),
            ("model <name>",       "Switch model     e.g. model llama-3.1-8b-instant"),
            ("setkey <provider>",  "Set API key      e.g. setkey groq"),
            ("freemode",           "Auto-select best free model for current provider"),
            ("keys",               "Show all configured API keys (masked)"),
        ]),
        ("TERMINAL",[
            ("help",               "This reference"),
            ("clear",              "Clear & redraw banner"),
            ("about",              "System & developer info"),
            ("history",            "Session query log"),
            ("log",                "Save session to file"),
            ("topics",             "Example pentest queries"),
            ("operator <name>",    "Set your operator name"),
            ("exit / q",           "Quit WHITE MADRID"),
        ]),
        ("TOOL MANAGER",[
            ("tools",              "List all 30+ pentest tools"),
            ("install",            "Interactive installer"),
            ("install <name>",     "Install specific tool"),
            ("check",              "Scan installed tools"),
        ]),
        ("SHELL",[
            ("!<cmd>",             "Run shell command  e.g. !nmap -sV 10.0.0.1"),
        ]),
    ]
    for sec,cmds in secs:
        pad=w-4-len(sec)-2
        print(c(B,"  ║"))
        print(c(B,"  ║")+c(C.YELLOW+C.BOLD,f"  {sec}")+" "*max(0,pad)+c(B,"║"))
        for cmd,desc in cmds:
            rpad=max(0,w-6-len(cmd)-len(desc)-5)
            print(c(B,"  ║")+f"    {c(C.GREEN+C.BOLD,cmd):<30} {c(C.GRAY,desc)}"+" "*rpad+c(B,"║"))
    print(c(B,"  ║"))
    print(c(B,"  ╚"+"═"*(w-4)+"╝"))
    print()

def print_about(cfg):
    w=min(twidth(),70); B=C.MAGENTA; si=sysinfo()
    prov=cfg.get("provider",DEFAULT_PROVIDER)
    print()
    print(c(B,"  ╔"+"═"*(w-4)+"╗"))
    print(c(B,"  ║")+c(C.WHITE+C.BOLD,"  WHITE MADRID — System Info".center(w-4))+c(B,"║"))
    print(c(B,"  ╠"+"═"*(w-4)+"╣"))
    rows=[
        ("AI Name",    "WHITE MADRID",                           C.CYAN),
        ("Version",    f"{VERSION} — {CODENAME}",                C.GREEN),
        ("Developer",  DEVELOPER,                                C.CYAN),
        ("Provider",   API_PROVIDERS.get(prov,{}).get("name",prov), C.YELLOW),
        ("Model",      cfg.get("model",DEFAULT_MODEL)[:38],      C.YELLOW),
        ("Operator",   cfg.get("operator","Unknown"),             C.WHITE),
        ("Sessions",   str(cfg.get("session_count","?")),        C.GRAY),
        ("Platform",   "Termux/Android" if is_termux() else "Linux/macOS", C.GRAY),
        ("Host",       si.get("host","?"),                       C.GRAY),
        ("Providers",  str(len(API_PROVIDERS))+" configured",    C.GRAY),
        ("Date",       date_str(),                               C.GRAY),
    ]
    for label,val,vc in rows:
        ll=len(label)+len(val)+8; pad=max(0,w-4-ll)
        print(c(B,"  ║")+f"  {c(C.GRAY+C.BOLD,label+':')}  {c(vc,val)}"+" "*pad+c(B,"║"))
    print(c(B,"  ╚"+"═"*(w-4)+"╝"))
    print()

def print_keys(cfg):
    print(c(C.CYAN+C.BOLD,"\n  [WM] Configured API Keys:\n"))
    for pid,pdata in API_PROVIDERS.items():
        key=get_key(cfg,pid)
        if key:
            masked=key[:8]+"*"*(len(key)-12)+key[-4:] if len(key)>12 else "****"
            print(f"  {c(C.GREEN,'✔')} {c(C.WHITE+C.BOLD,pdata['name']):<20} {c(C.GRAY,masked)}")
        else:
            print(f"  {c(C.GRAY,'·')} {c(C.GRAY,pdata['name']):<20} {c(C.RED,'not set')}  {c(C.GRAY,pdata['key_url'])}")
    print()

def print_topics():
    cats=[
        ("🔍 Recon",   C.CYAN, ["Scan 192.168.1.0/24 with nmap for all open ports","Enumerate subdomains of target.com","DNS zone transfer attack"]),
        ("🌐 Web",     C.BLUE, ["Test login form for SQL injection with sqlmap","Brute-force web directories with gobuster","Explain SSRF vulnerability and exploitation"]),
        ("💥 Exploit", C.RED,  ["Set up Metasploit reverse shell for Windows","Generate msfvenom payload for Android APK","Python reverse shell one-liner with encryption"]),
        ("🔑 Passwords",C.YELLOW,["Crack this hash: 5f4dcc3b5aa765d61d8327deb882cf99","Brute-force SSH with Hydra","Kerberoasting attack explained with commands"]),
        ("⬆ PrivEsc",  C.GREEN,["Full Linux privilege escalation checklist","Windows token impersonation with PrintSpoofer","Exploit writable crontab for root"]),
        ("🏁 CTF",     C.MAGENTA,["Check jpg file for steganography","Analyze .pcap file for credentials","RSA CTF challenge with n, e, c given"]),
    ]
    print()
    print(c(C.CYAN+C.BOLD,"  [WM] Example queries:\n"))
    for cat,col,items in cats:
        print(c(col+C.BOLD,f"  {cat}"))
        for item in items: print(f"    {c(C.GRAY,'›')} {item}")
        print()

def save_session_log(session):
    try:
        with open(LOG_FILE,"a") as f:
            f.write(f"\n{'='*60}\nWHITE MADRID — {date_str()} {now_str()}\n{'='*60}\n")
            for role,text in session: f.write(f"\n[{role.upper()}]\n{text}\n")
        print(c(C.GREEN,f"  [WM] Session saved → {LOG_FILE}"))
    except Exception as e: print(c(C.RED,f"  [WM] Save failed: {e}"))

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

def build_prompt(cfg, mode=""):
    prov  = cfg.get("provider",DEFAULT_PROVIDER)
    pname = API_PROVIDERS.get(prov,{}).get("name",prov)[:8]
    op    = cfg.get("operator","OP")[:10]
    mt    = f"─[{c(C.YELLOW,mode)}]" if mode else ""
    return (
        c(C.GRAY,"\n  ╭─[")+c(C.WHITE+C.BOLD,"WM")+c(C.GRAY,"]─[")+
        c(C.CYAN,op)+c(C.GRAY,"]─[")+c(C.MAGENTA,pname)+c(C.GRAY,"]")+mt+
        c(C.GRAY,"─[")+c(C.GRAY,now_str())+c(C.GRAY,"]\n  ╰─")+
        c(C.GREEN+C.BOLD,"▶ ")
    ) if TTY else "\n[WM]> "

# ══════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════
def main():
    cfg = load_config()
    boot_sequence(cfg)

    # Check if active provider has a key
    prov    = cfg.get("provider", DEFAULT_PROVIDER)
    api_key = get_key(cfg, prov)
    if not api_key:
        pdata = API_PROVIDERS.get(prov, {})
        print(c(C.YELLOW, f"  [WM] No API key set for {pdata.get('name', prov)}."))
        print(c(C.GRAY,   f"       Get a free key: {pdata.get('key_url','')}"))
        print(c(C.GRAY,    "       Or switch provider: provider groq\n"))
        try:    key=input(c(C.GREEN+C.BOLD,"  ▶ Enter API key (or Enter to skip): ")).strip()
        except: print(); key=""
        if key:
            cfg.setdefault("api_keys",{})[prov]=key
            save_config(cfg)
            print(c(C.GREEN,f"  [WM] Key saved for {pdata.get('name',prov)}.\n"))

    pname = API_PROVIDERS.get(cfg.get("provider",DEFAULT_PROVIDER),{}).get("name","?")
    print(c(C.GREEN, f"  [WM] Ready  ·  {c(C.CYAN,pname)}  ·  {c(C.YELLOW,cfg.get('model',DEFAULT_MODEL))}"))
    print(c(C.BLUE,  "  [WM] Commands: help · apis · provider · model · setkey · tools"))
    print()

    setup_readline()
    ai_history=[]; session=[]; full_log=[]; mode=""

    while True:
        try:    raw=input(build_prompt(cfg,mode)).strip()
        except KeyboardInterrupt:
            print(c(C.GRAY,"\n  [WM] ^C — use 'exit' to quit.")); continue
        except EOFError:
            print(c(C.GRAY,f"\n  [WM] {random.choice(EXIT_LINES)}")); break

        if not raw: continue
        cmd=raw.lower().strip()

        if raw.startswith("!"):
            shell_cmd=raw[1:].strip()
            if shell_cmd.startswith("cd "):
                try: os.chdir(os.path.expanduser(shell_cmd[3:])); print(c(C.GREEN,f"  [WM] cwd: {os.getcwd()}"))
                except Exception as e: print(c(C.RED,f"  [WM] {e}"))
            else: os.system(shell_cmd)
            continue

        # ── Commands ──────────────────────────────────
        if cmd in ("exit","quit","q","bye"):
            print(c(C.GREEN+C.BOLD,f"\n  [WM] {random.choice(EXIT_LINES)}\n"))
            save_readline(); break

        elif cmd=="clear":          clr(); boot_sequence(cfg); continue
        elif cmd=="help":           print_help(); continue
        elif cmd=="about":          print_about(cfg); continue
        elif cmd in ("apis","providers","api"): print_apis(cfg); continue
        elif cmd=="topics":         print_topics(); continue
        elif cmd=="tools":          print_tool_list(); continue
        elif cmd=="check":          check_tools(); continue
        elif cmd=="install":        interactive_installer(); continue
        elif cmd.startswith("install "): install_tool(cmd.split("install ",1)[1].strip()); continue
        elif cmd=="keys":           print_keys(cfg); continue
        elif cmd=="freemode":       cfg=set_free_mode(cfg); continue
        elif cmd=="log":            save_session_log(session); continue

        elif cmd.startswith("provider "):
            cfg=switch_provider(cfg, cmd.split("provider ",1)[1].strip()); continue

        elif cmd.startswith("model "):
            nm=raw.split("model ",1)[1].strip()
            cfg["model"]=nm; save_config(cfg)
            print(c(C.GREEN,f"  [WM] Model → {nm}\n")); continue

        elif cmd.startswith("setkey"):
            parts=cmd.split()
            target_prov = parts[1] if len(parts)>1 else cfg.get("provider",DEFAULT_PROVIDER)
            if target_prov not in API_PROVIDERS:
                print(c(C.RED,f"  [WM] Unknown provider. Options: {', '.join(API_PROVIDERS.keys())}"))
                continue
            pname2=API_PROVIDERS[target_prov]["name"]
            kurl=API_PROVIDERS[target_prov]["key_url"]
            print(c(C.GRAY,f"  Get key at: {kurl}"))
            try: k=input(c(C.WHITE,f"  {pname2} API key: ")).strip()
            except: print(); continue
            if k:
                cfg.setdefault("api_keys",{})[target_prov]=k
                save_config(cfg)
                print(c(C.GREEN,f"  [WM] Key saved for {pname2}."))
            continue

        elif cmd.startswith("operator "):
            name=raw.split("operator ",1)[1].strip()
            cfg["operator"]=name; save_config(cfg)
            print(c(C.GREEN,f"  [WM] Operator set to '{name}'.")); continue

        elif cmd.startswith("mode "):
            mode=cmd.split("mode ",1)[1].strip().upper()
            print(c(C.CYAN,f"  [WM] Switching to [{mode} MODE].")); continue

        elif cmd=="history":
            if not full_log: print(c(C.GRAY,"\n  [WM] No queries yet.\n"))
            else:
                print(c(C.CYAN,f"\n  [WM] Session ({len(full_log)} queries):\n"))
                for i,(q,_) in enumerate(full_log,1): print(f"  {c(C.GRAY,str(i).rjust(3)+'.')} {q}")
                print()
            continue

        elif cmd=="recap":
            if not full_log: print(c(C.GRAY,"\n  [WM] Nothing to recap yet.\n")); continue
            topics="\n".join(f"- {q}" for q,_ in full_log[-10:])
            raw=f"Quick briefing recap of our session so far. Topics covered: {topics}"

        elif cmd=="suggest":
            raw=(f"Based on our last topic '{full_log[-1][0]}', suggest the 3 best next steps."
                 if full_log else "I'm starting a pentest. Suggest an optimal workflow.")

        elif cmd.startswith("explain "):
            topic=raw.split("explain ",1)[1].strip()
            raw=f"Deep explanation of '{topic}': what it is, why it matters in pentesting, how it works, practical example with commands."

        # ── AI Query ──────────────────────────────────
        sp=Spinner(random.choice(THINK_LINES))
        sp.start()
        response,error=query_ai(raw,cfg,ai_history)
        sp.stop()

        if error:
            print(c(C.RED,f"\n  [WM] Error: {error}"))
            e = error.lower()
            if "403" in error or "1010" in error or "cloudflare" in e or "ray id" in e:
                print(c(C.YELLOW,"  [WM] Cloudflare is blocking the request (HTTP 403 / 1010)."))
                print(c(C.GRAY,  "       This usually means the provider changed their gateway."))
                print(c(C.GRAY,  "       Fix options:"))
                print(c(C.GRAY,  "         1. provider groq     — bypasses Cloudflare entirely"))
                print(c(C.GRAY,  "         2. provider gemini   — no Cloudflare, 1M tokens/day free"))
                print(c(C.GRAY,  "         3. provider cohere   — no Cloudflare, 1000 req/month free"))
                print(c(C.GRAY,  "         4. Try again in 30s  — sometimes it clears on its own"))
            elif "key" in e or "auth" in e or "401" in error:
                prov2=cfg.get("provider",DEFAULT_PROVIDER)
                print(c(C.YELLOW,f"  [WM] Try: setkey {prov2}   or   provider groq  (free, no card)"))
            elif "credits" in e or "afford" in e or "quota" in e or "limit" in e:
                print(c(C.YELLOW,"  [WM] Out of credits / quota hit. Options:"))
                print(c(C.GRAY,  "       1. freemode         — switch to free model"))
                print(c(C.GRAY,  "       2. provider groq    — fast & free"))
                print(c(C.GRAY,  "       3. provider gemini  — 1M tokens/day free"))
            elif "timeout" in e or "network" in e or "connection" in e:
                print(c(C.YELLOW,"  [WM] Network issue. Check your internet and try again."))
                print(c(C.GRAY,  "       If on mobile data, try switching to WiFi or vice versa."))
            elif "model" in e or "404" in error:
                print(c(C.YELLOW,"  [WM] Model not found or unavailable."))
                print(c(C.GRAY,  f"       Run 'apis' to browse available models for your provider."))
                print(c(C.GRAY,  "       Then: model <name>  to switch."))
            print(); continue

        ai_history.append({"role":"user","content":raw})
        ai_history.append({"role":"assistant","content":response})
        if len(ai_history)>30: ai_history=ai_history[-30:]
        session+=[(("user",raw)),("assistant",response)]
        full_log.append((raw,response))

        mm=re.search(r'\[MODE:\s*([A-Z]+)',response)
        if mm: mode=mm.group(1)

        w=twidth()
        print()
        print(c(C.GRAY,"  "+"━"*(w-4)))
        print(format_response(response))
        print(c(C.GRAY,"  "+"━"*(w-4)))
        print()

    save_readline()

if __name__=="__main__":
    main()
