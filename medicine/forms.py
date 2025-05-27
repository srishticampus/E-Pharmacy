from django import forms
from .models import Prescription

class PrescriptionUploadForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['uploaded_file']

    def clean_uploaded_file(self):
        file = self.cleaned_data.get('uploaded_file')
        if file:
            if not file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf')):
                raise forms.ValidationError('Unsupported file format.')
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size exceeds 5MB.')
        return file
