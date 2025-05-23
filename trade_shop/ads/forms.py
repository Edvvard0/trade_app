from django import forms

from ads.models import CONDITION_CHOICES, Ad


class AdCreateForm(forms.Form):
    title = forms.CharField(label='Название объявления',
                               widget=forms.TextInput())
    description = forms.CharField(label='Описание',
                               widget=forms.TextInput())
    image_url = forms.CharField(label='Ссылка на изображение',
                               widget=forms.TextInput(), required=False)
    category = forms.CharField(label='Категория',
                               widget=forms.TextInput())
    condition = forms.ChoiceField(label='Состояние',
                                  choices=CONDITION_CHOICES)


class AdUpdateForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название'}),
            'description': forms.Textarea(attrs={'placeholder': 'Опишите товар', 'rows': 5}),
            'image_url': forms.TextInput(attrs={'placeholder': 'Вставьте URL изображения (опционально)'}),
        }
