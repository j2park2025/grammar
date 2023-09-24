# django
**URL** 
- In the urls.py code, the django url path is imported
- 'Views' is imported (connects the [urls.py](./urls.py) with [views.py](./views.py))
- Then, using the path from django package, a page is created (with the same first part of the url) with an additional /'any_name' after the url given
- The page is then connected to the index function from [views.py](./views.py)

TODO: where is grammar from?
```python
from django.urls import path

from . import views

urlpatterns = [
    path('saved', views.index, name='index')
]
```
**VIEWS**
- From urls.py, index function is triggered
- POST: 
    - Usage: Transfer data/information to the program
    - Application: It is used to record the sentences submitted through the website. Then we save the recording as a file to transcribe it and continue to the next steps
    - *The file is reset every time there is a new submission (= when the website reloads)
    ```python
    if request.method == 'POST': 
        form = PostForm(request.POST) 
        if form.is_valid():
            print(form.cleaned_data['seconds'])
            fiel = record(form.cleaned_data['seconds']) 
            result, acc = transcribe_file("file.wav")
            spell_check(result)
            context = {"text": result, "accuracy": acc}
            return render(request, 'listen_check/index.html', context)
    ```
    - In the code above, when the POST method is triggered, the ```file.wav```, which is the recorded file of audio, is transcribed down using ```spell_check```. Then, the accuracy of the transcription along with the actual tanscription are saved in ```context```

- GET: 
    - Usage: The GET method uses urls to (blue) request a source
    - It stays undisturbed unlike the POST method which resets every time there is a new input
    - Application:
    ```python
    elif request.method == "GET":
        return render(request, 'listen_check/index.html', context)
    ```
    - The written code above is meant to activate the ```listen_check/index.html``` link



```python
def index(request):
    
    form = PostForm()
    context = {'form': form}
    if request.method == 'POST': 
        form = PostForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data['seconds'])
            fiel = record(form.cleaned_data['seconds']) 
            result, acc = transcribe_file("file.wav")
            spell_check(result)
            context = {"text": result, "accuracy": acc}
            return render(request, 'listen_check/index.html', context)

        result, acc = transcribe_file("file.wav")
        context = {"text": result, "accuracy": acc}
        return render(request, 'listen_check/index.html', context)

    elif request.method == "GET":
        return render(request, 'listen_check/index.html', context)   
```