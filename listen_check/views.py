# from cgitb import html
from cgitb import text
from unittest import result
from django.http import HttpResponse
from django.shortcuts import render
from django import forms

# from .models import Question

# from templates import index.html

# def vote(request, question_id):
#     return HttpResponse(index.html % question_id)
# Create your views here.

# def index(request):
#     return HttpResponse(index.html)

import speech_recognition as sr
import requests
import json
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/JacquelineP/Coding/stt_grammar/credentials.json"

# 3 ㄱㅐ의 함수 를 만들어야함 
# 1. 녹음 함수 
# 2. 음성 텍스트 변환 
# 3. 스펠 체크 

# 3개 함수를 순차적으로 실행하여 우리가 원하는 결과 나오면 굿 !

def record(seconds):
    import pyaudio
    import wave

    FORMAT = pyaudio.paInt16
    CHANNELS = 1  #only mono
    RATE = 16000 
    CHUNK = 1024  #확인 필요
    RECORD_SECONDS = int(seconds) #10초 녹음
    WAVE_OUTPUT_FILENAME = "file.wav"

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * int(RECORD_SECONDS))):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    speech_file = WAVE_OUTPUT_FILENAME
    return speech_file

def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech

    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )


    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    scribed = ''
    for result in response.results:

        # The first alternative is the most likely one for this portion.
        abi = result.alternatives[0].transcript
        confidencenum = result.alternatives[0].confidence
        print(u"Transcript: {}".format(abi)) # result of recording
        print("Confidence: {}%".format(confidencenum*100))
        scribed += abi
        percentage = confidencenum*100
        
    # audio = abi

    # try:
    #     print("Google Speech Recognition thinks you said : " + format(abi)(audio, language='en'))
    # except sr.UnknownValueError:
    #     print("Google Speech Recognition could not understand audio")
    # except sr.RequestError as e:
    #     print("Could not request results from Google Speech Recognition service; {0}".format(e))
    # print(scribed)
    return scribed, percentage #선생님 이거percentage 따로 저장하고 그 accuracy percentage 밑에다가 붙이고 싶은데 어떻게 그걸 해요
    

def spell_check(text):
    api_key = "02fb91fde9af457cb95078bea4a7319b"
    endpoint = "https://api.bing.microsoft.com/v7.0/SpellCheck"

    data = {'text': text}

    params = {
        'mkt':'en-us',
        'mode':'proof'
        }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': api_key,
        }

    response = requests.post(endpoint, headers=headers, params=params, data=data)

    json_response = response.json()
    print(json.dumps(json_response, indent=4))

CHOICES=(
        ("5","5 seconds"),
        ("10","10 seconds"),
        ("30","30 seconds"),
        ("40","40 seconds"),
    )

class PostForm(forms.Form):
    # seconds = forms.IntegerField()
    # content = forms.IntegerField(widget=forms.Textarea)

    seconds = forms.CharField(label="length", widget=forms.RadioSelect(choices=CHOICES))
    # if '10 seconds'==True:
    #     seconds = 

#from the urls code the code below is activated (bc of views.index)
def index(request):
    
    form = PostForm()
    context = {'form': form}
    if request.method == 'POST': 
        '''POST method and GET method
        Post method: transfer data/information to the program
        it is used to record the sentences submitted through the website
        then we save the recording as a file to transcribe it and move to the next steps
        the file is reset every time there is a new submission (= when the website reloads)
        '''
        form = PostForm(request.POST) # Note: 인자 순서주의 POST, FILES
        # record
        if form.is_valid():
            print(form.cleaned_data['seconds'])
            # record(form.cleaned_data['seconds']) 
            fiel = record(form.cleaned_data['seconds']) 
            # transcribe_file(fiel)
            result, acc = transcribe_file("file.wav")
            spell_check(result)
            context = {"text": result, "accuracy": acc}
            return render(request, 'listen_check/index.html', context)

        # record()
        result, acc = transcribe_file("file.wav")
        context = {"text": result, "accuracy": acc}
        return render(request, 'listen_check/index.html', context)
        
        # if request.POST:
        #     form = request.POST['geeks_field']
        #     print(form)
        #     return render(request, "index.html", context)
    # if request.method == "POST": 
    #     form = PostForm(request.POST) # PATCH, DELETE, UPDATE, 
    #     record(form.cleaned_data['seconds']) 
    #     result, acc = transcribe_file("file.wav")
    #     context = {"text": result, "accuracy": acc}
    #     return render(request, 'listen_check/index.html', context)


    elif request.method == "GET":
        '''
        The GET method uses urls to (blue) request a source
        it stays undisturbed unlike the POST method which resets every time there is a new input
        '''
        return render(request, 'listen_check/index.html', context)

        
    # elif request.method == "":
    #     if something == "tensec":
    #         return seconds
    #     elif something == "thirtysec":