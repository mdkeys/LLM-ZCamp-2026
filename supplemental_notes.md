# Supplemental notes
These are notes I've taken along the course to help job my memory.
These notes are not comprehensive. 

## [Mod 01 Lesson 02] (https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/lessons/02-environment.md)
* Working out of Github Codespaces using VS Code desktop
* Install `uv` and run `uv init`. This creates `pyproject.toml` and basic project structure for python. 
* Add anthropic too `uv add anthropic`
* When first time with the codespace, when you run the code in the python notebook, VSCode will suggest installing environment for python + jupyter notebook (yes). Then select Python, then select your environment (llm-zcamp...etc). Code in the notebook will run after that environment is connected. 
* Create '.gitignore' and add '.venv' and '.env' to it.
* In '.env', add 'ANTHROPIC_API_KEY=YOUR_KEY_HERE' 
* Get Anthropic credits: Go to console.anthropic.com, create an account, and purchase $5 in credits. 
    * Create a new workspace 'llm-zoomcamp'
    * In 'llm-zoomcamp' go to 'API Keys' > 'Create key' > copy key into .env. 
* In 'notebook.ipynb', copy code 
```
from dotenv import load_dotenv
load_dotenv()
```
* Next, in 'notebook.ipynb' load anthropic:
```
from anthropic import Anthropic
aiclient = Anthropic()
```
* Next in notebook, define a function "llm" to talk to the LLM. Use haiku model now because it's cheap/fast:
```
def llm(prompt):
    response = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```
* Test the function with an input: `llm('Hey whats up?')`
* Test the function with a course-specific question to see that it can't give a specific answer without context. 
* Add context (see lesson 3 code)
* Then add prompt that includes the question and the context
* Then run the prompt again using the 'answer' defined from before. You can see this is correct. 

What we did with RAG:
```
def rag(question):
    search_results = search(question)
    user_prompt = build_prompt(question, search_results)
    return llm(user_prompt)
```

## Mod 01 Lesson 03
* Fetch the data in your notebook 
```
import requests

docs_url = "https://datatalks.club/faq/json/courses.json"
response = requests.get(docs_url)
courses_raw = response.json()
```
For [Mod 01 Lesson 8]
* Create 'ingest.py' (load data, build search index) and 'rag_helper.py' (RAG logic for search, prompt, LLM)

## Mod 01 Lesson 9
* Discussion of Elastic search vs Persistent Search
* Install: `uv add sqlitesearch`
* Create new notebook 'persistent_rag_ingest.ipynb' for data ingestion
* Add faq.db and *.db, *.db-shm, *.db-wal to '.gitignore'
* Create new notebook 'persistent_rag.ipynb' to create rag assistent 

**Note:** I made an error in the 'persistent_rag_ingest.ipynb' and named the text_field "questions" instead of "question". But when I fixed and tried to run this, I received errors because the code was referring to the "faq.db" which was not updating. I needed to delete the database before re-running the code. 