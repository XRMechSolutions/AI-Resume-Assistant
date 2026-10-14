"""Logging to stderr and a rotating file. stdout carries MCP JSON-RPC and must stay clean."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def setup_logging(log_path: Path) -> None:
    root = logging.getLogger("job_mcp")
    if root.handlers:
        return
    root.setLevel(logging.INFO)
    stderr = logging.StreamHandler(sys.stderr)
    stderr.setFormatter(logging.Formatter(_FORMAT))
    root.addHandler(stderr)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(_FORMAT))
    root.addHandler(file_handler)
