# 오픈소스 AI 응용 공용 교재

## 목차

- [범위](#범위)
- [현재 상태](#현재-상태)
- [학교 적용](#학교-적용)
- [환경 원칙](#환경-원칙)

## 범위

Git·GitHub, 재현 가능한 Python 환경, Ollama, Hugging Face 공개 자원, RAG,
PEFT/LoRA, 테스트·보안·릴리스까지 연결하는 오픈소스 AI 응용 교재 영역이다.

## 현재 상태

교재 본문과 실행 패키지는 아직 없으며, [`materials_plan.md`](materials_plan.md)가 제작 범위와 품질 기준의 초안이다.
초안은 특정 학교의 적용안을 출발점으로 하므로 배점과 일정은 공용 불변 규칙이 아니다.

- 과목별 설치 프로그램: [`ta_setup_guide.md`](ta_setup_guide.md)
- 공통 설치 프로그램: [`../ta_lab_setup_guide.md`](../ta_lab_setup_guide.md)
- 환경 기준표: [`../environment_baseline_template.md`](../environment_baseline_template.md)

## 환경 원칙

- Python 패키지는 전역 `pip`가 아니라 `uv` 기반 격리환경과 lock 파일로 재현한다.
- Python·PyTorch·Ollama·모델 ID·양자화·GPU 드라이버·VRAM 기준은 환경 기준표에서 확정한다.
- 모델 다운로드 크기와 캐시 위치를 먼저 계산하고, 수업 직전 여러 PC에서 동시에 내려받지 않는다.
- GPU 실패 때 사용할 CPU 또는 소형 모델 대체 경로를 함께 검증한다.
