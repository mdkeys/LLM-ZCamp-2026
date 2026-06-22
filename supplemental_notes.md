# Supplemental notes
These are notes I've taken along the course to help job my memory.
These notes are not comprehensive. 

# MODULE 1
Documents:
- Lessons 2-7: 
    '.env', '.gitignore'
    'notebook.ipynb' (explore concepts)
- Lesson 8:
    - 'ingest.py'(load data, build search index) 
    - 'rag_helper.py' (RAG logic for search, prompt, LLM)
    - 'rag_cleaned.ipynb' (import .py files to test the RAG)
- Lesson 9:
    - 'persistent_rag_ingest.ipynb' (data ingestion)
    - 'persistent_rag.ipynb' (create rag assisten & test it)
    - 'faq.db' is created & used by rag (this is what makes it "persistent")
- Lesson 12: Re-ran 'rag_cleaned.ipynb' & added tests to show limitations
- Lesson 12-14:
    - 'agents.ipynb' 

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
## Mod 01 Lesson 8
* Create 'ingest.py' (load data, build search index) and 'rag_helper.py' (RAG logic for search, prompt, LLM)

## Mod 01 Lesson 9
* Discussion of Elastic search vs Persistent Search
* Install: `uv add sqlitesearch`
* Create new notebook 'persistent_rag_ingest.ipynb' for data ingestion
* Add faq.db and *.db, *.db-shm, *.db-wal to '.gitignore'
* Create new notebook 'persistent_rag.ipynb' to create rag assistent 

**Note:** I made an error in the 'persistent_rag_ingest.ipynb' and named the text_field "questions" instead of "question". But when I fixed and tried to run this, I received errors because the code was referring to the "faq.db" which was not updating. I needed to delete the database before re-running the code. 

## Mod 01 - Part 2

* Lesson 11:
- Instead of having fixed flow, have an agent to take control of the RAG by telling it the instructions to take the question from the user.

* Lesson 12:
- First, search component of RAG (query → search on the FAQ database)
- Second, build prompt with query + context form search. Includes instructions for the LLM on how to handle the query and context. 
- Then LLM gives the answer
- Re-use the code from the previous lesson to build RAG (rag_helper.py)

* Lesson 13:
- Adjust search function neutral to take in the query from the user.
- Using 'agents.ipynb'
- 1. Make a call to the LLM (the first call) <-- pay
- 2. LLM decided to invoke search('params')
- 3. We invoke the search --> have the results
- 4. Send the results back to the LLM (another call) <-- pay
- 5. LLM processes the results
- 6. LLM gives the answer

* Lesson 14:
- What if LLM decides to make another tool call after processing the result? 
    - 6. LLM decides to make another tool call
    - 7. Send one more API request <-- pay
    - 8. Process and gives the answer 
- Use a developer prompt that is more explicit and allows the agent to make multiple searches. 
- Put everything the LLM hands back into the message history (`messages.extend(response.output`). 
    - In example: Role of agent, query from student, 2 decisions of LLM to invoke the tool, results --> all this is in the message history to send back to the LLM.

* Lesson 15: ToyAIKit
- ToyAIKit is a small library. Look at the code for the agentic loop. Useful framework to use, but not required if you want to use another framework.
- Write your tool and then the framework figures out how to use it
- Interactive 

* Lesson 16: 
- Explore different frameworks and see what you like