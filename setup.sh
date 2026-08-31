#!/data/data/com.termux/files/usr/bin/bash
# ═══════════════════════════════════════════════════════
#  WHITE MADRID v6.0 — JARVIS Edition
#  Termux Setup Script
#  Developer : TONYPRIME
# ═══════════════════════════════════════════════════════

clear

# ── Colors ──────────────────────────────────────────────
R="\033[91m"; G="\033[92m"; Y="\033[93m"
B="\033[94m"; M="\033[95m"; C="\033[96m"
W="\033[97m"; GR="\033[90m"; BOLD="\033[1m"; RESET="\033[0m"

p()  { echo -e "${C}  [*]${RESET} $1"; }
ok() { echo -e "${G}  [+]${RESET} $1"; }
wn() { echo -e "${Y}  [!]${RESET} $1"; }
er() { echo -e "${R}  [-]${RESET} $1"; }
ln() { echo -e "${GR}  ────────────────────────────────────────────────${RESET}"; }

# ── Banner ───────────────────────────────────────────────
echo ""
echo -e "${W}${BOLD}  ██╗    ██╗██╗  ██╗██╗████████╗███████╗${RESET}"
echo -e "${W}${BOLD}  ██║    ██║██║  ██║██║╚══██╔══╝██╔════╝${RESET}"
echo -e "${W}${BOLD}  ██║ █╗ ██║███████║██║   ██║   █████╗  ${RESET}"
echo -e "${W}${BOLD}  ██║███╗██║██╔══██║██║   ██║   ██╔══╝  ${RESET}"
echo -e "${W}${BOLD}  ╚███╔███╔╝██║  ██║██║   ██║   ███████╗${RESET}"
echo -e "${W}${BOLD}   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝${RESET}"
echo -e "${W}${BOLD}  ███╗   ███╗ █████╗ ██████╗ ██████╗ ██╗██████╗ ${RESET}"
echo -e "${W}${BOLD}  ████╗ ████║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗${RESET}"
echo -e "${W}${BOLD}  ██╔████╔██║███████║██║  ██║██████╔╝██║██║  ██║${RESET}"
echo -e "${W}${BOLD}  ██║╚██╔╝██║██╔══██║██║  ██║██╔══██╗██║██║  ██║${RESET}"
echo -e "${W}${BOLD}  ██║ ╚═╝ ██║██║  ██║██████╔╝██║  ██║██║██████╔╝${RESET}"
echo -e "${W}${BOLD}  ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝${RESET}"
echo ""
echo -e "${C}${BOLD}  v6.0 JARVIS Edition — Full Setup${RESET}"
echo -e "${GR}  Developer  : TONYPRIME${RESET}"
echo -e "${GR}  Features   : Hacker Animation · JARVIS AI · Teaching Mode${RESET}"
echo -e "${GR}             : 9 API Providers · Scammer Reporter · Model Tester${RESET}"
ln
echo ""

BASHRC="$HOME/.bashrc"
DEST="$HOME/whitemadrid.py"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$SCRIPT_DIR/whitemadrid.py"

# ══════════════════════════════════════════════════════
#  STEP 1 — Update packages
# ══════════════════════════════════════════════════════
p "Updating package list..."
pkg update -y -q 2>/dev/null && ok "Packages updated." || wn "Update had warnings — continuing."
echo ""

# ══════════════════════════════════════════════════════
#  STEP 2 — Python
# ══════════════════════════════════════════════════════
p "Checking Python 3..."
if ! command -v python3 &>/dev/null; then
    p "Installing Python..."
    pkg install python -y
    ok "Python installed: $(python3 --version 2>&1)"
else
    ok "Found: $(python3 --version 2>&1)"
fi
echo ""

# ══════════════════════════════════════════════════════
#  STEP 3 — readline (arrow keys + history)
# ══════════════════════════════════════════════════════
p "Installing readline support..."
pkg install libreadline -y -q 2>/dev/null
ok "readline ready."
echo ""

# ══════════════════════════════════════════════════════
#  STEP 4 — git
# ══════════════════════════════════════════════════════
p "Checking git..."
if ! command -v git &>/dev/null; then
    pkg install git -y -q && ok "git installed." || wn "git install failed."
else
    ok "Found: $(git --version)"
fi
echo ""

# ══════════════════════════════════════════════════════
#  STEP 5 — Core tools
# ══════════════════════════════════════════════════════
p "Installing core tools (nmap, curl, wget, openssh, openssl)..."
pkg install nmap curl wget openssh openssl-tool -y -q 2>/dev/null
ok "Core tools ready."
echo ""

