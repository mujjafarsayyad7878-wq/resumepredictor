"""
Document and PDF Parsing Service
Robust multi-strategy extraction supporting native PDF streams, pypdf if available, and raw text.
"""
import io
import re
import zlib
from typing import Optional

try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    try:
        import PyPDF2 as pypdf
        PYPDF_AVAILABLE = True
    except ImportError:
        pypdf = None
        PYPDF_AVAILABLE = False

def extract_text_from_pdf_stream(pdf_bytes: bytes) -> str:
    """
    Pure Python stream extractor that scans and decompresses FlateDecode PDF streams
    and extracts text blocks (BT ... ET), ensuring zero crash even if external packages are missing.
    """
    text_chunks = []
    
    # 1. Search for FlateDecode compressed streams
    stream_pattern = re.compile(b'stream\r?\n(.*?)\r?\nendstream', re.DOTALL)
    for match in stream_pattern.finditer(pdf_bytes):
        raw_stream = match.group(1)
        decompressed = b""
        try:
            decompressed = zlib.decompress(raw_stream)
        except Exception:
            try:
                # Some PDFs use zlib without header
                decompressed = zlib.decompress(raw_stream, -15)
            except Exception:
                decompressed = raw_stream

        # Look for text operators: (Text) Tj, [(T) 10 (ext)] TJ
        if decompressed:
            try:
                text_str = decompressed.decode('latin-1', errors='ignore')
                
                # Match (text) Tj
                tj_matches = re.findall(r'\((.*?)\)\s*Tj', text_str)
                for t in tj_matches:
                    text_chunks.append(t)
                
                # Match array [(...)] TJ
                array_matches = re.findall(r'\[(.*?)\]\s*TJ', text_str)
                for arr in array_matches:
                    parts = re.findall(r'\((.*?)\)', arr)
                    if parts:
                        text_chunks.append("".join(parts))
            except Exception:
                pass

    extracted = " ".join(text_chunks)
    # Clean up PDF escape sequences
    extracted = re.sub(r'\\[nrtbf\\()]', ' ', extracted)
    extracted = re.sub(r'\s+', ' ', extracted).strip()
    return extracted

def parse_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Attempts pypdf extraction first, then falls back to pure Python PDF stream parsing.
    """
    extracted_text = ""

    # Strategy 1: pypdf if available
    if PYPDF_AVAILABLE and pypdf:
        try:
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            pages_text = []
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    pages_text.append(txt)
            if pages_text:
                extracted_text = "\n".join(pages_text).strip()
        except Exception:
            extracted_text = ""

    # Strategy 2: Native stream parsing fallback
    if len(extracted_text) < 50:
        stream_text = extract_text_from_pdf_stream(pdf_bytes)
        if len(stream_text) > len(extracted_text):
            extracted_text = stream_text

    # Strategy 3: Raw ascii / utf-8 text extraction
    if len(extracted_text) < 30:
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                decoded = pdf_bytes.decode(encoding, errors='ignore')
                # Filter printable ascii and basic symbols
                printable = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', ' ', decoded)
                words = [w for w in printable.split() if len(w) > 2 and w.isprintable()]
                if len(words) > 30:
                    extracted_text = " ".join(words)
                    break
            except Exception:
                continue

    return extracted_text

def parse_uploaded_file(file_bytes: bytes, filename: str) -> str:
    """
    Dispatches parser based on file extension.
    """
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        return parse_pdf_bytes(file_bytes)
    else:
        # Plain text, Markdown, CSV, etc.
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
            try:
                return file_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue
        return file_bytes.decode('utf-8', errors='replace')
