# v0.4.1 자연음 조정 · 2026-11-02 KST

사용자 확인: 휴대폰에서 호흡 알아차리기5분의 오디오가 5분 동안 정상으로 들렸음. 발화는 기계적으로 느껴짐. 이는 v0.4 재생 확인이며 이번 자연음 믹스의 청취 승인이나 전체 기기 검증은 아님. 현재 음성 파일은 그대로 유지. 참고 MP3/MP4를 받으면 발화 속도·구절 안 쉼·문장 사이 침묵을 분석하여 다음 음성 초안을 제작할 예정. 특정 화자 복제나 참고 음원 원본 재배포는 별도 작업.

## 변경 전 → 후

| 항목 | v0.4 | v0.4.1 |
|---|---|---|
| 물 바탕 | 연속 흐르는 시냇물 | 짧은 실제 물결/물 튀김 4종을 속도80%, 작은 음량과 여백으로 배치한48초 루프 |
| 도자기 | 합성 공명음, 첫22~40초/이후42~87초 | 실제 도자기끼리 접촉한 녹음. 첫8~14초/이후18~34초. 클립peak .52 + 액센트gain1.15, 기존peak .21보다 접촉 순간을 강조 |
| 숲 바탕 | 배경의 새소리와 별도 새 클립이 겹침 | 배경1100Hz lowpass + 70% gain으로 새소리 대역 감쇠. 모든 새를 완벽 분리한 것은 아님 |
| 별도 새소리 | 2초, 첫22~40초/이후34~79초 | 0.9초, 약8dB 감쇠(peak .13/gain .65). 첫44~80초/이후68~158초로 세션 빈도 약절반 |
| 미리 듣기 | 두 공간 모두 2회 액센트 | 숲1.7초에1회, 물1.7/5.2초2회. 총8초 유지 |
| 겹침 | 이전 공간 효과음 분리 | 유지 + 같은 버스에 액센트1개만 허용. pause/switch/종료에서 액센트 정지 |

‘빈도 수를2정도 덜어’는 약절반으로 해석해 구현했음. 조정값은 dist/audio-mix.js, 에셋 경로는 assets.js. 고정48초 물 루프와34.5초 숲 루프 위에 액센트 간격·좌우 위치는 제한된 범위 안에서 변함. 물결 효과는 포스터 움직임에 물리적으로 동기화되지 않음.

## 출처·사용 조건

- Water Waves, transitking (OpenGameArt 제출 qubodup), CC0. https://opengameart.org/content/water-waves . 원본 freesound11505에서 추출된 wave_01~04_cc0-11505__transitking__wavesound.flac. 네 소스 각각1.75/3.25/2.35/2.02초. 속도·EQ·음량·페이드·시간 배치 편집. 기존 stream1은 더 이상 연결하지 않음.
- ceramicCups2.wav, kikuchiyo, CC0. https://freesound.org/people/kikuchiyo/sounds/214186/ . 설명은 short hits, ceramic clinking together. 공개 HQ 미리 듣기 MP3를 원본으로 편집(약1.089초). 무손실 WAV는 아님. highpass150/lowpass9000, peak .52, 끝/시작4ms 페이드. 합성 공명음을 덧붙이지 않음.
- 숲/새는 기존 Park Ambiences, Thimras, CC0. 호주 녹음이며 제주 현장 아님. 원문과 CC0 링크는 앱 소개에 유지. 기존 파일에서 필터/구간/음량만 변경.
- CC0: https://creativecommons.org/publicdomain/zero/1.0/ . 원작 페이지에서 공개 이용 조건 확인. 앱 소개에 출처·편집 명시. 기존 미사용 파일은 이전 버전 비교/재현용이며 앱은 v041 파일만 연결.

## 재현·검증

REMIX_SOURCE_DIR에 네 flac와 ceramic-real.mp3를 넣고 python3 tools/audio/remix_nature.py 실행(numpy/ffmpeg 필요). 숲의 기존 forest-bed.mp3/forest-bird.mp3도 입력으로 사용. 음성 MP3는 재생성하지 않음. audio-remix-checks.json은 인코딩 전 duration/peak/RMS. 디코딩 후 peak·파일 존재·테스트는 별도 확인.

자동 검사: 기존12개 + 새 간격 범위, 미리 듣기 액센트 횟수, 동시 액센트 방지3개. 실제 모바일에서 이번 자연음의 음량·음색·영상 적합성은 미검증. 사용자에게 기존 정상재생 확인과 이번 믹스의 추가 청취 필요를 구분해 보고할 것.
