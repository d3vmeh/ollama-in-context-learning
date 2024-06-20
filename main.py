from database import *

from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings
from langchain_openai import OpenAIEmbeddings


from langchain_community.llms import Ollama


chunks = create_chunks("",replace_newlines=True)


#embeddings = OllamaEmbeddings(model="llama3")
#embeddings = BedrockEmbeddings(credentials_profile_name="default",region_name="us-east-1")
#embeddings = GPT4AllEmbeddings()
embeddings = OpenAIEmbeddings()

#save_database(embeddings,chunks)

db = load_database(embeddings)

model = Ollama(
    model = "llama3"
)



count = 1
while True:
    query = input("Enter a query: ")
    if query.lower() == "exit":
         break
    

    results = query_database(query, db, num_responses = 5)

    f = open("conversations.txt",'r')
    conversations = f.read()
    f.close()

    prompt = """
    Answer the question only based on previous conversations with the user, where greater context weight means greater relevance to the conversation, and the following context:


    Here are the previous conversations with the user:
    {conversations}


    Here is the context you can use:
    {context}

    ------------


    Answer the question based on previous conversations with the user, where greater context weight means greater relevance to the conversation, and the above context: {question}"""

    response = get_response(query, results, prompt, model,conversations=conversations)

    print(f"\n{response}")

    file = open("conversations.txt",'w')
    file.write(f"\nContext weight: {count}\nUser question: {query}\nYour response:{response}\n")
    file.close()

    count += 1
