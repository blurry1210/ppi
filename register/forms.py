from django import forms
from main.models import Author,Category
from django.core.exceptions import ValidationError

class UpdateForm(forms.ModelForm):
    
    class Meta:
        model = Author
        fields = ("fullname", "bio", "profile_pic")



class UpdateProfileForm(forms.ModelForm):
    chosen_categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  # Adjust the queryset as per your requirement
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Author
        fields = ['fullname', 'bio', 'profile_pic', 'chosen_categories']

    def clean_chosen_categories(self):
        categories = self.cleaned_data.get('chosen_categories')
        if categories and categories.count() != 2:
            raise ValidationError("Please select exactly 2 categories.")
        return categories