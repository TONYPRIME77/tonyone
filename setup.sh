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
echo "  ────────────────────────────────────────────────"
echo ""

BASHRC="$HOME/.bashrc"
DEST="$HOME/whitemadrid.py"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$SCRIPT_DIR/whitemadrid.py"

# ── Step 1: Update packages ───────────────────────────
echo "  [*] Updating package list..."
pkg update -y -q 2>/dev/null
echo "  [+] Done."
echo ""

# ── Step 2: Python ────────────────────────────────────
echo "  [*] Checking Python..."
if ! command -v python3 &>/dev/null; then
    echo "  [*] Installing Python..."
    pkg install python -y
else
    echo "  [+] $(python3 --version)"
fi
echo ""

# ── Step 3: readline ──────────────────────────────────
echo "  [*] Installing readline (arrow key support)..."
pkg install libreadline -y -q 2>/dev/null
echo "  [+] Done."
echo ""

# ── Step 4: git ───────────────────────────────────────
echo "  [*] Checking git..."
if ! command -v git &>/dev/null; then
    pkg install git -y -q
    echo "  [+] git installed."
else
    echo "  [+] $(git --version)"
fi
echo ""

# ── Step 5: Core pentest tools ────────────────────────
echo "  [*] Installing core tools..."
pkg install nmap curl wget openssh openssl-tool -y -q 2>/dev/null
echo "  [+] nmap, curl, wget, openssh, openssl ready."
echo ""

# ── Step 6: Copy whitemadrid.py ───────────────────────
echo "  [*] Installing whitemadrid.py..."
if [ -f "$SRC" ]; then
    cp "$SRC" "$DEST"
    chmod +x "$DEST"
    echo "  [+] Installed to $DEST"
else
    echo "  [!] whitemadrid.py not found next to setup.sh"
    echo "      Place both files in the same folder and re-run."
    echo ""
    exit 1
fi
echo ""

# ── Step 7: Clear old config ──────────────────────────
echo "  [*] Resetting config for v5.0..."
rm -f "$HOME/.whitemadrid_config"
rm -f "$HOME/.whitemadrid_session.log"
echo "  [+] Config cleared — fresh start."
echo ""

# ── Step 8: Shell alias ───────────────────────────────
echo "  [*] Setting up alias..."
if ! grep -q "alias whitemadrid=" "$BASHRC" 2>/dev/null; then
    {
        echo ""
        echo "# WHITE MADRID — TONYPRIME"
        echo "alias whitemadrid='python3 ~/whitemadrid.py'"
    } >> "$BASHRC"
    echo "  [+] Alias 'whitemadrid' added to ~/.bashrc"
else
    # Update existing alias just in case
    sed -i "s|alias whitemadrid=.*|alias whitemadrid='python3 ~/whitemadrid.py'|" "$BASHRC"
    echo "  [+] Alias updated in ~/.bashrc"
fi
echo ""

# ── Step 9: Multi-API Key Setup ───────────────────────
echo "  ────────────────────────────────────────────────"
echo "  [*] Multi-API Key Setup (9 Providers)"
echo ""
echo "  You only need ONE key to start."
echo "  Press Enter to skip any provider."
echo ""
echo "  ┌─────────────────────────────────────────────┐"
echo "  │  PROVIDER        FREE TIER                  │"
echo "  │  ─────────────────────────────────────────  │"
echo "  │  1. OpenRouter   10+ free models            │"
echo "  │  2. Groq         fastest free inference     │"
echo "  │  3. Gemini       1M tokens/day free         │"
echo "  │  4. Anthropic    \$5 free trial credits      │"
echo "  │  5. OpenAI       \$5 free trial credits      │"
echo "  │  6. Together AI  \$1 free credits            │"
echo "  │  7. Mistral      free experimental tier     │"
echo "  │  8. Cohere       1000 free req/month        │"
echo "  │  9. HuggingFace  free with account          │"
echo "  └─────────────────────────────────────────────┘"
echo ""
echo "  Get free keys at:"
echo "    OpenRouter  → https://openrouter.ai/keys"
echo "    Groq        → https://console.groq.com/keys"
echo "    Gemini      → https://aistudio.google.com/app/apikey"
echo "    Cohere      → https://dashboard.cohere.com/api-keys"
echo ""
echo "  ────────────────────────────────────────────────"
echo ""

