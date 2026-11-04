import json
import sys

def verify():
    with open("notebooks/omniverse_complete_walkthrough.ipynb", "r", encoding="utf-8") as f:
        nb = json.load(f)

    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] == "code":
            code = "".join(cell["source"])
            print(f"--- Executing Cell {i} ---")
            exec(code, globals())

    print("\n>>> ALL NOTEBOOK CELLS EXECUTED FLAWLESSLY! <<<")

if __name__ == "__main__":
    verify()
