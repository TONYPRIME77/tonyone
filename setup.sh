#!/data/data/com.termux/files/usr/bin/bash
# HexMind AI — Termux Setup Script

echo ""
echo "  ██╗  ██╗███████╗██╗  ██╗███╗   ███╗██╗███╗   ██╗██████╗"
echo "  ██║  ██║██╔════╝╚██╗██╔╝████╗ ████║██║████╗  ██║██╔══██╗"
echo "  ███████║█████╗   ╚███╔╝ ██╔████╔██║██║██╔██╗ ██║██║  ██║"
echo "  ██╔══██║██╔══╝   ██╔██╗ ██║╚██╔╝██║██║██║╚██╗██║██║  ██║"
echo "  ██║  ██║███████╗██╔╝ ██╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝"
echo "  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝"
echo ""
echo "  HexMind AI — Termux Setup"
echo "  ──────────────────────────────────────────"
echo ""

# Update packages
echo "[*] Updating package list..."
pkg update -y -q

# Install Python if not present
if ! command -v python3 &>/dev/null; then
    echo "[*] Installing Python..."
    pkg install python -y -q
else
    echo "[+] Python already installed: $(python3 --version)"
fi

# Install readline support for better terminal UX
echo "[*] Installing readline support..."
pkg install libreadline -y -q 2>/dev/null || true

# Copy hexmind.py to a good location
DEST="$HOME/hexmind.py"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE="$SCRIPT_DIR/hexmind.py"

if [ -f "$SOURCE" ]; then
    cp "$SOURCE" "$DEST"
    chmod +x "$DEST"
    echo "[+] Copied hexmind.py to $DEST"
else
    echo "[!] hexmind.py not found next to setup.sh — copy it manually to $DEST"
fi

# Create launcher alias
BASHRC="$HOME/.bashrc"
ALIAS_LINE="alias hexmind='python3 ~/hexmind.py'"

if ! grep -q "alias hexmind=" "$BASHRC" 2>/dev/null; then
    echo "" >> "$BASHRC"
    echo "# HexMind AI" >> "$BASHRC"
    echo "$ALIAS_LINE" >> "$BASHRC"
    echo "[+] Added 'hexmind' alias to ~/.bashrc"
else
    echo "[+] Alias already in ~/.bashrc"
fi

# API Key setup
echo ""
echo "  ──────────────────────────────────────────"
echo "  [*] API Key Setup"
echo "  ──────────────────────────────────────────"
echo ""
echo "  You need an Anthropic API key to use HexMind."
echo "  Get one free at: https://console.anthropic.com"
echo ""
read -p "  Enter your API key now (or press Enter to skip): " API_KEY

if [ -n "$API_KEY" ]; then
    # Save to shell profile for persistence
    ENV_LINE="export ANTHROPIC_API_KEY='$API_KEY'"
    if ! grep -q "ANTHROPIC_API_KEY" "$BASHRC" 2>/dev/null; then
        echo "" >> "$BASHRC"
        echo "# Anthropic API Key" >> "$BASHRC"
        echo "$ENV_LINE" >> "$BASHRC"
        echo "[+] API key saved to ~/.bashrc"
    else
        # Update existing line
        sed -i "s|export ANTHROPIC_API_KEY=.*|$ENV_LINE|" "$BASHRC"
        echo "[+] API key updated in ~/.bashrc"
    fi
    export ANTHROPIC_API_KEY="$API_KEY"
else
    echo "  [!] Skipped. You can set it later:"
    echo "      export ANTHROPIC_API_KEY='sk-ant-...'"
    echo "      Or enter it when HexMind starts."
fi

echo ""
echo "  ──────────────────────────────────────────"
echo "  [+] Setup complete!"
echo ""
echo "  Launch HexMind:"
echo "    source ~/.bashrc && hexmind"
echo ""
echo "  Or directly:"
echo "    python3 ~/hexmind.py"
echo "  ──────────────────────────────────────────"
echo ""
