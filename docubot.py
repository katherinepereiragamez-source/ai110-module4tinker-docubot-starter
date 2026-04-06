"""
Core DocuBot class responsible for:
- Loading documents from the docs/ folder
- Building a simple retrieval index (Phase 1)
- Retrieving relevant snippets (Phase 1)
<<<<<<< HEAD
- Supporting retrieval-only answers
=======
- Supporting retrieval only answers
>>>>>>> 6428137a609405c20ec0c08b35d5e97ef14cbbfc
- Supporting RAG answers when paired with Gemini (Phase 2)
"""

import os
import glob
<<<<<<< HEAD
import re


# Minimum number of query words that must match a chunk before it is
# returned as evidence. Raising this makes DocuBot stricter (fewer
# answers); lowering it makes it more permissive (more guesses).
# Keeping this as a named constant makes the policy explicit and easy
# to tune without hunting through logic.
MIN_SCORE_THRESHOLD = 2


def _chunk_text(text, min_chunk_len=40):
    """
    Splits a document into paragraphs by splitting on one or more blank
    lines (the natural paragraph boundary in Markdown and plain text).

    Paragraphs shorter than min_chunk_len characters are discarded —
    they're usually headings, dividers, or stray whitespace that add
    noise without useful signal.

    Kept as a module-level helper so it can be tested independently of
    the DocuBot class.
    """
    raw_chunks = re.split(r'\n{2,}', text)
    return [c.strip() for c in raw_chunks if len(c.strip()) >= min_chunk_len]


class DocuBot:
    def __init__(self, docs_folder="docs", llm_client=None):
        self.docs_folder = docs_folder
        self.llm_client = llm_client
        self.documents = self.load_documents()   # List of (filename, text)
        # Chunk corpus once at startup; every retrieve() call uses these.
        self.chunks = self._build_chunks(self.documents)
        self.index = self.build_index(self.chunks)
=======

class DocuBot:
    def __init__(self, docs_folder="docs", llm_client=None):
        """
        docs_folder: directory containing project documentation files
        llm_client: optional Gemini client for LLM based answers
        """
        self.docs_folder = docs_folder
        self.llm_client = llm_client

        # Load documents into memory
        self.documents = self.load_documents()  # List of (filename, text)

        # Build a retrieval index (implemented in Phase 1)
        self.index = self.build_index(self.documents)
>>>>>>> 6428137a609405c20ec0c08b35d5e97ef14cbbfc

    # -----------------------------------------------------------
    # Document Loading
    # -----------------------------------------------------------

    def load_documents(self):
        """
        Loads all .md and .txt files inside docs_folder.
        Returns a list of tuples: (filename, text)
        """
        docs = []
        pattern = os.path.join(self.docs_folder, "*.*")
        for path in glob.glob(pattern):
            if path.endswith(".md") or path.endswith(".txt"):
                with open(path, "r", encoding="utf8") as f:
                    text = f.read()
                filename = os.path.basename(path)
                docs.append((filename, text))
        return docs

    # -----------------------------------------------------------
<<<<<<< HEAD
    # Chunking
    # -----------------------------------------------------------

    def _build_chunks(self, documents):
        """
        Explodes every document into paragraph-level chunks.
        Returns a flat list of (filename, chunk_text) tuples.

        Storing source filename on each chunk means we can still tell
        the user which file the evidence came from.
        """
        chunks = []
        for filename, text in documents:
            for chunk in _chunk_text(text):
                chunks.append((filename, chunk))
        return chunks

    # -----------------------------------------------------------
    # Index Construction
    # -----------------------------------------------------------

    def build_index(self, chunks):
        """
        Builds an inverted index over chunks (not whole documents).

        Maps each lowercase token to the *set of integer positions*
        in self.chunks where that token appears, so retrieve() can jump
        directly to candidate chunks without a full scan.

        Structure:
            { "token": {0, 4, 17}, "database": {2, 5} }
        """
        index = {}
        for i, (_, chunk_text) in enumerate(chunks):
            tokens = re.split(r'[^a-zA-Z0-9]+', chunk_text.lower())
            for token in tokens:
                if not token:
                    continue
                if token not in index:
                    index[token] = set()
                index[token].add(i)
        return index

    # -----------------------------------------------------------
    # Scoring and Retrieval
=======
    # Index Construction (Phase 1)
    # -----------------------------------------------------------

    def build_index(self, documents):
        """
        TODO (Phase 1):
        Build a tiny inverted index mapping lowercase words to the documents
        they appear in.

        Example structure:
        {
            "token": ["AUTH.md", "API_REFERENCE.md"],
            "database": ["DATABASE.md"]
        }

        Keep this simple: split on whitespace, lowercase tokens,
        ignore punctuation if needed.
        """
        index = {}
        # TODO: implement simple indexing
        return index

    # -----------------------------------------------------------
    # Scoring and Retrieval (Phase 1)
