from django import forms
from .models import ExchangeProposal, STATUS_CHOICES


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'ad_sender': 'Выберите товар, который отдаете',
            'ad_receiver': 'Выберите товар, который хотите получить',
            'comment': 'Комментарий к предложению',
        }

