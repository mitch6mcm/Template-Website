#!/usr/bin/env python3
"""Fill template.html with one business's details and write a ready-to-deploy site.

Usage:
    python3 build.py site.json OUTPUT_FOLDER

site.json holds the business details (see example-site.json and README.md).
Photos must already be in OUTPUT_FOLDER/img/ (e.g. img/p1.jpg); list them in
site.json by their relative path ("img/p1.jpg").
Writes OUTPUT_FOLDER/index.html. Uses only the Python standard library.
"""
import datetime
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent


def esc(v):
    return html.escape(str(v), quote=True)


def emphasize(text):
    """Escape text, then turn *word* into <em>word</em> (accent-colored)."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", esc(text))


def dark_rgb(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def tel(phone):
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        digits = "1" + digits
    return "+" + digits


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 build.py site.json OUTPUT_FOLDER")
    d = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)

    name = d["business_name"]
    phone = d["phone"]
    colors = d.get("colors", {})
    c_dark = colors.get("dark", "#0b2a4a")
    photos = d.get("photos", [])
    first_photo = photos[0] if photos else ""
    services = d.get("services", [])
    reviews = d.get("reviews", [])
    faq = d.get("faq", [])
    benefits = d.get("benefits", [])
    stats = d.get("stats", [])
    gallery = d.get("gallery", photos)

    # Logo: real logo image if provided, else icon + two-tone business name
    words = name.split()
    name_html = esc(words[0]) + (" <span>" + esc(" ".join(words[1:])) + "</span>" if len(words) > 1 else "")
    if d.get("logo"):
        logo = f'<img src="{esc(d["logo"])}" alt="{esc(name)} logo">'
        if d.get("logo_has_name") is False:
            logo += name_html
    else:
        initial = esc(words[0][0].upper())
        logo = (f'<svg width="38" height="38" viewBox="0 0 40 40"><rect x="3" y="3" width="34" height="34" rx="7" fill="{esc(colors.get("main", "#1572c4"))}"/>'
                f'<text x="20" y="27" text-anchor="middle" font-family="system-ui,sans-serif" font-size="20" font-weight="800" fill="#fff">{initial}</text></svg>{name_html}')

    # Rating line
    rating = d.get("rating")
    count = d.get("review_count")
    rating_line = ""
    if rating:
        rating_line = f"{rating} Google Rating" + (f" · {count} reviews" if count else "")

    # Address
    addr = d.get("address", {})
    street = addr.get("street", "")
    cityline = ", ".join(x for x in [addr.get("city", ""), " ".join(x for x in [addr.get("state", ""), addr.get("zip", "")] if x)] if x)
    full_addr = ", ".join(x for x in [street, cityline] if x)
    address_html = "<br>".join(esc(x) for x in [street, cityline] if x)
    map_query = quote(full_addr or f'{name} {addr.get("city", "")} {addr.get("state", "")}')

    # Hours: list of [day, hours] pairs, or a plain string
    hours = d.get("hours")
    if isinstance(hours, list) and hours:
        hours_html = '<table class="hours">' + "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in hours) + "</table>"
    elif hours:
        hours_html = f"<p>{esc(hours)}</p>"
    else:
        hours_html = ""

    def pic(i):
        return photos[i % len(photos)] if photos else ""

    service_cards = "".join(
        (f'<div class="card"><img src="{esc(s.get("image") or pic(i + 1))}" alt="{esc(s["title"])}" loading="lazy">' if (s.get("image") or photos) else '<div class="card">')
        + f'<div><h3>{esc(s["title"])}</h3><p>{esc(s["text"])}</p></div></div>'
        for i, s in enumerate(services))
    benefit_cards = "".join(
        f'<div class="ben"><i>{esc(b.get("icon", "✔️"))}</i><h3>{esc(b["title"])}</h3><p>{esc(b["text"])}</p></div>'
        for b in benefits)
    gallery_imgs = "".join(f'<img src="{esc(g)}" alt="{esc(name)} work" loading="lazy">' for g in gallery)
    review_cards = "".join(
        f'<div class="rev"><div class="stars">{"★" * int(r.get("stars", 5))}</div><p>"{esc(r["text"])}"</p><b>— {esc(r["name"])}</b></div>'
        for r in reviews)
    faq_items = "".join(f"<details><summary>{esc(f['q'])}</summary><p>{esc(f['a'])}</p></details>" for f in faq)
    stats_html = "".join(f"<div><b>{esc(s['value'])}</b>{esc(s['label'])}</div>" for s in stats)
    about_ps = "".join(f"<p>{esc(p)}</p>" for p in d.get("about_paragraphs", []))
    form_opts = d.get("form_options") or [s["title"] for s in services] + ["Other"]

    nav = [("services", "Services")]
    if gallery: nav.append(("gallery", "Gallery"))
    nav.append(("about", "About"))
    if reviews: nav.append(("reviews", "Reviews"))
    if faq: nav.append(("faq", "FAQ"))
    nav.append(("location", "Location"))

    city = addr.get("city", "")
    state = addr.get("state", "")
    values = {
        "PAGE_TITLE": esc(d.get("page_title") or f"{name} | {city}, {state}"),
        "META_DESCRIPTION": esc(d.get("meta_description") or f"{name} in {city}, {state}. Call {phone} for a free quote."),
        "COLOR_DARK": esc(c_dark), "COLOR_MAIN": esc(colors.get("main", "#1572c4")),
        "COLOR_LIGHT": esc(colors.get("light", "#e8f4fd")), "COLOR_ACCENT": esc(colors.get("accent", "#5bc0f8")),
        "DARK_RGB": dark_rgb(c_dark),
        "ANNOUNCEMENT": esc(d.get("announcement", "")),
        "LOGO": logo,
        "NAV_LINKS": "".join(f'<a href="#{a}">{t}</a>' for a, t in nav),
        "PHONE": esc(phone), "PHONE_TEL": tel(phone),
        "CTA_BUTTON": esc(d.get("cta_button", "Get My Free Quote")),
        "RATING_LINE": esc(rating_line),
        "HERO_TITLE": emphasize(d["hero_title"]),
        "HERO_SUBTITLE": esc(d.get("hero_subtitle", "")),
        "HERO_BULLETS": "".join(f"<li>{esc(b)}</li>" for b in d.get("hero_bullets", [])),
        "HERO_IMAGE": esc(d.get("hero_image") or first_photo),
        "FORM_TITLE": esc(d.get("form_title", "Get Your Free Quote")),
        "FORM_OPTIONS": "".join(f"<option>{esc(o)}</option>" for o in form_opts),
        "SERVICES_TITLE": esc(d.get("services_title", "Our Services")),
        "SERVICES_SUBTITLE": esc(d.get("services_subtitle", "")),
        "SERVICE_CARDS": service_cards,
        "BENEFITS_EYEBROW": esc(d.get("benefits_eyebrow", "Why Choose Us")),
        "BENEFITS_TITLE": esc(d.get("benefits_title", f"The {words[0]} Difference")),
        "BENEFIT_CARDS": benefit_cards,
        "GALLERY_IMAGES": gallery_imgs,
        "BUSINESS_NAME": esc(name),
        "ABOUT_IMAGE": esc(d.get("about_image") or pic(len(photos) // 2 if photos else 0)),
        "ABOUT_TITLE": esc(d.get("about_title", f"About {name}")),
        "ABOUT_PARAGRAPHS": about_ps,
        "STATS": stats_html,
        "REVIEW_CARDS": review_cards,
        "FAQ_ITEMS": faq_items,
        "ADDRESS_HTML": address_html,
        "HOURS_HTML": hours_html,
        "SERVICE_AREA": esc(d.get("service_area", "")),
        "MAPS_URL": esc(d.get("maps_url", "")),
        "MAP_QUERY": map_query,
        "CTA_TITLE": esc(d.get("cta_title", "Ready to Get Started?")),
        "CTA_SUBTITLE": esc(d.get("cta_subtitle", "Get your free, no-obligation quote today.")),
        "CTA_IMAGE": esc(d.get("cta_image") or pic(4)),
        "YEAR": str(datetime.date.today().year),
        "FOOTER_ADDRESS": (" · " + esc(full_addr)) if full_addr else "",
    }

    present = {
        "announcement": bool(d.get("announcement")), "rating": bool(rating),
        "benefits": bool(benefits), "gallery": bool(gallery), "stats": bool(stats),
        "reviews": bool(reviews), "faq": bool(faq), "address": bool(address_html),
        "hours": bool(hours_html), "service_area": bool(d.get("service_area")),
        "maps_url": bool(d.get("maps_url")),
        "about_image": bool(values["ABOUT_IMAGE"]),
    }

    page = (HERE / "template.html").read_text(encoding="utf-8")
    # Remove optional sections that have no data (inner blocks first)
    for _ in range(3):
        page = re.sub(r"<!--IF (\w+)-->(.*?)<!--ENDIF \1-->",
                      lambda m: m.group(2) if present.get(m.group(1)) else "", page, flags=re.S)
    page = re.sub(r"\{\{(\w+)\}\}", lambda m: values.get(m.group(1), ""), page)
    leftover = re.findall(r"\{\{\w+\}\}|<!--(?:END)?IF", page)
    if leftover:
        sys.exit(f"Unfilled template markers: {leftover}")

    (out / "index.html").write_text(page, encoding="utf-8")
    missing = [p for p in set(photos) | {values["HERO_IMAGE"]} if p and not p.startswith("http") and not (out / p).exists()]
    print(f"Built {out / 'index.html'} ({len(page):,} bytes)")
    if missing:
        print("WARNING: these photos are listed but not in the output folder:", ", ".join(sorted(missing)))


if __name__ == "__main__":
    main()
