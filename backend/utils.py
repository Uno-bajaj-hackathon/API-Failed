import pdfplumber, docx2txt, os
from unstructured.partition.auto import partition

def read_env(var):
    return os.environ.get(var)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'eml'}

def parse_documents(file):
    ext = file.filename.split('.')[-1].lower()
    if ext == 'pdf':
        with pdfplumber.open(file) as pdf:
            return ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif ext == 'docx':
        return docx2txt.process(file)
    elif ext == 'eml':
        elems = partition(file)
        return ' '.join([e.text for e in elems])
    return ""

def chunk_texts(text, chunk_size=500):
    sentences = text.split('. ')
    chunks, chunk = [], []
    count = 0
    for sent in sentences:
        if count + len(sent) <= chunk_size:
            chunk.append(sent)
            count += len(sent)
        else:
            chunks.append('. '.join(chunk))
            chunk, count = [sent], len(sent)
    if chunk:
        chunks.append('. '.join(chunk))
    return chunks
