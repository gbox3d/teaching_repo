#!/usr/bin/env bash
# GitHub Classroom Shared-PC Reset — macOS / Linux 판 (Windows 판 GitHub-Classroom-Reset.ps1 과 같은 항목)
# 공용 실습 PC 에서 현재 사용자의 Git/GitHub 로그인 흔적을 정리한다. 관리자 권한은 필요 없다.
#
# 사용:
#   ./github-classroom-reset.sh                                   미리보기(아무것도 바꾸지 않는다)
#   ./github-classroom-reset.sh --execute                         항목마다 묻고 정리
#   ./github-classroom-reset.sh --execute --force                 묻지 않고 정리
#   옵션: --remove-ssh-keys (표준 이름 id_* 키 파일 삭제)  --remove-vscode-auth (VS Code GitHub 로그인 삭제)

set -u

EXECUTE=0; FORCE=0; REMOVE_SSH_KEYS=0; REMOVE_VSCODE_AUTH=0
for arg in "$@"; do
  case "$arg" in
    --execute) EXECUTE=1 ;;
    --force) FORCE=1 ;;
    --remove-ssh-keys) REMOVE_SSH_KEYS=1 ;;
    --remove-vscode-auth) REMOVE_VSCODE_AUTH=1 ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "알 수 없는 옵션: $arg (--help 참고)" >&2; exit 2 ;;
  esac
done

CHANGED=0; WARNINGS=0
OS="$(uname -s)"
if [ -t 1 ]; then C_CYAN=$'\e[36m'; C_GREEN=$'\e[32m'; C_YELLOW=$'\e[33m'; C_GRAY=$'\e[90m'; C_RED=$'\e[31m'; C_OFF=$'\e[0m'
else C_CYAN=; C_GREEN=; C_YELLOW=; C_GRAY=; C_RED=; C_OFF=; fi

step()   { printf '\n%s== %s ==%s\n' "$C_CYAN" "$1" "$C_OFF"; }
result() {  # result OK|SKIP|WARN|INFO 메시지
  local color="$C_GRAY"
  case "$1" in OK) color="$C_GREEN" ;; SKIP) color="$C_GRAY" ;; WARN) color="$C_YELLOW" ;; esac
  printf '%s[%s] %s%s\n' "$color" "$1" "$2" "$C_OFF"
}

# cleanup "대상" "동작" 명령 [인자…] — 미리보기면 알리기만, 실행이면 (묻고) 실행한다
cleanup() {
  local target="$1" action="$2"; shift 2
  if [ "$EXECUTE" -ne 1 ]; then result INFO "Would ${action}: ${target}"; return; fi
  if [ "$FORCE" -ne 1 ]; then
    local answer
    read -r -p "${action}: ${target} ? [y/N] " answer </dev/tty || answer=n
    case "$answer" in y|Y) ;; *) result SKIP "건너뜀: ${target}"; return ;; esac
  fi
  if "$@" >/dev/null 2>&1; then CHANGED=$((CHANGED + 1)); result OK "${action}: ${target}"
  else WARNINGS=$((WARNINGS + 1)); result WARN "${action} 실패: ${target}"; fi
}

remove_path() {  # remove_path 경로
  if [ -e "$1" ] || [ -L "$1" ]; then cleanup "$1" 'delete' rm -rf -- "$1"
  else result SKIP "Not found: $1"; fi
}

has() { command -v "$1" >/dev/null 2>&1; }

printf 'GitHub Classroom Shared-PC Reset (%s)\n' "$OS"
if [ "$EXECUTE" -ne 1 ]; then printf '%sPREVIEW MODE: nothing will be changed. Add --execute to clean.%s\n' "$C_YELLOW" "$C_OFF"
elif [ "$FORCE" -ne 1 ]; then printf '%sEXECUTE MODE: each cleanup action will be confirmed.%s\n' "$C_YELLOW" "$C_OFF"
else printf '%sEXECUTE + FORCE MODE: matching data will be removed without individual prompts.%s\n' "$C_RED" "$C_OFF"; fi

# 1. Git 전역 설정 — credential.helper 는 남겨 다음 학생도 로그인할 수 있게 한다
step 'Git global identity and authentication settings'
if has git; then
  keys="user.name user.email user.signingkey credential.username github.user"
  keys="$keys $(git config --global --name-only --get-regexp '^(credential\..*github\.com.*|http\.https://github\.com/\.extraheader)$' 2>/dev/null | sort -u | tr '\n' ' ')"
  for key in $keys; do
    if git config --global --get-all "$key" >/dev/null 2>&1; then
      cleanup "global Git setting '$key'" 'remove' git config --global --unset-all "$key"
    else result SKIP "Global Git setting '$key' is not set."; fi
  done
else result SKIP 'Git is not installed.'; fi

# 2. 설정된 credential helper(osxkeychain·libsecret·manager·store 등)에 github.com 자격 증명을 지우게 한다
step 'Git credential helper (github.com)'
if has git && [ -n "$(git config --get-all credential.helper 2>/dev/null)" ]; then
  cleanup 'github.com credentials in the configured Git credential helper' 'erase' \
    sh -c 'printf "protocol=https\nhost=github.com\n\n" | git credential reject'
