# 포스터 애니메이션 제작 메모

기존 구도와 도자기 재질을 보존하기 위해 원본의 그릇을 코드의 SVG 경로로 잘라 사용합니다. 그릇이 사라진 부분은 이미지 편집 도구로 만든 물 배경으로 채웠습니다. 최종 물 배경 파일: dist/assets/water-surface-aqua.webp. 원본 물 포스터: dist/assets/water-poster-aqua.webp.

물 배경 생성에 사용한 내장 이미지 편집 도구 프롬프트:

Edit target: supplied aqua porcelain meditation poster. Create a clean background plate for animation by removing BOTH porcelain bowls completely, including their contents, shadows and bowl-shaped reflections. Fill the removed regions seamlessly with the same clear pale turquoise/arctic aqua rippling water. Preserve all other water pixels and lighting as closely as possible, exact camera and 16:9 framing, same luminous restrained palette. Water fills entire frame, fine ripples with subtle gentle depth. No bowls, dishes, vessels, circles shaped like bowls, objects, shore, text, UI, logos. Photorealistic water only. This is a technical clean plate; don't change the scene's color mood or camera.

WebGL 수면 왜곡, 지원되지 않을 때 Canvas 2D 수면 변형, SVG 그릇 이동으로 합성합니다. 가려진 영역을 완전히 정확하게 복원하는 방식은 아니므로 큰 이동은 사용하지 않습니다. 숲은 원본 포스터와 빛·벡터 낙엽·새를 조합합니다. 실제 영상 생성 서비스는 사용하지 않습니다.
