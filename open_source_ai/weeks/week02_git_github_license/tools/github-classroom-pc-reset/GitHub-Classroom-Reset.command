#!/usr/bin/env bash
# macOS 에서 두 번 눌러 실행하는 정리 도구(Windows 의 GitHub-Classroom-Reset.bat 과 같은 일)
cd "$(dirname "$0")" || exit 1
echo "========================================================"
echo " GitHub Classroom Shared-PC Reset (macOS)"
echo "========================================================"
echo
echo "This removes Git/GitHub credentials for the CURRENT user."
echo "It also removes standard SSH keys and VS Code GitHub auth."
echo "Browser cookies are NOT removed."
echo
read -r -p "Continue? [y/N]: " answer
case "$answer" in
  y|Y) bash ./github-classroom-reset.sh --execute --force --remove-ssh-keys --remove-vscode-auth; code=$? ;;
  *) echo; echo "Cancelled. Nothing was changed."; code=0 ;;
esac
echo
read -r -p "Press Enter to close." _
exit $code
