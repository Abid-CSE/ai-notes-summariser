import argparse
import re
from collections import Counter

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "than", "so", "to", "of",
    "in", "on", "for", "with", "as", "at", "by", "from", "is", "are", "was", "were",
    "be", "been", "being", "this", "that", "these", "those", "it", "its", "into", "about",
    "can", "could", "should", "would", "will", "just", "we", "you", "they", "he", "she", "i"
}


def _split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())


def summarize_notes(text: str, max_sentences: int = 3) -> str:
    if not text or not text.strip():
        return ""

    sentences = _split_sentences(text)
    if not sentences:
        return ""

    words = [word for word in _tokenize(text) if word not in STOPWORDS and len(word) > 2]
    if not words:
        return " ".join(sentences[:max_sentences])

    frequencies = Counter(words)
    ranked: list[tuple[int, int, str]] = []

    for idx, sentence in enumerate(sentences):
        score = sum(frequencies.get(token, 0) for token in _tokenize(sentence) if token not in STOPWORDS)
        ranked.append((score, idx, sentence))

    top = sorted(ranked, key=lambda item: (item[0], -item[1]), reverse=True)[:max_sentences]
    ordered = sorted(top, key=lambda item: item[1])
    return " ".join(sentence for _, _, sentence in ordered)


def _read_input(file_path: str | None, text: str | None) -> str:
    if text:
        return text
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return input("Paste notes to summarise: ")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise notes using an extractive AI-like heuristic.")
    parser.add_argument("file", nargs="?", help="Path to a notes file")
    parser.add_argument("--text", help="Raw note text to summarise")
    parser.add_argument("--sentences", type=int, default=3, help="Number of sentences in summary")
    args = parser.parse_args()

    notes = _read_input(args.file, args.text)
    summary = summarize_notes(notes, max_sentences=max(1, args.sentences))
    print(summary)


if __name__ == "__main__":
    main()
