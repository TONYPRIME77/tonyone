#!/data/data/com.termux/files/usr/bin/bash
# WHITE MADRID — Termux Setup Script

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
echo "  Termux Setup — v1.0"
echo "  ──────────────────────────────────────────────"
echo ""

echo "  [*] Updating packages..."
pkg update -y -q 2>/dev/null

if ! command -v python3 &>/dev/null; then
    echo "  [*] Installing Python..."
    pkg install python -y -q
else
    echo "  [+] Python found: $(python3 --version)"
fi

pkg install libreadline -y -q 2>/dev/null || true

DEST="$HOME/whitemadrid.py"
SRC="$(cd "$(dirname "$0")" && pwd)/whitemadrid.py"

if [ -f "$SRC" ]; then
    cp "$SRC" "$DEST"
    chmod +x "$DEST"
    echo "  [+] Installed to $DEST"
else
    echo "  [!] whitemadrid.py not found next to setup.sh"
    echo "      Copy whitemadrid.py to $DEST manually."
fi

BASHRC="$HOME/.bashrc"
if ! grep -q "alias whitemadrid=" "$BASHRC" 2>/dev/null; then
    echo "" >> "$BASHRC"
    echo "# WHITE MADRID" >> "$BASHRC"
    echo "alias whitemadrid='python3 ~/whitemadrid.py'" >> "$BASHRC"
    echo "  [+] Added 'whitemadrid' alias to ~/.bashrc"
else
    echo "  [+] Alias already exists in ~/.bashrc"
fi

echo ""
echo "  ──────────────────────────────────────────────"
echo "  [*] OpenRouter API Key Setup"
echo "      Get a free key: https://openrouter.ai/keys"
echo "  ──────────────────────────────────────────────"
echo ""
read -p "  Enter your OpenRouter API key (or Enter to skip): " API_KEY

if [ -n "$API_KEY" ]; then
    ENV_LINE="export OPENROUTER_API_KEY='$API_KEY'"
    if ! grep -q "OPENROUTER_API_KEY" "$BASHRC" 2>/dev/null; then
        echo "" >> "$BASHRC"
        echo "# OpenRouter API Key" >> "$BASHRC"
        echo "$ENV_LINE" >> "$BASHRC"
    else
        sed -i "s|export OPENROUTER_API_KEY=.*|$ENV_LINE|" "$BASHRC"
    fi
    export OPENROUTER_API_KEY="$API_KEY"
    echo "  [+] API key saved to ~/.bashrc"
else
    echo "  [!] Skipped. Set later with:"
    echo "      export OPENROUTER_API_KEY='sk-or-...'"
fi

echo ""
echo "  ──────────────────────────────────────────────"
echo "  [+] Setup complete!"
echo ""
echo "  Launch WHITE MADRID:"
echo "    source ~/.bashrc && whitemadrid"
echo ""
echo "  Or directly:"
echo "    python3 ~/whitemadrid.py"
echo "  ──────────────────────────────────────────────"
echo ""
