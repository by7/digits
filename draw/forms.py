from django import forms

class ImageForm(forms.Form):
    draw_image = forms.CharField(max_length=2000, widget = forms.HiddenInput())