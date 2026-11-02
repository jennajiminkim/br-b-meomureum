# BR-B 최종 검증·보완 보고서

검증일: 2026-11-02 (한국). **사용자가 제공한 Vercel 공개 배포를 확인했습니다.** 실제 휴대폰 청취와 새 Chrome 시크릿 창 검증은 남아 있으며, 전체 기준을 무조건 통과로 처리하지 않습니다.

- 기존 공개 앱(변경하지 않음): https://meomureum-quiet-space-jimin.jimn2xo.chatgpt.site/
- 새 원본 기반 소스: https://github.com/jennajiminkim/br-b-meomureum
- 제출용 Vercel 공개 URL: https://br-b-meomureum.vercel.app/
- BR-A: https://br-a-portfolio-lime.vercel.app/#projects
- 원본 provenance: Work/Sites 프로젝트 appgprj_6ae7e2e58c0c81918326d3e89f4e7933, 원본 commit fe770552e44e3cf60aa637e70876555317840bb7. 원본 Git 저장소에서 확보한 정적 소스·포스터·음원·9종 대본·테스트·제작 스크립트이며 웹 화면 재제작이 아닙니다. MP4/WebM은 원래 없고 video 태그의 소스는 비어 있습니다. 포스터 애니메이션이 실제 구현입니다. TTS 모델 가중치·외부 음원 원본·기존 업로드 참고 영상은 앱 실행 필수 에셋이 아니며 포함하지 않습니다.

## C01 · 논문에서 앱으로 이어지는 한 문장

「성인 범불안장애 치료 전후 뇌 기능적 연결성 변화: 공개 출판자료의 근거 종합과 요약통계 재분석」에서 일부 마음챙김 연구의 연결성 변화와 불안 변화 연관성이 보고됐으나 치료 간 공통·차이는 확정할 수 없었다는 결과를 바탕으로, 머무름은 일상에서 잠시 멈추고 싶은 사람이 자연의 소리와 짧은 안내로 비판단적 마음챙김을 직접 경험하도록 돕는 비치료적 보조 웹 앱이며 앱 자체의 치료 효과나 뇌 변화는 검증되지 않았습니다.

이번 근거 해석은 사용자가 이번 요청에 제공한 논문 정식 제목·핵심 결과를 기준으로 합니다. 전체 논문이나 원자료를 이번 작업에서 재분석한 것은 아닙니다. 범불안장애 환자의 치료를 목적으로 제공하지 않으며 임상 효능을 단정하지 않습니다.

## C02 · 세 가지 실제 행동

검증 환경: 로컬 preview http://terminal.local:4173/ 의 cloud Chrome. 아래 C02 표는 이전 로컬 검증 기록이며, 이번 Vercel 실배포 검증은 문서 끝의 추가 기록에서 구분합니다. 이벤트 기록은 소리를 사람이 들었다는 증거가 아닙니다.

| 행동 | 실행 위치·실제 조작 | 기대 | 실제 결과·오류 | 증거 |
|---|---|---|---|---|
| ① 공간·미리 듣기 | 홈에서 물결 8초 미리 듣기 클릭 → 종료 확인 → 숲 미리 듣기 클릭 → 재생 중 물결 공간 선택 | 한 미리 듣기만 재생, 8초 정지, 설정 이동 시 정지 | 물결 aria-pressed true→false, 숲 재생 표시, 설정 진입. 이후 진단 preview:false. 오류 표시 없음. 실제 청취는 별도 | 이 표의 실행 기록; tests/core.test.mjs, tests/audio-mix.test.mjs, evidence/node-tests.txt |
| ② 호흡·5분·음성+자막 | 물결 설정의 기본 호흡·5분·음성+자막으로 시작 | 05:00, 첫 자막과 해당 안내 파일 시작 | 05:00 및 첫 문장 표시. breath-5-0 file-start offset0 duration7.753초→file-ended. context running, lastError:null. 실제 음질·발음 청취 판정 안 함 | 아래 진단 발췌, dist/guides.js, dist/narration-assets.js |
| ③ 가이드·멈춤·종료 | 세션 설정에서 숲 전환·끄기 → 닫기 → 일시정지 → 재개 → 마무리·확인 | 타이머 유지, 가이드 중지, 중간 종료 문구 | 공간 바꾸기 전후04:30, 가이드 꺼짐, pause/resume04:23 유지. 중간 종료 문구·홈 버튼 표시. 별도 thought·3분·자막 세션은 실제 3분 후 정상 완료 문구 표시 | evidence/brb-early-end.jpg/.txt, evidence/brb-complete.jpg/.txt |

