#!/usr/bin/env bash
# macOS 에서 두 번 눌러 삭제 예정 항목만 본다(아무것도 바꾸지 않음)
cd "$(dirname "$0")" || exit 1
bash ./github-classroom-reset.sh --remove-ssh-keys --remove-vscode-auth
echo
read -r -p "Press Enter to close." _
