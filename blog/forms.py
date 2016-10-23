from django import forms

from .models import Post, Utente

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class UserForm(forms.ModelForm):
    class Meta:
        model = Utente
        fields = [ 'nome_utente', 'password']