진단 발췌(직접 확인): context running, natural.preview false, natural.session true, natural.paused true(설정 패널), narration.session breath-5, source recorded, voiceId meomureum-kr-v042, pitchSemitones -0.6, volume .85, file-start breath-5-0 offset0 duration7.753015873, file-ended breath-5-0, lastError null. 설정 패널을 열면 의도적으로 세션이 일시정지합니다.

## C03 · 첫 화면 변경

메인 카피와 갤러리를 유지했습니다. home-intro 바로 아래 작은 연구 소개 영역에 논문 정식 제목, 대상·역할 한 문장, 근거와 한계를 추가했습니다. 상세 소개에 숨기지 않았습니다. evidence/brb-home.jpg/.txt는 로컬 수정본입니다. 기존 공개 ChatGPT 사이트는 보존했으며, 새 Vercel 공개 홈에서 이번 수정의 반영을 확인했습니다(evidence/brb-vercel-home.jpg/.txt). 375×812 CSS iframe viewport에서 제목·대상·한계가 첫 화면에 들어가는 것을 확인했습니다. 실제 휴대폰은 미검증이며, Vercel 데스크톱 홈은 확인했습니다.

## C04 · 근거 → 설계 → 행동 → 한계

| 논문 근거/별도 선택 | 앱에서 적용한 방법 | 사용자의 실제 행동 | 해석의 한계 |
|---|---|---|---|
| 사용자 제공 결과: 일부 마음챙김 연구의 연결성·불안 변화 연관성 | 호흡 알아차리기 프로그램으로 경험 경로 제공 | 지금의 자연스러운 호흡에 주의를 둠 | 앱이 해당 fMRI 변화를 재현하거나 불안을 치료한다는 근거 아님 |
| 마음챙김 접근을 바탕으로 설계자가 선택한 UX | 몸의 감각 살피기 | 접촉·무게·감각을 판단 없이 알아차림 | 이 앱의 몸 관찰 프로그램 자체가 논문에서 시험된 개입이라고 주장하지 않음 |
| 비판단성은 앱 설계 원칙 | 떠오르는 생각 바라보기, 공통 anchor 안내 | 원치 않는 생각·감정도 평가하지 않고 바라봄 | 생각 발생은 실패가 아니며 효과를 측정하지 않음 |
| 주의 관찰을 구현한 대본 선택 | “자연스럽게 이어지는 호흡”으로 돌아오는 안내·침묵 | 흩어진 주의를 호흡이나 주변 감각으로 돌려봄 | 개별 대본·침묵 길이의 임상 유효성은 별도 검증 안 됨 |
| 치료 간 공통·차별적 변화 확정 불가 | 효과 점수·뇌 변화·치료 보장 없음 | 로그인·기록 없이 필요한 동안 머묾 | 무기록·두 공간·시간 선택은 사용자/설계자의 UX 결정이며 논문 fMRI가 직접 입증한 설계 아님 |

## C05 · 정상·비정상 기능 검사

