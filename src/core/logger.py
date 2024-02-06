import logging

from .settings import settings

# Оставлю здесь, если потребуется в будущем
# LOGS_DIR_PATH = settings.APP_ROOT.parent / "logs"

# if not LOGS_DIR_PATH.exists():
#     LOGS_DIR_PATH.mkdir()

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO, force=True)