else result SKIP 'No Git credential helper is configured.'; fi

step 'Git HTTPS credential files'
remove_path "$HOME/.git-credentials"
remove_path "${XDG_CONFIG_HOME:-$HOME/.config}/git/credentials"

# 3. macOS 키체인 — Git(osxkeychain·GCM), GitHub CLI, GitHub Desktop 이 남기는 github.com 항목
if [ "$OS" = Darwin ] && has security; then
  step 'macOS Keychain (github.com)'
  found=0
  # 같은 항목이 여러 개일 수 있어 남아 있는 동안 지운다(최대 20개)
  delete_all() {  # delete_all find-명령 delete-명령 인자…
    local kind="$1"; shift
    local n=0
    while [ $n -lt 20 ] && security "find-$kind" "$@" >/dev/null 2>&1; do
      security "delete-$kind" "$@" >/dev/null 2>&1 || return 1
      n=$((n + 1))
    done
  }
  if security find-internet-password -s github.com >/dev/null 2>&1; then
    found=1; cleanup 'Keychain internet passwords for github.com' 'delete' delete_all internet-password -s github.com
  fi
  for svc in 'git:https://github.com' 'gh:github.com' 'GitHub - https://api.github.com' 'GitHub Desktop'; do
    if security find-generic-password -s "$svc" >/dev/null 2>&1; then
      found=1; cleanup "Keychain item '$svc'" 'delete' delete_all generic-password -s "$svc"
    fi
  done
  [ $found -eq 0 ] && result SKIP 'No GitHub-related Keychain items were found.'
fi

step 'GitHub CLI'
if has gh && gh auth status >/dev/null 2>&1; then
  cleanup 'GitHub CLI login (github.com)' 'log out' sh -c 'gh auth logout --hostname github.com </dev/null'
fi
remove_path "${XDG_CONFIG_HOME:-$HOME/.config}/gh"

step 'SSH agent and GitHub known_hosts entry'
if has ssh-add; then
  if ssh-add -l >/dev/null 2>&1; then cleanup 'current user SSH agent' 'remove all loaded keys from' ssh-add -D
  else result SKIP 'No keys are loaded in the SSH agent.'; fi
else result SKIP 'OpenSSH ssh-add is not installed.'; fi
for kh in "$HOME/.ssh/known_hosts" "$HOME/.ssh/known_hosts.old"; do
  if [ ! -f "$kh" ]; then result SKIP "Not found: $kh"
  elif grep -Eq '(^|,)github\.com([ ,]|$)' "$kh"; then
    cleanup "$kh" 'remove GitHub host entries from' sh -c 'grep -Ev "(^|,)github\.com([ ,]|\$)" "$1" > "$1.tmp"; mv "$1.tmp" "$1"' _ "$kh"
  else result SKIP "No GitHub host entry in $kh"; fi
done

if [ "$REMOVE_SSH_KEYS" -eq 1 ]; then
  step 'Standard user SSH keys'
  for k in id_rsa id_rsa.pub id_ed25519 id_ed25519.pub id_ecdsa id_ecdsa.pub id_dsa id_dsa.pub; do remove_path "$HOME/.ssh/$k"; done
else result INFO 'SSH key files were preserved. Use --remove-ssh-keys to include standard id_* key files.'; fi

step 'VS Code GitHub authentication'
if [ "$REMOVE_VSCODE_AUTH" -eq 1 ]; then
  if [ "$OS" = Darwin ]; then base="$HOME/Library/Application Support"; else base="${XDG_CONFIG_HOME:-$HOME/.config}"; fi
  remove_path "$base/Code/User/globalStorage/github.vscode-auth"
  remove_path "$base/Code - Insiders/User/globalStorage/github.vscode-auth"
  if [ "$OS" = Darwin ] && has security; then
    for svc in 'vscodevscode.github-authentication' 'vscode-insidersvscode.github-authentication'; do
      if security find-generic-password -s "$svc" >/dev/null 2>&1; then
        cleanup "Keychain item '$svc'" 'delete' sh -c 'while security find-generic-password -s "$1" >/dev/null 2>&1; do security delete-generic-password -s "$1" >/dev/null 2>&1 || exit 1; done' _ "$svc"
      fi
    done
  fi
  result INFO 'Close all VS Code windows before cleaning; active processes may retain a session.'
else result INFO 'VS Code auth storage was preserved. Use --remove-vscode-auth to include it.'; fi

step 'Summary'
if [ "$EXECUTE" -ne 1 ]; then
  printf '%sPreview complete. Re-run with --execute, or double-click GitHub-Classroom-Reset.command (macOS).%s\n' "$C_YELLOW" "$C_OFF"
else
  printf '%sCleanup complete. Successful actions: %d, warnings: %d%s\n' "$C_GREEN" "$CHANGED" "$WARNINGS" "$C_OFF"
  printf '%sAlso sign out of github.com in the browser, or use a Guest/Private browser window for class.%s\n' "$C_YELLOW" "$C_OFF"
fi
[ "$WARNINGS" -gt 0 ] && exit 1
exit 0
