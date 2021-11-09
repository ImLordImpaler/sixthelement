from basic.models import Order , Item 
from django.forms import ModelForm


class NewItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ("name" ,"price" ,"category", "qty","flavour","img1" , "img2" , "img3","img4", 'img5','img6' ,'servings','instock','percent' )