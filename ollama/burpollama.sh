#!/usr/bin/env zsh

burpollama () {
	emulate -L zsh
	setopt pipefail
	local SCRIPT_PATH="${(%):-%N}"
	local ROOT_DIR="${SCRIPT_PATH:A:h:h}"
	local CADDYFILE="$ROOT_DIR/common/Caddyfile"
	local LOG="/tmp/burp-mcp-caddy.log"
	local CADDY_PID=""
	if ! command -v caddy > /dev/null 2>&1
	then
		echo "[!] caddy not found (brew install caddy)"
		return 1
	fi
	if ! command -v ollama > /dev/null 2>&1
	then
		echo "[!] ollama not found (install from https://ollama.com)"
		return 1
	fi
	if ! command -v python3 > /dev/null 2>&1
	then
		echo "[!] python3 not found"
		return 1
	fi
	if [[ ! -f "$CADDYFILE" ]]
	then
		echo "[!] Caddyfile not found: $CADDYFILE"
		return 1
	fi
	if [[ -z "$1" ]]
	then
		echo "Usage: burpollama <ollama-model> [--burp <sse-url>]"
		return 1
	fi
	cleanup () {
		if [[ -n "$CADDY_PID" ]] && kill -0 "$CADDY_PID" 2> /dev/null
		then
			kill -TERM "$CADDY_PID" 2> /dev/null
			sleep 0.2
			kill -KILL "$CADDY_PID" 2> /dev/null
			wait "$CADDY_PID" 2> /dev/null
		fi
		local pids
		pids="$(lsof -ti tcp:19876 2>/dev/null | tr '\n' ' ')"
		if [[ -n "$pids" ]]
		then
			kill -TERM $pids 2> /dev/null
			sleep 0.2
			kill -KILL $pids 2> /dev/null
		fi
	}
	trap 'cleanup; return 130' INT TERM
	trap 'cleanup' EXIT
	caddy run --config "$CADDYFILE" > "$LOG" 2>&1 &
	CADDY_PID=$!
	echo "[*] Caddy started (pid=$CADDY_PID) - log: $LOG"
	python3 "$(dirname "$0")/ollama_mcp_agent.py" "$@"
	cleanup
	trap - INT TERM EXIT
}
