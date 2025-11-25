from typing import List
import io

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes.
    Handles cases where unstructured is not fully installed.
    """
    try:
        from unstructured.partition.pdf import partition_pdf
        elements = partition_pdf(file=io.BytesIO(pdf_bytes))
        text = "\n".join([e.text for e in elements if hasattr(e, "text")])
        return text
    except Exception as e:
        print(f"PDF extraction error: {e}")
        # Fallback: return placeholder
        return "PDF content extraction failed. Please ensure PDF is valid."