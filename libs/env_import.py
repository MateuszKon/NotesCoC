from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path.cwd() / ".env", verbose=True)
