from database import *

from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings
from langchain_openai import OpenAIEmbeddings

from langchain_community.llms import Ollama
from langchain_openai.llms import OpenAI

import os

chunks = create_chunks("ollama-in-context-learning/PDFs/",replace_newlines=True)

print(len(chunks))

#embeddings = OllamaEmbeddings(model="llama3")
#embeddings = BedrockEmbeddings(credentials_profile_name="default",region_name="us-east-1")
#embeddings = GPT4AllEmbeddings()
embeddings = OpenAIEmbeddings()

#save_database(embeddings,chunks,path="ollama-in-context-learning/Chroma")

db = load_database(embeddings,path="ollama-in-context-learning/Chroma")

model = Ollama(
     model = "llama3"
)



count = 1


lst = os.listdir("ollama-in-context-learning/conversations")
number_files = len(lst)

use_old_conversation = input("Enter the number of conversation you would like to use. Enter 0 if you want to start a new conversation ")
if use_old_conversation == "0":
    path_to_use = f"ollama-in-context-learning/conversations/conversations{number_files+1}.txt"
    f = open(path_to_use,'w')
    f.close()

else:
    path_to_use = f"ollama-in-context-learning/conversations/conversations{use_old_conversation}.txt"
    try:
        f = open(path_to_use,'r')
        count = int(f.read().split("\n")[-1])
        print(count)
        f.close()
    except:
        print("Error, unable to open file")
        exit()


while True:
    query = input("Enter a query: ")
    if query.lower() == "exit":
         break
    

    results = query_database(query, db, num_responses = 20)

    f = open(path_to_use,'r')
    conversations = f.read()
    f.close()

    
    
    prompt = """
    Answer the question only based on previous conversations with the user, where greater context weight means greater relevance to the conversation, and the following context:


    Here are the previous conversations with the user, you can use these to help you answer the questions:
    {conversations}


    Here is the context you can use to help you answer the questions:
    {context}

    ------------


    If you do not know the answer, just say you do not know. Answer the question based on previous conversations with the user, where greater context weight means greater relevance to the conversation, and the above context: {question}"""

    response, response_text = get_response(query, results, prompt, model,conversations=conversations)

    print(f"\n{response}")

    try: #In case a negative or invalid value is entered, file will fail to open
        file = open(path_to_use,'a')
        file.write(f"\nContext weight: {count}\nUser question: {query}\nYour response to the user:{response_text}\n")
        file.close()

    except:
        print("Error, unable to open conversation file")
    
    
    count += 1

f = open(path_to_use,'a')
f.write(str(count))
f.close()