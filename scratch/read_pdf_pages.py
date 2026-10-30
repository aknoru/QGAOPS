import pypdf
reader = pypdf.PdfReader('d:/QGPU/Project_format.pdf')
for i in range(4, len(reader.pages)):
    print(f"=== PAGE {i+1} ===")
    print(reader.pages[i].extract_text())

