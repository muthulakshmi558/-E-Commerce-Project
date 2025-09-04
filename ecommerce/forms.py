from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'textarea'}))
