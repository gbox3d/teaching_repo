# (프로젝트 이름)

> 한 문장: (사용자)가 (상황)에서 (문제)를 해결하도록 (핵심 기능)을 제공하는 로컬 AI 도우미.

## 무엇을 하는가

- (Must 1)
- (Must 2)
- (Must 3)

## 왜 만드는가

(문제 문장과 기존 해법의 한계 2~3문장. `docs/proposal.md`의 문제 절과 같은 내용이어야 한다.)

## 설치

```powershell
git clone (팀 저장소 URL)
Set-Location (폴더)
Copy-Item .env.example .env
uv sync
```

정확한 Python·uv·Ollama·모델 버전은 학기별 환경 기준표를 따른다.

## 실행

```powershell
uv run team-project doctor
```

(12주차 이후 서비스 실행 명령을 여기에 추가한다.)

## 예시

(입력 → 출력 예시 1개. 실제 실행 결과를 붙인다.)

## 제한

- (아직 못 하는 것, 알려진 오류)

## 프로젝트 문서

- 제안서: `docs/proposal.md`
- 마일스톤: `docs/milestones.md`
- 기여 방법: [CONTRIBUTING.md](CONTRIBUTING.md)
- 행동 강령: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- 출처·라이선스: [SOURCES.md](SOURCES.md)

## 라이선스

이 저장소의 코드는 (MIT 또는 Apache-2.0) 라이선스를 따른다. 선택 이유: (한 문장). 모델·데이터의 라이선스는 [SOURCES.md](SOURCES.md)에 따로 적는다.

## 팀

| 표시 이름 | 역할 | 이번 마일스톤 담당 |
|---|---|---|
| student01 | 모델·실험 | M1 |
| student02 | 데이터·평가 | M1 |
| student03 | 서비스·릴리스 | M2 |

실명·학번·연락처를 적지 않는다.
