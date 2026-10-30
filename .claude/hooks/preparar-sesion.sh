#!/usr/bin/env bash
# Prepara cada sesión de agente: instala yt-dlp y los plugins de la oficina si faltan.
# Lo ejecuta Claude Code al iniciar la sesión (SessionStart). Silencioso y sin fallar nunca.
{
  command -v yt-dlp >/dev/null 2>&1 || pip install -q --break-system-packages yt-dlp

  instalado() { grep -q "\"$1\"" "$HOME/.claude/plugins/installed_plugins.json" 2>/dev/null; }

  if ! instalado "hyperframes@hyperframes"; then
    claude plugin marketplace add heygen-com/hyperframes
    claude plugin install hyperframes@hyperframes
  fi
  if ! instalado "watch@claude-watch"; then
    claude plugin marketplace add taoufik123-collab/claude-watch
    claude plugin install watch@claude-watch
  fi
} >/dev/null 2>&1
exit 0
