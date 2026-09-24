# Building and running the English fork

The image runs MDCx **from source** instead of the PyInstaller binary upstream ships. That is a
deliberate choice — see the header of `../Dockerfile` for why.

## Build

From the root of this repository:

```bash
docker build -t mdcx-en:local --build-arg GIT_REV=$(git rev-parse --short HEAD) .
```

Notes:

- **`linux/amd64` only.** `pyproject.toml` pins `required-environments` to `linux/x86_64`,
  `darwin/x86_64`, `darwin/arm64` and `win32/AMD64`. There is no arm64 lock.
- The build installs Python 3.13 through `uv` (Ubuntu 24.04 ships only 3.12, and the code
  requires `>=3.13.4`), then `uv sync --frozen`. Expect a few hundred MB of wheels —
  PyQt6, `opencv-contrib-python-headless` and `av` dominate.
- The build verifies the translation map is present and prints the entry count. If that line
  is missing, stop — do not deploy.

## Run

`docker-compose.yml` in this directory is a minimal working example:

```bash
cd docker
docker compose up -d
```

It expects:

- `./mdcx-config/` — a host directory holding `config.v2.json`, plus `MDCx.config` (the marker
  file, one line: `/mdcx-config/config.v2.json`). It is mounted **twice**: at `/mdcx-config`
  for the config data, and at `/app/MDCx.config` where the app looks for the marker.
- A media path bind-mounted to `/torrents/adult` — the scan directory. Adjust to your layout.
- Ports `6800` (web UI) and `5900` (VNC).

The `MDCx.config` marker is what selects the **v2** config format. Without it the app falls back
to `config.ini`, which is the format this fork is *not* configured for. `startapp.sh` prints the
marker path at startup so you can see at a glance which format is in use.

## Fast iteration (no rebuild)

The venv lives at `/opt/venv`, outside `/app`, so the source can be bind-mounted over `/app`
without hiding it:

```bash
docker run --rm -it \
  -v "$PWD:/app" \
  -v /path/to/mdcx-config:/mdcx-config \
  -v /path/to/mdcx-config/MDCx.config:/app/MDCx.config \
  -v /path/to/media/torrents/adult:/torrents/adult \
  -p 6800:5800 -p 5900:5900 \
  mdcx-en:local
```

Edit `mdcx/i18n/en.json`, restart the container, and the interface reloads. No image rebuild.

## Verifying a build

```bash
# the map is really in the image, with the expected entry count
docker run --rm --entrypoint /opt/venv/bin/python mdcx-en:local -c \
  "import json,pathlib;print(len(json.loads(pathlib.Path('/app/mdcx/i18n/en.json').read_text())))"

# which revision is baked in
docker run --rm --entrypoint cat mdcx-en:local /app/.revision
```

## Updating from upstream

```bash
git remote add upstream https://github.com/Hazard804/mdcx.git   # once
git fetch upstream
git merge upstream/master          # on the english-i18n branch
```

The translation is a pure add-on: `mdcx/i18n/` plus a few lines in `main.py`. No upstream source
string was edited, so merges should stay clean. If a merge ever conflicts in `main.py`, the
conflict is the translator install — keep both sides.
