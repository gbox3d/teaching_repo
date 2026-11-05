# GitHub Classroom Shared-PC Reset

## 목차

- [개요](#개요)
- [정리 항목](#정리-항목)
- [Windows: 가장 쉬운 사용법](#windows-가장-쉬운-사용법)
- [결과 읽는 법](#결과-읽는-법)
- [PowerShell에서 직접 실행](#powershell에서-직접-실행)
- [macOS·Linux](#macoslinux)
- [수업실 운영 권장 방식](#수업실-운영-권장-방식)
- [주의 사항](#주의-사항)
- [검증 상태와 한계](#검증-상태와-한계)
- [2026-11 개정에서 바뀐 것](#2026-11-개정에서-바뀐-것)

## 개요

공용 실습 PC에서 다음 학생이 수업을 시작하기 전에 이전 학생의 GitHub 로그인 흔적을 정리한다. Windows는 PowerShell(`GitHub-Classroom-Reset.ps1`), macOS·Linux는 셸 스크립트(`github-classroom-reset.sh`)이며 같은 항목을 같은 순서로 정리한다. 기본은 미리보기이고 `-Execute`(`--execute`)를 주어야 실제로 지운다. 관리자 권한은 필요 없고 현재 로그인한 사용자 영역만 다룬다.

정리가 끝나면 **검증 단계**가 실제 상태를 다시 조사한다. Git이 묻지 않고 github.com 자격 증명을 꺼내 올 수 있는지(`git credential fill`을 프롬프트 금지 상태로 실행), Windows 자격 증명 관리자에 GitHub 항목이 남았는지, VS Code 로그인 저장소가 남았는지를 확인해 `[OK]`/`[WARN]`으로 보여 준다. "완료" 메시지보다 이 단계의 결과를 믿는다.

## 정리 항목

실행 순서대로다.

1. **Git 전역 설정** — `user.name`, `user.email`, `user.signingkey`, `credential.username`, `github.user`, 그리고 `credential.https://github.com.*`(username·provider·useHttpPath 등)과 `http.https://github.com/.extraheader`. `credential.helper`는 남겨 다음 학생이 로그인할 수 있게 한다.
2. **GitHub CLI** — `gh auth status`에 보이는 계정마다 `gh auth logout`을 실행한 뒤 설정 폴더(`%APPDATA%\GitHub CLI`, `~/.config/gh`)를 지운다. gh의 git 자격 증명 도우미는 `erase`를 무시하므로 반드시 다음 단계보다 먼저 한다.
3. **설정된 Git 자격 증명 도우미** — Git Credential Manager, wincred, store, cache, osxkeychain, libsecret 등 무엇이 설정돼 있든 `git credential fill`로 github.com·gist.github.com 자격 증명을 꺼내 보고, 있으면 그 계정으로 `git credential reject`를 보내 지운다. 여러 계정이 저장돼 있으면 없어질 때까지 반복한다. 프롬프트는 전부 막아 두므로 멈춰 서지 않는다.
4. **자격 증명 파일** — `~/.git-credentials`, `~/.config/git/credentials`, GCM 파일 저장소(`~/.gcm/store`, `~/.gcm/dpapi_store`)의 github.com 폴더.
5. **Windows 자격 증명 관리자** — `cmdkey /list`에서 `…:target=` 줄만 골라(표시 언어와 무관) 이름에 `github`가 들어간 항목을 `cmdkey /delete`로 지운다. GCM(`git:https://github.com`, `git:https://<계정>@github.com`), GitHub CLI(`gh:github.com:<계정>`), GitHub Desktop(`GitHub - https://api.github.com/<계정>`), 옛 VS Code(`vscodevscode.github-authentication/…`)가 모두 여기에 해당한다. macOS는 키체인의 같은 항목을 지운다.
6. **SSH** — 에이전트에 올라간 키 전부(`ssh-add -D`; 에이전트가 꺼져 있으면 건너뜀), `known_hosts`의 github.com 줄. 선택 `-RemoveSshKeys`: 표준 이름(`id_rsa`, `id_ed25519`, `id_ecdsa`, `id_dsa`)의 키 파일.
7. **VS Code**(선택 `-RemoveVSCodeAuth`) — GitHub·Microsoft 로그인은 `state.vscdb`(SQLite) 안에 암호화되어 들어 있고, Windows 최신 판은 `%USERPROFILE%\.vscode-shared\sharedStorage\state.vscdb`에도 있다. 행 단위로 지울 방법이 없어 이 데이터베이스 파일들을 통째로 지운다(VS Code가 다음 실행 때 새로 만든다). 그래서 **최근 폴더 목록·작업 영역 신뢰·확장별 전역 상태도 함께 초기화**된다. `settings.json`, 키 바인딩, 스니펫, 설치된 확장은 별도 파일이라 남는다. VS Code가 실행 중이면 건너뛰고 검증 단계에서 `[WARN]`으로 알린다. 다른 편집기용 Copilot 토큰(`%LOCALAPPDATA%\github-copilot`, `~/.config/github-copilot`)도 지운다.
8. **브라우저**(선택 `-OpenGitHubLogout`) — 기본 브라우저로 `https://github.com/logout`을 열어 준다. 로그아웃 버튼은 사람이 눌러야 한다.

브라우저가 github.com에 로그인된 채라면 **이 도구가 무엇을 지웠든 소용이 없다.** 다음 학생이 `git push`를 하면 GCM이 브라우저를 열고, GitHub는 이미 승인된 앱이라 아무 화면도 보이지 않고 이전 학생 계정으로 토큰을 새로 발급해 다시 저장한다. 겉으로는 "초기화가 안 됐다"로 보인다. 수업에서는 게스트/InPrivate 창만 쓰게 하는 것이 유일하게 확실한 방법이다.

## Windows: 가장 쉬운 사용법

1. 실행 중인 VS Code를 모두 닫는다.
2. `Preview-Reset.bat`을 두 번 눌러 삭제 예정 항목을 확인한다(아무것도 바꾸지 않음).
3. `GitHub-Classroom-Reset.bat`을 두 번 누르고 `Y`를 누른다. 브라우저에 GitHub 로그아웃 페이지가 뜨면 **Sign out**을 누른다.
4. 창에 남은 `== Verification ==` 아래가 전부 `[OK]`인지 본다.

**PC 앞에서(또는 원격 데스크톱으로) 실행해야 한다.** SSH로 들어간 세션이나 예약 작업에서는 Windows 자격 증명 관리자가 보이지 않아 `cmdkey /list`가 비어 나오고 GitHub 항목을 못 지운다. 스크립트는 이 경우 `[WARN] Not a desktop or Remote Desktop session`으로 알린다.

## 결과 읽는 법

| 표시 | 뜻 |
|---|---|
| `[OK]` | 지웠다(검증 단계에서는: 남은 것이 없다) |
| `[SKIP]` | 지울 것이 없었다, 또는 확인 질문에서 거절했다 |
| `[INFO]` | 미리보기의 "Would …" 등 안내 |
| `[WARN]` | 지우지 못했거나 아직 남아 있다. 종료 코드가 1이 되고 BAT는 "finished with one or more warnings"를 띄운다 |

검증 단계의 `[WARN] Git still obtains a github.com credential for '<계정>'`은 어딘가의 자격 증명 도우미가 여전히 그 계정을 내주고 있다는 뜻이다. `[INFO] Not verifiable …`은 설정된 도우미(보통 `manager`)가 설치돼 있지 않아 조사 자체가 불가능했다는 뜻이다. 이 PC는 Git 로그인도 안 될 것이니 Git for Windows를 다시 설치해야 한다.

## PowerShell에서 직접 실행

```powershell
.\GitHub-Classroom-Reset.ps1 -RemoveSshKeys -RemoveVSCodeAuth -OpenGitHubLogout                    # 미리보기
.\GitHub-Classroom-Reset.ps1 -Execute -RemoveSshKeys -RemoveVSCodeAuth -OpenGitHubLogout           # 항목마다 확인
.\GitHub-Classroom-Reset.ps1 -Execute -Force -RemoveSshKeys -RemoveVSCodeAuth -OpenGitHubLogout    # 확인 없이(BAT와 같음)
```

`.ps1`을 직접 실행했을 때 "이 시스템에서 스크립트를 실행할 수 없으므로"라고 나오면 실행 정책 때문이다. BAT는 `-ExecutionPolicy Bypass`로 띄우므로 그런 문제가 없다. 직접 실행하려면 `powershell -ExecutionPolicy Bypass -File .\GitHub-Classroom-Reset.ps1 …` 형태로 띄운다. Windows PowerShell 5.1과 PowerShell 7 모두에서 동작하도록 썼다(ASCII만 사용).

## macOS·Linux

```bash
./github-classroom-reset.sh --remove-ssh-keys --remove-vscode-auth --open-github-logout                     # 미리보기
./github-classroom-reset.sh --execute --remove-ssh-keys --remove-vscode-auth --open-github-logout           # 항목마다 확인
./github-classroom-reset.sh --execute --force --remove-ssh-keys --remove-vscode-auth --open-github-logout   # 확인 없이
```

macOS에서는 `Preview-Reset.command`로 확인한 뒤 `GitHub-Classroom-Reset.command`를 두 번 누르고 `y`를 입력한다. 처음 실행할 때 "확인되지 않은 개발자" 경고가 나오면 Finder에서 파일을 우클릭하고 **열기**를 고른다. 실행 권한이 빠졌으면 `chmod +x *.sh *.command`.

macOS 고유 항목: 키체인의 `github.com` 인터넷 암호, `git:https://github.com`(GCM·osxkeychain), `gh:github.com`, `GitHub - https://api.github.com`(GitHub Desktop), `--remove-vscode-auth` 때 `vscodevscode.github-authentication`. 키체인 항목을 지울 때 로그인 암호를 물을 수 있고, 거절하면 `[WARN]`으로 남는다. VS Code 상태 파일은 `~/Library/Application Support/Code/User/globalStorage/state.vscdb`(Linux는 `~/.config/Code/…`)다.

## 수업실 운영 권장 방식

- GitHub 웹 로그인은 **게스트/InPrivate 창에서만** 하게 한다. 이것이 없으면 아래 어떤 조치도 다음 `git push` 한 번에 되돌아간다.
- 수업이 끝나면 `GitHub-Classroom-Reset.bat`을 실행하고 브라우저의 Sign out까지 누른다.
- 다음 수업 전에 `Preview-Reset.bat`으로 잔여 항목을 점검한다.
- SSH 실습이 아니라면 HTTPS + Git Credential Manager 방식을 권장한다.
- 가능하면 학생마다 별도의 Windows 계정 또는 복원형 PC 환경을 쓴다. 그 편이 이 도구보다 확실하다.

## 주의 사항

- `GitHub-Classroom-Reset.bat`/`.command`는 표준 이름의 SSH 개인키·공개키를 **영구 삭제**한다. 개인 PC에서는 먼저 미리보기를 실행한다.
- `-RemoveVSCodeAuth`는 VS Code 전역 상태를 초기화한다(위 7번). 로그인뿐 아니라 최근 폴더 목록·확장 상태도 사라진다. 설정·확장은 남는다.
- `~/.git-credentials`, GitHub CLI 설정 폴더는 통째로 지우므로 그 안의 다른 서비스 계정도 함께 사라진다. SSH 에이전트의 모든 키도 내려간다.
- GCM 파일 저장소는 github.com 폴더만 지우고 다른 호스트는 남긴다.

## 검증 상태와 한계

- 두 스크립트 모두 이 저장소를 관리하는 Linux 호스트에서 가짜 홈 폴더로 검증했다. Windows 판은 PowerShell 7.6과 `cmdkey.exe`·`ssh-add`·`gh` 가짜 명령(영어·한국어 출력, 자격 증명 관리자가 비어 보이는 SSH 세션 상황 포함)으로, macOS·Linux 판은 실제 bash·git(`store` 도우미에 두 계정)으로 미리보기·실행·확인 거절·도우미 미설치 경우를 돌려 보았다. **실제 Windows PC와 Windows PowerShell 5.1에서는 아직 돌려 보지 않았다.** 테스트용 Windows 계정에서 `Preview-Reset.bat` → `GitHub-Classroom-Reset.bat` → 검증 단계 `[OK]`를 확인한 뒤 배포한다.
- 자동 정리 범위 밖: 브라우저 쿠키(로그아웃 페이지만 열어 줌), 사용자 환경 변수의 `GH_TOKEN`·`GITHUB_TOKEN`, `~/.ssh/config`의 github.com 항목과 사용자 지정 이름의 키, 저장소별 로컬 Git 설정, 시스템 범위 Git 설정, WSL 안의 별도 Git 자격 증명, JetBrains IDE·Sourcetree·GitKraken 등 다른 도구의 GitHub 계정, 해시된 `known_hosts` 항목. 이런 것이 의심되면 수동으로 확인한다.
- Windows 자격 증명 관리자 처리는 `cmdkey` 표시 문자열을 기반으로 한다. 검증 단계가 다시 조사하므로 남은 항목이 있으면 `[WARN]`에 이름이 나온다.

## 2026-11 개정에서 바뀐 것

이전 Windows 판이 "아무 효과가 없다"고 보였던 원인을 고쳤다.

- VS Code 로그인은 `%APPDATA%\Code\User\globalStorage\github.vscode-auth`라는 폴더를 지우는 것으로 처리했는데, 그런 경로는 어느 VS Code 판에도 없다. 실제 저장 위치(`state.vscdb`, Windows는 `.vscode-shared`도)를 지우고, VS Code가 켜져 있으면 알린다.
- GitHub 전용 `credential.https://github.com.*` 설정이 정규식 오류로 한 번도 지워지지 않았다. 이전 학생 이름이 다음 로그인 창에 미리 채워지는 원인이었다.
- 자격 증명 관리자만 비우고 **설정된 자격 증명 도우미에게 직접 지우라고 하지 않았다.** 이제 `git credential reject`로 어떤 도우미든 비우고, 끝에 `git credential fill`로 정말 비었는지 확인한다.
- `cmdkey /list` 출력에서 `User:` 줄까지 대상으로 잡던 것을 `…:target=` 줄만 보도록 바꿨다.
- Windows의 ssh-agent 서비스는 기본으로 꺼져 있는데 그 상태를 `[WARN]`으로 세어 늘 "경고와 함께 종료"가 나왔다. 이제 `[SKIP]`이다.
- GitHub CLI는 폴더만 지우던 것을 `gh auth logout`부터 하도록 바꿨다(gh의 도우미는 `erase`를 무시한다).
- 브라우저 세션이 남아 있으면 다음 push 한 번에 되돌아간다는 사실을 화면과 이 문서에 적고, `-OpenGitHubLogout`으로 로그아웃 페이지를 열어 준다.
- `.bat`·`.ps1`이 LF 줄바꿈으로 체크아웃되던 것을 `.gitattributes`에서 CRLF로 바꿨다(cmd.exe는 LF만 있는 배치 파일에서 `goto` 라벨을 놓칠 수 있다).