# Provider metadata
PROV_IDS=(   ""           "openrouter"     "groq"        "gemini"       "anthropic"      "openai"      "together"          "mistral"        "cohere"      "huggingface"     )
PROV_NAMES=( ""           "OpenRouter"     "Groq"        "Gemini"       "Anthropic"      "OpenAI"      "Together AI"       "Mistral"        "Cohere"      "Hugging Face"    )
PROV_VARS=(  ""           "OPENROUTER_API_KEY" "GROQ_API_KEY" "GEMINI_API_KEY" "ANTHROPIC_API_KEY" "OPENAI_API_KEY" "TOGETHER_API_KEY" "MISTRAL_API_KEY" "COHERE_API_KEY" "HUGGINGFACE_API_KEY" )
PROV_MODELS=("" "meta-llama/llama-3.1-8b-instruct:free" "llama-3.1-8b-instant" "gemini-1.5-flash" "claude-haiku-4-5" "gpt-4o-mini" "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo" "open-mistral-7b" "command-r" "mistralai/Mistral-7B-Instruct-v0.3" )

declare -A KEYS

for i in 1 2 3 4 5 6 7 8 9; do
    read -p "  [${i}] ${PROV_NAMES[$i]} key: " KEY
    if [ -n "$KEY" ]; then
        KEYS[$i]="$KEY"
        echo "  [+] ${PROV_NAMES[$i]} key saved."
    fi
done

echo ""

# Find default provider (first key entered)
DEFAULT_PROV="openrouter"
DEFAULT_MODEL="meta-llama/llama-3.1-8b-instruct:free"

for i in 1 2 3 4 5 6 7 8 9; do
    if [ -n "${KEYS[$i]}" ]; then
        DEFAULT_PROV="${PROV_IDS[$i]}"
        DEFAULT_MODEL="${PROV_MODELS[$i]}"
        echo "  [+] Default provider: ${PROV_NAMES[$i]}"
        echo "  [+] Default model:    ${PROV_MODELS[$i]}"
        break
    fi
done

# ── Step 10: Write config JSON ────────────────────────
echo ""
echo "  [*] Writing config..."

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
    "operator":      "Operator",
    "session_count": 0,
}

path = os.path.expanduser("~/.whitemadrid_config")
with open(path, "w") as f:
    json.dump(cfg, f, indent=2)

print(f"  [+] Config saved to {path}")
print(f"  [+] {len(keys)} API key(s) stored.")
PYEOF

# ── Step 11: Export keys to .bashrc ───────────────────
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
echo "  [+] Keys exported to ~/.bashrc"
echo ""

# Handle case where no keys were entered
if [ ${#KEYS[@]} -eq 0 ]; then
    echo "  [!] No keys entered. Writing minimal config..."
    python3 -c "
import json, os
cfg = {
    'provider': 'openrouter',
    'model': 'meta-llama/llama-3.1-8b-instruct:free',
    'api_keys': {},
    'operator': 'Operator',
    'session_count': 0
}
with open(os.path.expanduser('~/.whitemadrid_config'), 'w') as f:
    json.dump(cfg, f, indent=2)
print('  [+] Minimal config written.')
"
    echo "  [!] Add keys later inside WHITE MADRID with: setkey <provider>"
    echo ""
fi

# ── Done ─────────────────────────────────────────────
echo "  ────────────────────────────────────────────────"
echo "  [+] WHITE MADRID v5.0 setup complete!"
echo ""
echo "  Launch:"
echo "    source ~/.bashrc && whitemadrid"
echo ""
echo "  Or directly:"
echo "    python3 ~/whitemadrid.py"
echo ""
echo "  Quick commands inside WHITE MADRID:"
echo "    apis             — browse all 9 providers & models"
echo "    provider groq    — switch to Groq (fastest free)"
echo "    provider gemini  — switch to Gemini (1M tokens/day)"
echo "    freemode         — auto-select free model"
echo "    setkey <name>    — add/update an API key"
echo "    install          — install pentest tools"
echo "    help             — full command reference"
echo ""
echo "  If you see HTTP 403 / 1010 error:"
echo "    → type: provider groq   (no Cloudflare, always free)"
echo ""
echo "  If you see utf-8 decode error:"
echo "    → already fixed in v5.0 automatically"
echo ""
echo "  ────────────────────────────────────────────────"
echo "  Stay ethical. — TONYPRIME"
echo "  ────────────────────────────────────────────────"
echo ""
