from django import forms
from django.contrib.auth.models import User

from weblog.models import Blog, Author, Entry


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    logo = forms.FileField()


class UploadMultipleFilesForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'
