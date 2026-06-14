import os
from typing import List, Dict, Any

class DocumentChunk:
    def __init__(self, text: str, source_file: str, chunk_id: int):
        self.text = text
        self.source_file = source_file
        self.chunk_id = chunk_id

class LocalRAG:
    def __init__(self, doc_dir: str = "sample_data/runbooks"):
        self.doc_dir = doc_dir
        self.chunks: List[DocumentChunk] = []
        self._load_and_chunk_documents()

    def _extract_text(self, filepath: str) -> str:
        ext = os.path.splitext(filepath)[1].lower()
        if ext in ['.txt', '.md']:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.pdf':
            import pypdf
            text = ""
            try:
                reader = pypdf.PdfReader(filepath)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            except Exception as e:
                print(f"Error reading PDF {filepath}: {e}")
            return text
        elif ext == '.docx':
            import docx
            text = ""
            try:
                doc = docx.Document(filepath)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            except Exception as e:
                print(f"Error reading DOCX {filepath}: {e}")
            return text
        return ""

    def _load_and_chunk_documents(self):
        self.chunks = []
        if not os.path.exists(self.doc_dir):
            os.makedirs(self.doc_dir, exist_ok=True)
            return

        for filename in os.listdir(self.doc_dir):
            filepath = os.path.join(self.doc_dir, filename)
            if not os.path.isfile(filepath):
                continue

            text = self._extract_text(filepath)
            if not text:
                continue

            # Simple chunking logic (e.g. by paragraphs or fixed size)
            # Here we chunk by double newlines or roughly 500 characters
            raw_chunks = text.split("\n\n")
            chunk_id = 0
            for chunk_text in raw_chunks:
                chunk_text = chunk_text.strip()
                if not chunk_text:
                    continue
                # Further split if too long
                if len(chunk_text) > 1000:
                    words = chunk_text.split()
                    temp_chunk = []
                    for w in words:
                        temp_chunk.append(w)
                        if len(" ".join(temp_chunk)) > 800:
                            self.chunks.append(DocumentChunk(" ".join(temp_chunk), filename, chunk_id))
                            chunk_id += 1
                            temp_chunk = []
                    if temp_chunk:
                        self.chunks.append(DocumentChunk(" ".join(temp_chunk), filename, chunk_id))
                        chunk_id += 1
                else:
                    self.chunks.append(DocumentChunk(chunk_text, filename, chunk_id))
                    chunk_id += 1

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves top_k chunks using simple keyword matching (BM25 placeholder).
        """
        # Reload to ensure newly uploaded docs are included. In production this would be handled better.
        self._load_and_chunk_documents()

        query_words = set(query.lower().split())
        scored_chunks = []

        for chunk in self.chunks:
            chunk_words = set(chunk.text.lower().split())
            # Jaccard-ish similarity or simple overlap
            overlap = len(query_words.intersection(chunk_words))
            scored_chunks.append((overlap, chunk))

        # Sort by highest score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, chunk in scored_chunks[:top_k]:
            if score >= 0: # Returning top chunks even with low overlap for demo fallback
                results.append({
                    "text": chunk.text,
                    "source": chunk.source_file,
                    "chunk_id": chunk.chunk_id
                })
        return results

# Singleton instance
rag_engine = LocalRAG()
