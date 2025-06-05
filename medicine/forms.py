from django import forms

from django import forms
from .models import Prescription
from django.contrib.auth import get_user_model

User = get_user_model()

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['doctor', 'description', 'file']

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        # Filter the doctor queryset to include only users with user_type='doctor'
        self.fields['doctor'].queryset = User.objects.filter(user_type='doctor')
