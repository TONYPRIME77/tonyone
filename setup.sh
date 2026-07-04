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
echo "  v5.0 JARVIS Edition — Multi-API Setup"
echo "  Developer : TONYPRIME"
echo "  ────────────────────────────────────────────────"
echo ""

BASHRC="$HOME/.bashrc"
DEST="$HOME/whitemadrid.py"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$SCRIPT_DIR/whitemadrid.py"

# ── Step 1: Update packages ──────────────────────────
echo "  [*] Updating package list..."
pkg update -y -q 2>/dev/null
echo "  [+] Done."
echo ""

# ── Step 2: Python ───────────────────────────────────
echo "  [*] Checking Python..."
if ! command -v python3 &>/dev/null; then
    pkg install python -y
else
    echo "  [+] $(python3 --version)"
fi
echo ""

# ── Step 3: readline ─────────────────────────────────
echo "  [*] Installing readline (arrow key history)..."
pkg install libreadline -y -q 2>/dev/null
echo "  [+] Done."
echo ""

# ── Step 4: git ──────────────────────────────────────
echo "  [*] Checking git..."
if ! command -v git &>/dev/null; then
    pkg install git -y -q
    echo "  [+] git installed."
else
    echo "  [+] $(git --version)"
fi
echo ""

# ── Step 5: Core tools ───────────────────────────────
echo "  [*] Installing core tools..."
pkg install nmap curl wget openssh openssl-tool -y -q 2>/dev/null
echo "  [+] nmap, curl, wget, openssh, openssl ready."
echo ""

# ── Step 6: Copy whitemadrid.py ──────────────────────
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

# ── Step 7: Clear old config ─────────────────────────
echo "  [*] Resetting config for v5.0..."
rm -f "$HOME/.whitemadrid_config"
echo "  [+] Config cleared — fresh start."
echo ""

# ── Step 8: Shell alias ──────────────────────────────
echo "  [*] Setting up alias..."
if ! grep -q "alias whitemadrid=" "$BASHRC" 2>/dev/null; then
    {
        echo ""
        echo "# WHITE MADRID — TONYPRIME"
        echo "alias whitemadrid='python3 ~/whitemadrid.py'"
    } >> "$BASHRC"
    echo "  [+] Alias 'whitemadrid' added to ~/.bashrc"
else
    echo "  [+] Alias already exists."
fi
echo ""

# ── Step 9: Multi-API Key Setup ──────────────────────
echo "  ────────────────────────────────────────────────"
echo "  [*] Multi-API Key Setup (v5.0)"
echo ""
echo "  WHITE MADRID supports 9 AI providers."
echo "  You only need ONE key to get started."
echo "  All providers below have a free tier."
echo ""
echo "  [1] OpenRouter  — 10+ free models (recommended)"
echo "      https://openrouter.ai/keys"
echo ""
echo "  [2] Groq        — fastest free inference"
echo "      https://console.groq.com/keys"
echo ""
echo "  [3] Google Gemini — 1M tokens/day free"
echo "      https://aistudio.google.com/app/apikey"
echo ""
echo "  [4] Anthropic   — \$5 free trial credits"
echo "      https://console.anthropic.com/api-keys"
echo ""
echo "  [5] OpenAI      — \$5 free trial credits"
echo "      https://platform.openai.com/api-keys"
echo ""
echo "  [6] Together AI — \$1 free credits"
echo "      https://api.together.xyz/settings/api-keys"
echo ""
echo "  [7] Mistral     — free experimental tier"
echo "      https://console.mistral.ai/api-keys"
echo ""
echo "  [8] Cohere      — 1000 free req/month forever"
echo "      https://dashboard.cohere.com/api-keys"
echo ""
echo "  [9] Hugging Face — free with HF account"
echo "      https://huggingface.co/settings/tokens"
echo ""
echo "  ────────────────────────────────────────────────"
echo ""

# Collect keys — skip any that are empty
declare -A KEYS
declare -A PROVIDERS
PROVIDERS[1]="openrouter"
PROVIDERS[2]="groq"
PROVIDERS[3]="gemini"
PROVIDERS[4]="anthropic"
PROVIDERS[5]="openai"
PROVIDERS[6]="together"
PROVIDERS[7]="mistral"
PROVIDERS[8]="cohere"
PROVIDERS[9]="huggingface"

PROVIDER_NAMES[1]="OpenRouter"
PROVIDER_NAMES[2]="Groq"
PROVIDER_NAMES[3]="Google Gemini"
PROVIDER_NAMES[4]="Anthropic"
PROVIDER_NAMES[5]="OpenAI"
PROVIDER_NAMES[6]="Together AI"
PROVIDER_NAMES[7]="Mistral"
PROVIDER_NAMES[8]="Cohere"
PROVIDER_NAMES[9]="Hugging Face"

