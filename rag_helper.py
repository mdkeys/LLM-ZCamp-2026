# Create instructions and prompt template 

INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

PROMPT_TEMPLATE = """
QUESTION: {question}

CONTEXT: {context}
""".strip()

# Create the class: RAGBase
class RAGBase:

    # constructor = runs when you create a new RAGBase instance
    # all parameters expect index and llm_client have defaults so they're optional
    def __init__(
        self,
        index, # index is anything with a search method (e.g., minsearch, sqlitesearch)
        llm_client, # the llm client you're using (required)
        instructions=INSTRUCTIONS, #system prompt, defaults to predefined constant
        prompt_template=PROMPT_TEMPLATE, #user prompt template, defaults to predefined constant
        course="llm-zoomcamp", #filters results to this course
        model="claude-haiku-4-5-20251001"
    ):
        #store each argument on the instance so other methods can access them via self
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions 
        self.course = course
        self.prompt_template = prompt_template
        self.model = model

    # Search method delegates to the index
    def search(self, query, num_results=5):
        boost_dict = {"question": 3.0, "section": 0.5}
        filter_dict = {"course": self.course} #filter restricts results to docs matching this course only (self.course was defined in __init__ to "llm-zoomcamp")

        # Run the search and return results to the caller 
        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            filter_dict=filter_dict
        )
    
    # Build_context and build_promot format the search results:
    def build_context(self, search_results):
        lines = [] #empty list to accumulate formatted lines 

        for doc in search_results:
            lines.append(doc["section"])
            lines.append("Q: " + doc["question"])
            lines.append("A: " + doc["answer"])
            lines.append("")
        
        #join all lins above into one string with newlines, trimming whitespace
        return "\n".join(lines).strip()
    
    def build_prompt(self, query, search_results):
        # Format the search results into readable text block
        context = self.build_context(search_results)

        # Inject user's question + receive context into the prompt template
        # and return the final string ready to send to the LLM
        return self.prompt_template.format(
            question=query, context=context 
        )
    
    # Build te message history to send to the LLM
    # 2 messages: 1) instructions, 2) user prompt
    def llm(self, prompt):
        input_messages = [
            {"role": "assistant", "content": self.instructions},
            {"role": "user", "content": prompt} #user's question + context
        ]

        # code updated to reflect Anthropic model 
        response = self.llm_client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=input_messages
        )

        return response.content[0].text
    
    # Build the RAG method to tie it all together:
    def rag(self, query):
        #step 1: search the index for documents relevant to the query
        search_results = self.search(query)
        #step 2: format the query and search results into a prompt for LLM
        prompt = self.build_prompt(query, search_results)
        #step 3: send the prompt to the LLM to get an answer
        answer = self.llm(prompt)
        #step 4: return the final answer
        return answer
    