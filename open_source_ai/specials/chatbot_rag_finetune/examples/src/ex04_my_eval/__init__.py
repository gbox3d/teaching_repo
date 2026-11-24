"""1교시: 내 평가 문항이나 공개 20문항을 14주 채점기로 재고, 잃은 점수를 실패 종류별로 나눈다.
채점은 14주 shared.evaluation.evaluate가 그대로 한다. 이 예제는 문항 내용 검사와 결과 읽기를 더한다."""

import json
import unicodedata
from datetime import datetime
from urllib.request import ProxyHandler, build_opener

import shared
from lab_shared import load_set, worker_command
from shared import configure_utf8, normalize
from shared.evaluation import QUESTION_TIMEOUT, WARMUP_TIMEOUT, evaluate, validate_dataset

BOT = "student_bot"  # "rag_bot"으로 바꾸면 특강의 임베딩 RAG 봇을 잰다.
QUESTION_SET = "mine"  # "public"이면 14주차 공개 20문항, "train"이면 3교시 학습 문항을 잰다.
OLLAMA_HOST = "http://127.0.0.1:11434"  # 평가 뒤 버전과 올라간 모델을 조회한다. 채점에는 쓰지 않는다.
RESPONSE_WIDTH = 160  # 문항별 응답·오류와 실패한 문항의 질문은 이 글자 수까지만 보여 준다.

# 실패 종류. 표는 이 순서로 출력한다.
STATUS_KINDS = {"timeout": "시간 초과", "error": "실행 오류", "invalid_response": "형식 오류"}
KINDS = (*STATUS_KINDS.values(), "답변 불가인데 답함", "답할 수 있는데 거절",
         "사실 누락·불필요한 답", "출처 누락·불필요한 출처")


def squeeze(text: str) -> str:
    """채점처럼 NFKC·casefold를 적용하고 공백을 모두 지운다. 별칭이 문서 본문에 나오는지 볼 때 쓴다."""
    return "".join(unicodedata.normalize("NFKC", text).casefold().split())


def check_content(questions: list, answers: list, corpus: list, public_questions: list) -> tuple[list, list]:
    """문항 내용을 검사해 (오류, 경고) 목록을 돌려준다. 형식은 validate_dataset이 따로 본다."""
    # 문항 작성 규칙대로 별칭은 근거 문서의 본문(text)에서 찾는다. 제목은 보지 않는다.
    documents = {doc["id"]: squeeze(doc["text"]) for doc in corpus}
    public = {normalize(question["question"]): question["id"] for question in public_questions}
    gold_by_id = {item["id"]: item for item in answers}
    errors, warnings, seen = [], [], {}
    for question in questions:
        item_id, item = question["id"], gold_by_id[question["id"]]
        key = normalize(question["question"])
        if key in public:
            errors.append(f"[{item_id}] 공개 문항과 같은 질문: {public[key]}")
        if key in seen:
            errors.append(f"[{item_id}] 세트 안에서 같은 질문: {seen[key]}")
        seen.setdefault(key, item_id)
        missing = [doc_id for doc_id in item["sources"] if doc_id not in documents]
        if missing:
            errors.append(f"[{item_id}] corpus에 없는 근거 문서 ID: {', '.join(missing)}")
        for index, group in enumerate(item["expected"]):
            # fact_sources가 있으면 그 사실의 근거 문서만, 없으면 문항의 근거 문서를 모두 본다.
            doc_ids = [item["fact_sources"][index]] if "fact_sources" in item else item["sources"]
            texts = [documents[doc_id] for doc_id in doc_ids if doc_id in documents]
            if texts and not any(squeeze(alias).rstrip(".") in text for alias in group for text in texts):
                warnings.append(f"[{item_id}] 사실 {index + 1}의 별칭이 근거 문서 본문에 없음: "
                                f"{group[0]} ({', '.join(doc_ids)})")
        if question["category"] == "composite" and len(item["expected"]) == 1:
            warnings.append(f"[{item_id}] composite인데 사실이 하나")
    return errors, warnings


def lost_points(row: dict) -> dict[str, float]:
    """채점 결과 한 행이 잃은 점수(100 - score)를 실패 종류에 나눈다. 다시 채점하지 않는다."""
    lost = 100 - row["score"]
    if row["status"] != "ok":
        return {STATUS_KINDS[row["status"]]: lost}
    if lost <= 0:
        return {}
    if row["gold"]["abstain"]:
        return {"답변 불가인데 답함": lost}
    if row["response"]["abstain"]:
        return {"답할 수 있는데 거절": lost}
    if row["subscores"]["answer_f1"] == 0:
        # 맞힌 사실이 없으면 출처 점수도 0이 되므로 잃은 점수를 모두 사실 쪽에 둔다.
        return {"사실 누락·불필요한 답": lost}
    parts = {"사실 누락·불필요한 답": 80 - row["subscores"]["answer_points"],
             "출처 누락·불필요한 출처": 20 - row["subscores"]["source_points"]}
    return {kind: points for kind, points in parts.items() if points > 1e-9}


def failure_table(results: list) -> list[tuple[str, list, float]]:
    """종류마다 (종류, 문항 id 목록, 잃은 점수 합)을 KINDS 순서로 돌려준다."""
    ids = {kind: [] for kind in KINDS}
    lost = dict.fromkeys(KINDS, 0.0)
    for row in results:
        for kind, points in lost_points(row).items():
            ids[kind].append(row["id"])
            lost[kind] += points
    return [(kind, ids[kind], lost[kind]) for kind in KINDS]


