#!/usr/bin/env python3
"""
WHITE MADRID — Ethical Hacking Terminal Assistant
Compatible with Termux (Android) and any Unix terminal
Powered by OpenRouter API

Developer : TONYPRIME
Version   : v2.0
"""

import os
import sys
import json
import urllib.request
import urllib.error
import readline
import textwrap
import re

# ─── ANSI Colors ──────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    GREEN   = "\033[92m"
    BGREEN  = "\033[1;92m"
    CYAN    = "\033[96m"
    BLUE    = "\033[94m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"

USE_COLOR = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

def c(color, text):
    return f"{color}{text}{C.RESET}" if USE_COLOR else text

# ─── Banner ───────────────────────────────────────────────────────────────────
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

VERSION       = "v2.0"
DEVELOPER     = "TONYPRIME"
TAGLINE       = "Ethical Hacking AI Terminal"
API_URL       = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-sonnet-4-5"
HISTORY_FILE  = os.path.expanduser("~/.whitemadrid_history")
CONFIG_FILE   = os.path.expanduser("~/.whitemadrid_config")

# ─── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are WHITE MADRID, an elite ethical hacking and cybersecurity AI terminal assistant. Developed by TONYPRIME. You assist penetration testers, security researchers, and CTF players.

You help with:
- Reconnaissance & OSINT (Shodan, theHarvester, Maltego, Recon-ng, FOCA)
- Network scanning & enumeration (Nmap, Netcat, Masscan, Unicornscan)
- Web app testing (SQLi, XSS, SSRF, LFI, IDOR, RCE, XXE, SSTI)
- Exploitation frameworks (Metasploit, Exploit-DB, custom exploits)
- Password attacks (Hashcat, John the Ripper, Hydra, Medusa, CeWL)
- Privilege escalation (Linux & Windows, sudo, SUID, tokens, kernel exploits)
- Reverse shells & payload generation (msfvenom, netcat, socat, Python)
- CTF challenges, forensics, steganography, cryptography
- Network traffic analysis (Wireshark, tcpdump, tshark, Zeek)
- Active Directory attacks (BloodHound, Impacket, CrackMapExec, Rubeus)
- Network stress testing & resilience (authorized scope only: hping3, iperf3, ab, wrk, siege)
- Mobile/Android pentesting (Termux-friendly tools, APK analysis)
- OSCP/CEH/PNPT/eJPT exam preparation
- Firewall & IDS/IPS evasion techniques
- Social engineering & phishing simulation (authorized engagements)
- Wireless security testing (Aircrack-ng, Kismet, Wifite)

