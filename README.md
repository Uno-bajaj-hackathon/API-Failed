Absolutely! Here’s a **README.md** that will help anyone run and adapt your project with options for OpenAI, Gemini, and clear troubleshooting for typical API/quota issues.

# Insurance Policy LLM Eligibility Checker

This project lets users check insurance eligibility by uploading policy documents and asking natural language questions. The backend uses Python (Flask) and the frontend is rendered with Flask templates.

**Supports:**
- OpenAI (ChatGPT GPT-3.5/GPT-4, if available)
- Google Gemini (1.5-pro, quota/restrictions apply)
- Modular: extendable to other LLM providers or local models!

## Features

- **User can upload PDF, DOCX, and EML insurance policies (drag & drop/upload).**
- **Ask natural language queries (e.g., "46-year-old male, knee surgery, 3-month policy in Pune").**
- **Semantically parses policies, finds relevant clauses, and presents answers with decisions and justification.**
- **Download final report (JSON or PDF) with a button.**
- **Choose LLM provider (OpenAI or Gemini) per-query or set as default.**

## How To Run

### 1. Prerequisites
- Python 3.8+
- pip
- Internet access for API calls

### 2. Clone and Set Up

```sh
git clone 
cd insurance-llm-app/backend
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables

Copy the example and set your real API keys:

```sh
cp .env.example .env
```

Then edit `.env`:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxx
LLM_PROVIDER=openai       # or gemini
```

- **Tip:** Only paste valid, active keys (no quotes, spaces, or comments on the same line).

### 4. Start the Flask App

```sh
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### 5. Use The App

- Fill in your insurance claim query.
- Drag & drop, or upload, your policy files.
- Select the LLM provider (if shown).
- Click **Submit**.
- See results and/or download as JSON or PDF.

## Troubleshooting & Common Issues

### 🔸 **OpenAI Errors**
- **401 Authentication Error:** Your OPENAI_API_KEY is invalid or expired. Get a fresh API key at https://platform.openai.com/account/api-keys and update `.env`.
- **404 Model Not Found:** Your account **does not have GPT-4** access. Use "gpt-3.5-turbo" as the model in your code instead.

### 🔸 **Gemini Errors**
- **429: Quota Exhausted:** Free-tier Gemini API is rate-limited. Wait for the quota to reset or add billing for higher limits. See [Google Gemini quotas](https://ai.google.dev/gemini-api/docs/rate-limits).
- **400: API key expired:** Delete all old Gemini API keys, generate a new one, and set it in `.env`. Sometimes waiting or using a different Google account may help.

### 🔸 **Switching Models**
- For OpenAI: Use `"gpt-3.5-turbo"` (works for all users). `"gpt-4"` is restricted to paid or approved accounts.
- For Gemini: Use `"gemini-1.5-pro-latest"` or `"gemini-1.5-pro"`. Do NOT use vision or embedding models unless you're building for images.

### 🔸 **Alternative: Local/Open-Source Models**
If you do not want to use online APIs, integrate open-source LLMs using HuggingFace, llama-cpp-python, vLLM, etc. (Code not included in this repo.)

## FAQ

**Q: What if both OpenAI and Gemini are unavailable?**  
A: You will see error messages. Use the provider with available quota/API or switch to a local model.

**Q: My .env changes don’t work?**  
A: Fully stop and restart the Flask app after changing `.env`. Ensure `python-dotenv` is installed.

**Q: Where do I get sample policies?**  
A: See the `sample_policies/` directory or use your own documents.

## Project Structure

```
backend/
│   app.py              # Flask app
│   llm.py              # LLM API calls
│   embeddings.py       # Embedding & search logic
│   utils.py            # File/text parsing helpers
│   requirements.txt
│   templates/
│     index.html        # Main UI template
│   static/
│     script.js         # Frontend behavior
│     styles.css        # UI styles
│   sample_policies/    # Example files
.env
.env.example
```

## Extending

- Plug in other LLMs or cloud providers easily in `llm.py`.
- Add more robust document parsing in `utils.py`.

## Security

- Never share your real API keys publicly.
- Always use `.env` for secrets, and **add `.env` to `.gitignore`**.

## Credits

- Built with Flask, Sentence Transformers, pdfplumber, Google Generative AI, OpenAI Python, and more.

## License

MIT

**Happy insurance policy reasoning with LLMs!**  
_If you run into issues, check your API key, quota, and model before debugging code!_
