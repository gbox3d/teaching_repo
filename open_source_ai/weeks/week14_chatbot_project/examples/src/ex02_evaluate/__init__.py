import json

from shared import DATA_DIR, configure_utf8
from shared.evaluation import QUESTION_TIMEOUT, WARMUP_TIMEOUT, evaluate


def print_result(row: dict) -> None:
    print(f"\n[{row['id']}] category={row['category']}  {row['question']}")
    print("response:", json.dumps(row["response"], ensure_ascii=False))
    print("gold:", json.dumps(row["gold"], ensure_ascii=False))
    print("subscores:", json.dumps(row["subscores"], ensure_ascii=False))
    print(f"score={row['score']:.2f}/100  status={row['status']}  latency={row['latency']:.3f}s")
    print("error:", row["error"] or "없음", flush=True)


def main() -> None:
    configure_utf8()
    try:
        questions = json.loads((DATA_DIR / "public_questions.json").read_text(encoding="utf-8"))
        answers = json.loads((DATA_DIR / "public_answers.json").read_text(encoding="utf-8"))
        print(f"모델 준비: 워커 시작마다 최대 {WARMUP_TIMEOUT:g}초, 준비 질문은 점수에서 제외합니다.")
        print(f"공개 시험: {len(questions)}문항, 문항당 최대 {QUESTION_TIMEOUT:g}초입니다.", flush=True)
        report = evaluate(questions, answers, on_result=print_result)
    except KeyboardInterrupt:
        print("\n평가 중단: 워커 종료 완료. 전체 평가 점수는 산출하지 않습니다.")
        return
    except (OSError, ValueError) as exc:
        print(f"평가 시작 오류: {exc}")
        raise SystemExit(1) from exc
    for number, warmup in enumerate(report["warmups"], 1):
        print(f"\n모델 준비 {number} 결과:", json.dumps(warmup, ensure_ascii=False))
    for category, values in report["categories"].items():
        mean = values["mean_score"]
        label = f"{mean:.2f}" if mean is not None else "해당 문항 없음"
        print(f"{category}: {values['count']}문항, 평균 {label}")
    print(f"전체 {report['total']}문항 평균: {report['mean_score']:.2f}/100")
    print(f"총 소요 시간: {report['elapsed_seconds']:.3f}초 (준비 포함, 점수 반영 없음)")
