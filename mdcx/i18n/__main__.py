"""``python -m mdcx.i18n [language]`` -- report what a mapping file covers."""

import logging

from . import _main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    raise SystemExit(_main())
