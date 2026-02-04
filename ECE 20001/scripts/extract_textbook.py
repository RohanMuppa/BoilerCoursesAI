"""
ECE 20001 Textbook Extraction Tool
Extracts equations, examples, figures, and builds searchable index
"""

import fitz
import re
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR.parent.parent / "config.json"


def load_config():
    """Load configuration from config.json"""
    if not CONFIG_PATH.exists():
        print("Error: config.json not found.")
        print("Copy config.example.json to config.json and fill in your values.")
        sys.exit(1)

    with open(CONFIG_PATH) as f:
        return json.load(f)


def get_paths():
    """Get textbook and output paths from config"""
    config = load_config()
    base_path = Path(config["workspace_path"])

    ece20001_config = config["courses"].get("ECE 20001", {})
    local_folder = ece20001_config.get("local_folder_name", "ECE 20001")
    textbook_filename = ece20001_config.get("textbook_filename", "textbook.pdf")
    extracted_folder = ece20001_config.get("extracted_folder", "extracted")

    course_path = base_path / local_folder
    textbook_path = course_path / textbook_filename
    output_dir = course_path / extracted_folder

    return textbook_path, output_dir


def ensure_output_dir(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "pages").mkdir(exist_ok=True)
    (output_dir / "examples").mkdir(exist_ok=True)


def extract_toc(doc):
    """Extract table of contents"""
    toc = doc.get_toc()
    chapters = []
    for level, title, page in toc:
        chapters.append({
            "level": level,
            "title": title,
            "page": page
        })
    return chapters


def extract_examples(doc):
    """Find all examples with page numbers"""
    examples = []
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        matches = re.findall(r'Example\s+(\d+\.\d+\.?\d*)', text)
        for ex in matches:
            if not any(e["id"] == ex for e in examples):
                examples.append({
                    "id": ex,
                    "page": page_num + 1
                })
    return examples


def extract_equations(doc):
    """Find all numbered equations"""
    equations = []
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        matches = re.findall(r'\((\d+\.\d+)\)', text)
        for eq in matches:
            if not any(e["id"] == eq for e in equations):
                equations.append({
                    "id": eq,
                    "page": page_num + 1
                })
    return equations


def extract_page_as_image(doc, page_num, output_dir, zoom=2):
    """Render a page as PNG image"""
    page = doc[page_num - 1]  # Convert to 0-indexed
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    output_path = output_dir / "pages" / f"page_{page_num:03d}.png"
    pix.save(str(output_path))
    return output_path


def extract_example_pages(doc, examples, output_dir):
    """Extract images of all example pages"""
    for ex in examples:
        page_num = ex["page"]
        output_path = output_dir / "examples" / f"example_{ex['id'].replace('.', '_')}.png"
        page = doc[page_num - 1]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        pix.save(str(output_path))
        ex["image_path"] = str(output_path)
    return examples


def extract_page_text(doc, page_num):
    """Get text from a specific page"""
    return doc[page_num - 1].get_text()


def search_textbook(doc, query):
    """Search for text across all pages"""
    results = []
    query_lower = query.lower()
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        if query_lower in text.lower():
            # Find context around match
            lower_text = text.lower()
            idx = lower_text.find(query_lower)
            start = max(0, idx - 100)
            end = min(len(text), idx + len(query) + 100)
            context = text[start:end].replace('\n', ' ')
            results.append({
                "page": page_num + 1,
                "context": f"...{context}..."
            })
    return results


def build_index(doc):
    """Build complete searchable index"""
    index = {
        "total_pages": len(doc),
        "toc": extract_toc(doc),
        "examples": extract_examples(doc),
        "equations": extract_equations(doc)
    }
    return index


def main():
    textbook_path, output_dir = get_paths()

    if not textbook_path.exists():
        print(f"Error: Textbook not found at {textbook_path}")
        print("Check textbook_filename in config.json")
        sys.exit(1)

    ensure_output_dir(output_dir)
    doc = fitz.open(str(textbook_path))

    print("Building textbook index...")
    index = build_index(doc)

    # Save index
    index_path = output_dir / "index.json"
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)

    print(f"Total pages: {index['total_pages']}")
    print(f"Chapters/sections: {len(index['toc'])}")
    print(f"Examples found: {len(index['examples'])}")
    print(f"Equations found: {len(index['equations'])}")
    print(f"\nIndex saved to {index_path}")

    doc.close()


if __name__ == "__main__":
    main()
