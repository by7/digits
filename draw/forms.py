from django import forms

class ImageForm(forms.Form):
    draw_image = forms.CharField(max_length=40000)