#!/data/data/com.termux/files/usr/bin/bash
# WHITE MADRID v5.0 — Termux Setup Script
# Developer: TONYPRIME

clear
echo ""
echo "  ██╗    ██╗██╗  ██╗██╗████████╗███████╗"
echo "  ██║    ██║██║  ██║██║╚══██╔══╝██╔════╝"
echo "  ██║ █╗ ██║███████║██║   ██║   █████╗  "
echo "  ██║███╗██║██╔══██║██║   ██║   ██╔══╝  "
echo "  ╚███╔███╔╝██║  ██║██║   ██║   ███████╗"
echo "   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝"
echo "  ███╗   ███╗ █████╗ ██████╗ ██████╗ ██╗██████╗"
echo "  ████╗ ████║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗"
echo "  ██╔████╔██║███████║██║  ██║██████╔╝██║██║  ██║"
echo "  ██║╚██╔╝██║██╔══██║██║  ██║██╔══██╗██║██║  ██║"
echo "  ██║ ╚═╝ ██║██║  ██║██████╔╝██║  ██║██║██████╔╝"
echo "  ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝"
echo ""
echo "  v5.0 JARVIS Edition — Termux Setup"
echo "  Developer : TONYPRIME"
echo "  Features  : Hacker animation · Typing FX · Relax mode · 9 APIs"
echo "  ────────────────────────────────────────────────"
echo ""

BASHRC="$HOME/.bashrc"
DEST="$HOME/whitemadrid.py"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$SCRIPT_DIR/whitemadrid.py"

# ─────────────────────────────────────────────────────
step() { echo "  [*] $1"; }
ok()   { echo "  [+] $1"; }
warn() { echo "  [!] $1"; }
fail() { echo "  [-] $1"; }
# ─────────────────────────────────────────────────────

# ── Step 1: Update packages ───────────────────────────
step "Updating package list..."
pkg update -y -q 2>/dev/null
ok "Packages updated."
echo ""

# ── Step 2: Python ────────────────────────────────────
step "Checking Python..."
if ! command -v python3 &>/dev/null; then
    step "Installing Python..."
    pkg install python -y
    ok "Python installed: $(python3 --version)"
else
    ok "Found: $(python3 --version)"
fi
echo ""

# ── Step 3: readline ──────────────────────────────────
step "Installing readline (arrow key / history support)..."
pkg install libreadline -y -q 2>/dev/null
ok "readline ready."
echo ""

# ── Step 4: git ───────────────────────────────────────
step "Checking git..."
if ! command -v git &>/dev/null; then
    pkg install git -y -q
    ok "git installed."
else
    ok "Found: $(git --version)"
fi
echo ""

# ── Step 5: Core pentest tools ────────────────────────
step "Installing core tools (nmap, curl, wget, openssh, openssl)..."
pkg install nmap curl wget openssh openssl-tool -y -q 2>/dev/null
ok "Core tools ready."
echo ""

# ── Step 6: Optional extras ───────────────────────────
step "Installing optional extras (tmux, python-pip)..."
pkg install tmux -y -q 2>/dev/null
pip install requests --quiet --break-system-packages 2>/dev/null
ok "Extras installed."
echo ""

# ── Step 7: Copy whitemadrid.py ───────────────────────
step "Installing whitemadrid.py..."
if [ -f "$SRC" ]; then
    cp "$SRC" "$DEST"
    chmod +x "$DEST"
    ok "Installed to $DEST"
else
    warn "whitemadrid.py not found next to setup.sh"
    warn "Place both files in the same folder and re-run: bash setup.sh"
    echo ""
    exit 1
fi
echo ""

# ── Step 8: Reset old config ──────────────────────────
step "Resetting config for v5.0..."
rm -f "$HOME/.whitemadrid_config"
rm -f "$HOME/.whitemadrid_session.log"
ok "Old config cleared — fresh start."
echo ""

# ── Step 9: Shell alias ───────────────────────────────
step "Setting up shell alias..."
if ! grep -q "alias whitemadrid=" "$BASHRC" 2>/dev/null; then
    {
        echo ""
        echo "# WHITE MADRID — TONYPRIME"
        echo "alias whitemadrid='python3 ~/whitemadrid.py'"
        echo "alias wm='python3 ~/whitemadrid.py'"
    } >> "$BASHRC"
    ok "Alias 'whitemadrid' and 'wm' added to ~/.bashrc"
else
    sed -i "s|alias whitemadrid=.*|alias whitemadrid='python3 ~/whitemadrid.py'|" "$BASHRC"
    ok "Alias updated in ~/.bashrc"
fi
echo ""

# ── Step 10: Operator name ────────────────────────────
step "Setting your operator name..."
echo ""
read -p "  Enter your operator name (default: Operator): " OP_NAME
if [ -z "$OP_NAME" ]; then
    OP_NAME="Operator"
fi
ok "Operator set to: $OP_NAME"
echo ""

