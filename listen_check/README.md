# django
**URL** 
- In the urls.py code, the django url path is imported
- 'Views' is imported (connects the urls.py with views.py)
- Then, using the path from django package, a page is created (with the same first part of the url) with an additional /'any_name' after the url given
- The page is then connected to the index function from views.py

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
- GET: blah... 
- POST: blah...

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