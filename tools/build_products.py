"""products.json 으로 index.html 의 제작 품목(탭 + 사진 카드) 구역을 다시 만든다.

    python3 tools/build_products.py

index.html 의 <!-- PRODUCTS:START --> 와 <!-- PRODUCTS:END --> 사이만 바꾼다.
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHONE = "0632833370"

ICONS = {
    "circle": '<circle cx="12" cy="12" r="8"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    "barcode": '<path d="M4 6v12M7 6v12M10 6v12M14 6v12M16 6v12M20 6v12"/>',
    "roll": '<circle cx="9" cy="12" r="6"/><circle cx="9" cy="12" r="2"/><path d="M9 6h11v12H9"/>',
    "plate": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 10h10M7 14h6"/>',
    "star": '<path d="M12 3l2.6 5.6 6.1.6-4.6 4.1 1.3 6-5.4-3.1-5.4 3.1 1.3-6L3.3 9.2l6.1-.6z"/>',
    "gift": '<rect x="4" y="9" width="16" height="11" rx="1"/><path d="M12 9v11M4 13h16M12 9c-2-4-6-3-5 0M12 9c2-4 6-3 5 0"/>',
    "clear": '<rect x="4" y="4" width="16" height="16" rx="3" stroke-dasharray="3 3"/>',
}

ALL_DESC = "용도와 수량을 말씀해 주시면 알맞은 용지와 가공 방법을 안내해 드립니다. 모양 따기(도무송)도 함께 해 드립니다."


def build(data):
    cats = {c["id"]: c for c in data["categories"]}
    out = []
    out.append('      <div class="tabs" role="tablist" aria-label="스티커 종류">')
    out.append(f'        <button type="button" class="tab is-active" data-cat="all" data-desc="{escape(ALL_DESC)}" aria-selected="true">전체</button>')
    for c in data["categories"]:
        out.append(f'        <button type="button" class="tab" data-cat="{c["id"]}" data-desc="{escape(c["desc"])}" aria-selected="false">{escape(c["name"])}</button>')
    out.append("      </div>")
    out.append(f'      <p class="cat-desc" id="cat-desc">{escape(ALL_DESC)}</p>')
    out.append('      <div class="products">')
    for it in data["items"]:
        c = cats[it["cat"]]
        if it.get("img"):
            media = f'<img src="{escape(it["img"])}" alt="{escape(it["title"])}" loading="lazy" width="600" height="600">'
        else:
            media = (f'<span class="ph {c["color"]}" aria-hidden="true">'
                     f'<svg viewBox="0 0 24 24">{ICONS[c["icon"]]}</svg><span>사진 준비 중</span></span>')
        out.append(f'        <article class="product" data-cat="{c["id"]}">')
        out.append(f'          <button type="button" class="product-media" data-cat="{c["id"]}" aria-label="{escape(c["name"])}만 보기">{media}</button>')
        out.append(f'          <div class="product-body">')
        out.append(f'            <span class="product-cat">{escape(c["name"])}</span>')
        out.append(f'            <h3>{escape(it["title"])}</h3>')
        out.append(f'            <p>{escape(it["desc"])}</p>')
        out.append(f'            <a href="tel:{PHONE}" class="product-ask">견적 문의</a>')
        out.append("          </div>")
        out.append("        </article>")
    out.append("      </div>")
    return "\n".join(out)


def main():
    data = json.loads((ROOT / "products.json").read_text(encoding="utf-8"))
    path = ROOT / "index.html"
    html = path.read_text(encoding="utf-8")
    start, end = "<!-- PRODUCTS:START -->", "<!-- PRODUCTS:END -->"
    a, b = html.index(start) + len(start), html.index(end)
    html = html[:a] + "\n" + build(data) + "\n      " + html[b:]
    path.write_text(html, encoding="utf-8")
    print(f"품목 {len(data['items'])}개로 index.html 을 다시 만들었습니다.")


if __name__ == "__main__":
    main()