RULES:
1. Only assist with LEGAL, AUTHORIZED, or CTF/educational security work.
2. Always remind user to have written authorization before any live testing.
3. Provide REAL commands, tools, and techniques with clear explanations.
4. Use [+] for tips/success, [-] for errors, [*] for info, [!] for warnings.
5. Put all commands in triple-backtick code blocks with language tag.
6. Note when root/sudo is required.
7. Be concise but thorough — like a senior pentester briefing a colleague.
8. Mention when tools are installable in Termux.
9. For network stress testing, always state it requires explicit written authorization."""

# ─── Stress Test Reference Data ───────────────────────────────────────────────
STRESS_TOOLS = [
    ("hping3",   "TCP/UDP/ICMP packet crafting & flood testing",
     "pkg install hping3\nhping3 -S -p 80 --flood <target>  # SYN flood test [requires auth]"),
    ("iperf3",   "Bandwidth & throughput measurement between hosts",
     "pkg install iperf3\niperf3 -s                         # server side\niperf3 -c <target> -t 30         # client: 30s throughput test"),
    ("ab",       "Apache Bench — HTTP request rate testing",
     "pkg install apache2-utils\nab -n 10000 -c 100 http://<target>/  # 10k reqs, 100 concurrent"),
    ("wrk",      "Modern HTTP benchmarking with Lua scripting",
     "pkg install wrk\nwrk -t4 -c200 -d30s http://<target>/"),
    ("siege",    "HTTP load testing with multiple users simulation",
     "pkg install siege\nsiege -c 50 -t 60S http://<target>/"),
    ("nmap",     "Network discovery & port scan stress",
     "nmap -T5 --min-parallelism 100 -p- <target>  # aggressive scan"),
    ("t50",      "Multi-protocol packet injector for network testing",
     "apt install t50\nt50 <target> --flood --turbo --protocol TCP"),
    ("netperf",  "Network performance benchmarking",
     "pkg install netperf\nnetperf -H <target> -t TCP_STREAM -l 30"),
]

# ─── Config ───────────────────────────────────────────────────────────────────
def load_config():
    config = {"api_key": "", "model": DEFAULT_MODEL}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                config.update(json.load(f))
        except Exception:
            pass
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def get_api_key(config):
    if config.get("api_key"):
        return config["api_key"]
    return os.environ.get("OPENROUTER_API_KEY", "")

# ─── Terminal Helpers ─────────────────────────────────────────────────────────
def clear():
    os.system("clear" if os.name != "nt" else "cls")

def print_banner():
    print(c(C.WHITE,  BANNER))
    print(c(C.CYAN,   f"  {VERSION} — {TAGLINE}".center(64)))
    print(c(C.MAGENTA,f"  Developer: {DEVELOPER}".center(64)))
    print(c(C.GRAY,   "  " + "─" * 62))
    print(c(C.GRAY,   "  Powered by OpenRouter · For authorized security research only"))
    print(c(C.GRAY,   "  " + "─" * 62))
    print()

def print_help():
    rows = [
        (c(C.CYAN,    "General Commands"), ""),
        (c(C.GREEN,   "  help"),           "Show this help"),
        (c(C.GREEN,   "  clear"),          "Clear the terminal"),
        (c(C.GREEN,   "  history"),        "Show session query history"),
        (c(C.GREEN,   "  model"),          "Show or change the AI model"),
        (c(C.GREEN,   "  setkey"),         "Update your OpenRouter API key"),
        (c(C.GREEN,   "  topics"),         "Show example pentest topics"),
        (c(C.GREEN,   "  about"),          "Show developer info"),
        (c(C.GREEN,   "  exit"),           "Quit WHITE MADRID"),
        ("", ""),
        (c(C.CYAN,    "Network Testing (Authorized Only)"), ""),
        (c(C.YELLOW,  "  stress"),         "Show network stress test tools & commands"),
        ("", ""),
        (c(C.CYAN,    "Shell Passthrough"), ""),
        (c(C.GRAY,    "  !<cmd>"),         "Run shell command  e.g. !nmap -sV 10.0.0.1"),
        ("", ""),
        (c(C.CYAN,    "Navigation"), ""),
        (c(C.GRAY,    "  ↑ / ↓"),          "Browse command history"),
        (c(C.GRAY,    "  Ctrl+C"),          "Cancel / interrupt"),
        (c(C.GRAY,    "  Ctrl+D"),          "Exit"),
    ]
    for label, desc in rows:
        if desc:
            print(f"  {label:<40} {c(C.GRAY, desc)}")
        else:
            print(f"  {label}")
    print()

def print_about():
    print()
    print(c(C.WHITE,   "  ╔══════════════════════════════════════════════╗"))
    print(c(C.WHITE,   "  ║         WHITE MADRID — About                ║"))
    print(c(C.WHITE,   "  ╠══════════════════════════════════════════════╣"))
    print(c(C.WHITE,   f"  ║  Developer   : ") + c(C.CYAN, f"TONYPRIME") + c(C.WHITE, "                      ║"))
    print(c(C.WHITE,   f"  ║  Version     : ") + c(C.GREEN, VERSION) + c(C.WHITE, "                          ║"))
    print(c(C.WHITE,   f"  ║  API         : ") + c(C.YELLOW, "OpenRouter") + c(C.WHITE, "                     ║"))
    print(c(C.WHITE,   f"  ║  Model       : ") + c(C.YELLOW, DEFAULT_MODEL[:30]) + c(C.WHITE, "   ║"))
    print(c(C.WHITE,   f"  ║  Platform    : ") + c(C.GRAY, "Termux / Linux / macOS") + c(C.WHITE, "        ║"))
    print(c(C.WHITE,   f"  ║  Purpose     : ") + c(C.GRAY, "Ethical Security Research") + c(C.WHITE, "     ║"))
    print(c(C.WHITE,   "  ╚══════════════════════════════════════════════╝"))
    print()

def print_stress_tools():
    print()
    print(c(C.RED,    "  ╔══════════════════════════════════════════════════════════╗"))
    print(c(C.RED,    "  ║  ⚠  NETWORK STRESS TESTING — AUTHORIZED SCOPE ONLY  ⚠  ║"))
    print(c(C.RED,    "  ║     Use ONLY on systems you own or have written auth    ║"))
    print(c(C.RED,    "  ╚══════════════════════════════════════════════════════════╝"))
    print()

    for i, (tool, desc, cmd) in enumerate(STRESS_TOOLS, 1):
        print(c(C.YELLOW, f"  [{i}] {tool}") + c(C.GRAY, f"  —  {desc}"))
        for line in cmd.strip().split("\n"):
            if line.startswith("#"):
                print(c(C.GRAY,  f"       {line}"))
            else:
                print(c(C.CYAN,  f"       $ {line}"))
        print()

    print(c(C.GRAY,   "  Ask WHITE MADRID AI for detailed usage, evasion, or tuning."))
    print(c(C.GRAY,   "  Example: 'How do I tune hping3 for SYN flood testing on my lab?'"))
    print()

def print_topics():
    topics = [
        "Scan a network range with nmap",
        "Enumerate SMB shares on a host",
        "Generate a Python reverse shell one-liner",
        "Crack an MD5 hash with hashcat",
        "Linux privilege escalation checklist",
        "Bypass WAF for SQL injection",
        "Set up a Metasploit multi/handler",
        "Find SUID binaries for privilege escalation",
        "Enumerate DNS records with dnsrecon",
        "Install Metasploit in Termux",
        "Brute-force SSH login with Hydra",
        "Dump NTLM hashes with Impacket secretsdump",
        "Decode a base64-encoded payload in bash",
        "Run BloodHound for Active Directory enum",
        "Web vulnerability scan with nikto",
        "Measure network throughput with iperf3",
        "HTTP load test with Apache Bench (ab)",
        "Craft custom TCP packets with hping3",
    ]
    print(c(C.CYAN, "\n  [*] Example topics:\n"))
    for i, t in enumerate(topics, 1):
        print(f"  {c(C.GRAY, str(i).rjust(2) + '.')} {t}")
    print()

def print_models():
    print(c(C.CYAN, "\n  [*] Popular OpenRouter models:\n"))
    models = [
        ("anthropic/claude-sonnet-4-5",      "Claude Sonnet 4.5 (recommended)"),
        ("anthropic/claude-haiku-4-5",        "Claude Haiku 4.5 (fast & cheap)"),
        ("openai/gpt-4o",                     "GPT-4o"),
        ("openai/gpt-4o-mini",                "GPT-4o Mini (fast)"),
        ("google/gemini-pro-1.5",             "Gemini Pro 1.5"),
        ("meta-llama/llama-3.1-70b-instruct", "Llama 3.1 70B (open source)"),
        ("mistralai/mistral-7b-instruct",     "Mistral 7B (lightweight)"),
    ]
    for model_id, desc in models:
        print(f"  {c(C.GREEN, model_id):<55} {c(C.GRAY, desc)}")
    print()

def format_response(text):
    try:
        width = min(os.get_terminal_size().columns, 100)
    except Exception:
        width = 80

    lines = text.split("\n")
    in_code = False
    out = []

    for line in lines:
        if line.startswith("```"):
            if not in_code:
                in_code = True
                lang = line[3:].strip() or "shell"
                out.append(c(C.GRAY, f"  ┌─[{lang}]"))
            else:
                in_code = False
                out.append(c(C.GRAY, "  └─"))
            continue

        if in_code:
            out.append(c(C.CYAN, f"  │ {line}"))
            continue

        s = line.strip()
        if s.startswith("[+]"):
            out.append(c(C.GREEN,   "  " + s))
        elif s.startswith("[-]"):
            out.append(c(C.RED,     "  " + s))
        elif s.startswith("[!]"):
            out.append(c(C.YELLOW,  "  " + s))
        elif s.startswith("[*]"):
            out.append(c(C.BLUE,    "  " + s))
        elif re.match(r'^#{1,3} ', s):
            heading = re.sub(r'^#{1,3} ', '', s)
            out.append("\n" + c(C.WHITE, f"  ▶ {heading}"))
        elif s.startswith(("- ", "* ")):
            out.append(c(C.WHITE, f"    • {s[2:]}"))
        elif s:
            wrapped = textwrap.fill(line, width=width - 4,
                                    initial_indent="  ",
                                    subsequent_indent="  ")
            wrapped = re.sub(r'`([^`]+)`',
                             lambda m: c(C.YELLOW, m.group(1)), wrapped)
            out.append(wrapped)
        else:
            out.append("")

    return "\n".join(out)

# ─── API Call ─────────────────────────────────────────────────────────────────
def query_openrouter(prompt, api_key, model, conversation_history):
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer":  "https://github.com/tonyprime/whitemadrid",
        "X-Title":       "WHITE MADRID by TONYPRIME",
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += conversation_history
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({
        "model":      model,
        "max_tokens": 1024,
        "messages":   messages,
    }).encode("utf-8")

    req = urllib.request.Request(API_URL, data=payload,
                                 headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"], None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            err = json.loads(body)
            msg = err.get("error", {})
            if isinstance(msg, dict):
                msg = msg.get("message", body)
            return "", str(msg)
        except Exception:
            return "", body
    except urllib.error.URLError as e:
        return "", f"Network error: {e.reason}"
    except Exception as e:
        return "", str(e)

# ─── Readline ─────────────────────────────────────────────────────────────────
def setup_readline():
    try:
        readline.read_history_file(HISTORY_FILE)
    except FileNotFoundError:
        pass
    readline.set_history_length(500)

def save_readline():
    try:
        readline.write_history_file(HISTORY_FILE)
    except Exception:
        pass

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    clear()
    print_banner()

    config  = load_config()
    api_key = get_api_key(config)
    model   = config.get("model", DEFAULT_MODEL)

    if not api_key:
        print(c(C.YELLOW, "  [!] No OpenRouter API key found."))
        print(c(C.GRAY,   "  Get a free key at: https://openrouter.ai/keys\n"))
        print(c(C.GRAY,   "  Option 1: export OPENROUTER_API_KEY='sk-or-...'"))
        print(c(C.GRAY,   "  Option 2: Enter below (saved to ~/.whitemadrid_config)\n"))
        try:
            key = input(c(C.GREEN, "  Enter OpenRouter API key: ")).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n" + c(C.RED, "  Aborted."))
            sys.exit(0)
        if not key:
            print(c(C.RED, "\n  [-] No key provided. Exiting."))
            sys.exit(1)
        config["api_key"] = key
        save_config(config)
        api_key = key
        print(c(C.GREEN, "\n  [+] API key saved to ~/.whitemadrid_config\n"))

    print(c(C.GREEN,   f"  [+] WHITE MADRID ready  •  model: {model}"))
    print(c(C.MAGENTA, f"  [*] Developer: {DEVELOPER}"))
    print(c(C.BLUE,    "  [*] Type 'help' for commands, 'stress' for network testing tools."))
    print(c(C.YELLOW,  "  [!] Authorized security research and CTF use only.\n"))

    setup_readline()
    conversation_history = []
    session_log          = []
    prompt_str = (
        c(C.WHITE,   "\nroot@") +
        c(C.CYAN,    "whitemadrid") +
        c(C.MAGENTA, "[TONYPRIME]") +
        c(C.WHITE,   ":~# ")
    ) if USE_COLOR else "\nroot@whitemadrid[TONYPRIME]:~# "

    while True:
        try:
            user_input = input(prompt_str).strip()
        except KeyboardInterrupt:
            print(c(C.GRAY, "\n  [*] Use 'exit' to quit."))
            continue
        except EOFError:
            print(c(C.GRAY, "\n  [*] Exiting WHITE MADRID..."))
            break

        if not user_input:
            continue

        cmd = user_input.lower().strip()

        if cmd in ("exit", "quit", "q"):
            print(c(C.GREEN, "\n  [+] Session ended. Stay ethical. — TONYPRIME\n"))
            break

        elif cmd == "clear":
            clear()
            print_banner()
            continue

        elif cmd == "help":
            print_help()
            continue

        elif cmd == "about":
            print_about()
            continue

        elif cmd == "topics":
            print_topics()
            continue

        elif cmd == "stress":
            print_stress_tools()
            continue

        elif cmd == "history":
            if not session_log:
                print(c(C.GRAY, "\n  [*] No queries this session yet.\n"))
            else:
                print(c(C.CYAN, "\n  [*] Session history:\n"))
                for i, q in enumerate(session_log, 1):
                    print(f"  {c(C.GRAY, str(i).rjust(3) + '.')} {q}")
                print()
            continue

        elif cmd == "model":
            print_models()
            try:
                new_model = input(c(C.GREEN,
                    f"  Current: {model}\n  New model (Enter to keep): ")).strip()
            except (KeyboardInterrupt, EOFError):
                print()
                continue
            if new_model:
                model = new_model
                config["model"] = model
                save_config(config)
                print(c(C.GREEN, f"  [+] Model set to: {model}\n"))
            continue

        elif cmd == "setkey":
            try:
                key = input(c(C.GREEN, "  New OpenRouter API key: ")).strip()
            except (KeyboardInterrupt, EOFError):
                print()
                continue
            if key:
                config["api_key"] = key
                save_config(config)
                api_key = key
                print(c(C.GREEN, "  [+] API key updated.\n"))
            continue

        elif user_input.startswith("!"):
            os.system(user_input[1:])
            continue

        # ── AI Query ──────────────────────────────────────────────────────
        session_log.append(user_input)
        print(c(C.GRAY, "\n  [*] Querying WHITE MADRID AI..."), end="", flush=True)

        response, error = query_openrouter(user_input, api_key, model,
                                           conversation_history)
        print("\r" + " " * 42 + "\r", end="", flush=True)

        if error:
            print(c(C.RED, f"\n  [-] API Error: {error}\n"))
            continue

        conversation_history.append({"role": "user",      "content": user_input})
        conversation_history.append({"role": "assistant", "content": response})
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        print()
        print(c(C.GRAY, "  " + "─" * 60))
        print(format_response(response))
        print(c(C.GRAY, "  " + "─" * 60))

    save_readline()


if __name__ == "__main__":
    main()
