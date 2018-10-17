from django import forms


class TestGeoSyntaxForm(forms.Form):
    query_text = forms.CharField(label='Текст запроса', widget=forms.Textarea)
    city_id = forms.ChoiceField(label='Город', choices=[])

    def set_cities_choices(self, cities):
        self.fields['city_id'].choices = [(city['id'], city['name']) for city in cities]


class TTSGenForm(forms.Form):
    query_text = forms.CharField(label='Текст запроса', widget=forms.Textarea)
