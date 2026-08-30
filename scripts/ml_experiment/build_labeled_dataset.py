import json

from pathlib import Path

from scripts.edgar_spike import save_results

ROOT = Path(__file__).resolve().parents[2]



pos_file = ROOT / "data" / "debt_classifier" / "labeled" / "true_exhibits.json"
neg_file =  ROOT / "data" / "debt_classifier" / "labeled" / "false_exhibits.json"

DATA_DIR = ROOT / "data" / "debt_classifier" / "labeled" 

OUTPUT_DIR = ROOT / "data" / "debt_classifier" / "labeled" 

inputs = [pos_file, neg_file]

def build_labeled_dataset(file_paths: list[Path]) -> None:

    results = []  # we will collect the objects with the target label
    label = "human_label"

    for file in file_paths:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

            for obj in data:
                if label not in obj:
                    continue
                results.append(obj)


    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        print(f"wrote labeled examples to: {output_path}")


candidate_file = DATA_DIR / "candidate_exhibits_v2.json"
OUTPUT_PATH = DATA_DIR / "candidate_exhibits_v2_flattened.json"


def flatten(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = []
    for filing in data:
        for exhibit in filing["exhibits"]:
            result.append({
                "issuer_name": filing["issuer_name"],
                "cik": filing["cik"],
                "filing_date": filing["filing_date"],
                "accession": filing["accession"],
                **exhibit,
            })

    save_results(result, OUTPUT_PATH)
    print(f"saved to: {OUTPUT_PATH}")

flatten(candidate_file)