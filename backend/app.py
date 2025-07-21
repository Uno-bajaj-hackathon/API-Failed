from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os, io, tempfile, json
from utils import parse_documents, chunk_texts, read_env, allowed_file
from embeddings import embed_chunks, load_vector_db, search_clauses
from llm import parse_query, evaluate_policy
from dotenv import load_dotenv; load_dotenv()



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

api_keys = {
    "OPENAI_API_KEY": read_env("OPENAI_API_KEY"),
    "GEMINI_API_KEY": read_env("GEMINI_API_KEY"),
}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query_route():
    files = request.files.getlist('files')
    user_query = request.form['query']
    llm_choice = request.form.get("llm", None)
    structured_query = parse_query(user_query, api_keys, llm_choice=llm_choice)
    results = []
    for file in files:
        if not allowed_file(file.filename): continue
        text = parse_documents(file)
        chunks = chunk_texts(text)
        embedded_chunks = embed_chunks(chunks)
        vecdb = load_vector_db(embedded_chunks)
        relevant_clauses = search_clauses(vecdb, structured_query, top_k=3)
        decision = evaluate_policy(relevant_clauses, structured_query, api_keys, llm_choice=llm_choice)
        results.append({
            'scheme': file.filename,
            **decision,
            'matched_clauses': [rc['chunk_id'] for rc in relevant_clauses]
        })
    return jsonify({'results': results})

@app.route('/download', methods=['POST'])
def download_report():
    data = request.get_json()
    results = data.get('results', [])
    as_pdf = data.get('as_pdf', False)
    if as_pdf:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        pdf_io = io.BytesIO()
        c = canvas.Canvas(pdf_io, pagesize=letter)
        c.drawString(30, 750, "Insurance Policy Eligibility Report")
        ypos = 725
        for res in results:
            c.drawString(30, ypos, str(res))
            ypos -= 30
        c.save()
        pdf_io.seek(0)
        return send_file(pdf_io, as_attachment=True, download_name="report.pdf")
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)  # Visit http://localhost:5000/