| 검사 | 실행 범위 | 결과/상태 | 증거 |
|---|---|---|---|
| 두 공간 선택·전환 | 실제 Chrome UI | 충족; 세션04:30 유지 | C02 기록 |
| 3프로그램×3시간 선택 | 9조합 실제 클릭, aria-pressed 확인 | 충족(선택); 9종 전체 시간을 청취한 것은 아님 | evidence/brb-selections.json |
| 9종 대본·음원·자막 시간 | Node 실제 실행 | 충족;63cue 파일·동일화자·측정길이·침묵 간격 | evidence/node-tests.txt |
| 음성+자막 | 호흡5분 시작 | 부분 충족; 시작 로그·첫 자막 확인, 실제 청취 미검증 | C02 진단 |
| 음성만 | 실제 음성만 UI 및 breath-5-1 재생 로그 | 부분 충족; breath-5-1 file-start/end 확인, 실제 청취 안 함 | dist/app.js, tests/narration.test.mjs |
| 가이드 Off·다시 켜기 | Off→On 복원·음성만 실제 UI | 부분 충족; Off→On 시 음성만 모드 복원·자막 비움 확인, 청취 미검증 | C02 |
| 일시정지·재개 | 실제 UI와 시계 단위 검사 | 충족(상태·시간); 청감상 무중첩은 별도 | C02, tests/core.test.mjs |
| 정상 완료·중간 종료 | 실제3분 thought·text 완료 / 호흡5분 중간 종료 | 충족; 서로 다른 정확한 문구 | evidence/brb-complete.*, brb-early-end.* |
| 빠른 연속 시작·공간 변경·미리 듣기 취소 | 비동기 경합·취소 단위 검사 | 부분 충족; 엔진 경합 테스트 통과. 시작 dblclick 후 단일 세션 확인. 실기기 다중 터치 스트레스 미검증 | tests/core.test.mjs, tests/audio-mix.test.mjs |
| 미리 듣기 중 다른 공간 선택 | 숲 미리 듣기 중 물결 설정 진입 | 충족; preview false 확인 | C02 |
| 파일 로딩 실패 | 내레이션 실패·취소 단위 검사 | 부분 충족; FILE_PLAY_FAILED/HTTP_404 및 취소 시 무재생. 실제 자연음 누락 AMBIENT_LOAD alert 확인 | tests/narration.test.mjs |
| 영상 로딩 실패 | 영상 없음·포스터 표시 실확인, error 핸들러 코드 검토 | 부분 충족; 실제 손상 영상은 미검증 | dist/assets.js, dist/media.js |
| 작은 모바일 화면·실기기 | 375×812 iframe 실제 렌더·설정5분 클릭 | 부분 충족; 콘텐츠 viewport360px(scrollbar15px), scrollWidth360으로 가로 넘침 없음. 실제 휴대폰 미검증 | evidence/brb-mobile-375.*, brb-mobile-settings.* |
| 새로고침 | Vercel 세션 중 실제 reload | 충족; 진행 상태를 저장하지 않고 홈·소리 활성화로 초기화 | evidence/brb-vercel-reload.txt |
| 브라우저 뒤로 가기 | Vercel back→about:blank, forward→공개 앱 | 충족(관찰 범위); 내부 화면 history route는 없어 이전 문서로 이동하며 복귀 시 홈. 화면별 뒤로 이동 기능은 아님 | evidence/brb-vercel-history.txt |
| 독립 음량 | 실제 UI 자연음35→30%, 안내85→80% 독립 조작 | 부분 충족 | dist/app.js, tests/narration.test.mjs |

사용자가 이전에 실제 휴대폰 호흡5분의 한국어 음성 정상 재생과 v0.4.5 자연음 만족을 확인했습니다. 이번 새 배포·9개 세션·최종 피치 전부의 실기기 확인으로 확대 해석하지 않습니다. 브라우저 console에는 확장프로그램 chrome-extension 출처의 metadata 오류가 있었으며 앱 자체 오디오 진단 lastError는 null이었습니다.

## C06·C07·C12 · 개인정보·비밀값·미디어

- evidence/source-audit.json: 텍스트 소스의 private key·GitHub token·API key·AWS·JWT·하드코딩 credential·이메일·한국 휴대폰 패턴 검사. 실제 값을 보고서에 복사하지 않습니다. .env 파일 없음. 서버/API/환경변수 필요 없음. 임상 개인별 데이터 없음.
- evidence/asset-manifest.json: 배포 대상 에셋 파일명·크기·SHA256. 파일 누락·MP3 디코딩 오류 없음.
- 패턴 검사는 모든 형태의 비밀값 부재를 증명하지 않으며 이름·음성·영상 속 개인정보를 자동 판독한 검사도 아닙니다. 전체 GitHub 계정·다른 저장소 과거 이력을 이 결과로 보증하지 않습니다.
- MEDIA_LICENSES.md: 현재 사용 소스의 원문 CC0·MeloTTS 모델 MIT 재확인, 제작법·수정법·실제 제주 자료가 아님 명시. 기존 미사용15개 음원·검토 믹스는 신규 제출 저장소에서 제외; 원본 Work 소스는 보존.
- 참고 영상 원음·추출 Clinamen 파일은 배포하지 않음. 타인 후기 이름 없음. 소스의 공개 제작자 이름·URL은 저작자 출처 표기.

