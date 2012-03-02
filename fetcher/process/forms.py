from django import forms

class UploadedFileForm(forms.Form):
    instance_num =  forms.IntegerField()
    file = forms.FileField()
