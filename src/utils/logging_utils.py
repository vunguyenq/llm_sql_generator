import logging
from pathlib import Path
from typing import Union
from collections import deque

MAX_LOG_ENTRIES = 2_000

def cleanup_log_file(file_path: Path):
    with open(file_path, "r") as f:
        latest_entries = deque(f, maxlen=MAX_LOG_ENTRIES)

    with open(file_path, "w") as f:
        f.writelines(latest_entries)


def setup_logging(console: bool = True, output_dir: Union[str, Path] = 'logs', filename: str = 'logging.log') -> None:
    """Set up logging to both file and console for a specific processing job."""
    output_dir = Path(output_dir)
    log_file = output_dir / filename

    # Reset logger to remove any existing handlers
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    # File handler - includes timestamps
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)

    # Console handler - cleaner output without timestamps
    if console:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch_formatter = logging.Formatter("%(message)s")
        ch.setFormatter(ch_formatter)
        logger.addHandler(ch)

    logging.info(f"Started processing. Log file: {log_file}")
    
    cleanup_log_file(log_file)
