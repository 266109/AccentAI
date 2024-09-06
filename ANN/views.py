from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from transformers import pipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
#import pyttsx3
import edge_tts
import asyncio
import playsound

#engine=pyttsx3.init()
# model= pipeline(model="huseinzol05/text-to-speech-tacotron-male")



async def generate_voice(text: str):

    asyncio.sleep(1)

    tts = edge_tts.Communicate(text=text, voice="en-IN-PrabhatNeural", rate="+0%", pitch="+20Hz")
    
    with open("output_audio.mp3", "wb") as audio_file:
        async for chunk in tts.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])



memory=ConversationBufferMemory()


llm=ChatGoogleGenerativeAI(model="gemini-pro",api_key="AIzaSyB0_JjKxykqnqZkviJ2-JDQtqO0CjMnJkE")


prompt="""You are a highly knowledgeable expert Vijay on car care and maintenance. 
I will ask you questions about various aspects of car care, such as engine maintenance, tire care, interior cleaning, and more. 
Please provide comprehensive and informative answers to my queries. 
Respond to the user's questions only in the language in which they ask, 
but use English transliteration for all responses. 
For example, if the user asks in Hindi, like 'tum kon ho,' respond with 'Mai Ek Bot hu.' 
Ensure that the response is in the original language's structure and syntax but written only using the English alphabet
If I ask you a question outside of the car care domain, 
please respond with a polite message indicating that you can only assist with car-related topics..  
            Question: {promp}"""


prompt=PromptTemplate(template=prompt)
chain=LLMChain(llm=llm,memory=memory,prompt=prompt)



def index(request):
    return render(request, 'index.html')


def process_transcript(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        transcript = data.get('transcript')
        # Process the transcript here
        if transcript.strip()!="":
            result=chain.invoke({"promp":transcript})
            print(result["text"])
            asyncio.run(generate_voice(result["text"].replace("*","")))
            playsound.playsound('D:/Ascentt/UI UX/AccentAI/AccentAI/output_audio.mp3',True)
                # model(result.content)
            return JsonResponse({'status': 'success', 'transcript': transcript})
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})
