from pathlib import Path
import subprocess
import sys


def main() -> None:
    app_path = Path(__file__).with_name("streamlit_app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)], check=False)


if __name__ == "__main__":
    main()