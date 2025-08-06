from django import forms
from .models import Rutina, Ejercicio

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre', 'descripcion', 'aporte_muscular']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'border rounded w-full p-2',
                'placeholder': 'Nombre del ejercicio'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'border rounded w-full p-2',
                'placeholder': 'Descripción del ejercicio'
            }),
            'aporte_muscular': forms.TextInput(attrs={
                'class': 'border rounded w-full p-2',
                'placeholder': 'Aporte muscular'
            }),
        }

class RutinaForm(forms.ModelForm):
    ejercicios = forms.ModelMultipleChoiceField(
        queryset=Ejercicio.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Rutina
        fields = ['nombre', 'descripcion', 'ejercicios']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'border rounded w-full p-2',
                'placeholder': 'Nombre de la rutina'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'border rounded w-full p-2',
                'placeholder': 'Descripción de la rutina'
            }),
        }
