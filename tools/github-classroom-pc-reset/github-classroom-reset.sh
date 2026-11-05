#!/usr/bin/env bash
# GitHub Classroom Shared-PC Reset — macOS / Linux (same items as the Windows GitHub-Classroom-Reset.ps1).
# Clears the previous student's GitHub logins for the CURRENT user. No admin rights needed.
#
# Usage:
#   ./github-classroom-reset.sh                                   preview: nothing is changed
#   ./github-classroom-reset.sh --execute                         ask before each cleanup action
#   ./github-classroom-reset.sh --execute --force                 no questions
#   Options: --remove-ssh-keys        delete standard id_* key files
#            --remove-vscode-auth     reset VS Code sign-in storage (also clears recently-opened list, extension state)
#            --open-github-logout     open https://github.com/logout in the default browser
# A browser that is still signed in to github.com re-authorizes Git Credential Manager silently, so the
# browser session has to be signed out as well; the script cannot do that for you.

set -u

EXECUTE=0; FORCE=0; REMOVE_SSH_KEYS=0; REMOVE_VSCODE_AUTH=0; OPEN_LOGOUT=0
for arg in "$@"; do
  case "$arg" in
    --execute) EXECUTE=1 ;;
    --force) FORCE=1 ;;
    --remove-ssh-keys) REMOVE_SSH_KEYS=1 ;;
    --remove-vscode-auth) REMOVE_VSCODE_AUTH=1 ;;
    --open-github-logout) OPEN_LOGOUT=1 ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "Unknown option: $arg (see --help)" >&2; exit 2 ;;
  esac
done

CHANGED=0; WARNINGS=0
OS="$(uname -s)"
CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
GITHUB_HOSTS="github.com gist.github.com"
if [ -t 1 ]; then C_CYAN=$'\e[36m'; C_GREEN=$'\e[32m'; C_YELLOW=$'\e[33m'; C_GRAY=$'\e[90m'; C_RED=$'\e[31m'; C_OFF=$'\e[0m'
else C_CYAN=; C_GREEN=; C_YELLOW=; C_GRAY=; C_RED=; C_OFF=; fi

step()   { printf '\n%s== %s ==%s\n' "$C_CYAN" "$1" "$C_OFF"; }
result() {  # result OK|SKIP|WARN|INFO message
  local color="$C_GRAY"
  case "$1" in OK) color="$C_GREEN" ;; SKIP) color="$C_GRAY" ;; WARN) color="$C_YELLOW"; WARNINGS=$((WARNINGS + 1)) ;; esac
  printf '%s[%s] %s%s\n' "$color" "$1" "$2" "$C_OFF"
}
has() { command -v "$1" >/dev/null 2>&1; }

# cleanup "target" "action" command [args...]
# preview: report only (returns 1); execute: (ask, then) run; returns 0 only when the command ran and succeeded.
cleanup() {
  local target="$1" action="$2"; shift 2
  if [ "$EXECUTE" -ne 1 ]; then result INFO "Would ${action}: ${target}"; return 1; fi
  if [ "$FORCE" -ne 1 ]; then
    local answer
    read -r -p "${action}: ${target} ? [y/N] " answer </dev/tty || answer=n
    case "$answer" in y|Y) ;; *) result SKIP "Skipped by user: ${target}"; return 1 ;; esac
  fi
  if "$@" >/dev/null 2>&1; then CHANGED=$((CHANGED + 1)); result OK "${action}: ${target}"; return 0
  else result WARN "${action} failed: ${target}"; return 1; fi
}

remove_path() {  # remove_path path
  if [ -e "$1" ] || [ -L "$1" ]; then cleanup "$1" 'delete' rm -rf -- "$1"
  else result SKIP "Not found: $1"; return 1; fi
}

# git_cred fill|reject host [user] — talks to the configured credential helpers without ever prompting.
git_cred() {
  local op="$1" host="$2" user="${3:-}"
  { printf 'protocol=https\nhost=%s\n' "$host"; [ -n "$user" ] && printf 'username=%s\n' "$user"; printf '\n'; } |
    ( cd "$HOME" && env -u GIT_ASKPASS -u SSH_ASKPASS GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never \
        git -c core.askPass= credential "$op" 2>&1 )
}
cred_user()      { printf '%s\n' "$1" | sed -n 's/^username=//p' | head -n 1; }
cred_has_pw()    { printf '%s\n' "$1" | grep -q '^password='; }
cred_no_helper() { printf '%s\n' "$1" | grep -q 'is not a git command'; }

# Asks the helpers for a stored credential and, in execute mode, erases it; repeats until none is left.
clear_helper_credentials() {  # host
  local host="$1" round out user
  for round in 1 2 3 4 5 6 7 8 9 10; do
    out="$(git_cred fill "$host")"
    if ! cred_has_pw "$out"; then
      if [ "$round" = 1 ]; then
        if cred_no_helper "$out"; then
          result WARN "A Git credential helper for $host is configured but not installed: $(printf '%s\n' "$out" | grep 'is not a git command' | head -n 1)"
        else result SKIP "No stored credential for $host in the Git credential helpers."; fi
      fi
      return 0
    fi
    user="$(cred_user "$out")"
    cleanup "$host credential for '${user:-unknown}' held by the Git credential helper" 'erase' git_cred reject "$host" "$user" || return 0
  done
  result WARN "Gave up after 10 rounds; the helper still returns a credential for $host."
}

