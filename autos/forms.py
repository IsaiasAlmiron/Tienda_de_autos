from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'phone', 'address', 'password1', 'password2')

class CustomUserEditForm(forms.ModelForm):
    """Formulario para editar usuarios (sin cambiar contraseña aquí)"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'})
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección', 'rows': 3})
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='¿Usuario activo?'
    )
    is_staff = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='¿Puede acceder al panel admin?'
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'address', 'is_active', 'is_staff')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    
    def clean_email(self):
        """Validar que el email sea único (excepto el del usuario que se edita)"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email