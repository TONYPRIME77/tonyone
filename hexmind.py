#!/usr/bin/env python3
"""
HexMind AI — Ethical Hacking Terminal Assistant
Compatible with Termux (Android) and any Unix terminal
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
    DIM     = "\033[2m"
    GREEN   = "\033[92m"
    BGREEN  = "\033[1;92m"
    CYAN    = "\033[96m"
    BLUE    = "\033[94m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"
    BG_DARK = "\033[40m"

def supports_color():
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

USE_COLOR = supports_color()

def c(color, text):
    return f"{color}{text}{C.RESET}" if USE_COLOR else text

# ─── Banner ───────────────────────────────────────────────────────────────────
BANNER = r"""
 ██╗  ██╗███████╗██╗  ██╗███╗   ███╗██╗███╗   ██╗██████╗
 ██║  ██║██╔════╝╚██╗██╔╝████╗ ████║██║████╗  ██║██╔══██╗
 ███████║█████╗   ╚███╔╝ ██╔████╔██║██║██╔██╗ ██║██║  ██║
 ██╔══██║██╔══╝   ██╔██╗ ██║╚██╔╝██║██║██║╚██╗██║██║  ██║
 ██║  ██║███████╗██╔╝ ██╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
 ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝"""

VERSION  = "v2.0"
TAGLINE  = "Ethical Hacking AI Assistant"
API_URL  = "https://api.anthropic.com/v1/messages"
MODEL    = "claude-sonnet-4-6"
API_VER  = "2023-06-01"
HISTORY_FILE = os.path.expanduser("~/.hexmind_history")
CONFIG_FILE  = os.path.expanduser("~/.hexmind_config")

# ─── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are HexMind, an elite ethical hacking and cybersecurity AI running in a terminal. You assist penetration testers, security researchers, and CTF players.

You help with:
- Reconnaissance & OSINT (Shodan, theHarvester, Maltego, Recon-ng)
- Network scanning & enumeration (Nmap, Netcat, Masscan)
- Web app testing (SQLi, XSS, SSRF, LFI, IDOR, RCE)
- Exploitation (Metasploit, Exploit-DB, custom exploits)
- Password attacks (Hashcat, John the Ripper, Hydra, Medusa)
- Privilege escalation (Linux & Windows, sudo, SUID, tokens)
- Reverse shells & payload generation
- CTF challenges, forensics, steganography, crypto
- Network traffic analysis (Wireshark, tcpdump, tshark)
- Active Directory attacks (BloodHound, Impacket, CrackMapExec)
- Mobile/Android pentesting (in Termux context)
- OSCP/CEH/PNPT exam preparation

RULES:
1. Only assist with LEGAL, AUTHORIZED, or CTF/educational security work.
2. If no authorization context is clear for a real target, remind about ethics and legality.
3. Provide REAL commands and tools with explanations.
4. Use [+] for success/tips, [-] for errors/warnings, [*] for info, [!] for important notes.
5. Put all commands in code blocks using backtick markdown.
6. Note when root/sudo is required.
7. Be concise but thorough — like a senior pentester briefing a colleague.
8. When relevant, mention if a tool is available/installable in Termux."""

# ─── Config ───────────────────────────────────────────────────────────────────
def load_config():
    config = {"api_key": "", "stream": False}
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
    # 1. From config file
    if config.get("api_key"):
        return config["api_key"]
    # 2. From environment variable
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key
    return None

# ─── Terminal Helpers ─────────────────────────────────────────────────────────
def clear():
    os.system("clear" if os.name != "nt" else "cls")

def print_banner():
    print(c(C.GREEN, BANNER))
    print(c(C.BGREEN, f"  {VERSION} — {TAGLINE}".center(62)))
    print(c(C.GRAY,   "  " + "─" * 60))
    print(c(C.GRAY,   f"  Powered by Claude · For authorized security research only"))
    print(c(C.GRAY,   "  " + "─" * 60))
    print()

