# 웹프로그래밍 실습조교용 설치 프로그램 목록

## 목차

- [필수 설치](#필수-설치)
- [필요할 때만 설치](#필요할-때만-설치)
- [별도 설치가 없는 서비스](#별도-설치가-없는-서비스)
- [설치 확인](#설치-확인)

## 필수 설치

| 프로그램 | 공식 경로 | 비고 |
|---|---|---|
| [Git for Windows](https://git-scm.com/install/windows) | Git 공식 사이트 | Git·GitHub 실습 |
| [VS Code](https://code.visualstudio.com/docs/setup/windows) | VS Code 공식 사이트 | 코드 편집 |
| [Node.js LTS](https://nodejs.org/en/download) | Node.js 공식 사이트 | npm이 함께 설치됨 |
| 학교 승인 브라우저 | Chrome 또는 Edge 공식 사이트 | DevTools 사용 가능 여부 확인 |

## 필요할 때만 설치

| 프로그램 | 설치 조건 |
|---|---|
| Python | 10주차 로컬 서버를 Python 방식으로 실행하기로 승인한 경우 |
| VS Code 확장 | 학기별 환경 기준표에 지정된 확장만 설치 |
| Marp | 조교가 슬라이드 변환까지 담당하는 경우 |

## 별도 설치가 없는 서비스

- GitHub와 GitHub Pages
- Supabase
- Kakao Developers

위 서비스는 브라우저에서 사용한다. 계정과 API key 운영 방식은 담당 교수 안내를 따른다.

## 설치 확인

```powershell
git --version
code --version
node --version
npm --version
```

정확한 Git·VS Code·Node.js 버전은 [학기별 환경 기준표](../environment_baseline_template.md)에서 담당 교수가 확정한다.
