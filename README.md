# Living TV Channels

A hand-picked, family-friendly list of free, legal live TV channels, set up for **Living TV** on Apple TV. It works in any IPTV player that accepts M3U playlists.

*This is an unofficial community list. It is not part of the Living TV app and isn't built into it.*

This is not a dump of every stream on the internet. Every channel here:

- comes from the broadcaster itself or an ad-supported free TV service (Pluto TV, Stingray, Tubi, Samsung TV Plus, Rakuten TV and similar);
- is in English and works in Canada;
- was checked to be playing when the list was last built;
- sits in one clear category.

## Add it to Living TV

In Living TV open **Settings → My Playlists → Add Your Own Playlist**:

| Field | Value |
|---|---|
| Playlist link | `https://maplepaladin73.github.io/livingtv-channels/livingtv.m3u` |
| Program guide (EPG) link | `https://maplepaladin73.github.io/livingtv-channels/guide.xml.gz` |

Want only part of it? Every category has its own playlist, for example
`https://maplepaladin73.github.io/livingtv-channels/categories/nature-wildlife.m3u`. See [CATEGORIES.md](CATEGORIES.md).

The guide link is optional. Living TV also finds now/next listings by itself for most channels.

## Categories

Canadian News · World News · Business News · Weather · Science & Space · Nature & Wildlife · History & Documentary · Travel & Scenic · Food & Home · Kids & Family · Classic TV Series · Drama & Crime Series · Comedy · Reality & Game Shows · Movies · Music Videos & Concerts · Relax: Music & Scenery · Sports & Outdoors · Faith

## What plays on Apple TV

Living TV uses Apple's own player, so a link works if it is:

- **HLS** (`.m3u8`): almost every live channel;
- **a direct video or audio file or stream**: `.mp4`, `.mov`, `.mp3`, `.aac` and internet radio.

These do **not** work: YouTube or Twitch pages, DASH (`.mpd`), RTMP, and web pages with a video embedded in them.

## Rules for adding a channel

See [SOURCES.md](SOURCES.md). In short: official or free-and-legal only, it has to be good, and it has to be on.

## Building

```sh
python3 tools/build.py --probe --guide merged-guide.xml
```

This checks every stream, drops dead ones, and writes `dist/`: the full playlist, one playlist per category, the filtered guide and `report.json`.

## Disclaimer

This repository only lists links that the channel owners publish openly. It hosts no video. Channels change or go away. If one stops working, please [open an issue](../../issues).
