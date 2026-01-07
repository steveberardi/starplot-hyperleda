from pathlib import Path


__version__ = "0.1.0"

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE.parent / "data"
BUILD_PATH = HERE.parent / "build"

BUILD_FILE_PATH = BUILD_PATH / f"hyperleda.{__version__}.parquet"