def print_help():
    help_text = [
        (c(C.CYAN,   "Commands:"), ""),
        (c(C.GREEN,  "  help"),    "Show this help"),
        (c(C.GREEN,  "  clear"),   "Clear the terminal"),
        (c(C.GREEN,  "  history"), "Show session history"),
        (c(C.GREEN,  "  setkey"),  "Set your Anthropic API key"),
        (c(C.GREEN,  "  topics"),  "Show example topics"),
        (c(C.GREEN,  "  exit"),    "Quit HexMind"),
        ("", ""),
        (c(C.CYAN,   "Tips:"), ""),
        (c(C.GRAY,   "  ↑/↓"),    "Navigate command history"),
        (c(C.GRAY,   "  Ctrl+C"), "Cancel current query"),
        (c(C.GRAY,   "  Ctrl+D"), "Exit"),
    ]
    for cmd, desc in help_text:
        if desc:
            print(f"  {cmd:<30} {c(C.GRAY, desc)}")
        else:
            print(f"  {cmd}")
    print()

def print_topics():
    topics = [
        "Scan a subnet with nmap",
        "Enumerate SMB shares",
        "Generate a Python reverse shell",
        "Crack MD5 hash with hashcat",
        "Linux privilege escalation checklist",
        "Bypass WAF for SQL injection",
        "Set up a Metasploit listener",
        "Find SUID binaries for privesc",
        "Enumerate DNS with dnsrecon",
        "Install Metasploit in Termux",
        "Brute force SSH with Hydra",
        "Extract NTLM hashes with Impacket",
        "Decode a base64-encoded payload",
        "Run BloodHound for AD enumeration",
        "Scan for web vulnerabilities with nikto",
    ]
    print(c(C.CYAN, "\n  [*] Example queries:\n"))
    for i, t in enumerate(topics, 1):
        print(f"  {c(C.GRAY, str(i).rjust(2) + '.')} {t}")
    print()

def format_response(text):
    """Format AI response with colors and indentation."""
    terminal_width = min(os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else 80, 100)
    lines = text.split("\n")
    in_code_block = False
    output = []

    for line in lines:
        # Code block toggle
        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                lang = line[3:].strip() or "shell"
                output.append(c(C.GRAY, f"  ┌─[{lang}]"))
            else:
                in_code_block = False
                output.append(c(C.GRAY, "  └─"))
            continue

        if in_code_block:
            output.append(c(C.CYAN, f"  │ {line}"))
            continue

        # Prefix coloring
        stripped = line.strip()
        if stripped.startswith("[+]"):
            output.append(c(C.GREEN,  "  " + stripped))
        elif stripped.startswith("[-]"):
            output.append(c(C.RED,    "  " + stripped))
        elif stripped.startswith("[!]"):
            output.append(c(C.YELLOW, "  " + stripped))
        elif stripped.startswith("[*]"):
            output.append(c(C.BLUE,   "  " + stripped))
        elif re.match(r'^#{1,3} ', stripped):
            # Markdown headings
            heading = re.sub(r'^#{1,3} ', '', stripped)
            output.append("\n" + c(C.BGREEN, f"  ▶ {heading}"))
        elif stripped.startswith("- ") or stripped.startswith("* "):
            output.append(c(C.WHITE, f"    • {stripped[2:]}"))
        else:
            # Wrap long lines
            if line.strip():
                wrapped = textwrap.fill(line, width=terminal_width - 4,
                                        initial_indent="  ", subsequent_indent="  ")
                # Inline code coloring
                wrapped = re.sub(r'`([^`]+)`', lambda m: c(C.YELLOW, m.group(1)), wrapped)
                output.append(wrapped)
            else:
                output.append("")

    return "\n".join(output)

# ─── API Call ─────────────────────────────────────────────────────────────────
def query_claude(prompt, api_key, conversation_history):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": API_VER,
    }

    # Build messages from conversation history + new prompt
    messages = conversation_history + [{"role": "user", "content": prompt}]

    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": messages,
    }).encode("utf-8")

    req = urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "content" in data and data["content"]:
                return data["content"][0].get("text", ""), None
            return "", "Empty response from API"
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            err = json.loads(body)
            return "", err.get("error", {}).get("message", body)
        except Exception:
            return "", body
    except urllib.error.URLError as e:
        return "", f"Network error: {e.reason}"
    except Exception as e:
        return "", str(e)

