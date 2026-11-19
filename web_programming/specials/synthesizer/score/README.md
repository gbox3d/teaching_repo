# 참고 악보 JSON

이 폴더의 JSON 3개는 `track_info`, `score` 및 선택적 `master_templates`를 사용하는 참고 자료입니다. 연주기의 `sections[].progression[]` 형식과 다르므로 조합기에서 직접 열면 `sections 배열이 없습니다` 오류가 발생합니다. 외부 음악 주소를 자동으로 실행하거나 음원을 내려받지 않습니다.

| 파일 | 기준 정보 |
|---|---|
| [hyunjinyoung_sexy_woman_quantized_score.json](hyunjinyoung_sexy_woman_quantized_score.json) | Fm · 112 BPM |
| [kiiikiii_pop_off_pop_off_full_melody_score.json](kiiikiii_pop_off_pop_off_full_melody_score.json) | F#m · 128 BPM |
| [savage_only_you_full_score.json](savage_only_you_full_score.json) | Am · 109 BPM |

선택 연구에서는 구간·마디·음 데이터를 먼저 조사하고, [연주기 형식](../examples/build/README.md)에 맞춰 변환합니다. 반복 템플릿을 펼치는 규칙과 박자 단위를 확인한 뒤 변환해야 합니다. 이 특강에는 자동 변환기가 포함되어 있지 않습니다. 공개 결과물에는 직접 만든 자료 또는 사용 권한을 확인한 자료를 사용합니다.
