from django.shortcuts import render
from django.http import HttpResponseRedirect
import re
import base64

import tensorflow as tf
import numpy as np

from .forms import ImageForm

def index(request):
    #initiallize predictions
    y_list = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
            ImageData = form.cleaned_data["draw_image"]
            ImageData = dataUrlPattern.match(ImageData).group(2)

            # Decode the 64 bit string into 32 bit
            y_list = predict_number(base64.b64decode(ImageData))[0].tolist()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImageForm()

    return render(request, 'draw/index.html', {'form': form, 'y_list': y_list})

def predict_number(ImageData):
    sess=tf.Session()
    
    # Load meta graph and restore weights
    saver = tf.train.import_meta_graph('deep_model/deep_model.meta')
    saver.restore(sess,tf.train.latest_checkpoint('./deep_model/'))

    # Load placeholders variables and create feed-dict to feed new data
    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    keep_prob = graph.get_tensor_by_name("dropout/keep_prob:0")

    # Convert ImageData to TensorFlow image
    image = tf.image.decode_png(ImageData, channels=1)
    
    # Process image to fit MNIST parameters
    #image = tf.transpose(image, [1, 0, 2])
    image = tf.image.rgb_to_grayscale(tf.image.resize_images(image,[28,28]))
    image = tf.reshape(image, [1, 784]).eval(session=sess)
    image = 1-(image/255)
    
    feed_dict ={x: image, keep_prob: 1.0}

    # Now, access the op that predicts the values
    y_conv = graph.get_tensor_by_name("fc2/y_conv:0")

    pred = sess.run(tf.nn.softmax(y_conv),feed_dict)
    return pred