# 신성스티커 홈페이지

전주 완산구 스티커 인쇄업체 "신성스티커"의 한 페이지짜리 정적 홈페이지. 빌드 과정 없음.

- 주소: `https://sinsung.dbhouse.net` (Cloudflare `dbhouse.net` 영역 — 바꾸기 전 `/home/dbhouse/문서/infra/공용설정.md` 확인)
- GitHub: `dbhouselab/sinsung-pages`(공개), `main` 브랜치. Cloudflare Pages 프로젝트 `sinsung-pages` 에 연결됨(2026-11-08) — `main` 에 push 하면 1분 안팎에 자동 배포
- `다운받은 사진/` 은 사용자가 넣는 원본 자료 폴더 — git 에서 뺌(.gitignore)
- 파일: `index.html`, `style.css`, `images/logo.png`(원본 `logo.jpg`의 흰 배경을 지운 것), `robots.txt`, `sitemap.xml`
- 디자인: 깔끔·신뢰감. 로고 색 — 파랑 `#1650a6`(주색), 빨강 `#8e1b1e`, 노랑 `#f2c230`, 청록 `#2a6e8a`
- 휴대폰 우선. 600px 이하에서 하단 고정 [전화 상담 | 길찾기] 버튼

## 업체 정보 (화면 · 검색용 JSON-LD 양쪽에 있음 — 바꿀 때 둘 다)
- 주소: 전북특별자치도 전주시 완산구 현무3길 42-1 (지번 중노송동 551-1)
- 전화: 063-283-3370(대표), 0507-1495-3371(네이버 안내번호)
- 영업: 월~금, 토·일 휴무(2026-11-08 사용자 결정). 시각은 아직 모름
- 제작 품목(스티커 8종, 2026-11-08 사용자 제공): 일반, 유포지, 바코드, 로타리 롤, 은무데드롱, 홀로그램, 은무지/금무지, 투명지. 설명 문구는 Claude 가 씀

## 제작 품목 구역 (탭 + 사진 카드, 금정특수인쇄 상품 목록 방식을 참고)
- 데이터는 `products.json`(categories = 탭 8개, items = 카드). 고친 뒤 `python3 tools/build_products.py` → `index.html` 의 `<!-- PRODUCTS:START -->` ~ `END` 사이를 다시 만든다. 그 사이는 손으로 고치지 않는다
- 카드 사진은 `images/products/`. 지금 8장은 `tools/make_samples.py` 로 그린 **예시 그림**(2026-11-08). 실제 사진이 오면(`다운받은 사진/`) 정사각형 600px 정도 JPG 로 줄여 넣고 items 의 img 를 바꾼다. 한 품목에 사진 여러 장이면 items 를 여러 개로
- 탭 필터는 `index.html` 맨 아래 작은 스크립트. 카드는 HTML 에 그대로 있어 검색엔진이 읽는다

## 미리 보기
`python3 -m http.server 8765` → http://localhost:8765
