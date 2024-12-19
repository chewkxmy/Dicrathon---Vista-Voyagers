from django import forms
from django import forms

class FlightDetailsForm(forms.Form):
    from_location = forms.ChoiceField(
        choices=[
            ('KUL', 'Kuala Lumpur International Airport (KLIA & KLIA2)'),
            ('SZB', 'Sultan Abdul Aziz Shah Airport (Subang Airport)'),
            ('PEN', 'Penang International Airport'),
            ('JHB', 'Senai International Airport, Johor Bahru'),
            ('KBR', 'Sultan Ismail Petra Airport, Kota Bharu'),
            ('TGG', 'Sultan Mahmud Airport, Kuala Terengganu'),
            ('LGK', 'Langkawi International Airport'),
            ('AOR', 'Sultan Abdul Halim Airport, Alor Setar'),
            ('IPH', 'Sultan Azlan Shah Airport, Ipoh'),
            ('BKI', 'Kota Kinabalu International Airport'),
            ('KCH', 'Kuching International Airport'),
            ('MYY', 'Miri Airport'),
            ('SDK', 'Sandakan Airport'),
            ('TWU', 'Tawau Airport'),
            ('SBW', 'Sibu Airport'),
            ('BTU', 'Bintulu Airport'),
            ('LBU', 'Labuan Airport'),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'style': 'width: 100%; height: 52px; font-size: large;',
            'id': 'fromLocation'
        })
    )

    to_location = forms.ChoiceField(
        choices=[
            ('PEN', 'Penang International Airport'),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'style': 'width: 100%; height: 52px; font-size: large;',
            'id': 'toLocation'
        })
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Select start date',
            'style': 'height: 52px;',
            'id': 'startDate',
            'type': 'date'
        })
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Select end date',
            'style': 'height: 52px; font-size: large;',
            'id': 'endDate',
            'type': 'date'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        from_location = cleaned_data.get('from_location')
        to_location = cleaned_data.get('to_location')

        if from_location == to_location:
            self.add_error('to_location', 'The destination must be different from the departure location.')
