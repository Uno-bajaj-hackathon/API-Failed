from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks):
    embeddings = model.encode(chunks, convert_to_numpy=True)
    return [{'chunk_id': f'clause-{i}', 'text': chunk, 'embedding': embeddings[i]} for i, chunk in enumerate(chunks)]

def load_vector_db(embedded_chunks):
    vectors = np.vstack([ec['embedding'] for ec in embedded_chunks])
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    return {'index': index, 'documents': embedded_chunks}

def search_clauses(vecdb, query_struct, top_k=3):
    query_text = ' '.join(str(value) for value in query_struct.values())
    query_emb = model.encode([query_text])
    D, I = vecdb['index'].search(query_emb, top_k)
    return [vecdb['documents'][i] for i in I[0]]
