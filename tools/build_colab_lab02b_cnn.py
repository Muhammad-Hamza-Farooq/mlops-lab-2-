from __future__ import annotations

import json
from pathlib import Path


def _code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line if line.endswith("\n") else line + "\n" for line in source.splitlines()],
    }


def _md_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line if line.endswith("\n") else line + "\n" for line in source.splitlines()],
    }


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src = repo_root / "lab08" / "notebooks" / "lab02b_cnn.ipynb"
    dst = repo_root / "colab_lab2b_cnn.ipynb"

    src_nb = json.loads(src.read_text(encoding="utf-8"))

    setup_md = _md_cell(
        "# Colab · Lab 02b (CNN)\n"
        "\n"
        "This notebook is an auto-generated Colab runner.\n"
        "It contains **all cells** from `lab08/notebooks/lab02b_cnn.ipynb`, plus an extra setup section at the top\n"
        "to clone the latest GitHub repo and install dependencies.\n"
    )

    setup_clone = _code_cell(
        "# --- Colab setup: clone latest repo + cd into lab08 ---\n"
        "import os\n"
        "import sys\n"
        "from pathlib import Path\n"
        "\n"
        "REPO_URL = 'https://github.com/Muhammad-Hamza-Farooq/mlops-lab-2-'\n"
        "REPO_DIR = Path('mlops-lab-2-')\n"
        "\n"
        "if not REPO_DIR.exists():\n"
        "    !git clone {REPO_URL} {REPO_DIR}\n"
        "\n"
        "%cd {REPO_DIR}\n"
        "!git fetch --all -p\n"
        "!git reset --hard origin/master\n"
        "\n"
        "%cd lab08\n"
        "print('cwd:', os.getcwd())\n"
        "\n"
        "# Put lab08 on sys.path so imports work\n"
        "lab_dir = str(Path.cwd())\n"
        "if lab_dir not in sys.path:\n"
        "    sys.path.insert(0, lab_dir)\n"
    )

    setup_deps = _code_cell(
        "# --- Colab setup: install dependencies ---\n"
        "import os\n"
        "import sys\n"
        "\n"
        "# Avoid W&B login prompts\n"
        "os.environ.setdefault('WANDB_SILENT', 'true')\n"
        "os.environ.setdefault('WANDB_MODE', 'disabled')\n"
        "\n"
        "# Core deps pinned by the repo\n"
        "!{sys.executable} -m pip install -q -r ../requirements/prod.in\n"
        "\n"
        "# Training deps (not in prod.in)\n"
        "!{sys.executable} -m pip install -q pytorch-lightning==2.1.3 torchmetrics tensorboard wandb scipy toml nltk\n"
        "\n"
        "import torch\n"
        "print('torch:', torch.__version__)\n"
        "print('cuda available:', torch.cuda.is_available())\n"
        "if torch.cuda.is_available():\n"
        "    print('gpu:', torch.cuda.get_device_name(0))\n"
    )

    new_cells = [setup_md, setup_clone, setup_deps]

    # Keep all original cells after our setup
    new_cells.extend(src_nb.get("cells", []))

    out_nb = dict(src_nb)
    out_nb["cells"] = new_cells
    out_nb.setdefault("metadata", {})
    out_nb["metadata"].setdefault(
        "kernelspec",
        {"display_name": "Python 3", "language": "python", "name": "python3"},
    )
    out_nb.setdefault("nbformat", 4)
    out_nb.setdefault("nbformat_minor", 5)

    dst.write_text(json.dumps(out_nb, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {dst} with {len(out_nb['cells'])} cells.")


if __name__ == "__main__":
    main()

