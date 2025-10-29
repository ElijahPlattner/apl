import subprocess
import time
import json
from pathlib import Path
from api import word_cache


def parse_pdf(filepath: str):
    """Parse PDF into a list of words using pdftotext, then clean up result.txt."""
    output_path = Path('result.txt')

    cmd = ['pdftotext', '-nopgbrk', filepath, str(output_path)]
    ret = subprocess.run(cmd, capture_output=True)

    if ret.returncode != 0:
        raise RuntimeError(f"Error running pdftotext: {ret.stderr.decode('utf-8')}")

    if not output_path.exists():
        raise RuntimeError("Could not open result.txt")

    try:
        text = output_path.read_text(encoding='utf-8')
        return text.split()
    finally:
        # Always try to delete, even if an error happens during reading
        try:
            output_path.unlink()
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"⚠️ Warning: could not delete {output_path}: {e}")


def clean_words(words):
    """Clean words: lowercase, remove non-alphabetic chars, remove short words, dedupe."""
    result = []
    seen = set()

    for word in words:
        cleaned = ''.join(c.lower() if c.isalpha() else ' ' for c in word)
        tokens = cleaned.split()
        for token in tokens:
            if len(token) > 1 and token not in seen:
                result.append(token)
                seen.add(token)
    return result


def analyze_pdf(filepath: str):
    """
    Analyze a PDF using preloaded word caches.
    Returns a dict with categorized word lists and counts.
    """
    # Ensure caches are loaded in this process
    if not word_cache.caps_map:
        print("🔁 Reloading word caches in analyzer process...")
        word_cache.load_all_word_lists()

    start_time = time.time()

    words = parse_pdf(filepath)
    words = clean_words(words)

    caps_count = uncommon_count = unknown_count = looked_up_count = 0
    caps_words, uncommon_words, looked_up_words, unknown_words = [], [], [], []

    for w in words:
        if w in word_cache.skip_map:
            continue
        elif w in word_cache.looked_up_map:
            looked_up_count += 1
            looked_up_words.append(w)
        elif w in word_cache.caps_map:
            caps_count += 1
            caps_words.append(w)
        elif w in word_cache.uncommon_map:
            uncommon_count += 1
            uncommon_words.append(w)
        elif w in word_cache.common_map:
            continue
        else:
            unknown_count += 1
            unknown_words.append(w)

    elapsed = time.time() - start_time

    return {
        "counts": {
            "caps": caps_count,
            "uncommon": uncommon_count,
            "unknown": unknown_count,
            "looked_up": looked_up_count,
            "elapsed_time": round(elapsed, 3),
        },
        "caps_words": caps_words,
        "uncommon_words": uncommon_words,
        "unknown_words": unknown_words,
        "looked_up_words": looked_up_words,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: python3 {Path(__file__).name} file.pdf")
        sys.exit(1)

    result = analyze_pdf(sys.argv[1])
    print(json.dumps(result, indent=2))