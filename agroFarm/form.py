from django import forms

class SignupForm(forms.Form):
    first_name = forms.CharField(label='first_name', max_length='20',required=True)
    last_name = forms.CharField(label='last_name', max_length='20',required=True)
    username = forms.CharField(label='username', max_length='20',required=True)
    email = forms.EmailField(label='email', max_length='256',required=True)
    password = forms.DecimalField(label='password',widget=forms.PasswordInput, required=True)
    status = forms.CharField(label='status', max_length='20', required=True)
    
    