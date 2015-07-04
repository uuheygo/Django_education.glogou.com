from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)