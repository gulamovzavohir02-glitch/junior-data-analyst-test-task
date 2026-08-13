"""Execute the notebook from top to bottom without changing the saved file."""

from pathlib import Path

import nbformat
from nbclient import NotebookClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "analysis.ipynb"


def main() -> None:
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(PROJECT_ROOT)}},
    )
    client.execute()
    print("Notebook checks passed.")


if __name__ == "__main__":
    main()
