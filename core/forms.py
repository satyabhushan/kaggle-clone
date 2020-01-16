from django import forms
from .models import Competition


class HostCompetitionForm(forms.ModelForm):
    required_css_class = 'form-data'

    class Meta:
        model = Competition
        fields = (
            "title",
            "brief",
            "description",
            # "start_time",
            # "end_time",
            "train_csv",
            "train_solution_csv",
            "test_csv",
            "test_solution_csv",
            "hidden_test_csv",
            "hidden_test_solution_csv",
        )

    def __init__(self, *args, **kwargs):
        super(HostCompetitionForm, self).__init__(*args, **kwargs)
        # self.fields['end_time'].initial = 'Infinite'
        # self.fields['end_time'].validators = [validate_end]
        self.fields['description'].widget = forms.Textarea()
        
