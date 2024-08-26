from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return render(request, 'index.html')
def process_transcript(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transcript = data.get('transcript')
        
        # Now you have access to the 'transcript' variable
        print("Received transcript:", transcript)

        # Do something with the transcript...
        response_data = {'message': 'Transcript received successfully'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)