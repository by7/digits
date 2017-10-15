from django.shortcuts import render
from django.http import HttpResponseRedirect
import re
import base64

from .forms import ImageForm

#def index(request):
#    return render(request, 'draw/index.html')

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
            ImageData = form.cleaned_data["draw_image"]
            print(ImageData)
            ImageData = dataUrlPattern.match(ImageData).group(2)
            print(ImageData)
            # If none or len 0, means illegal image data
            #if (ImageData == None or len(ImageData) == 0:
                # PRINT ERROR MESSAGE HERE
                #pass

            # Decode the 64 bit string into 32 bit and save
            with open("imageToSave.png", "wb") as fh:
                fh.write(base64.b64decode(ImageData))
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImageForm()

    return render(request, 'draw/index.html', {'form': form})