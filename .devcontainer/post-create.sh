#!/bin/bash
set -e

echo "========================================"
echo " Setting up Synthetic Global Equity"
echo "========================================"

# zmq (used by Jupyter) needs libstdc++.so.6, which lives in the Nix store.
# Written to /etc/bash.bashrc so it's available in VS Code's non-login interactive shells.
LIBSTDCPP_DIR=$(dirname "$(find /nix/store -name 'libstdc++.so.6' 2>/dev/null | head -1)")
if [ -n "$LIBSTDCPP_DIR" ] && ! grep -q 'nix-libs' /etc/bash.bashrc 2>/dev/null; then
    printf '\n# libstdc++ for zmq/Jupyter in Nix environment\nexport LD_LIBRARY_PATH="%s${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n' \
        "$LIBSTDCPP_DIR" >> /etc/bash.bashrc
    echo "Nix libstdc++ path written to /etc/bash.bashrc"
fi

# Register the .venv kernel with Jupyter so notebooks pick it up automatically
if [ -f .venv/bin/python ]; then
    .venv/bin/python -m ipykernel install --user --name synthetic-global-equity --display-name "Python (synthetic-global-equity)"
    echo "Jupyter kernel registered."
fi

echo ""
echo "========================================"
echo " Ready!"
echo "========================================"
echo ""
echo "Quick start:"
echo "  Open a notebook directly in VS Code — the kernel is pre-configured."
echo ""
echo "  Or launch Jupyter in the terminal:"
echo "    uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root"
echo "    uv run jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root"
echo ""
echo "  Then open:  http://localhost:8888"
echo ""
echo "Notebook:"
echo "  synthetic_ftse_all_world.ipynb"
echo ""
echo "Or use Claude Code:  claude"
echo ""