def shorten(text: str) -> str:
    return text if len(text) <= RESPONSE_WIDTH else text[:RESPONSE_WIDTH] + "..."


def print_result(row: dict) -> None:
    lost = lost_points(row)
    failures = ", ".join(f"{kind} -{points:.2f}" for kind, points in lost.items())
    print(f"[{row['id']}] {row['category']}  점수 {row['score']:.2f}  status={row['status']}"
          f"  실패: {failures or '없음'}")
    if lost:  # 실패한 문항은 질문도 보여 준다. 같은 질문을 ex07에 넣어 재현할 때 쓴다.
        print("    질문", shorten(" ".join(row["question"].split())))
    print("    응답", shorten(json.dumps(row["response"], ensure_ascii=False)), flush=True)
    if row["error"]:
        print("    오류", shorten(" ".join(row["error"].split())), flush=True)


def print_summary(report: dict) -> None:
    print(f"\n모델 준비 {len(report['warmups'])}회:", ", ".join(w["status"] for w in report["warmups"]))
    for category, values in report["categories"].items():
        mean = values["mean_score"]
        label = f"{mean:.2f}" if mean is not None else "해당 문항 없음"
        print(f"{category}: {values['count']}문항, 평균 {label}")
    print(f"전체 {report['total']}문항 평균: {report['mean_score']:.2f}/100")


def print_failures(report: dict) -> None:
    total = report["total"]
    print(f"\n실패 종류 표 (전체 평균에서 빠진 점수 = 잃은 점수 합 / 전체 {total}문항)")
    print("| 종류 | 문항 수 | 문항 id | 잃은 점수 합 | 전체 평균에서 빠진 점수 |")
    print("|---|---:|---|---:|---:|")
    missing = 0.0
    for kind, ids, lost in failure_table(report["results"]):
        missing += lost / total
        print(f"| {kind} | {len(ids)} | {', '.join(ids) or '-'} | {lost:.2f} | {lost / total:.2f} |")
    mean = report["mean_score"]
    print(f"빠진 점수 합 {missing:.2f} + 전체 평균 {mean:.2f} = {missing + mean:.2f}")


def fetch(path: str) -> dict:
    # 조회만 한다. 로컬 요청은 운영체제·환경 변수의 외부 프록시를 거치지 않는다.
    with build_opener(ProxyHandler({})).open(OLLAMA_HOST.rstrip("/") + path, timeout=5) as response:
        return json.load(response)


def loaded_models() -> list[str]:
    """평가 뒤 Ollama에 올라가 있는 모델마다 이름과 digest 앞 12자리. BOT이 쓰지 않는 모델도 나온다."""
    try:
        models = fetch("/api/ps")["models"]
        return [f"{model['name']} digest {model['digest'][:12]}" for model in models] or ["없음"]
    except Exception as exc:  # 조회 실패는 기록 칸만 비우고 평가 결과는 그대로 둔다.
        return [f"확인 못 함 ({type(exc).__name__})"]


def ollama_version() -> str:
    try:
        return str(fetch("/api/version")["version"])
    except Exception as exc:
        return f"확인 못 함 ({type(exc).__name__})"


def print_record(report: dict) -> None:
    categories = ", ".join(
        f"{name} {values['mean_score']:.2f}" if values["mean_score"] is not None else f"{name} 문항 없음"
        for name, values in report["categories"].items())
    print("\n기록할 값")
    print(f"- 실행 시각: {datetime.now():%Y-%m-%d %H:%M}")
    print(f"- 문항 세트: {QUESTION_SET} ({report['total']}문항)")
    print(f"- BOT: {BOT}")
    print(f"- 전체 평균: {report['mean_score']:.2f}")
    print(f"- 범주 평균: {categories}")
    for model in loaded_models():  # 모델마다 한 줄. 기록표에는 BOT이 쓰는 모델의 줄만 옮긴다.
        print(f"- 평가 뒤 올라가 있는 모델: {model}")
    print(f"- Ollama 버전: {ollama_version()}")


def main() -> None:
    configure_utf8()
    try:
        command = worker_command(BOT)
        questions, answers = load_set(QUESTION_SET)
        validate_dataset(questions, answers)  # 형식이 맞아야 내용을 볼 수 있다. evaluate도 다시 확인한다.
        print(f"평가 대상: BOT={BOT}, 문항 세트={QUESTION_SET} ({len(questions)}문항)")
        if QUESTION_SET != "public":
            corpus = json.loads((shared.DATA_DIR / "corpus.json").read_text(encoding="utf-8"))
            errors, warnings = check_content(questions, answers, corpus, load_set("public")[0])
            print(f"내용 검사: 오류 {len(errors)}건, 경고 {len(warnings)}건")
            for message in errors:
                print("  오류", message)
            for message in warnings:
                print("  경고", message)
            if errors:
                print("오류를 고친 뒤 다시 실행하세요. 평가는 시작하지 않았습니다.")
                raise SystemExit(1)
        print(f"모델 준비: 워커 시작마다 최대 {WARMUP_TIMEOUT:g}초, 준비 질문은 점수에서 제외합니다.")
        print(f"평가: {len(questions)}문항, 문항당 최대 {QUESTION_TIMEOUT:g}초입니다.\n", flush=True)
        report = evaluate(questions, answers, worker_command=command, on_result=print_result)
    except KeyboardInterrupt:
        print("\n평가 중단: 워커 종료 완료. 전체 평가 점수는 산출하지 않습니다.")
        return
    except (OSError, ValueError) as exc:
        print(f"평가 시작 오류: {exc}")
        raise SystemExit(1) from exc
    print_summary(report)
    print_failures(report)
    print_record(report)