# ── Step 11: Multi-API Key Setup ──────────────────────
echo "  ────────────────────────────────────────────────"
echo "  [*] Multi-API Key Setup (9 Providers)"
echo ""
echo "  You only need ONE key to start."
echo "  Press Enter to skip any provider."
echo ""
echo "  ┌─────────────────────────────────────────────┐"
echo "  │  #   PROVIDER        FREE TIER              │"
echo "  │  ─────────────────────────────────────────  │"
echo "  │  1.  OpenRouter      10+ free models        │"
echo "  │  2.  Groq            fastest free — no card │"
echo "  │  3.  Gemini          1M tokens/day free     │"
echo "  │  4.  Anthropic       \$5 trial credits       │"
echo "  │  5.  OpenAI          \$5 trial credits       │"
echo "  │  6.  Together AI     \$1 trial credits       │"
echo "  │  7.  Mistral         free experimental      │"
echo "  │  8.  Cohere          1000 req/month free    │"
echo "  │  9.  HuggingFace     free with HF account   │"
echo "  └─────────────────────────────────────────────┘"
echo ""
echo "  Get free keys:"
echo "    OpenRouter → https://openrouter.ai/keys"
echo "    Groq       → https://console.groq.com/keys"
echo "    Gemini     → https://aistudio.google.com/app/apikey"
echo "    Cohere     → https://dashboard.cohere.com/api-keys"
echo ""
echo "  ────────────────────────────────────────────────"
echo ""

PROV_IDS=(    ""  "openrouter"    "groq"    "gemini"    "anthropic"    "openai"    "together"    "mistral"    "cohere"    "huggingface" )
PROV_NAMES=(  ""  "OpenRouter"    "Groq"    "Gemini"    "Anthropic"    "OpenAI"    "Together AI" "Mistral"    "Cohere"    "HuggingFace" )
PROV_VARS=(   ""  "OPENROUTER_API_KEY" "GROQ_API_KEY" "GEMINI_API_KEY" "ANTHROPIC_API_KEY" "OPENAI_API_KEY" "TOGETHER_API_KEY" "MISTRAL_API_KEY" "COHERE_API_KEY" "HUGGINGFACE_API_KEY" )
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
    read -p "  [${i}] ${PROV_NAMES[$i]} key: " KEY
    if [ -n "$KEY" ]; then
        KEYS[$i]="$KEY"
        ok "${PROV_NAMES[$i]} key saved."
    fi
done

echo ""

# Find default provider
DEFAULT_PROV="openrouter"
DEFAULT_MODEL="meta-llama/llama-3.1-8b-instruct:free"
DEFAULT_NAME="OpenRouter"

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

# ── Step 12: Write config JSON ────────────────────────
step "Writing config file..."

python3 << PYEOF
import json, os

keys = {}
$(for i in 1 2 3 4 5 6 7 8 9; do
    if [ -n "${KEYS[$i]}" ]; then
        echo "keys['${PROV_IDS[$i]}'] = '${KEYS[$i]}'"
    fi
done)

cfg = {
    "provider":      "$DEFAULT_PROV",
    "model":         "$DEFAULT_MODEL",
    "api_keys":      keys,
    "operator":      "$OP_NAME",
    "session_count": 0,
}

path = os.path.expanduser("~/.whitemadrid_config")
with open(path, "w") as f:
    json.dump(cfg, f, indent=2)

print(f"  [+] Config saved → {path}")
print(f"  [+] Operator: $OP_NAME")
print(f"  [+] {len(keys)} API key(s) stored.")
PYEOF

echo ""

# ── Step 13: Export env vars to .bashrc ───────────────
step "Exporting API keys to environment..."
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

# Handle no keys entered
if [ ${#KEYS[@]} -eq 0 ]; then
    warn "No keys entered. Writing minimal config..."
    python3 -c "
import json, os
cfg = {
    'provider': 'openrouter',
    'model': 'meta-llama/llama-3.1-8b-instruct:free',
    'api_keys': {},
    'operator': '$OP_NAME',
    'session_count': 0
}
with open(os.path.expanduser('~/.whitemadrid_config'), 'w') as f:
    json.dump(cfg, f, indent=2)
"
    warn "Add keys later inside WHITE MADRID with: setkey <provider>"
    echo ""
fi

# ── Done ──────────────────────────────────────────────
echo "  ════════════════════════════════════════════════"
echo "  [+] WHITE MADRID v5.0 setup complete!"
echo "      Operator : $OP_NAME"
echo "      Provider : $DEFAULT_NAME"
echo "      Model    : $DEFAULT_MODEL"
echo "  ════════════════════════════════════════════════"
echo ""
echo "  Launch:"
echo "    source ~/.bashrc && whitemadrid"
echo "    source ~/.bashrc && wm          ← short alias"
echo ""
echo "  Or directly:"
echo "    python3 ~/whitemadrid.py"
echo ""
echo "  ── What happens on launch ───────────────────"
echo "    Matrix rain      → falls before banner"
echo "    Glitch banner    → title resolves from noise"
echo "    Hex dump scan    → fake memory read"
echo "    Progress bars    → AI modules loading"
echo "    Boot log         → kernel-style scroll"
echo "    Time greeting    → morning/afternoon/night"
echo "    Typing animation → all AI text types itself"
echo ""
echo "  ── Key commands ─────────────────────────────"
echo "    help             full command reference"
echo "    apis             browse all 9 providers"
echo "    provider groq    switch to Groq (fastest free)"
echo "    provider gemini  switch to Gemini (1M/day free)"
echo "    freemode         auto-select free model"
echo "    setkey <name>    add/update API key"
echo "    install          pentest tool installer"
echo "    relax            chill mode — games & jokes"
echo "    joke             random hacker joke"
echo "    wisdom           hacker wisdom quote"
echo "    trivia           security trivia quiz"
echo ""
echo "  ── Error fixes built in ─────────────────────"
echo "    HTTP 403 / 1010  → type: provider groq"
echo "    utf-8 decode err → fixed automatically"
echo "    Out of credits   → type: freemode"
echo "    No key error     → type: setkey <provider>"
echo ""
echo "  ════════════════════════════════════════════════"
echo "  Stay ethical. — TONYPRIME"
echo "  ════════════════════════════════════════════════"
echo ""
