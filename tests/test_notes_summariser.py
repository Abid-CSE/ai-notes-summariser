import unittest

from notes_summariser import summarize_notes


class TestSummarizeNotes(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(summarize_notes(""), "")

    def test_limits_sentence_count(self):
        text = (
            "Python is used for automation. "
            "Automation saves engineering time. "
            "Testing automation improves reliability. "
            "Gardening tips are unrelated."
        )
        summary = summarize_notes(text, max_sentences=2)
        self.assertLessEqual(summary.count(".") + summary.count("!") + summary.count("?"), 2)

    def test_prefers_repeated_topics(self):
        text = (
            "Machine learning models require clean data. "
            "Data quality affects model performance. "
            "Clean data pipelines reduce failures. "
            "I took a walk in the evening."
        )
        summary = summarize_notes(text, max_sentences=2)
        self.assertIn("data", summary.lower())
        self.assertNotIn("walk", summary.lower())


if __name__ == "__main__":
    unittest.main()