## C08·C15·C22 · 공개 배포 상태

제출용 공개 주소: https://br-b-meomureum.vercel.app/ . 사용자가 주소를 제공한 뒤 cloud Chrome에서 계정 생성·로그인·초대·CAPTCHA·비밀번호 요구 없이 홈·연구 소개·두 공간을 확인했습니다. 인증 쿠키나 Authorization 없이 독립 HTTP 요청을 보내 홈과 실행 파일도 확인했습니다. 이것은 새 Chrome 시크릿 창의 실측과 구분합니다.

배포 파일 86개 요청 중 실행 파일·에셋 85개는 HTTP200 및 로컬 원본과 SHA256이 같았습니다. 현재 사용 미디어 72개 전부 포함입니다. dist/README.md 한 개는404였으며 이 배포에서 제공되지 않은 비실행 개발 메모입니다. 이미지·음원·JS 누락은 발견하지 못했습니다(evidence/vercel-http-assets.json). 실제 Vercel 대시보드의 Git 연결/배포ID는 연결된 API 계정 권한 범위에서 확인하지 못했으며, API가 배포했다고 주장하지 않습니다.

정적 설정은 저장소 루트 / Framework Other / Build·Install 비움 / Output dist, vercel.json입니다. 앞선 API 생성403은 당시 시도의 실패 이력이고 현재 공개 배포 실패를 뜻하지 않습니다. 원본 ChatGPT 사이트는 유지했습니다. 기존 공개 앱의 시크릿 접근은 사용자 확인 자료이며, **새 Vercel URL의 실제 휴대폰 청취·새 시크릿 창은 아직 미검증**입니다.

## C10 · BR-A 대표작 연결과 순서

BR-A index.html의 13번 앱 카드 한 곳만 교체했습니다. 작품명·논문 기반 비치료적 설명·한계와 **확인한 새 Vercel 공개 앱 링크 https://br-b-meomureum.vercel.app/**를 연결했습니다. GitHub commit72765d3a46c5579ac145c84cfac93db063717d76. 기존 Vercel 자동배포가 반영된 공개 페이지에서 카드·링크를 직접 확인했습니다(evidence/brb-portfolio-link.jpg/.txt). 자기소개서·문서3종·수치·다른 작품은 변경하지 않았습니다. 후속 commit63ade697d588e375a7afa48b7b7a4bb8b623f2de에서 링크 주소만 Vercel로 변경했습니다. 공개 BR-A 페이지에서 링크 href가 새 Vercel 주소인 것을 직접 확인했습니다(evidence/brb-vercel-portfolio.txt/.jpg).

BR-A 원본 README와 제출문에는 13번 앱 제작예정(2026-11-01)이라고 기록돼 있었고 저장소는 BR-B보다 먼저 공개되어 있었습니다. 과제 시스템의 BR-A 최종 제출·승인 상태에는 접근하지 못했습니다. 따라서 최종 확정을 확인했다고 말하지 않습니다. BR-B 완성 후 BR-A 최종 확정이라는 순서 조건이 있다면 제출·승인 이력을 사용자/평가자와 확인해야 합니다. 기존 10번 논문 카드 제목도 이번 제공 정식 제목과 달랐으나 다른 작품 보존 범위에 따라 건드리지 않았습니다.

## C11 · 익명 동료 후기 (사용자 제공 원문)

“웹 앱에 들어가기만 했는데도 무엇을 위한 사이트인지 알겠고, 명상 스페이스를 보기만 해도 힐링이 된다.”

실제 동료 한 사람의 사용 후기를 사용자가 제공했습니다. 추가 인터뷰·독립 재인터뷰·의학적 효과 검증을 수행한 것은 아닙니다.

## C13 · 짧은 확인 방법 (Vercel 공개 앱 기준)

