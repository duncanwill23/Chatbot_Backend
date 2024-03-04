from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import json

from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA

# Create your views here.
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        print(request.POST)
        #put info into database
        
        response = JsonResponse({'message': 'Hello, World!'}, status=200)
        return response
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_doctors(request):
    if request.method == 'GET':
        response = JsonResponse([{ 'name': 'Dr. John Doe', 'specialty': 'Cardiologist' }, { 'name': 'Dr. Jane Smith', 'specialty': 'Neurologist' }], safe=False, status=200)
        return response
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def get_provider(request):
    if request.method == 'GET':
        response = JsonResponse([{ 'name': 'Blue Cross Blue Sheild'}, { 'name': 'Metlife'}], safe=False, status=200)
        return response
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        key_param = {
            "MONGO_URI": "mongodb+srv://Blobman:Blobman@myatlasclusteredu.hrwoqma.mongodb.net/?retryWrites=true&w=majority&appName=myAtlasClusterEDU",
            "open_api_key": "openai_api_key_here"
        }
        
        data = json.loads(request.body)
        query = data['query']
        
        print("the front end sent this: "+query)

        client = MongoClient(key_param['MONGO_URI'])
        dbName = "langchain_chatbot"
        collectionName = "chatbot_data"
        collection = client[dbName][collectionName]

        embeddings = OpenAIEmbeddings(openai_api_key=key_param['open_api_key'])

        vectorStore = MongoDBAtlasVectorSearch(collection, embeddings)

        def query_data(query):
            docs = vectorStore.similarity_search(query, k=1)
            if not docs:
                return "Sorry, I don't know that. Please ask a doctor or a professional.", "Sorry, I don't know that. Please ask a doctor or a professional."
            as_output = docs[0].page_content
            llm = OpenAI(openai_api_key=key_param['open_api_key'], temperature=0)
            retriever = vectorStore.as_retriever()
            qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
            retriever_output = qa.run(query)
            return as_output, retriever_output

        as_output, retriever_output = query_data(query)

        return JsonResponse({'message': retriever_output}, status=200)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'})
