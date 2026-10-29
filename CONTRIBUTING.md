# Contributing

1. Add the channel to `channels.json` with `name`, `category` (one of the category ids), `url`, `tvg_id` (the [iptv-org](https://github.com/iptv-org/database) id when one exists, so the guide matches), `logo` and `provider`.
2. Run `python3 tools/build.py --probe`. It has to come back alive.
3. In the pull request, say where the stream comes from and why it is worth watching.

Read [SOURCES.md](SOURCES.md) first. A PR that adds a pirated stream is closed.