1. 위치: https://br-b-meomureum.vercel.app/ . 로그인 없이 두 공간과 메인 문구·논문 정식 제목·앱 대상/역할을 확인합니다.
2. 행동: 카드의 8초 미리 듣기 → 공간 선택·호흡5분·음성+자막으로 시작 → 설정에서 가이드 Off·공간 변경, 일시정지·재개 후 중간 종료합니다.
3. 통과 모습: 미리 듣기 재생 표시가 끝나고, 세션 타이머·자막이 표시되며, 공간 전환 전후 남은 시간이 유지되고 “여기에서 마무리해도 괜찮아요.”가 표시됩니다. 안내 파일 재생 로그도 확인했습니다. 정상 완료를1분 안에 시험할 수는 없으며 실제3분 세션이 필요합니다. 실제 한국어 음성과 자연음은 평가자가 직접 듣습니다.
4. 오류 모습: 음원 누락 시 AMBIENT_LOAD 등 오류 안내가 표시됩니다. 실패 경로는 이전 로컬 재현으로 확인했으며 공개 배포에서는 파일을 일부러 삭제하지 않았습니다. 새 휴대폰·시크릿 확인은 별도로 남습니다.

## C14 · AI와 나의 판단 세 줄

① AI에게 맡긴 일: 반응형 갤러리·포스터 애니메이션·9종 대본 시간표와 통일된 사전 한국어 안내 음원·자연음 편집·세션/오디오 충돌 방지 구현, 오류 진단·회귀 테스트·원본 확보·과제용 연구 소개·GitHub 반영·검증 문서 작성을 맡겼습니다(Vercel 최초 생성 요청403 이후 사용자가 제공한 공개 배포 주소를 검증).

② 내가 직접 판단한 일: 두 공간을 추상 예술과 밝은 제주 숲으로 나누고, 평면 도자기 대신 영상 중심 방향과 현재 포스터 애니메이션 대안을 선택했으며, 무로그인·무기록·무점수, 비판단적 안내 원칙을 결정하고 실제 휴대폰 음성과 물·도자기·새·미풍을 직접 듣고 수정 의견과 최종 승인 의견을 주었습니다.

③ AI 제안을 따르지 않은 일과 이유: 전후 긴장감 점수와 기록 저장은 마음을 평가하거나 기록하기 위해 방문하는 공간이 아니라는 목적에 맞지 않아 채택하지 않았고, 깊은 코발트 수면·날카로운 도자기·도심 소음이 섞인 숲도 원하는 경험과 달라 색·음향 수정을 요청했습니다.

근거 범위는 이 Work 스레드에서 보이는 기획·수정·검증 대화와 이번 사용자가 명시한 판단 목록입니다. 접근하지 못한 다른 대화를 읽었다고 주장하지 않습니다.

## 전체 평가표

사용자가 이번 요청에 설명한 기준의 범위를 적용했습니다. 원문 체크리스트에서 별도 세부 문구가 있다면 대조가 필요합니다. “충족”은 아래 증거 범위의 판단이며 과제 시스템의 최종 합격 판정이 아닙니다.

| 기준 | 상태 | 근거·남은 점 | 증거 위치 |
|---|---|---|---|
| BRB-C01 논문→앱 문장 | 충족 | 대상·역할·결과·한계 한 문장 | 본문 C01 |
| BRB-C02 세 행동 | 부분 충족 | 로컬 UI 실행; 새 배포·실기기 청취 남음 | C02, evidence/ |
| BRB-C03 첫 화면 | 충족 | Vercel 공개 홈에서 연구 제목·대상·한계 확인 | dist/index.html, evidence/brb-vercel-home.jpg |
| BRB-C04 논문 적용 | 충족 | 연구 결과와 UX 선택 구분·연결표 | C04 |
| BRB-C05 정상·비정상 | 부분 충족 | 단위19개 및 UI; 모바일·전체 청취·뒤로가기 등 남음 | C05, evidence/node-tests.txt |
| BRB-C06 개인정보 | 충족 | 검사 범위에서 탐지 없음; 개인 임상자료 없음 | evidence/source-audit.json |
| BRB-C07 사용 권리 | 충족 | 현재 배포 미디어 원문 재확인; 미사용 과거 음원 신규 제출 제외 | MEDIA_LICENSES.md, asset-manifest |
| BRB-C08 공개 접근 | 충족 | Vercel 일반 브라우저·익명 HTTP 접근 확인, 시크릿은 별도 | C08·15·22, evidence/vercel-http-assets.json |
| BRB-C09 독립 폴더 실행 | 해당 없음 | 이번 제출은 URL·GitHub, 새 ZIP 미제출 | README 실행법 |
| BRB-C10 BR-A 대표작 | 충족 | 기존 공개 앱 연결, 실제 BR-A 자동배포 확인 | C10, evidence/brb-portfolio-link.* |
| BRB-C11 동료 후기 | 충족 | 익명 원문·사용자 제공 출처 명시 | C11 |
| BRB-C12 비밀값 | 충족 | 패턴 검사·환경변수 없음, 한계 명시 | source-audit.json |
| BRB-C13 확인법 | 충족 | 위치·행동·통과·오류 구분, 기존 URL 기준 | C13 |
| BRB-C14 판단3줄 | 충족 | 맡김·직접판단·거절 이유 구분 | C14 |
| BRB-C15 새 공개 검증 | 부분 충족 | Vercel 데스크톱·익명 HTTP 확인; 새 시크릿·실기기 미검증 | C08·15·22 |
| BRB-C22 GitHub/Vercel | 충족 | 공개 GitHub와 Vercel 실행 파일·에셋 일치 확인 | README, evidence/vercel-http-assets.json |

