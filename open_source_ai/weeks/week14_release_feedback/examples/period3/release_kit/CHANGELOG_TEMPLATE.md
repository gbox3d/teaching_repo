# Changelog

이 프로젝트의 **사용자에게 보이는 변경**을 기록한다. 형식은 Keep a Changelog, 버전은 Semantic Versioning 을 따른다.
최신 버전이 위에 온다. commit 제목을 그대로 복사하지 않고 사용자 관점으로 다시 쓴다.

<!--
첫 릴리스 전에는 모든 변경이 [Unreleased] 아래에 쌓인다. 아래 항목은 예시이므로 팀 프로젝트 내용으로 바꾼다.
태그를 만들기 직전에 `tag_notes.py --version 0.1.0 --promote` 를 실행하면 [Unreleased] 절이
`[0.1.0] - YYYY-MM-DD` 절로 바뀌고 빈 [Unreleased] 절이 위에 새로 생긴다. 릴리스 뒤의 변경은 새 [Unreleased] 에 적는다.
맨 아래 링크 줄의 REPO_URL 은 태그를 push 한 뒤 실제 저장소 주소로 바꾼다.
-->

## [Unreleased]

### Added
- Ollama `/api/chat` 기반 질의응답 CLI (`chat`, `stream` 서브커맨드)
- 출처를 표시하는 문서 검색 답변기
- FastAPI `/health`, `/chat`, `/chat/stream`
- pytest 3개와 GitHub Actions CI

### Changed
- 설정을 `.env` 로 외부화 (`OLLAMA_HOST`, `OLLAMA_MODEL`)

### Fixed
- Ollama 미기동 시 502 대신 연결 안내 메시지를 반환 (#12)

[Unreleased]: REPO_URL/compare/v0.1.0...HEAD
[0.1.0]: REPO_URL/releases/tag/v0.1.0
