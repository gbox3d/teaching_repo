# GitHub Classroom Shared-PC Reset

## 목차

- [정리 항목](#정리-항목)
- [가장 쉬운 사용법](#가장-쉬운-사용법)
- [PowerShell에서 직접 실행](#powershell에서-직접-실행)
- [macOS·Linux](#macoslinux)
- [수업실 운영 권장 방식](#수업실-운영-권장-방식)
- [주의 사항](#주의-사항)
- [검증 상태와 한계](#검증-상태와-한계)

공용 실습 PC에서 다음 학생이 수업을 시작하기 전에 이전 사용자의 Git/GitHub 인증 흔적을 정리하는 도구입니다. Windows는 PowerShell(`GitHub-Classroom-Reset.ps1`), macOS·Linux는 셸 스크립트(`github-classroom-reset.sh`)를 씁니다. 두 판은 같은 항목을 정리합니다.

## 정리 항목

- Git 전역 `user.name`, `user.email`, 서명 키 및 GitHub 계정별 credential 설정
- 평문 Git credential 파일
- Windows 자격 증명 관리자에 저장된 GitHub 관련 항목
- GitHub CLI 로그인 및 설정
- 현재 사용자의 SSH agent에 올라간 키
- `known_hosts`의 GitHub 항목
- 선택 사항: 표준 이름의 SSH 키 파일
- 선택 사항: VS Code GitHub 인증 저장소

브라우저의 GitHub 쿠키는 제거하지 않습니다. 수업에서는 Edge/Chrome의 게스트 또는 InPrivate 창 사용을 권장합니다.

## 가장 쉬운 사용법

1. 실행 중인 VS Code를 모두 닫습니다.
2. `Preview-Reset.bat`을 실행하여 삭제 예정 항목을 확인합니다.
3. 실제 초기화 시 `GitHub-Classroom-Reset.bat`을 더블클릭합니다.
4. 확인 질문에서 `Y`를 누릅니다.

관리자 권한은 필요하지 않습니다. 현재 로그인한 Windows 사용자 영역만 정리합니다.
Git Credential Manager 자체의 `credential.helper` 설정은 보존하므로 다음 학생도 정상적으로 로그인할 수 있습니다.

## PowerShell에서 직접 실행

미리보기(아무것도 변경하지 않음):

```powershell
.\GitHub-Classroom-Reset.ps1 -RemoveSshKeys -RemoveVSCodeAuth
```

항목별 확인 후 실행:

```powershell
.\GitHub-Classroom-Reset.ps1 -Execute -RemoveSshKeys -RemoveVSCodeAuth
```

개별 확인 없이 실행:

```powershell
.\GitHub-Classroom-Reset.ps1 -Execute -Force -RemoveSshKeys -RemoveVSCodeAuth
```

SSH 키 파일을 보존하려면 `-RemoveSshKeys`를 빼고, VS Code 인증을 보존하려면 `-RemoveVSCodeAuth`를 뺍니다.

## macOS·Linux

`github-classroom-reset.sh` 는 Windows 판과 같은 항목을 정리합니다. 자격 증명 저장소만 운영체제에 맞게 다릅니다.

- 설정된 Git credential helper(osxkeychain·libsecret·Git Credential Manager·store)에 `github.com` 자격 증명 삭제를 요청합니다(`git credential reject`).
- macOS 키체인의 GitHub 항목: `github.com` 인터넷 암호, `git:https://github.com`(GCM), `gh:github.com`(GitHub CLI), GitHub Desktop 항목.
- GitHub CLI 는 `gh auth logout` 뒤 `~/.config/gh` 를 지웁니다.
- `--remove-vscode-auth` 를 주면 VS Code 의 GitHub 로그인 저장소도 지웁니다. macOS 에서는 키체인의 `vscodevscode.github-authentication` 도 함께 지웁니다.

macOS 에서 두 번 눌러 쓰기:

1. 실행 중인 VS Code 를 모두 닫습니다.
2. `Preview-Reset.command` 로 삭제 예정 항목을 확인합니다.
3. `GitHub-Classroom-Reset.command` 를 두 번 누르고 `y` 를 입력합니다.

처음 실행할 때 "확인되지 않은 개발자" 경고가 나오면 Finder 에서 파일을 우클릭하고 **열기**를 고릅니다. 실행 권한이 빠졌으면 터미널에서 `chmod +x *.sh *.command` 를 실행합니다.

터미널에서 직접 실행:

```bash
./github-classroom-reset.sh --remove-ssh-keys --remove-vscode-auth                    # 미리보기(아무것도 바꾸지 않음)
./github-classroom-reset.sh --execute --remove-ssh-keys --remove-vscode-auth          # 항목마다 확인
./github-classroom-reset.sh --execute --force --remove-ssh-keys --remove-vscode-auth  # 확인 없이
```

키체인 항목을 지울 때 macOS 가 로그인 암호를 물을 수 있습니다. 거절하면 그 항목은 `[WARN]` 으로 남고, 끝의 종료 코드는 1 입니다.

## 수업실 운영 권장 방식

- GitHub 웹 로그인은 게스트/InPrivate 창에서만 진행합니다.
- 수업 종료 때 `GitHub-Classroom-Reset.bat`을 실행합니다.
- 다음 수업 시작 전에 `Preview-Reset.bat`으로 잔여 항목을 점검합니다.
- SSH 실습이 아니라면 HTTPS + Git Credential Manager 방식을 권장합니다.
- 가능하면 학생마다 별도의 Windows 계정 또는 복원형 PC 환경을 사용합니다.

## 주의 사항

`GitHub-Classroom-Reset.bat`은 표준 이름(`id_rsa`, `id_ed25519` 등)의 SSH 개인키와 공개키를 영구 삭제합니다. 공용 실습 PC가 아닌 개인 PC에서는 먼저 미리보기를 실행하십시오.

VS Code가 실행 중이면 메모리에 남은 세션 때문에 로그아웃이 완전하지 않을 수 있습니다. 초기화 전에 VS Code를 종료하십시오.

## 검증 상태와 한계

Windows 판은 실기 테스트 전 버전입니다. 테스트용 Windows 사용자 계정에서 미리보기와 실제 정리를 검증한 뒤 배포하십시오. macOS 판은 실제 Mac 에서 미리보기를 확인했고, 실제 정리는 가짜 홈 폴더(키체인·`gh`·`ssh-add` 를 기록용 가짜 명령으로 바꾼 상태)에서만 확인했습니다. 실제 키체인 삭제와 Linux 는 테스트용 계정에서 먼저 확인하십시오. 완료 메시지는 전체 인증이 제거되었다는 보장이 아닙니다.

- 평문 credential 파일과 GitHub CLI 설정 폴더는 통째로 삭제하므로 다른 서비스 계정과 설정도 영향을 받을 수 있습니다. SSH agent의 모든 키도 내려갑니다. 개인 PC에는 일괄 실행하지 마십시오.
- VS Code의 위 폴더 정리만으로 모든 인증 저장소가 제거되지는 않습니다. VS Code 계정 메뉴에서 GitHub 로그아웃을 별도로 확인하십시오.
- 브라우저 쿠키, 환경변수 토큰, 사용자 지정 SSH 키, 다른 위치의 CLI 설정, 저장소별 로컬 Git 설정 및 별도 credential helper는 자동 정리 범위 밖입니다.
- 해시된 known_hosts 항목은 남을 수 있습니다. known_hosts는 사용자 로그인 인증이 아니라 서버 신뢰 정보입니다.
- Windows 자격 증명 목록은 표시 문자열을 기반으로 처리합니다. 실행 후 자격 증명 관리자에서 잔여 GitHub 항목을 확인하십시오.
