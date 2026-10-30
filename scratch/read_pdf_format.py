import sys

try:
    import pypdf
    reader = pypdf.PdfReader('d:/QGPU/Project_format.pdf')
    print(f"Total Pages: {len(reader.pages)}")
    for i in range(min(5, len(reader.pages))):
        print(f"--- PAGE {i+1} ---")
        print(reader.pages[i].extract_text())
except Exception as e:
    print(f"pypdf error: {e}")
    try:
        import fitz
        doc = fitz.open('d:/QGPU/Project_format.pdf')
        print(f"Total Pages: {len(doc)}")
        for i in range(min(5, len(doc))):
            print(f"--- PAGE {i+1} ---")
            print(doc[i].get_text())
    except Exception as e2:
        print(f"fitz error: {e2}")