# ══════════════════════════════════════════════════════
#  STEP 6 — Optional extras
# ══════════════════════════════════════════════════════
p "Installing optional extras (tmux, python-pip)..."
pkg install tmux -y -q 2>/dev/null
pip install requests --quiet --break-system-packages 2>/dev/null
ok "Extras done."
echo ""

# ══════════════════════════════════════════════════════
#  STEP 7 — Install whitemadrid.py
# ══════════════════════════════════════════════════════
p "Installing whitemadrid.py..."
if [ -f "$SRC" ]; then
    cp "$SRC" "$DEST"
    chmod +x "$DEST"
    ok "Installed → $DEST"
else
    er "whitemadrid.py not found next to setup.sh"
    er "Put both files in the same folder and re-run: bash setup.sh"
    echo ""
    exit 1
fi
echo ""

# ══════════════════════════════════════════════════════
#  STEP 8 — Reset old config (important for v6.0)
# ══════════════════════════════════════════════════════
p "Resetting config for v6.0..."
rm -f "$HOME/.whitemadrid_config"
rm -f "$HOME/.whitemadrid_session.log"
ok "Config cleared — fresh v6.0 start."
echo ""

# ══════════════════════════════════════════════════════
#  STEP 9 — Shell aliases
# ══════════════════════════════════════════════════════
p "Setting up shell aliases..."
if ! grep -q "alias whitemadrid=" "$BASHRC" 2>/dev/null; then
    {
        echo ""
        echo "# WHITE MADRID v6.0 — TONYPRIME"
        echo "alias whitemadrid='python3 ~/whitemadrid.py'"
        echo "alias wm='python3 ~/whitemadrid.py'"
    } >> "$BASHRC"
    ok "Aliases 'whitemadrid' and 'wm' added to ~/.bashrc"
else
    sed -i "s|alias whitemadrid=.*|alias whitemadrid='python3 ~/whitemadrid.py'|" "$BASHRC"
    ok "Aliases updated in ~/.bashrc"
fi
echo ""

# ══════════════════════════════════════════════════════
#  STEP 10 — Operator name
# ══════════════════════════════════════════════════════
ln
p "Operator Setup"
echo ""
echo -e "${GR}  This name appears in your prompt and greetings.${RESET}"
echo ""
read -p "  Enter your operator name (default: Operator): " OP_NAME
if [ -z "$OP_NAME" ]; then
    OP_NAME="Operator"
fi
ok "Operator: $OP_NAME"
echo ""

# ══════════════════════════════════════════════════════
#  STEP 11 — Multi-API Key Setup
# ══════════════════════════════════════════════════════
ln
echo -e "${C}${BOLD}  [*] Multi-API Key Setup — 9 Providers${RESET}"
echo ""
echo -e "${W}  You only need ONE key to start. Press Enter to skip any.${RESET}"
echo ""
echo -e "${G}${BOLD}  ┌──────────────────────────────────────────────────────┐${RESET}"
echo -e "${G}${BOLD}  │  #   PROVIDER        FREE TIER                      │${RESET}"
echo -e "${G}${BOLD}  │  ──────────────────────────────────────────────────  │${RESET}"
echo -e "${G}${BOLD}  │  1.  OpenRouter      10+ free models (:free suffix)  │${RESET}"
echo -e "${G}${BOLD}  │  2.  Groq            Fastest free — no card needed   │${RESET}"
echo -e "${G}${BOLD}  │  3.  Gemini          1M tokens/day free              │${RESET}"
echo -e "${G}${BOLD}  │  4.  Anthropic       \$5 free trial credits           │${RESET}"
echo -e "${G}${BOLD}  │  5.  OpenAI          \$5 free trial credits           │${RESET}"
echo -e "${G}${BOLD}  │  6.  Together AI     \$1 free credits                 │${RESET}"
echo -e "${G}${BOLD}  │  7.  Mistral         Free experimental tier          │${RESET}"
echo -e "${G}${BOLD}  │  8.  Cohere          1000 free req/month forever     │${RESET}"
echo -e "${G}${BOLD}  │  9.  HuggingFace     Free with HF account            │${RESET}"
echo -e "${G}${BOLD}  └──────────────────────────────────────────────────────┘${RESET}"
echo ""
echo -e "${GR}  Get free keys:${RESET}"
echo -e "${B}    OpenRouter → https://openrouter.ai/keys${RESET}"
echo -e "${B}    Groq       → https://console.groq.com/keys${RESET}"
echo -e "${B}    Gemini     → https://aistudio.google.com/app/apikey${RESET}"
echo -e "${B}    Cohere     → https://dashboard.cohere.com/api-keys${RESET}"
echo ""
ln
echo ""

