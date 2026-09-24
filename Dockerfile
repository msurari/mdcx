# syntax=docker/dockerfile:1.4
#
# MDCx — English interface fork, built to run FROM SOURCE.
#
# Why not PyInstaller?
# Upstream freezes the app into a single binary (build-mdcx/Dockerfile.build-mdcx:
# `pyinstaller -n MDCx -F -w main.py --add-data "resources:resources" ...`) and then
# copies that binary into a jlesage/baseimage-gui image. A frozen build would need an
# extra `--add-data mdcx/i18n/en.json:mdcx/i18n` for the translation map, and if that
# flag were ever missed the map would simply be absent at runtime: the UI would
# silently fall back to Chinese with no error anywhere. Running from source removes
# that failure mode, and a translation edit takes effect on restart instead of
# requiring a re-freeze.
#
# Build:
#   docker build -t mdcx-en:local --build-arg GIT_REV=$(git rev-parse --short HEAD) .
#
FROM jlesage/baseimage-gui:ubuntu-24.04-v4

LABEL maintainer="msurari"
LABEL description="MDCx with an English interface (fork of Hazard804/mdcx), run from source"

ENV APP_NAME="MDCx"
ENV USER_ID=1000
ENV GROUP_ID=1000
ENV ENABLE_CJK_FONT=1
ENV DISPLAY_WIDTH=1200
ENV DISPLAY_HEIGHT=750

# fontconfig-config is configured through debconf, which is Perl. With no locale set, Perl
# warns ("Setting locale failed") and debconf hits an uninitialised value, so dpkg fails to
# configure fontconfig-config and the whole transaction aborts with "returned an error code
# (1)" on fontconfig-config / libfontconfig1 / fontconfig / fonts-wqy-zenhei. C.UTF-8 is
# built into glibc, so this needs no locale generation. DEBIAN_FRONTEND keeps debconf from
# trying to prompt in a headless build.
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Runtime libraries: deliberately the SAME set upstream's gui-base installs, so the
# app's rendering behaves identically. Every entry below was taken from
# northsea4/mdcx-docker gui-base/Dockerfile.gui-base.
# jlesage's base image keeps the user databases OUTSIDE the image:
#     /etc/passwd -> /tmp/.passwd      /etc/group -> /tmp/.group
# and those targets are only created when the container STARTS. So at build time no user or
# group resolves at all, and fontconfig-config's post-install script — which runs
# `chown root:staff` — fails with "chown: invalid user: 'root:staff'". Note the wording:
# "invalid user", because it is *root* that cannot be resolved, not staff. dpkg then leaves
# fontconfig-config unconfigured, which cascades to libfontconfig1, fontconfig and
# fonts-wqy-zenhei, and the whole apt transaction aborts with exit code 100.
#
# Put real files in place for the duration of the install, then restore the symlinks so the
# base image's runtime user management is unaffected.
#
# The same base image also relocates runtime directories: /var/log -> /config/log and
# /var/tmp -> /config/var/tmp, neither of which exists at build time. fontconfig's postinst
# ends with `touch /var/log/fontconfig.log`, which then fails with
# "cannot create /var/log/fontconfig.log: Directory nonexistent" and aborts the install.
# Creating the real targets (not replacing the symlinks) is what the base image expects.
RUN mkdir -p /config/log /config/var/tmp \
    && rm -f /etc/passwd /etc/group \
    && printf 'root:x:0:0:root:/root:/bin/bash\n' > /etc/passwd \
    && printf 'root:x:0:\nstaff:x:50:\n' > /etc/group \
    && apt-get update -y && apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      unrar \
      locales \
      libgl1 \
      libegl1 \
      libglu1-mesa \
      fonts-dejavu-core \
      fonts-liberation \
      fonts-wqy-zenhei \
      fonts-noto-color-emoji \
      libglib2.0-0 \
      libdbus-1-3 \
      libxcb1 \
      libxcb-xinerama0 \
      libxcb-randr0 \
      libxcb-cursor0 \
      libxcb-keysyms1 \
      libxcb-image0 \
      libxcb-shm0 \
      libxcb-icccm4 \
      libxcb-sync1 \
      libxcb-xfixes0 \
      libxcb-shape0 \
      libxcb-render-util0 \
      libxcb-render0 \
      libxcb-glx0 \
      libx11-6 \
      libxext6 \
      libxrender1 \
      libsm6 \
      libfontconfig1 \
      libfreetype6 \
      libtiff6 \
      libwebpdemux2 \
      libxkbcommon0 \
      libxkbcommon-x11-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && rm -f /etc/passwd /etc/group \
    && ln -sf /tmp/.passwd /etc/passwd \
    && ln -sf /tmp/.group /etc/group

# Locale left exactly as upstream sets it. The interface language comes from the i18n
# layer, NOT from the locale. Changing LC_ALL would shift date/number formatting through
# QLocale and buy nothing, so it is left alone.
RUN locale-gen zh_CN.UTF-8
ENV LANG=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8

# uv, which also supplies the interpreter: pyproject requires >=3.13.4 (the code uses
# os.path.ALLOW_MISSING and type-parameter defaults) and Ubuntu 24.04 only ships 3.12.
#
# Take the binary from the official image instead of curl|sh. The installer finds its
# target by resolving $HOME, and HOME is EMPTY in this base image — same root cause as the
# apt failure: /etc/passwd is a dangling symlink, so the current user's home cannot be
# looked up. It therefore printed "installing to //.local/bin" and the following mv failed
# with "cannot stat '/root/.local/bin/uv'".
#
# HOME is set explicitly as well, because uv's cache path depends on it in later steps.
ENV HOME=/root
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
RUN uv --version
ENV UV_PYTHON_INSTALL_DIR=/opt/python
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
RUN uv python install 3.13

WORKDIR /app
COPY . /app

# The venv lives at /opt/venv, OUTSIDE /app on purpose: bind-mounting the source over
# /app for fast iteration must not hide the venv.
RUN uv sync --frozen --no-dev \
    && rm -rf /root/.cache/uv \
    && /opt/venv/bin/python -c "import PyQt6.QtCore, cv2, PIL, curl_cffi, lxml, av; print('runtime deps ok')" \
    && /opt/venv/bin/python -c "import json,pathlib; m=json.loads(pathlib.Path('/app/mdcx/i18n/en.json').read_text()); print('translation map present:', len(m), 'entries')"

ARG GIT_REV=unknown
# Bake a sane DEFAULT config marker. The marker is what selects the v2 config format;
# without it the app falls back to config.ini, which this fork is not configured for.
# Baking it removes a whole class of "why can't it find its config" errors, and a
# mounted marker still overrides this file.
RUN echo "$GIT_REV" > /app/.revision \
    && printf '%s\n' '/mdcx-config/config.v2.json' > /app/MDCx.config \
    && chmod -R a+rX /app /opt/venv /opt/python \
    && chmod a+r /app/MDCx.config \
    && mkdir -p /app/userdata /app/Log

COPY docker/startapp.sh /startapp.sh
COPY docker/rootfs/ /
RUN chmod +x /startapp.sh \
    && chmod +x /etc/cont-init.d/*.sh 2>/dev/null || true
