# Contributing

1. Add the channel to `channels.json` with `name`, `category` (one of the category ids), `url`, `tvg_id` (the [iptv-org](https://github.com/iptv-org/database) id when one exists, so the guide matches), `logo`, `provider`, `language` (for example `en`) and `country` (the channel's home country code, for example `CA`). Optional fields: `rank` (order within the category, lower first), `user_agent` and `referrer` (sent when the stream needs them).
2. Run `python3 tools/build.py --probe`. It has to come back alive (not listed under `dead` in `dist/report.json`).
3. In the pull request, say where the stream comes from and why it is worth watching.

Read [SOURCES.md](SOURCES.md) first. A PR that adds a pirated stream is closed.
