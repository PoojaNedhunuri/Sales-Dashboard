import logging

from datetime import datetime

from pathlib import Path

from logging.handlers import RotatingFileHandler
 
 
LOG_DIR = Path("logs")

LOG_DIR.mkdir(parents=True, exist_ok=True)
 
LOG_FILE = LOG_DIR / "pipeline.log"
 
 
def get_logger(name: str) -> logging.Logger:

    # Create reusable logger

    logger = logging.getLogger(name)
 
    if logger.handlers:

        return logger
 
    logger.setLevel(logging.INFO)
 
    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    )
 
    # Write logs to file

    file_handler = RotatingFileHandler(

        LOG_FILE,

        maxBytes=5_000_000,

        backupCount=5,

        encoding="utf-8",

    )

    file_handler.setFormatter(formatter)
 
    # Show logs in terminal

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)
 
    logger.addHandler(file_handler)

    logger.addHandler(console_handler)
 
    return logger
 
 
def log_run_start(logger: logging.Logger, process_name: str) -> str:

    # Create unique run ID

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
 
    logger.info("=" * 80)

    logger.info("RUN START | %s | Run ID: %s", process_name, run_id)

    logger.info("=" * 80)
 
    return run_id
 
 
def log_run_end(

    logger: logging.Logger,

    process_name: str,

    run_id: str,

    status: str,

) -> None:

    # Close current run

    logger.info("-" * 80)

    logger.info(

        "RUN END | %s | Run ID: %s | Status: %s",

        process_name,

        run_id,

        status,

    )

    logger.info("-" * 80)
 