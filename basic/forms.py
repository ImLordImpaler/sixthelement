from django.forms import ModelForm
from django import forms
from . models import *
STATE_CHOICES = (
   ("--","--"),
   ("AN","Andaman and Nicobar Islands"),
   ("AP","Andhra Pradesh"),
   ("AR","Arunachal Pradesh"),
   ("AS","Assam"),
   ("BR","Bihar"),
   ("CG","Chhattisgarh"),
   ("CH","Chandigarh"),
   ("DN","Dadra and Nagar Haveli"),
   ("DD","Daman and Diu"),
   ("DL","Delhi"),
   ("GA","Goa"),
   ("GJ","Gujarat"),
   ("HR","Haryana"),
   ("HP","Himachal Pradesh"),
   ("JK","Jammu and Kashmir"),
   ("JH","Jharkhand"),
   ("KA","Karnataka"),
   ("KL","Kerala"),
   ("LA","Ladakh"),
   ("LD","Lakshadweep"),
   ("MP","Madhya Pradesh"),
   ("MH","Maharashtra"),
   ("MN","Manipur"),
   ("ML","Meghalaya"),
   ("MZ","Mizoram"),
   ("NL","Nagaland"),
   ("OD","Odisha"),
   ("PB","Punjab"),
   ("PY","Pondicherry"),
   ("RJ","Rajasthan"),
   ("SK","Sikkim"),
   ("TN","Tamil Nadu"),
   ("TS","Telangana"),
   ("TR","Tripura"),
   ("UP","Uttar Pradesh"),
   ("UK","Uttarakhand"),
   ("WB","West Bengal")
)
PAYMENT_CHOICES = (
   ('COD' , 'Cash on Delivery'),
   ('Paytm' , 'Paytm'),
   ('Card' , 'Card'),
   
)
GENDER_CHOICES = (
    ('Male','Male'),
    ('Female','Female'),
)
class CheckoutForm(forms.Form):
   name=forms.CharField(max_length=1000)
   street_address = forms.CharField()
   phone = forms.CharField(max_length=10)
   state = forms.CharField(widget=forms.Select(choices=STATE_CHOICES))
   email = forms.EmailField(max_length=10000)

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(ModelForm):
   class Meta:
      model = Profile
      fields= ['phone' , 'birth_date', 'email' , 'gender']
      widgets = {
            'birth_date': DateInput(),
        }
   
class EnquiryForm(ModelForm):
   class Meta:
      model = Enquiry
      fields = "__all__"
   
   
