# Source policy

A channel is added only if all of these are true.

1. **Legal source.** The stream comes from the broadcaster itself (BBC, DW, France 24, NHK, Al Jazeera, Bloomberg, NBC, Global/Corus, Rogers CityNews, TVO and so on) or from an ad-supported free TV service that licenses its channels (Pluto TV, Stingray, Tubi, Samsung TV Plus, Rakuten TV, Xumo/Plex, Amagi/Wurl playouts). These are **never** accepted: re-streams of cable channels on bare IP addresses or "free IPTV" hosts, links that need someone else's login, and DRM workarounds.
2. **Plays on Apple TV.** HLS or a direct media file. No YouTube, DASH or RTMP.
3. **Works in Canada.** Geo-blocked channels are left out. A future list for each region can add them.
4. **Good programming.** It is a real channel with a clear identity, not a loop of shopping, a test feed or a placeholder.
5. **Family-safe.** No channel built around horror, adult reality dating or mature animation.
6. **English** for now.

## Checked and left out

- CBC News Network (international feed) and PBS Nature/Travel: the stream loads, but the video is blocked from Canada.
- NASA TV: the old public NASA TV feeds still answer, but all their video is gone (404). NASA's live coverage is now on NASA+ and YouTube, and neither has a public HLS link. We'll add it if one appears.
- Cable channels (A&E, AMC, CNN, CP24, HGTV, TLC and others) that showed up in public IPTV lists: these are unlicensed re-streams.
