from django import forms
import logging

log = logging.getLogger(__name__)

class TwitterUpdateForm(forms.Form):
    form_id = "TwitterUpdateForm"
    form_id = forms.CharField(widget=forms.HiddenInput(), max_length=100, required=False, initial=form_id)
