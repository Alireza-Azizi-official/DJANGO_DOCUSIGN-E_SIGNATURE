from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Contract

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ContractForm(forms.ModelForm):
    signer_position = forms.CharField(
        max_length=255,
        required=False,
        label='Signer Position',
        widget=forms.TextInput(attrs={'placeholder': 'Enter signature location or leave as default'})
    )
        
    contract_name = forms.CharField(
        max_length=255, 
        required=True, 
        label="Contract Name"
    )

    start_date = forms.DateField(
        required=True,
        label="Start Date (Signature Date)",
        widget=forms.SelectDateWidget(years=range(2000, 2030))
    )

    end_date = forms.DateField(
        required=True,
        label="End Date (Signature Date)",
        widget=forms.SelectDateWidget(years=range(2000, 2030))
    )
    
    contract_text = forms.CharField(
        label="Contract Text",
        widget=forms.Textarea(attrs={
            'rows': 15,  
            'cols': 80, 
            'placeholder': 'Enter contract text here...'
        }),
        required=True
    )

    class Meta:
        model = Contract
        fields = [
            'recipient_email', 'contract_text', 'signer_position', 
            'contract_name', 'start_date', 'end_date', 'name_of_other_signer', 
            'email_of_other_signer'
        ]
