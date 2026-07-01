#!/data/data/com.termux/files/usr/bin/bash
# WHITE MADRID v4.0 — Termux Setup Script
# Developer: TONYPRIME

clear
echo ""
echo "  ██╗    ██╗██╗  ██╗██╗████████╗███████╗"
echo "  ██║    ██║██║  ██║██║╚══██╔══╝██╔════╝"
echo "  ██║ █╗ ██║███████║██║   ██║   █████╗  "
echo "  ██║███╗██║██╔══██║██║   ██║   ██╔══╝  "
echo "  ╚███╔███╔╝██║  ██║██║   ██║   ███████╗"
echo "   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝"
echo "  ███╗   ███╗ █████╗ ██████╗ ██████╗ ██╗██████╗ "
echo "  ████╗ ████║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗"
echo "  ██╔████╔██║███████║██║  ██║██████╔╝██║██║  ██║"
echo "  ██║╚██╔╝██║██╔══██║██║  ██║██╔══██╗██║██║  ██║"
echo "  ██║ ╚═╝ ██║██║  ██║██████╔╝██║  ██║██║██████╔╝"
echo "  ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝"
echo ""
echo "  v4.0 JARVIS Edition — Termux Setup"
echo "  Developer: TONYPRIME"
echo "  ────────────────────────────────────────────────"
echo ""

# ── Step 1: Update packages ───────────────────────────────────────────
echo "  [*] Updating package list..."
pkg update -y -q 2>/dev/null
echo "  [+] Done."
echo ""

# ── Step 2: Install Python ────────────────────────────────────────────
echo "  [*] Checking Python..."
if ! command -v python3 &>/dev/null; then
    echo "  [*] Installing Python..."
    pkg install python -y
else
    echo "  [+] Python found: $(python3 --version)"
fi
echo ""

# ── Step 3: Install readline (arrow key history support) ──────────────
echo "  [*] Installing readline support..."
pkg install libreadline -y -q 2>/dev/null
echo "  [+] Done."
echo ""

# ── Step 4: Install git (needed for cloning exploit repos) ───────────
echo "  [*] Checking git..."
if ! command -v git &>/dev/null; then
    pkg install git -y -q
    echo "  [+] git installed."
else
    echo "  [+] git found: $(git --version)"
fi
echo ""

# ── Step 5: Install core pentest deps ────────────────────────────────
echo "  [*] Installing core tools (nmap, curl, wget, openssh, openssl)..."
pkg install nmap curl wget openssh openssl-tool -y -q 2>/dev/null
echo "  [+] Core tools ready."
echo ""

# ── Step 6: Copy whitemadrid.py ───────────────────────────────────────
DEST="$HOME/whitemadrid.py"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$SCRIPT_DIR/whitemadrid.py"

echo "  [*] Installing whitemadrid.py..."
if [ -f "$SRC" ]; then
    cp "$SRC" "$DEST"
    chmod +x "$DEST"
    echo "  [+] Installed to $DEST"
else
    echo "  [!] whitemadrid.py not found next to setup.sh"
    echo "      Make sure both files are in the same folder."
    echo "      Then re-run: bash setup.sh"
    echo ""
    exit 1
fi
echo ""

# ── Step 7: Reset old config (important for model switch) ────────────
echo "  [*] Clearing old config (if any)..."
rm -f "$HOME/.whitemadrid_config"
echo "  [+] Config reset — will use free model by default."
echo ""

# ── Step 8: Add shell alias ───────────────────────────────────────────
BASHRC="$HOME/.bashrc"
ALIAS_LINE="alias whitemadrid='python3 ~/whitemadrid.py'"

echo "  [*] Setting up alias..."
if ! grep -q "alias whitemadrid=" "$BASHRC" 2>/dev/null; then
    echo "" >> "$BASHRC"
    echo "# WHITE MADRID — TONYPRIME" >> "$BASHRC"
    echo "$ALIAS_LINE" >> "$BASHRC"
    echo "  [+] Alias 'whitemadrid' added to ~/.bashrc"
else
    echo "  [+] Alias already exists in ~/.bashrc"
fi
echo ""

# ── Step 9: OpenRouter API key ────────────────────────────────────────
echo "  ────────────────────────────────────────────────"
echo "  [*] OpenRouter API Key Setup"
echo "      Free key: https://openrouter.ai/keys"
echo "      (Free models available — no billing needed)"
echo "  ────────────────────────────────────────────────"
echo ""
read -p "  Enter your OpenRouter API key (or press Enter to skip): " API_KEY

if [ -n "$API_KEY" ]; then
    # Save to environment
    if ! grep -q "OPENROUTER_API_KEY" "$BASHRC" 2>/dev/null; then
        echo "" >> "$BASHRC"
        echo "# OpenRouter API Key" >> "$BASHRC"
        echo "export OPENROUTER_API_KEY='$API_KEY'" >> "$BASHRC"
        echo "  [+] API key saved to ~/.bashrc"
    else
        sed -i "s|export OPENROUTER_API_KEY=.*|export OPENROUTER_API_KEY='$API_KEY'|" "$BASHRC"
        echo "  [+] API key updated in ~/.bashrc"
    fi
    export OPENROUTER_API_KEY="$API_KEY"

    # Also save to config file so whitemadrid reads it immediately
    python3 - << PYEOF
import json, os
cfg = {
    "api_key": "$API_KEY",
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "operator": "Operator",
    "session_count": 0
}
with open(os.path.expanduser("~/.whitemadrid_config"), "w") as f:
    json.dump(cfg, f, indent=2)
print("  [+] Config written with free model set.")
PYEOF

else
    echo "  [!] Skipped. You can set it later with:"
    echo "      export OPENROUTER_API_KEY='sk-or-...'"
    echo "      Or enter it when WHITE MADRID starts."
fi

echo ""
echo "  ────────────────────────────────────────────────"
echo "  [+] Setup complete!"
echo ""
echo "  Default model : meta-llama/llama-3.1-8b-instruct:free"
echo "  No credits needed for free models."
echo ""
echo "  Launch WHITE MADRID:"
echo "    source ~/.bashrc && whitemadrid"
echo ""
echo "  Or directly:"
echo "    python3 ~/whitemadrid.py"
echo ""
echo "  Other free models (use 'model' command inside WM):"
echo "    meta-llama/llama-3.2-3b-instruct:free"
echo "    mistralai/mistral-7b-instruct:free"
echo "    google/gemma-2-9b-it:free"
echo "    qwen/qwen-2-7b-instruct:free"
echo ""
echo "  ────────────────────────────────────────────────"
echo "  Stay ethical. — TONYPRIME"
echo "  ────────────────────────────────────────────────"
echo ""