# ─── Setup readline history ───────────────────────────────────────────────────
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

# ─── Main Loop ────────────────────────────────────────────────────────────────
def main():
    clear()
    print_banner()

    config = load_config()
    api_key = get_api_key(config)

    if not api_key:
        print(c(C.YELLOW, "  [!] No API key found."))
        print(c(C.GRAY,   "  Set it via environment variable or enter it now:\n"))
        print(c(C.GRAY,   "  Option 1: export ANTHROPIC_API_KEY='sk-ant-...'"))
        print(c(C.GRAY,   "  Option 2: Enter below (saved to ~/.hexmind_config)\n"))
        try:
            key = input(c(C.GREEN, "  Enter Anthropic API key: ")).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n" + c(C.RED, "  Aborted."))
            sys.exit(0)
        if not key:
            print(c(C.RED, "\n  [-] No key provided. Exiting."))
            sys.exit(1)
        config["api_key"] = key
        save_config(config)
        api_key = key
        print(c(C.GREEN, "\n  [+] API key saved to ~/.hexmind_config\n"))

    print(c(C.GREEN,  "  [+] HexMind ready. Type 'help' for commands, 'topics' for ideas."))
    print(c(C.YELLOW, "  [!] For authorized security research and CTF use only.\n"))

    setup_readline()
    conversation_history = []
    session_log = []
    prompt_str = c(C.BGREEN, "\nroot@hexmind:~# ") if USE_COLOR else "\nroot@hexmind:~# "

    while True:
        try:
            user_input = input(prompt_str).strip()
        except KeyboardInterrupt:
            print(c(C.GRAY, "\n  [*] Use 'exit' to quit."))
            continue
        except EOFError:
            print(c(C.GRAY, "\n  [*] Exiting HexMind..."))
            break

        if not user_input:
            continue

        # Built-in commands
        cmd = user_input.lower()

        if cmd in ("exit", "quit", "q"):
            print(c(C.GREEN, "\n  [+] Session ended. Stay ethical.\n"))
            break

        elif cmd == "clear":
            clear()
            print_banner()
            continue

        elif cmd == "help":
            print_help()
            continue

        elif cmd == "topics":
            print_topics()
            continue

        elif cmd == "history":
            if not session_log:
                print(c(C.GRAY, "\n  [*] No queries yet this session.\n"))
            else:
                print(c(C.CYAN, "\n  [*] Session history:\n"))
                for i, q in enumerate(session_log, 1):
                    print(f"  {c(C.GRAY, str(i).rjust(3) + '.')} {q}")
                print()
            continue

        elif cmd == "setkey":
            try:
                key = input(c(C.GREEN, "  New API key: ")).strip()
            except (KeyboardInterrupt, EOFError):
                print()
                continue
            if key:
                config["api_key"] = key
                save_config(config)
                api_key = key
                print(c(C.GREEN, "  [+] API key updated.\n"))
            continue

        elif cmd.startswith("!"):
            # Shell passthrough (useful in Termux)
            os.system(user_input[1:])
            continue

        # ── Send to Claude ──
        session_log.append(user_input)
        print(c(C.GRAY, "\n  [*] Querying HexMind AI..."), end="", flush=True)

        response, error = query_claude(user_input, api_key, conversation_history)

        # Clear the "querying" line
        print("\r" + " " * 40 + "\r", end="", flush=True)

        if error:
            print(c(C.RED, f"\n  [-] API Error: {error}\n"))
            continue

        # Update conversation history (keep last 10 turns to manage context)
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": response})
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        print()
        print(c(C.GRAY, "  " + "─" * 58))
        print(format_response(response))
        print(c(C.GRAY, "  " + "─" * 58))

    save_readline()


if __name__ == "__main__":
    main()
