from django import forms

from .models import User, Lawyer, Counsel, CounselAnswer

from .models import User, Lawyer, Counsel, Inquiry


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'user_email',
            'user_password',
            'user_name',
            'user_nickname',
            'user_birthday',
            'user_mobile'
        )


class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = (
            'lawyer_email',
            'lawyer_password',
            'lawyer_name',
            'lawyer_birthday',
            'lawyer_mobile',
            'lawyer_gender',
            'lawyer_license_num',
            'lawyer_license_year',
            'lawyer_status_date'
        )


class SearchForm(forms.ModelForm):
    category = forms.CharField
    sub_keyword = forms.CharField
    keyword = forms.CharField


class CounselForm(forms.ModelForm):
    class Meta:
        model = Counsel
        fields = (
            'category_sub_idx',
            'sido_idx',
            'counsel_title',
            'counsel_contents'
        )

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = (
            'title',
            'content',
            'mobile',
            'name',
            'email'
        )


class CounselAnswerForm(forms.ModelForm):
    class Meta:
        model = CounselAnswer
        fields = (
        'counsel_answer_title',
        'counsel_answer_contents'
        )
