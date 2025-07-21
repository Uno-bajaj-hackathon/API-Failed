import os
import json
from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
import google.generativeai as genai

def get_llm_provider(llm_choice=None):
    if llm_choice:
        return llm_choice.lower()
    return os.environ.get("LLM_PROVIDER", "openai").lower()

def parse_query(user_query, api_keys, llm_choice=None):
    provider = get_llm_provider(llm_choice)
    prompt = (
        'Parse the following query into structured fields: age, gender, procedure, location, policy_duration.\n'
        f'QUERY: "{user_query}"\nRespond as JSON.'
    )
    if provider == 'gemini':
        return parse_query_gemini(user_query, api_keys['GEMINI_API_KEY'])
    else:
        return parse_query_openai(user_query, api_keys['OPENAI_API_KEY'], prompt)

def parse_query_openai(user_query, api_key, prompt):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    data = response.choices[0].message.content
    return json.loads(data)

def parse_query_gemini(user_query, api_key):
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = (
        'Parse the following query into structured fields: age, gender, procedure, location, policy_duration.\n'
        f'QUERY: "{user_query}"\nRespond as JSON.'
    )
    r = model.generate_content(prompt)
    return json.loads(r.text)

def evaluate_policy(clauses, structured_query, api_keys, llm_choice=None):
    provider = get_llm_provider(llm_choice)
    if provider == 'gemini':
        return evaluate_policy_gemini(clauses, structured_query, api_keys['GEMINI_API_KEY'])
    else:
        return evaluate_policy_openai(clauses, structured_query, api_keys['OPENAI_API_KEY'])

def evaluate_policy_openai(clauses, structured_query, api_key):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    prompt = (
        f'User query structured: {json.dumps(structured_query)}\n'
        f'Policy clauses: {json.dumps([c["text"] for c in clauses])}\n'
        'For this request: \n'
        '- Is the procedure covered?\n'
        '- Decision (approved/rejected):\n'
        '- Amount covered (₹):\n'
        '- Clause justification and reference.\n'
        'Respond as JSON with keys: decision, amount, justification.'
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    data = response.choices[0].message.content
    return json.loads(data)

def evaluate_policy_gemini(clauses, structured_query, api_key):
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-pro")
    prompt = (
        f'User query structured: {json.dumps(structured_query)}\n'
        f'Policy clauses: {json.dumps([c["text"] for c in clauses])}\n'
        'For this request: \n'
        '- Is the procedure covered?\n'
        '- Decision (approved/rejected):\n'
        '- Amount covered (₹):\n'
        '- Clause justification and reference.\n'
        'Respond as JSON with keys: decision, amount, justification.'
    )
    r = model.generate_content(prompt)
    return json.loads(r.text)