# Provider metadata arrays
PROV_IDS=(    ""  "openrouter"    "groq"    "gemini"    "anthropic"    "openai"    "together"    "mistral"    "cohere"    "huggingface" )
PROV_NAMES=(  ""  "OpenRouter"    "Groq"    "Gemini"    "Anthropic"    "OpenAI"    "Together AI" "Mistral"    "Cohere"    "HuggingFace" )
PROV_VARS=(   ""
    "OPENROUTER_API_KEY"
    "GROQ_API_KEY"
    "GEMINI_API_KEY"
    "ANTHROPIC_API_KEY"
    "OPENAI_API_KEY"
    "TOGETHER_API_KEY"
    "MISTRAL_API_KEY"
    "COHERE_API_KEY"
    "HUGGINGFACE_API_KEY"
)
PROV_MODELS=( ""
    "meta-llama/llama-3.1-8b-instruct:free"
    "llama-3.1-8b-instant"
    "gemini-1.5-flash"
    "claude-haiku-4-5"
    "gpt-4o-mini"
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    "open-mistral-7b"
    "command-r"
    "mistralai/Mistral-7B-Instruct-v0.3"
)

declare -A KEYS

for i in 1 2 3 4 5 6 7 8 9; do
    read -p "  [${i}] ${PROV_NAMES[$i]} key (Enter to skip): " KEY
    if [ -n "$KEY" ]; then
        KEYS[$i]="$KEY"
        ok "${PROV_NAMES[$i]} key saved."
    fi
done

echo ""

# Find default provider — first one with a key
DEFAULT_PROV="openrouter"
DEFAULT_MODEL="meta-llama/llama-3.1-8b-instruct:free"
DEFAULT_NAME="OpenRouter (no key — free models)"

for i in 1 2 3 4 5 6 7 8 9; do
    if [ -n "${KEYS[$i]}" ]; then
        DEFAULT_PROV="${PROV_IDS[$i]}"
        DEFAULT_MODEL="${PROV_MODELS[$i]}"
        DEFAULT_NAME="${PROV_NAMES[$i]}"
        ok "Default provider: ${PROV_NAMES[$i]}"
        ok "Default model:    ${PROV_MODELS[$i]}"
        break
    fi
done

# ══════════════════════════════════════════════════════
#  STEP 12 — Write config JSON
# ══════════════════════════════════════════════════════
p "Writing v6.0 config..."

python3 << PYEOF
import json, os

keys = {}
$(for i in 1 2 3 4 5 6 7 8 9; do
    if [ -n "${KEYS[$i]}" ]; then
        echo "keys['${PROV_IDS[$i]}'] = '${KEYS[$i]}'"
    fi
done)

cfg = {
    "provider":       "$DEFAULT_PROV",
    "model":          "$DEFAULT_MODEL",
    "api_keys":       keys,
    "operator":       "$OP_NAME",
    "session_count":  0,
    "teaching_mode":  False,
    "theme":          "green",
    "auto_suggest":   True,
}

path = os.path.expanduser("~/.whitemadrid_config")
with open(path, "w") as f:
    json.dump(cfg, f, indent=2)

print(f"  [+] Config saved → {path}")
print(f"  [+] Operator : $OP_NAME")
print(f"  [+] Provider : $DEFAULT_NAME")
print(f"  [+] Model    : $DEFAULT_MODEL")
print(f"  [+] {len(keys)} API key(s) stored.")
PYEOF

echo ""

# ══════════════════════════════════════════════════════
#  STEP 13 — Export keys to .bashrc
# ══════════════════════════════════════════════════════
p "Exporting API keys to environment..."
for i in 1 2 3 4 5 6 7 8 9; do
    if [ -n "${KEYS[$i]}" ]; then
        VAR="${PROV_VARS[$i]}"
        KEY="${KEYS[$i]}"
        if ! grep -q "$VAR" "$BASHRC" 2>/dev/null; then
            echo "export $VAR='$KEY'" >> "$BASHRC"
        else
            sed -i "s|export $VAR=.*|export $VAR='$KEY'|" "$BASHRC"
        fi
    fi