vscode_running() {
  pgrep -f '(/Visual Studio Code[^/]*\.app/Contents/MacOS/|/share/code/code|/vscode/code|/bin/code$|/code-insiders)' >/dev/null 2>&1
}

printf 'GitHub Classroom Shared-PC Reset (%s)\n' "$OS"
if [ "$EXECUTE" -ne 1 ]; then printf '%sPREVIEW MODE: nothing will be changed. Add --execute to clean.%s\n' "$C_YELLOW" "$C_OFF"
elif [ "$FORCE" -ne 1 ]; then printf '%sEXECUTE MODE: each cleanup action will be confirmed.%s\n' "$C_YELLOW" "$C_OFF"
else printf '%sEXECUTE + FORCE MODE: matching data will be removed without individual prompts.%s\n' "$C_RED" "$C_OFF"; fi

step 'Environment'
result INFO "$(uname -sr), user ${USER:-$(id -un)}"
has git || result SKIP 'Git is not on PATH; Git settings and credential helpers are skipped.'
VSCODE_RUNNING=0
if vscode_running; then VSCODE_RUNNING=1; result INFO 'VS Code is running (close every window before resetting its sign-in storage).'; fi

# 1. Git global identity and GitHub-specific settings — credential.helper stays so the next student can sign in
step 'Git global identity and GitHub-specific settings'
if has git; then
  keys="user.name user.email user.signingkey credential.username github.user"
  keys="$keys $(git config --global --name-only --get-regexp '^(credential\..*github\.com.*|http\.https://github\.com/\.extraheader)$' 2>/dev/null | sort -u | tr '\n' ' ')"
  for key in $keys; do
    if git config --global --get-all "$key" >/dev/null 2>&1; then
      cleanup "global Git setting '$key'" 'remove' git config --global --unset-all "$key"
    else result SKIP "Global Git setting '$key' is not set."; fi
  done
  result INFO 'credential.helper is kept so the next student can sign in.'
else result SKIP 'Git is not installed.'; fi

# 2. GitHub CLI first: its git-credential helper ignores "erase", so the token must go through gh auth logout
step 'GitHub CLI'
if has gh; then
  accounts="$(GH_PROMPT_DISABLED=1 gh auth status 2>&1 </dev/null | sed -n -E 's/.*github\.com (account|as) ([^ ]+).*/\2/p' | sort -u)"
  [ -z "$accounts" ] && result SKIP 'GitHub CLI is not logged in to github.com.'
  for account in $accounts; do
    cleanup "GitHub CLI login '$account'" 'log out' sh -c \
      'GH_PROMPT_DISABLED=1 gh auth logout --hostname github.com --user "$1" </dev/null || GH_PROMPT_DISABLED=1 gh auth logout --hostname github.com </dev/null' _ "$account"
  done
else result SKIP 'GitHub CLI is not installed.'; fi
remove_path "$CONFIG_HOME/gh"

# 3. Whatever credential helper is configured (osxkeychain, libsecret, manager, store, cache ...)
step 'Git credential helpers (osxkeychain, libsecret, Git Credential Manager, store ...)'
if has git; then
  helpers="$(git config --get-all credential.helper 2>/dev/null | tr '\n' ' ')"
  [ -n "$helpers" ] && result INFO "Configured helpers: $helpers"
  for host in $GITHUB_HOSTS; do clear_helper_credentials "$host"; done
else result SKIP 'Git is not installed.'; fi

step 'Credential files'
remove_path "$HOME/.git-credentials"
remove_path "$CONFIG_HOME/git/credentials"
if [ -d "$HOME/.gcm/store" ]; then
  found=0
  while IFS= read -r dir; do [ -n "$dir" ] || continue; found=1; remove_path "$dir"; done <<EOF
$(find "$HOME/.gcm/store" -type d -iname '*github.com*' 2>/dev/null)
EOF
  [ $found -eq 0 ] && result SKIP "No github.com entry in $HOME/.gcm/store"
else result SKIP "Not found: $HOME/.gcm/store"; fi

# 4. macOS Keychain — Git (osxkeychain, GCM), GitHub CLI, GitHub Desktop entries for github.com
delete_all() {  # delete_all internet-password|generic-password find/delete args...
  local kind="$1"; shift
  local n=0
  while [ $n -lt 20 ] && security "find-$kind" "$@" >/dev/null 2>&1; do
    security "delete-$kind" "$@" >/dev/null 2>&1 || return 1
    n=$((n + 1))
  done
}
if [ "$OS" = Darwin ] && has security; then
  step 'macOS Keychain (github.com)'
  found=0
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

