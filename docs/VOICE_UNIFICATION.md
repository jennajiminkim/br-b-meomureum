# v0.4.2 · 안내 목소리 통일

사용자 요청: 기존보다 살짝 낮은 피치, 차분하고 담백한 목소리. 모든 명상 안내 음성을 하나로 통일. 이전 호흡5분의 정상 모바일 재생은 사용자 확인을 받았으나, 음색의 자연스러움은 개선 요청이 있었음.

## 현재 변경

- 호흡·몸의 감각·떠오르는 생각 ×3/5/10분, 9개 세션의63개 cue를 MeloTTS Korean 기본 KR 화자 하나로 제작. 중복 문장 공유로 실제 파일은55개. 기존 호흡5분의 원본 WAV7개는 같은 소스 재사용.
- 모든 파일에 동일한 pitch -0.6 semitones 적용. 비율2^(-0.6/12) ≈0.96594, 원래보다약3.4% 낮음. FFmpeg rubberband의 formant=preserved 사용, 속도·길이는 유지. 음량 -19 LUFS / true peak -3dB, mono44.1kHz MP3 128kbps. 음색을 깊게 바꾸거나 특정인의 화자를 복제하지 않음.
- 생성: speed .98, noise_scale .45, 같은 KR화자. 새 문장은 text hash로 seed를 고정. 안내 문구·cue 시작·세션 총길이·비판단적 원칙은 유지. 자막 종료는 파일의 실제 디코딩 길이에 맞춤. 긴 침묵 유지.
- NarrationEngine은 파일만 재생. browser speechSynthesis 코드 제거. 누락/실패는 오류를 표시하며 다른 기기 목소리로 자동 대체하지 않음.
- 모든 공간에서 같은 voiceId/meomureum-kr-v042 사용. 공간 변경은 자연음만 바꾸고 안내 음색·대본·시간을 유지. 가이드Off/모드·독립음량·pause/resume 취소 토큰 유지.
- v0.4.1의 물결·실제 도자기·새소리 믹스와 화면 디자인은 변경하지 않음.

## 파일과 재현

- dist/narration-assets.js:9개 세션, 동일 voiceId/settings, cue별src/text/duration. 이번 파일 버전의 mobile/human_listening은pending. 이전 버전의 사용자 정상 청취와 구분.
- dist/assets/audio/narration/ko-kr-v042/:55개 문장 MP3와 침묵을 포함한 호흡5분 검토 파일. 앱은 문장별 파일을 재생.
- docs/narration-audio-checks.json:63개 cue의duration/peak/RMS. docs/guide-timelines.json 및 GUIDE_TIMELINES.md가 같은 길이를 사용.
- tools/audio/generate_unified.py: 기존 Korean-only Melo 준비 환경에서 실행. UNIFIED_WAV_DIR 지정, 선택적으로 PILOT_WAV_DIR 지정. HF_HOME 모델 캐시, PYTHONPATH는공식 MeloTTS소스. 메모리 사용을 제한하기 위해 기본8개씩 제작하며 ALL_GENERATED까지 같은 명령을 반복. 각파일 뒤 gc/메모리 반환. 의존성·MIT출처는 AUDIO.md와 licenses/MeloTTS-MIT.txt 참고.
- tools/audio/package_unified.py: UNIFIED_WAV_DIR 지정 후 numpy/ffmpeg(rubberband 지원)로 전체 패키징. 공유 텍스트는 SHA256 앞20자로 식별. 모델/가상환경은 배포하지 않음.

## 검증과 한계

각 파일을 디코딩해 유한한 비제로 파형과 peak<1 확인. 모든 문장의 길이가 다음cue전3초를 침범하지 않는지 확인. 자동검사는9개 세션의동일목소리/피치, 원문일치, 실파일존재, 실측자막길이, 파일실패·resume seek·취소·가이드/세션/자연음회귀를 포함.

첫 문장의 간단한 자기상관 측정에서도 기본주파수 중앙값이 약222Hz→216Hz로 낮아짐을 확인했음(추정값, 전체 음색/청취 검증 아님).

클라우드Chrome에서9개 세션의첫파일 재생시작과 오류없음, 동일voiceId/-0.6pitch 진단, 음성만모드·가이드Off·공간변경 시간유지를 확인. 자동검사15개 통과. 실제파일 길이/원문/하나의목소리 검증과 실제청취를 구분.

이번 버전의 실제 휴대폰 청취·63개 문장의 발음·음색의 자연스러움은미검증. 피치를 낮춘 것만으로 사람의 호흡·억양·담백함이 완성됐다고 판단하지 않음. 참고영상 원본을 앱 음원으로 사용하거나 복제하지 않았음. 최종 청감은 사용자가 다시 확인해야 함.