done
ok "Keys exported to ~/.bashrc"
echo ""

# Handle zero keys — write minimal config
if [ ${#KEYS[@]} -eq 0 ]; then
    wn "No keys entered — writing minimal config."
    python3 -c "
import json, os
cfg = {
    'provider': 'openrouter',
    'model': 'meta-llama/llama-3.1-8b-instruct:free',
    'api_keys': {},
    'operator': '$OP_NAME',
    'session_count': 0,
    'teaching_mode': False,
    'theme': 'green',
    'auto_suggest': True,
}
with open(os.path.expanduser('~/.whitemadrid_config'), 'w') as f:
    json.dump(cfg, f, indent=2)
print('  [+] Minimal config written.')
"
    wn "Add keys later inside WHITE MADRID: setkey <provider>"
    echo ""
fi

# ══════════════════════════════════════════════════════
#  DONE
# ══════════════════════════════════════════════════════
echo ""
echo -e "${G}${BOLD}  ════════════════════════════════════════════════${RESET}"
echo -e "${G}${BOLD}  [+] WHITE MADRID v6.0 setup complete!${RESET}"
echo -e "${GR}      Operator : $OP_NAME${RESET}"
echo -e "${GR}      Provider : $DEFAULT_NAME${RESET}"
echo -e "${GR}      Model    : $DEFAULT_MODEL${RESET}"
echo -e "${G}${BOLD}  ════════════════════════════════════════════════${RESET}"
echo ""
echo -e "${W}${BOLD}  Launch WHITE MADRID:${RESET}"
echo -e "${G}    source ~/.bashrc && whitemadrid${RESET}"
echo -e "${GR}    source ~/.bashrc && wm          ← short alias${RESET}"
echo ""
echo -e "${W}${BOLD}  Or directly:${RESET}"
echo -e "${G}    python3 ~/whitemadrid.py${RESET}"
echo ""
ln
echo -e "${C}${BOLD}  What happens on launch:${RESET}"
echo -e "${GR}    Matrix rain      → falling characters before banner${RESET}"
echo -e "${GR}    Glitch banner    → title resolves from noise${RESET}"
echo -e "${GR}    Hex dump         → fake memory scan${RESET}"
echo -e "${GR}    Progress bars    → AI modules loading${RESET}"
echo -e "${GR}    Boot log         → kernel-style scroll${RESET}"
echo -e "${GR}    Time greeting    → morning/afternoon/evening/night${RESET}"
echo -e "${GR}    Typing animation → all AI text types itself${RESET}"
echo ""
ln
echo -e "${C}${BOLD}  First commands to try:${RESET}"
echo -e "${G}    qs               ${GR}← quick start guide (do this first!)${RESET}"
echo -e "${G}    testmodels       ${GR}← test which providers are online${RESET}"
echo -e "${G}    teach            ${GR}← beginner learning mode${RESET}"
echo -e "${G}    report           ${GR}← report Instagram scammer${RESET}"
echo -e "${G}    help             ${GR}← full command reference${RESET}"
echo -e "${G}    apis             ${GR}← browse all 9 AI providers${RESET}"
echo -e "${G}    install          ${GR}← install pentest tools${RESET}"
echo -e "${G}    relax            ${GR}← games, jokes, trivia${RESET}"
echo ""
ln
echo -e "${C}${BOLD}  Key commands for AI issues:${RESET}"
echo -e "${Y}    testmodels       ${GR}← find which providers work${RESET}"
echo -e "${Y}    provider groq    ${GR}← fastest free, no Cloudflare${RESET}"
echo -e "${Y}    provider gemini  ${GR}← 1M tokens/day free${RESET}"
echo -e "${Y}    freemode         ${GR}← auto-select free model${RESET}"
echo -e "${Y}    setkey <name>    ${GR}← add/update API key${RESET}"
echo ""
ln
echo -e "${C}${BOLD}  Free API keys (no credit card):${RESET}"
echo -e "${B}    OpenRouter  → https://openrouter.ai/keys${RESET}"
echo -e "${B}    Groq        → https://console.groq.com/keys${RESET}"
echo -e "${B}    Gemini      → https://aistudio.google.com/app/apikey${RESET}"
echo -e "${B}    Cohere      → https://dashboard.cohere.com/api-keys${RESET}"
echo ""
ln
echo -e "${G}${BOLD}  Stay ethical. — TONYPRIME${RESET}"
ln
echo ""
