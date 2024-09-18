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
import requests
#import boto3
#from botocore.exceptions import NoCredentialsError
#api_key='ASIASFL3AHUURWOXS2HJ'
#secret_key='GKIQsBboO5+PlAf9CNMZNVWGp6NogMWp+xAUwgBf'
#bucket_name = 'ascentt-wl-training-s3'
#s3_file_key = 'ANN/output_audio.mp3'  # Local file to be uploaded

# model= pipeline(model="huseinzol05/text-to-speech-tacotron-male")

#def upload_file_to_s3(local_file,bucket, s3_file_key):
#    s3 = boto3.client('s3',aws_access_key_id=api_key, 
#                      aws_secret_access_key=secret_key)
#    try:
        # Upload the file to S3 and overwrite if it already exists
#        s3.upload_file(local_file, bucket, s3_file_key)
#        print(f"File '{local_file}' uploaded to S3 bucket '{bucket}' as '{s3_file_key}' (overwritten if exists).")
#    except FileNotFoundError:
#        print("The local file was not found.")
#    except NoCredentialsError:
#        print("Credentials not available.")


async def generate_voice(text: str,Language: str):

    asyncio.sleep(1)
    voices={
        "Bengali":"bn-IN-TanishaaNeural",
        "English":"en-IN-PrabhatNeural",
        "Gujarati":"gu-IN-NiranjanNeural",
        "Hindi":"hi-IN-MadhurNeural",
        "Kannada":"kn-IN-GaganNeural",
        "Malayalam":"ml-IN-SobhanaNeural",
        "Marathi":"mr-IN-AarohiNeural",
        "Tamil":"ta-IN-ValluvarNeural",
        "Telugu":"te-IN-MohanNeural",}
    try:
        tts = edge_tts.Communicate(text=text, voice=voices[Language], rate="+10%", pitch="+20Hz")
        with open("output_audio.mp3", "wb") as audio_file:
            async for chunk in tts.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
    except:
        pass

API_KEY = 'AIzaSyAWuefqnSJ8_Zh7iefNf03ggdeqjN8G8kk'


memory=ConversationBufferMemory()


llm=ChatGoogleGenerativeAI(model="gemini-pro",api_key="AIzaSyAWuefqnSJ8_Zh7iefNf03ggdeqjN8G8kk")

prompt="""You are a highly knowledgeable expert Eco on car care and maintenance. 
I will ask you questions about various aspects of car care, such as engine maintenance, tire care, interior cleaning, and more. 
Please provide comprehensive and informative answers to my queries.
If I ask you a question outside of the car care domain, 
please respond with a polite message indicating that you can only assist with car-related topics..  
Question: {promp}"""

prompt1="""Detect the language of the following text and return only the name of the language without any additional information:

[{}]"""

prompt2="""Convert the following text into [Target Language] but write it using the English alphabet (transliteration). and do not provide Additional Information:

Text: "[{}]"
Target Language: "[{}]"""

prompt3="""Translate the following text from [Source Language] to [Target Language]. Return only the translated text without any additional information:

Text: "[{}]"
Source Language: "[{}]"
Target Language: "[{}]"""
prompt=PromptTemplate(template=prompt)
chain=LLMChain(llm=llm,memory=memory,prompt=prompt)


def index(request):
    return render(request, 'index.html')



@csrf_exempt  
def receive_data(request):
    if request.method == 'POST':
        # Parse the JSON data from the request
        transcript = json.loads(request.body)
        print('Received data:', transcript)
        transcript=transcript["transcript"]
        language=llm.invoke(prompt1.format(transcript)).content
        text=llm.invoke(prompt3.format(transcript,language,"English")).content
        result=chain.invoke({"promp":text})
        result=result["text"]
        final_result=llm.invoke(prompt2.format(result,language)).content
        api_url = 'https://ofw4cpczm4.execute-api.us-east-1.amazonaws.com/prod'
        data = {
            'body':{
               'received_data': transcript, 
               'Input Language':language,
               'result in Native':final_result
              }
        }

        response = send_data_to_lambda(api_url, data)
        response_injson=response.json()
        response_body=response_injson['body']
#        audio_url= response_body.audio_file_url
       
        return JsonResponse({'status': 'success', 'received_data': transcript,'Input Language':language,'result in Native':final_result,'audio_url':response_body})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

def send_data_to_lambda(api_url, data, headers=None):
    try:
        # Convert data to JSON format
        json_data = json.dumps(data)
        data['body'] = json.dumps(data['body'])

        # If no headers are provided, use default Content-Type
        if headers is None:
            headers = {
                'Content-Type': 'application/json'
            }

        # Send POST request to API Gateway
        response = requests.post(api_url, headers=headers, data=json.dumps(data))

        # Check if the request was successful
        if response.status_code == 200:
            print("Data successfully sent to Lambda!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")

        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

