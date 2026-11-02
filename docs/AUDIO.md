> 이 문서는 v0.4 진단·제작 이력입니다. 현재 전체9종은 [v0.4.2 안내](VOICE_UNIFICATION.md), 자연음은 [v0.4.1 믹스](AUDIO_REMIX.md)를 따릅니다. 아래 기기음성8종/합성도자기 설명은 당시 상태입니다.

# 오디오 v0.4 · 모바일 청취 검증 대기

## 진단과 변경

기존 코드는 음성 목록을 한 번만 읽어, 모바일의 빈 초기 목록을 음성 부재로 오인했습니다. 첫 speak가 requestAnimationFrame에서 호출되어 사용자 제스처 경계도 불확실했고, 재생 실패는 보이는 오류 없이 지나갔습니다. 이는 코드에서 확인한 취약점이며 실제 해당 휴대폰에서 원인이 재현·확정된 것은 아닙니다.

- voiceschanged + 지연 재확인, 빈 목록에서도 ko-KR 요청. 한국어가 없거나 시작/종료 이벤트가 누락되면 코드와 원인 표시. onstart/onend/onerror 수집. 선택 모드 자동 변경 없음.
- 시작·재개·음성 확인 버튼의 터치에서 AudioContext resume 및 기기 음성 요청. 사전 제작 파일은 미리 디코딩한 뒤 같은 시계로 자막과 파일을 시작. 파일 실패 시 멈추고 다시 듣기/자막 선택 제공.
- 호흡 알아차리기 5분: 문장별 한국어 MP3 7개. 자막 창은 디코딩 길이 사용. 중간 침묵·기존 문구 유지. 일시정지에서 소스 정지, 재개 시 경과 위치에서 새 소스 생성. 전체 300초 미리 듣기는 침묵을 포함한 검토 파일이며 앱은 문장별 파일 사용.
- 다른 8종: 브라우저 한국어 TTS 임시 유지. 기기별 음색/길이는 달라질 수 있어 자막 지속은 추정값. 파일럿 승인 전 확장하지 않음.
- 자연음/안내 gain 독립, 안내 시작 시 자연음 42%로 duck. 가이드 Off는 안내 소스 취소. 공간 변경은 시간·대본 유지, 배경만 짧은 crossfade, 이전 효과음 분리. pause 시 액센트 정지. 비동기 재생 토큰으로 늦게 완료된 로드 무시.
- 설정 → 오디오 오류 확인: context 상태, 소스, 최근 시작/종료·오류코드. 메모리 전용, 외부 전송/저장 없음. 재생 이벤트 확인은 실제 스피커 청취 확인이 아님.

## 파일럿 음성 제작

공식 MeloTTS (MIT), 모델 myshell-ai/MeloTTS-Korean (MIT), 기본 KR 화자. 특정 인물 음성 복제 없음. speed .98 / noise_scale .45 / CPU. 한국어 BERT kykim/bert-kor-base. FFmpeg highpass60Hz, -19 LUFS / true peak -3dB, mono44.1kHz MP3 128kbps. 실측 길이·peak·RMS는 narration-audio-checks.json. 비제로 파형·간격·디코딩 확인, 음색/발음/실제 청취는 미확인.

- 공식 소스: https://github.com/myshell-ai/MeloTTS
- 모델과 라이선스: https://huggingface.co/myshell-ai/MeloTTS-Korean
- MIT 고지: licenses/MeloTTS-MIT.txt
- 제작 도구: tools/audio/{generate_pilot,package_pilot,prepare_nature}.py. ffmpeg 및 Python 환경 필요. PILOT_WAV_DIR / NATURE_SOURCE_DIR 지정. Korean-only Melo 소스와 torch2.6 CPU, transformers4.38.2를 사용. g2pkk의 NLTK 원격 corpus 호출 대신 PyPI cmudict의 로컬 사전을 사용했음. 모델/가상환경은 배포에 포함하지 않음.

새 파일은 dist/narration-assets.js에 session key / cue ID / src / 실측 duration / text를 추가. 원문은 guides.js의 timeline과 일치해야 함. caption window가 다음 cue 전 3초를 침범하지 않는지 확인. 실제 발음과 호흡 5분 믹스를 승인한 뒤 나머지 8종을 제작.

## 음원 사용 권한과 편집

| 파일 | 출처 / 권한 | 편집 / 한계 |
|---|---|---|
| water-bed.mp3 | Stream Sounds, kurt, CC BY 3.0; https://opengameart.org/content/stream-sounds | stream1.ogg를 고역/저역·음량 보정, 30초 구간의 끝/처음 1.5초 crossfade. 잔잔한 수면에 어울리는지는 청취 평가 필요 |
| forest-bed.mp3 / forest-bird.mp3 | Park Ambiences, Thimras, CC0; https://opengameart.org/content/park-ambiences | park_ambience_birds.wav에서 배경/새 구간 추출, EQ·음량·루프 편집. 호주 Adelaide 녹음, 제주 현장 아님 |
| ceramic-tone.mp3 | 자체 제작 정현파 공명음 | 실제 도자기 녹음 아님. 허가된 실제 울림으로 교체할 임시 파일 |

CC BY 3.0: https://creativecommons.org/licenses/by/3.0/ ; CC0: https://creativecommons.org/publicdomain/zero/1.0/ . 원작 페이지의 배포 허가 확인, 앱 소개에 저자·원문·라이선스·편집 표시. 미사용 다운로드는 배포 제외. 자연음 액센트는 좌우 ±0.35 범위, 초기22~40초 후 물42~87초/숲34~79초 간격. 8초 미리 듣기는1.7초에 대표 클립,5.2초 추가,8초 종료. 홈 진입 자동 소리 없음.

## 검증 상태

자동 테스트: 음성 목록 지연, 한국어 없음, onerror, 시작 타임아웃, 파일 실패, resume seek, 로드 중 취소, 세션 시계·빠른 공간 변경·미리 듣기 총12개 통과. MP3 7개 파형 비제로, peak<1, 다음 문장과 겹치지 않음.

실제 iPhone Safari / Android Chrome의 스피커·이어폰 청취, 음색·발음·주관적 음질, 전체5분 음성/자막 체감 동기, 전화/화면 잠금 복귀는 **미검증**. 클라우드 Chrome에서는 파일 시작/종료, 음성만 모드, 6.415초 seek 재개, 물→숲 변경 후 시간 유지, 독립 음량(자연음0/안내100), 가이드Off를 DOM·진단 이벤트로 확인했습니다. 처음 발견한 fetch receiver 오류는 바인딩으로 수정하고 회귀 검사했습니다. 클라우드 데스크톱 브라우저 재생 이벤트만으로 휴대폰 청취 성공을 판단하지 않음.

휴대폰 확인: 음성 확인 → 호흡5분 음성만 시작 → 첫 문장과35초 문장 → 일시정지/재개 → 설정에서 두 음량 독립 조절 → 가이드Off → 공간 변경 → 종료. 문제가 있으면 오디오 오류 확인의 코드와 기기/브라우저를 확인. 오류 기록에는 명상 이력을 저장하지 않음.