## 수정 파일·전후 차이

| 파일 | 이전 → 이후·이유 |
|---|---|
| dist/index.html | 메인카피 아래 연구 소개 없었음 → 정식 제목·대상·역할·한계 추가 |
| dist/styles.css | 기존 스타일 그대로 + research-intro 전용 작은 글·모바일 줄바꿈 규칙 |
| vercel.json, .gitignore | 신규 정적 Import 설정·로컬 비밀/로그 제외 |
| README.md | 원본 provenance·실행·Vercel 설정·실패/미검증 상태 추가 |
| docs/BRB_REPORT.md, MEDIA_LICENSES.md, evidence/* | 평가표·실행 증거·출처·범위·해시·검증 한계 추가 |
| tools/audit_brb.py | 재실행 가능한 소스 패턴·에셋·디코딩 검사 |
| 신규 저장소 dist/assets/audio의 미사용 과거15파일 | 현재 실행에 불필요한 이전 음원·검토 믹스는 제외. 원본에는 보존 |
| BR-A index.html | 13번 예정 카드 → 머무름 완성 앱 링크·연구 연결. 그 외 동일 |

앱 JS 엔진·가이드·승인 음원·포스터·애니메이션 파일은 변경하지 않았습니다. 연구 소개 이외 디자인 확장이나 새 기능을 추가하지 않았습니다.

## 남은 일

새 Vercel URL에서 실제 휴대폰의 한국어 안내·자연음 청취와 새 Chrome 시크릿 창의 무로그인 접근을 확인한 뒤 남은 미검증 상태를 업데이트합니다. 데스크톱 UI·익명 파일 요청과 실제 휴대폰 청취를 혼동하지 않습니다. BR-A 최종 확정·과제 순서는 과제 시스템 확인이 필요합니다. 완료하지 않은 항목을 완료로 표시하지 않습니다.

## 추가 브라우저 실행 기록

- 로컬 자연음 파일을 일시적으로 옮겨 404 상황을 만들고 새로고침한 페이지에서 숲을 선택했습니다. 비동기 로드 후 실제 alert “자연음 파일을 불러오지 못했습니다. [AMBIENT_LOAD]”와 status를 확인했습니다(evidence/brb-audio-failure.txt). 확인 직후 원본 파일을 복구했습니다. 배포 파일을 누락시킨 채 제출하지 않습니다.
- 홈 reload 후 소리 활성화(Off)·기본 홈으로 초기화 확인. 이후 Vercel 세션 중 reload 및 back/forward를 실행해 문서 끝에 후속 기록을 추가했습니다.

- 가이드 음성만 선택→Off→On을 실제 클릭해 음성만 모드로 복원됨을 확인했습니다. 자연음 슬라이더35→30%, 안내85→80%를 각각 키보드로 조작했습니다(evidence/brb-guide-volume.txt). 파일 재생 청취 판정은 별도입니다. 시작 dblclick 후 화면에는 단일 세션 타이머가 표시됐습니다.
- GitHub 원본 기반 import commit: a63ec3f393fc311bf023a6bbac64d4184baf6e20. 이후 검증 문서만 추가로 커밋합니다.

- 음성만 모드 재개 후 breath-5-1 file-start(재개/프레임 위치 offset 약0.459초)→file-ended, 자막 비움, 자연음0.3·안내0.8, lastError:null을 실제 UI 진단에서 확인했습니다(evidence/brb-voice-only-diagnostics.txt). 기기 부하에 따른 미세한 시작 지연의 청감 검증은 별도입니다.

- 좁은 화면 검증은 desktop Chrome 안의 375×812 CSS iframe입니다. iframe 내부 콘텐츠 폭360px, 문서 scrollWidth360px로 가로 넘침이 없었고, 첫 화면의 논문 제목·대상·한계와 한 열 갤러리, 설정의 세로 배치·5분 선택을 확인했습니다. 실제 휴대폰·터치·모바일 오디오 정책 검증으로 대체하지 않습니다. 검사용 iframe 페이지는 임시 QA 파일이며 신규 배포에 포함하지 않습니다.

## Vercel 후속 실배포 검증 · 2026-11-02

사용자가 제공한 실제 공개 주소 https://br-b-meomureum.vercel.app/ 에서 실행했습니다. 기존 로컬 테스트를 공개 배포 결과로 바꿔 부르는 것이 아니라 아래 조작을 다시 수행했습니다.

| 행동 | 위치·실제 조작 | 기대·실제 결과 | 오류 여부·증거 |
|---|---|---|---|
| ① 두 공간 미리 듣기 | Vercel 홈 물결 클릭→종료 확인→숲 클릭→종료 확인 | 양쪽 재생 표시 및 aria-pressed true→false. 실제 도자기·새 accent-start 로그 | 오류표시 없음. evidence/brb-vercel-home.*, brb-vercel-diagnostics.txt |
| ② 호흡5분·음성+자막 | Vercel 물결 기본 설정으로 시작 | 05:00·첫 자막, breath-5-0 file-start offset0 duration7.753초→file-ended. AudioContext running,lastError:null,preview:false | evidence/brb-vercel-session.jpg, brb-vercel-diagnostics.txt. 실제 사람이 들은 검증은 아님 |
| ③ 설정·중간 종료 | 숲 전환·가이드 Off→닫기→pause/resume→마무리 | 공간 변경 전후04:48, pause/resume04:23 유지, 중간 종료 정확한 문구 | evidence/brb-vercel-world-switch.txt, brb-vercel-early.txt |
| 정상 완료 추가 | 숲·호흡3분·자막만 실제 시작 후 시간 단축 없이 진행 | “잠시 머물렀던 시간을 그대로 두어도 괜찮아요.”·홈 버튼 | evidence/brb-vercel-complete.txt/.jpg |
| 좁은 화면 추가 | 공개 Vercel 페이지를375×812 iframe으로 실제 로드·설정 선택 | 홈 연구 소개·한 열 갤러리 표시. 설정 콘텐츠 폭360/scrollWidth360, 가로 넘침 없음 | evidence/brb-vercel-mobile.*, brb-vercel-mobile-settings.txt. 실제 휴대폰 아님 |
| 새로고침·이동 | 세션 중 reload, 이후 browser back→forward | 홈·소리 Off 초기화. back은 이전 문서 about:blank, forward는 공개 앱 홈 복귀 | evidence/brb-vercel-reload.txt, brb-vercel-history.txt |

실행 파일·미디어는 쿠키·인증 헤더 없이 조회해85개 SHA256 일치를 확인했습니다. 비실행 dist/README.md만404입니다. Vercel에서 파일을 삭제하거나 앱 코드·디자인·음향을 바꾸지 않았습니다. 이 후속 변경은 배포 상태/제출 문서/증거 갱신과 BR-A 링크 주소 교체뿐입니다. 기존19개 단위 테스트 결과는 코드가 동일하므로 유지합니다.

남은 직접 확인: 새 Vercel 주소의 실제 휴대폰 한국어 안내·자연음 청취, 새 Chrome 시크릿 창 접근. 손상 영상·실기기 다중 터치·9종 전체 장시간 청취는 기존 미검증 범위를 유지합니다. 과제 시스템의 BR-A 확정/순서 역시 별도입니다.
