# 2주차 예제 — 협업 템플릿과 라이선스 도구

이번 주 예제는 Python·GPU·모델이 필요 없다. Git, PowerShell, 브라우저만 쓴다. 파일은 모두 개인 저장소나 별도 연습 폴더에 **복사해서** 쓰고, 수업 자료 원본은 수정하지 않는다.

## 파일 구성

| 파일 | 역할 | 쓰는 교시 |
|---|---|---|
| `pr_template/.github/PULL_REQUEST_TEMPLATE.md` | PR을 열 때 본문에 자동 삽입되는 양식 | 2교시 |
| `pr_template/.github/ISSUE_TEMPLATE/proposal.md` | "제안(proposal)" Issue 양식 | 2교시 |
| `CONTRIBUTING_sample.md` | 기여 절차·규칙 안내 예시 | 2교시 확장, 9주차 |
| `license_cards.md` | 라이선스 판별 카드 10문항(정답 없음) | 3교시 |
| `license_matrix_template.md` | 코드·모델·데이터 라이선스 표 양식 | 3교시 |
| `merge_conflict_demo.ps1` | 같은 줄 충돌을 재현하는 명령 순서(실행 가능) | 1교시 시연·확장 |

## 실행 방법

아래에서 `<수업자료>`는 수업 자료 저장소를 clone한 폴더, `<개인 저장소>`는 1주차에 만든 개인 연습 저장소 폴더다.

### 템플릿 설치(2교시 준비)

개인 저장소의 `main`에 `.github/` 폴더를 넣고 push해야 짝이 여는 Issue·PR에 양식이 나타난다.

```powershell
Set-Location <개인 저장소>
git status
Copy-Item -Recurse <수업자료>\open_source_ai\weeks\week02_git_github_license\examples\pr_template\.github .\.github
git add .github
git commit -m "Add issue and PR templates"
git push
```

### 판별 카드·라이선스 표(3교시 준비)

```powershell
Set-Location <개인 저장소>
Copy-Item <수업자료>\open_source_ai\weeks\week02_git_github_license\examples\license_cards.md .\license_cards_answers.md
Copy-Item <수업자료>\open_source_ai\weeks\week02_git_github_license\examples\license_matrix_template.md .\license_matrix.md
```

### 충돌 재현 스크립트(1교시 시연·확장)

별도 연습 폴더에서 실행한다. 현재 폴더 아래에 `conflict-demo` 저장소를 만들고 충돌 상태에서 멈춘다. 만들어진 저장소 안에서만 유효한 사용자 이름(`student01`)을 설정하며 전역 Git 설정은 바꾸지 않는다.

```powershell
Set-Location <연습 폴더>
pwsh -ExecutionPolicy Bypass -File <수업자료>\open_source_ai\weeks\week02_git_github_license\examples\merge_conflict_demo.ps1
```

충돌 해결과 merge commit까지 자동으로 보려면 `-AutoResolve`를 붙인다. 다른 위치나 이름으로 만들려면 `-Path`, `-Name`을 쓴다.

```powershell
pwsh -ExecutionPolicy Bypass -File <수업자료>\open_source_ai\weeks\week02_git_github_license\examples\merge_conflict_demo.ps1 -Name conflict-auto -AutoResolve
```

`pwsh`(PowerShell 7)가 없으면 `powershell`로 바꿔 실행한다. 다만 Windows PowerShell 5.1은 BOM 없는 UTF-8 스크립트를 ANSI로 읽으므로 콘솔에 찍히는 한국어 안내 문구가 깨져 보인다. git 단계는 그대로 동작하며 안내 문구는 이 문서와 `lab.md`를 본다. 스크립트가 만드는 README 내용은 콘솔 코드페이지와 무관하게 보이도록 영문이다.

## 관찰 지점

1. `merge_conflict_demo.ps1` 4단계의 `git log --graph --oneline --all`: 두 갈래가 같은 commit에서 갈라진 모양
2. 5단계의 `git status --short`: `UU README.md`(both modified)와 README 안의 `<<<<<<< HEAD`, `=======`, `>>>>>>> feature/readme`
3. `-AutoResolve` 6단계의 graph: 부모가 둘인 merge commit(`*   ... Merge branch 'feature/readme'`)
4. GitHub에서 Issue를 새로 만들 때 "제안(proposal)" 선택지가 나타나는지, PR 본문에 체크리스트가 자동으로 들어오는지
5. `license_cards.md`에서 판단이 "조건부"인 카드가 몇 개인지, 조건이 무엇에 걸려 있는지(고지, 소스 공개, 네트워크, 비상업, 사용 정책)

## GPU 없을 때·네트워크 없을 때 대체 경로

- GPU: 이번 주는 GPU를 쓰지 않는다. 대체 경로가 필요 없다.
- Ollama·모델: 이번 주는 Ollama 서버와 모델을 쓰지 않는다. 서버가 꺼져 있거나 모델이 없어도 영향이 없다.
- GitHub 접속 불가(1교시): 로컬 bare 저장소를 원격으로 삼아 `push`·`fetch`·`pull`까지 진행한다. 접속이 복구되면 `git remote set-url origin <GitHub URL>`로 바꾼다.

```powershell
git init --bare ..\osa-practice-remote.git
git remote add origin ..\osa-practice-remote.git
git push -u origin main
```

- GitHub 접속 불가(2교시): Issue·PR·리뷰는 GitHub 기능이므로 접속이 복구된 뒤 한다. 그동안 짝의 저장소를 로컬 경로로 clone해 branch·commit까지 준비하고, 리뷰 코멘트는 `REVIEW.md`에 줄 번호와 함께 적어 두었다가 복구 후 PR에 옮긴다.
- GitHub 접속 불가(3교시): choosealicense.com도 열리지 않으면 강의자가 배포한 라이선스 원문 파일을 쓴다. 라이선스 표의 출처 URL 칸은 접속 복구 후 채운다.

## 복사 후 변형

- `.github/` 템플릿의 항목 이름·순서는 자기 프로젝트에 맞게 바꿔도 된다. 단 "관련 Issue", "확인 방법", "비밀 없음" 세 항목은 유지한다.
- `CONTRIBUTING_sample.md`의 branch 규칙·응답 시간은 팀 규칙으로 바꾼다. 9주차 팀 저장소 템플릿에서 다시 쓴다.
- `license_matrix_template.md`의 예시 행(`httpx`)은 직접 출처를 확인한 뒤 유지하거나 수정한다. 확인하지 않은 값을 그대로 두지 않는다.
- `merge_conflict_demo.ps1`의 문장을 바꿔 다른 줄·다른 파일에서 충돌이 나는지, 나지 않는지 실험한다.