step 'SSH agent and GitHub known_hosts entry'
if has ssh-add; then
  ssh-add -l >/dev/null 2>&1; rc=$?
  case $rc in
    0) cleanup 'current user SSH agent' 'remove all loaded keys from' ssh-add -D ;;
    1) result SKIP 'No keys are loaded in the SSH agent.' ;;
    *) result SKIP 'The SSH agent is not running.' ;;
  esac
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

# 5. VS Code: the GitHub (and Microsoft) sign-ins live encrypted inside state.vscdb; there is no dependency-free way
#    to delete single rows, so the global state database is removed. settings.json, keybindings, snippets and
#    extensions are separate and stay.
step 'VS Code sign-in storage and Copilot tokens'
if [ "$OS" = Darwin ]; then VSCODE_BASE="$HOME/Library/Application Support"; else VSCODE_BASE="$CONFIG_HOME"; fi
VSCODE_STATE_FILES=""
for app in 'Code' 'Code - Insiders'; do
  for f in state.vscdb state.vscdb.backup; do VSCODE_STATE_FILES="$VSCODE_STATE_FILES
$VSCODE_BASE/$app/User/globalStorage/$f"; done
done
if [ "$REMOVE_VSCODE_AUTH" -eq 1 ]; then
  if [ "$VSCODE_RUNNING" -eq 1 ] && [ "$EXECUTE" -eq 1 ]; then
    result SKIP 'VS Code is running; it would rewrite its state on exit, so the databases were left alone.'
  else
    while IFS= read -r f; do [ -n "$f" ] && remove_path "$f"; done <<EOF
$VSCODE_STATE_FILES
EOF
  fi
  if [ "$OS" = Darwin ] && has security; then
    for svc in 'vscodevscode.github-authentication' 'vscode-insidersvscode.github-authentication'; do
      if security find-generic-password -s "$svc" >/dev/null 2>&1; then
        cleanup "Keychain item '$svc'" 'delete' delete_all generic-password -s "$svc"
      fi
    done
  fi
  remove_path "$CONFIG_HOME/github-copilot"
else result INFO 'VS Code sign-in storage was preserved. Use --remove-vscode-auth to reset it (also clears the recently-opened list and extension state).'; fi

step 'Browser session on github.com'
result INFO 'A browser still signed in to github.com re-authorizes Git Credential Manager silently: the next git push would store the previous student again.'
if [ "$OPEN_LOGOUT" -eq 1 ]; then
  if [ "$OS" = Darwin ]; then opener=open; else opener=xdg-open; fi
  if has "$opener"; then
    cleanup 'https://github.com/logout in the default browser' 'open' "$opener" 'https://github.com/logout' && result INFO 'Click "Sign out" in the browser window that opened.'
  else result WARN "Cannot open a browser here ($opener not found); sign out of github.com manually."; fi
else result INFO 'Use --open-github-logout to open the GitHub sign-out page, or sign out manually.'; fi

if [ "$EXECUTE" -eq 1 ]; then
  step 'Verification'
  if has git; then
    for host in $GITHUB_HOSTS; do
      out="$(git_cred fill "$host")"
      if cred_has_pw "$out"; then result WARN "Git still obtains a $host credential for '$(cred_user "$out")' without asking."
      elif cred_no_helper "$out"; then result INFO "Not verifiable for $host: the configured credential helper is not installed."
      else result OK "Git credential helpers return nothing for $host."; fi
    done
  fi
  if [ "$OS" = Darwin ] && has security; then
    left=""
    security find-internet-password -s github.com >/dev/null 2>&1 && left="$left github.com(internet)"
    for svc in 'git:https://github.com' 'gh:github.com' 'GitHub - https://api.github.com'; do
      security find-generic-password -s "$svc" >/dev/null 2>&1 && left="$left '$svc'"
    done
    if [ -n "$left" ]; then result WARN "Keychain still has:$left"; else result OK 'No GitHub-related Keychain item left.'; fi
  fi
  if [ "$REMOVE_VSCODE_AUTH" -eq 1 ]; then
    left=""
    while IFS= read -r f; do [ -n "$f" ] && [ -e "$f" ] && left="$left $f"; done <<EOF
$VSCODE_STATE_FILES
EOF
    if [ -n "$left" ]; then result WARN "VS Code sign-in storage still present (close VS Code and run again):$left"
    else result OK 'VS Code state databases are gone.'; fi
  fi
fi

step 'Summary'
if [ "$EXECUTE" -ne 1 ]; then
  printf '%sPreview complete. Re-run with --execute, or double-click GitHub-Classroom-Reset.command (macOS).%s\n' "$C_YELLOW" "$C_OFF"
else
  printf '%sCleanup complete. Successful actions: %d, warnings: %d%s\n' "$C_GREEN" "$CHANGED" "$WARNINGS" "$C_OFF"
  printf '%sSign out of github.com in every browser, or use a Guest/Private window in class.%s\n' "$C_YELLOW" "$C_OFF"
fi
[ "$WARNINGS" -gt 0 ] && exit 1
exit 0
