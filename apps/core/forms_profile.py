from django import forms
from .models_profile import ParentProfile, Child

class ParentProfileForm(forms.ModelForm):
    """Valideyn profil redaktə forması"""
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        label="Ad",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        label="Soyad",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyadınız'})
    )
    email = forms.EmailField(
        required=True, 
        label="E-poçt",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    
    class Meta:
        model = ParentProfile
        fields = ['phone']
        labels = {
            'phone': 'Telefon nömrəsi'
        }
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+994XX XXX XX XX'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            profile.save()
        return profile


class ChildForm(forms.ModelForm):
    """Uşaq əlavə etmə/redaktə forması"""
    class Meta:
        model = Child
        fields = ['name', 'birth_date']
        labels = {
            'name': 'Uşağın adı',
            'birth_date': 'Doğum tarixi'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uşağın adı'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
