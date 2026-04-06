from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre', 'apellido', 'fecha_nacimiento', 'genero',
            'telefono', 'email', 'direccion', 'contacto_emergencia',
            'certificado_medico', 'documento_adicional', 'tipo_inscripcion', 'curp',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'ClearableFileInput':
                field.widget.attrs.update({'class': 'form-control'})