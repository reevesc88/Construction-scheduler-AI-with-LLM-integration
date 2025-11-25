import os

class VectorDB:
    """Simple in-memory vector store for demo"""
    def __init__(self):
        self.documents = {}
        self.doc_counter = 0
    
    def add_document(self, filename: str, text: str) -> str:
        """Add document and return ID"""
        doc_id = f"doc_{self.doc_counter}"
        self.documents[doc_id] = {"filename": filename, "text": text}
        self.doc_counter += 1
        return doc_id
    
    def search(self, query: str, k: int = 5) -> list:
        """Simple search by keyword"""
        results = []
        for doc_id, doc in self.documents.items():
            if query.lower() in doc["text"].lower():
                results.append(doc["text"][:500])
        return results[:k]