for i in 1 2 3 4 5 6 7 8 9; do
    read -p "  ${PROVIDER_NAMES[$i]} key (Enter to skip): " KEY
    if [ -n "$KEY" ]; then
        KEYS[$i]="$KEY"
        echo "  [+] ${PROVIDER_NAMES[$i]} key saved."
    fi
done

echo ""

# Determine default provider (first one with a key)
DEFAULT_PROV="openrouter"
DEFAULT_KEY=""
DEFAULT_MODEL="meta-llama/llama-3.1-8b-instruct:free"

declare -A PROV_DEFAULTS
PROV_DEFAULTS[openrouter]="meta-llama/llama-3.1-8b-instruct:free"
PROV_DEFAULTS[groq]="llama-3.1-8b-instant"
PROV_DEFAULTS[gemini]="gemini-1.5-flash"
PROV_DEFAULTS[anthropic]="claude-haiku-4-5"
PROV_DEFAULTS[openai]="gpt-4o-mini"
PROV_DEFAULTS[together]="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
PROV_DEFAULTS[mistral]="open-mistral-7b"
PROV_DEFAULTS[cohere]="command-r"
PROV_DEFAULTS[huggingface]="mistralai/Mistral-7B-Instruct-v0.3"

for i in 1 2 3 4 5 6 7 8 9; do
    pid="${PROVIDERS[$i]}"
    if [ -n "${KEYS[$i]}" ]; then
        DEFAULT_PROV="$pid"
        DEFAULT_KEY="${KEYS[$i]}"
        DEFAULT_MODEL="${PROV_DEFAULTS[$pid]}"
        break
    fi
done

# Write config JSON
if [ ${#KEYS[@]} -gt 0 ]; then
python3 - << PYEOF
import json, os

keys = {}
$(for i in 1 2 3 4 5 6 7 8 9; do
    pid="${PROVIDERS[$i]}"
    key="${KEYS[$i]}"
    if [ -n "$key" ]; then
        echo "keys['$pid'] = '$key'"
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
print(f"  [+] Config written → {path}")
print(f"  [+] Default provider: $DEFAULT_PROV")
print(f"  [+] Default model:    $DEFAULT_MODEL")
PYEOF

    # Also export to bashrc for env var access
    for i in 1 2 3 4 5 6 7 8 9; do
        pid="${PROVIDERS[$i]}"
        key="${KEYS[$i]}"
        if [ -n "$key" ]; then
            case "$pid" in
                openrouter)  VAR="OPENROUTER_API_KEY"  ;;
                groq)        VAR="GROQ_API_KEY"         ;;
                gemini)      VAR="GEMINI_API_KEY"       ;;
                anthropic)   VAR="ANTHROPIC_API_KEY"    ;;
                openai)      VAR="OPENAI_API_KEY"       ;;
                together)    VAR="TOGETHER_API_KEY"     ;;
                mistral)     VAR="MISTRAL_API_KEY"      ;;
                cohere)      VAR="COHERE_API_KEY"       ;;
                huggingface) VAR="HUGGINGFACE_API_KEY"  ;;
            esac
            if ! grep -q "$VAR" "$BASHRC" 2>/dev/null; then
                echo "export $VAR='$key'" >> "$BASHRC"
            else
                sed -i "s|export $VAR=.*|export $VAR='$key'|" "$BASHRC"
            fi
        fi
    done
    echo "  [+] Keys exported to ~/.bashrc"
else
    echo "  [!] No keys entered. You can add them later with 'setkey <provider>' inside WHITE MADRID."
    # Write minimal config
    python3 -c "
import json,os
cfg={'provider':'openrouter','model':'meta-llama/llama-3.1-8b-instruct:free','api_keys':{},'operator':'Operator','session_count':0}
with open(os.path.expanduser('~/.whitemadrid_config'),'w') as f: json.dump(cfg,f,indent=2)
"
fi

# ── Done ─────────────────────────────────────────────
echo ""
echo "  ────────────────────────────────────────────────"
echo "  [+] WHITE MADRID v5.0 setup complete!"
echo ""
echo "  Launch:"
echo "    source ~/.bashrc && whitemadrid"
echo ""
echo "  Or directly:"
echo "    python3 ~/whitemadrid.py"
echo ""
echo "  Inside WHITE MADRID:"
echo "    apis             — browse all providers & models"
echo "    provider groq    — switch to Groq (fastest free)"
echo "    provider gemini  — switch to Gemini (most free tokens)"
echo "    freemode         — auto-select free model"
echo "    setkey <name>    — add a key later"
echo "    help             — full command reference"
echo ""
echo "  Free API keys:"
echo "    OpenRouter  → https://openrouter.ai/keys"
echo "    Groq        → https://console.groq.com/keys"
echo "    Gemini      → https://aistudio.google.com/app/apikey"
echo "    Cohere      → https://dashboard.cohere.com/api-keys"
echo ""
echo "  ────────────────────────────────────────────────"
echo "  Stay ethical. — TONYPRIME"
echo "  ────────────────────────────────────────────────"
echo ""
