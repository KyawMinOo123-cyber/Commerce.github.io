from django import forms
from .models import AuctionItem,Category


class Create_Form(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = ['title','img_url','description','price']
        labels = {
            'title': 'Title',
            'img_url' : 'Image Url',
            'description' : 'Description',
            'price' : 'Price',
        }

        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control','required':True}),
            'img_url' : forms.TextInput(attrs={'class' : 'form-control','required':True}),
            'description' : forms.Textarea(attrs={'class' : 'from-control desc-form p-3','rows': 3,'cols': 100}),
            'price' : forms.TextInput(attrs={'class' : 'form-control','required':True,'maxlength':8,"pattern" :"\d*"})
        }