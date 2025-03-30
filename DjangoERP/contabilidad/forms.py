from django import forms
from .models import AccountingAccount, CuentaContable

class AccountingAccountForm(forms.ModelForm):
    class Meta:
        model = AccountingAccount
        fields = '__all__'  # Or specify the fields you want to include
    
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        # You can also set the initial value of the company field here if needed
        # self.fields['company'].initial = self.company

class CuentaForm(forms.ModelForm):
    class Meta:
        model = CuentaContable
        fields = '__all__'