>>>>>>> 6428137a609405c20ec0c08b35d5e97ef14cbbfc
    # -----------------------------------------------------------

    def score_document(self, query, text):
        """
<<<<<<< HEAD
        Returns a relevance score: the count of unique query words that
        appear at least once in text (case-insensitive).

        Unchanged from Phase 1 — the scoring logic is the same whether
        the unit is a whole document or a paragraph chunk.
        """
        query_tokens = set(re.split(r'[^a-zA-Z0-9]+', query.lower()))
        query_tokens.discard("")
        doc_lower = text.lower()
        return sum(1 for token in query_tokens if token in doc_lower)

    def retrieve(self, query, top_k=3):
        """
        Returns up to top_k (filename, chunk_text) pairs most relevant
        to the query, with two guardrails:

        1. Candidate filtering via the inverted index — only chunks
           containing at least one query word are scored at all.
        2. Confidence threshold (MIN_SCORE_THRESHOLD) — chunks that match
           too few query words are silently dropped. If nothing clears the
           threshold, an empty list is returned and the caller will produce
           a refusal rather than a low-confidence answer.
        """
        query_tokens = [
            t for t in re.split(r'[^a-zA-Z0-9]+', query.lower()) if t
        ]

        # Step 1: use index to collect candidate chunk indices
        candidate_indices = set()
        for token in query_tokens:
            for idx in self.index.get(token, set()):
                candidate_indices.add(idx)

        # Step 2: score candidates and apply confidence threshold
        scored = []
        for idx in candidate_indices:
            filename, chunk_text = self.chunks[idx]
            score = self.score_document(query, chunk_text)
            if score >= MIN_SCORE_THRESHOLD:          # ← confidence guardrail
                scored.append((score, filename, chunk_text))

        # Step 3: sort by score desc, filename as stable tiebreaker
        scored.sort(key=lambda item: (-item[0], item[1]))

        return [(fname, chunk) for _, fname, chunk in scored[:top_k]]
=======
        TODO (Phase 1):
        Return a simple relevance score for how well the text matches the query.

        Suggested baseline:
        - Convert query into lowercase words
        - Count how many appear in the text
        - Return the count as the score
        """
        # TODO: implement scoring
        return 0

    def retrieve(self, query, top_k=3):
        """
        TODO (Phase 1):
        Use the index and scoring function to select top_k relevant document snippets.

        Return a list of (filename, text) sorted by score descending.
        """
        results = []
        # TODO: implement retrieval logic
        return results[:top_k]
>>>>>>> 6428137a609405c20ec0c08b35d5e97ef14cbbfc

    # -----------------------------------------------------------
    # Answering Modes
    # -----------------------------------------------------------

    def answer_retrieval_only(self, query, top_k=3):
        """
<<<<<<< HEAD
        Phase 1 retrieval-only mode.
        Returns raw chunk text and source filenames; no LLM involved.
        An explicit refusal message is returned when retrieve() finds
        nothing above the confidence threshold.
        """
        snippets = self.retrieve(query, top_k=top_k)
        if not snippets:
            return "I don't have enough information in these docs to answer that."
        formatted = [f"[{filename}]\n{chunk}\n" for filename, chunk in snippets]
=======
        Phase 1 retrieval only mode.
        Returns raw snippets and filenames with no LLM involved.
        """
        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        formatted = []
        for filename, text in snippets:
            formatted.append(f"[{filename}]\n{text}\n")

>>>>>>> 6428137a609405c20ec0c08b35d5e97ef14cbbfc
        return "\n---\n".join(formatted)

    def answer_rag(self, query, top_k=3):
        """
        Phase 2 RAG mode.
<<<<<<< HEAD
        Uses chunk-level retrieval to select evidence, then passes it
        to the LLM to synthesise an answer.
=======
        Uses student retrieval to select snippets, then asks Gemini
        to generate an answer using only those snippets.
>>>>>>> 6428137a609405c20ec0c08b35d5e97ef14cbbfc
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )
<<<<<<< HEAD
        snippets = self.retrieve(query, top_k=top_k)
        if not snippets:
            return "I don't have enough information in these docs to answer that."
        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Bonus Helper
=======

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Bonus Helper: concatenated docs for naive generation mode
>>>>>>> 6428137a609405c20ec0c08b35d5e97ef14cbbfc
    # -----------------------------------------------------------

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
<<<<<<< HEAD
        Used in Phase 0 for naive 'generation only' baselines.
        """
        return "\n\n".join(text for _, text in self.documents)
=======
        This is used in Phase 0 for naive 'generation only' baselines.
        """
        return "\n\n".join(text for _, text in self.documents)
>>>>>>> 6428137a609405c20ec0c08b35d5e97ef14cbbfc
