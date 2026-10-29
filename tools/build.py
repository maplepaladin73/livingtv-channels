#!/usr/bin/env python3
"""Build the Living TV channel lists from channels.json.

    python3 tools/build.py                  # validate + write dist/
    python3 tools/build.py --probe          # also check every stream; drop dead ones
    python3 tools/build.py --guide in.xml   # also write dist/guide.xml.gz filtered to our channels

Outputs (dist/):
    livingtv.m3u              every channel, grouped by category, with url-tvg header
    categories/<id>.m3u       one playlist per category
    guide.xml.gz              XMLTV programme guide (only when --guide given)
    report.json               probe results and EPG coverage
Standard library only, so it runs on a stock GitHub Actions runner.
"""
import argparse, gzip, json, re, sys, urllib.request, urllib.error
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = "https://maplepaladin73.github.io/livingtv-channels"
UA = "Mozilla/5.0 (AppleTV; CPU OS 18_0 like Mac OS X) AppleCoreMedia/1.0 LivingTV-probe"
PLAYABLE = re.compile(r"\.(m3u8|mp4|m4v|mov|mp3|aac|m4a)(\?|$)|/plu-[0-9a-f]{24}|stream", re.I)
NOT_PLAYABLE = re.compile(r"\.mpd(\?|$)|^rtmp|youtube\.com|youtu\.be|twitch\.tv", re.I)


def load():
    data = json.loads((ROOT / "channels.json").read_text())
    cats = {c["id"]: c for c in data["categories"]}
    errors, seen = [], set()
    for ch in data["channels"]:
        if ch["category"] not in cats:
            errors.append(f"{ch['name']}: unknown category {ch['category']}")
        if NOT_PLAYABLE.search(ch["url"]):
            errors.append(f"{ch['name']}: Apple TV (AVPlayer) can't play this URL type")
        if ch["url"] in seen:
            errors.append(f"{ch['name']}: duplicate URL")
        seen.add(ch["url"])
        m = re.search(r"/channel/([0-9a-f]{24})/", ch["url"])  # raw Pluto stitcher -> stable redirector
        if m and "pluto.tv" in ch["url"]:
            ch["url"] = f"https://jmp2.uk/plu-{m.group(1)}.m3u8"
    if errors:
        sys.exit("channels.json problems:\n  " + "\n  ".join(errors))
    return data, cats


def fetch(url, headers, limit=65536):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, r.geturl(), r.read(limit)


def probe(ch):
    """Alive = master playlist loads, and for HLS the first media segment answers."""
    h = {"User-Agent": ch.get("user_agent") or UA}
    if ch.get("referrer"):
        h["Referer"] = ch["referrer"]
    try:
        status, final, body = fetch(ch["url"], h)
        text = body.decode("utf-8", "replace")
        if "#EXTM3U" not in text:
            return "alive" if status < 400 else f"http {status}"
        for _ in range(2):  # master -> variant -> segment
            lines = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
            if not lines:
                return "empty playlist"
            nxt = urllib.parse.urljoin(final, lines[0])
            status, final, body = fetch(nxt, h, 4096)
            text = body.decode("utf-8", "replace")
            if "#EXTM3U" not in text:
                return "alive" if status < 400 else f"http {status}"
        return "alive"
    except urllib.error.HTTPError as e:
        return f"http {e.code}"
    except Exception as e:  # timeouts, DNS, TLS
        return type(e).__name__


def extinf(ch, cat):
    attrs = [f'tvg-id="{ch.get("tvg_id", "")}"', f'tvg-name="{ch["name"]}"']
    if ch.get("logo"):
        attrs.append(f'tvg-logo="{ch["logo"]}"')
    attrs.append(f'group-title="{cat["title"]}"')
    lines = [f'#EXTINF:-1 {" ".join(attrs)},{ch["name"]}']
    if ch.get("user_agent"):
        lines.append(f'#EXTVLCOPT:http-user-agent={ch["user_agent"]}')
    if ch.get("referrer"):
        lines.append(f'#EXTVLCOPT:http-referrer={ch["referrer"]}')
    lines.append(ch["url"])
    return "\n".join(lines)


def write_m3u(path, channels, cats):
    head = f'#EXTM3U url-tvg="{PAGES}/guide.xml.gz" x-tvg-url="{PAGES}/guide.xml.gz"'
    body = [extinf(ch, cats[ch["category"]]) for ch in channels]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(head + "\n" + "\n".join(body) + "\n")


def filter_guide(src, ids, out):
    opener = gzip.open if str(src).endswith(".gz") else open
    with opener(src, "rb") as f:
        tree = ET.parse(f)
    root = tree.getroot()
    covered = set()
    for el in list(root):
        cid = el.get("id") if el.tag == "channel" else el.get("channel")
        if cid not in ids:
            root.remove(el)
        elif el.tag == "programme":
            covered.add(cid)
    root.set("generator-info-name", "livingtv-channels")
    with gzip.open(out, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
    return covered


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--guide", help="merged XMLTV file (.xml or .xml.gz) to filter")
    args = ap.parse_args()
    data, cats = load()
    order = {c: i for i, c in enumerate(cats)}
    channels = sorted(data["channels"], key=lambda c: (order[c["category"]], c.get("rank", 99)))
    report = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "channels": len(channels)}
    if args.probe:
        with ThreadPoolExecutor(16) as pool:
            results = list(pool.map(probe, channels))
        report["dead"] = {c["name"]: r for c, r in zip(channels, results) if r != "alive"}
        channels = [c for c, r in zip(channels, results) if r == "alive"]
        report["alive"] = len(channels)
    dist = ROOT / "dist"
    write_m3u(dist / "livingtv.m3u", channels, cats)
    for cid in cats:
        members = [c for c in channels if c["category"] == cid]
        if members:
            write_m3u(dist / "categories" / f"{cid}.m3u", members, cats)
    if args.guide:
        ids = {c["tvg_id"] for c in channels if c.get("tvg_id")}
        covered = filter_guide(args.guide, ids, dist / "guide.xml.gz")
        report["epg_covered"] = len(covered)
        report["epg_missing"] = sorted(c["name"] for c in channels if c.get("tvg_id") not in covered)
    report["per_category"] = {cid: sum(c["category"] == cid for c in channels) for cid in cats}
    (dist / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps({k: v for k, v in report.items() if k != "epg_missing"}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    import urllib.parse  # noqa: E402  (used in probe)
    main()
