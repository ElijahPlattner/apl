import sys
import subprocess
import time
from pathlib import Path


def load_wordlist(filename):
    """Load words from a file into a set"""
    words = set()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    words.add(word)
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
    return words


def parse_pdf(filepath):
    """Parse PDF using pdftotext"""
    cmd = ['pdftotext', '-nopgbrk', filepath, 'result.txt']
    ret = subprocess.run(cmd, capture_output=True)
    
    if ret.returncode != 0:
        raise RuntimeError("Error running pdftotext")
    
    try:
        with open('result.txt', 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        raise RuntimeError("Could not open result.txt")
    
    words = text.split()
    return words


def clean_words(words):
    """Clean words: lowercase, remove non-alphabetic chars, remove short words, dedupe"""
    result = []
    seen = set()
    
    for word in words:
        # Keep only alphabetic characters, replace others with space
        cleaned = ''.join(c.lower() if c.isalpha() else ' ' for c in word)
        
        # Split on whitespace and process tokens
        tokens = cleaned.split()
        for token in tokens:
            if len(token) > 1 and token not in seen:
                result.append(token)
                seen.add(token)
    
    return result


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file.pdf")
        sys.exit(1)
    
    try:
        start_time = time.time()
        
        # Load word lists
        caps_list = load_wordlist("analyzer/src/caps.txt")
        common_list = load_wordlist("analyzer/src/common.txt")
        uncommon_list = load_wordlist("analyzer/src/uncommon.txt")
        
        # Step 1: Parse PDF
        words = parse_pdf(sys.argv[1])
        
        # Step 2: Clean words and remove duplicates
        words = clean_words(words)
        
        caps_count = 0
        common_count = 0
        uncommon_count = 0
        unknown_count = 0
        
        caps_words = []
        uncommon_words = []
        unknown_words = []
        
        # Step 3: Classify words
        for w in words:
            if w in caps_list:
                caps_count += 1
                caps_words.append(w)
            elif w in common_list:
                common_count += 1
                # skip writing common words to CSV
            elif w in uncommon_list:
                uncommon_count += 1
                uncommon_words.append(w)
            else:
                unknown_count += 1
                unknown_words.append(w)
        
        # Step 4: Print summary counts
        print(f"Caps count: {caps_count}")
        print(f"Common count: {common_count}")
        print(f"Uncommon count: {uncommon_count}")
        print(f"Unknown count: {unknown_count}")
        
        # Step 5: Write categorized words to CSV
        with open('output.csv', 'w', encoding='utf-8') as outfile:
            outfile.write("not in,caps,uncommon\n")
            
            max_size = max(len(unknown_words), len(caps_words), len(uncommon_words))
            for i in range(max_size):
                u = unknown_words[i] if i < len(unknown_words) else ""
                c = caps_words[i] if i < len(caps_words) else ""
                un = uncommon_words[i] if i < len(uncommon_words) else ""
                outfile.write(f"{u},{c},{un}\n")
        
        print("Wrote categorized words to output.csv")
        
        # End timer
        elapsed = time.time() - start_time
        print(f"Execution time: {elapsed:.6f} seconds")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()