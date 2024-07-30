from django import forms

class SignupForm(forms.form):
    username = forms.CharField(label='username', max_length='20',required=True)
    firstName = forms.CharField(label='firstName', max_length='20',required=True)
    lastName = forms.CharField(label='lastName', max_length='20',required=True)
    is_staff = forms.CharField(label='is_staff', max_length='20',required=True)
    is_superuser = forms.CharField(label='is_superuser', max_length='20',required=True)
    email = forms.EmailField(label='mail', max_length='20',required=True)
    mobileNumber = forms.DecimalField(label='monileNumber',max_digits=10,decimal_places=0, required=True)
    