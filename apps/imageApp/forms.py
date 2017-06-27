from django import forms

class ImageUploadForm(forms.Form):
    # name = forms.CharField(max_length=200)
    # description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(label='image')
    #
    # def clean_message(self):
    #     name = self.cleaned_data['name']
    #     description = self.cleaned_data['description']
    #     if len(name) < 4:
    #         raise forms.ValidationError("Not enough characters in the name!!")
    #     if len(description) < 4:
    #         raise forms.ValidationError("Not enough characters in the description!!")
    #     return name
