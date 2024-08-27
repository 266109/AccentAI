from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return render(request, 'index.html')
def process_transcript(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        global transcript 
        transcript = data.get('transcript')
        # Process the transcript here
        return JsonResponse({'status': 'success', 'transcript': transcript})
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})
