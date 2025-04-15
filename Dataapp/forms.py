from django import forms
from .models import *
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]
trans_categ = [
    ('gadget', 'Gadget'),
    ('vehicle', 'Vehicle'),
    ('shopping', 'Shopping'),
    ('travel', 'Travel'),
    ('food', 'Food'),
    ('entertainment', 'Entertainment'),
    ]
class UserForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    class Meta:
        model=User
        fields= ['name', 'gender', 'dob', 'contact_no', 'city', 'state', 'country']

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Login
        fields = ['email', 'password']

class BussinesForm(forms.ModelForm):
    class Meta:
        model=Bussines
        fields=['bussines_name','bussines_category','address','district','city','contact_no']

class login_form(forms.Form):
    email=forms.EmailField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput())

class EmailForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['email']

class SurveyForm(forms.ModelForm):
    class Meta:
        model=Survey
        fields=['question','option1','option2','option3','option4']

class UserSurveyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(UserSurveyForm,self).__init__(*args, **kwargs)
        self.fields['option']=forms.ChoiceField(choices=[
            ('option1',question.option1),
            ('option2',question.option2),
            ('option3',question.option3),
            ('option4',question.option4),
        ],widget=forms.RadioSelect)
    class Meta:
        model=UserSurvey
        fields=['option']

class UploadFileForm(forms.ModelForm):
    trans_CHOICES = [
    ('purchase', 'Purchase'),
    ('refund', 'Refund'),
    ('subscription', 'Subscription'),
    ('donation', 'Donation'),
    ]
    payment_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('debit_card', 'Debit Card'),
    ('paypal', 'PayPal'),
    ('upi', 'UPI'),
    ('crypto', 'Cryptocurrency'),
    ]
    
    transaction_type = forms.ChoiceField(choices=trans_CHOICES)
    payment_method = forms.ChoiceField(choices=payment_CHOICES)
    category = forms.ChoiceField(choices=trans_categ)
    class Meta:
        model = UploadedFile
        fields = ['file', 'transaction_id', 'dateee', 'transaction_type', 'amount', 'payment_method', 'merchant_name', 'category']

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['product_name', 'model_number', 'rating', 'positive_feedback', 'negative_feedback', 'suggestions']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i+1} Stars') for i in range(1, 5)]),
            'positive_feedback': forms.Textarea(attrs={'rows': 3}),
            'negative_feedback': forms.Textarea(attrs={'rows': 3}),
            'suggestions': forms.Textarea(attrs={'rows': 3}),}
        
class EmployeeDetailsForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = ['file','department', 'designation','company_name','salary','location', 'date_of_joining', 'reason_to_leave_previous_company']
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'reason_to_leave_previous_company': forms.Textarea(attrs={'rows': 3}),
        }

class EducationDetailForm(forms.ModelForm):
    class Meta:
        model = EducationDetail
        fields = ['degree_level', 'degree_name', 'institution', 'year_of_passing', 'grade_or_percentage','file']
        widgets = {
            'degree_level': forms.Select(attrs={'class': 'form-control'}),
            'degree_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. B.Sc Computer Science'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. XYZ University'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 2099}),
            'grade_or_percentage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 85% or A+'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model=Payment
        fields=['card_no', 'name_card', 'expiry_date', 'cvv', 'amount']

class data_rate_form(forms.ModelForm):
    class Meta:
        model = data_rate
        fields = ['data_category', 'amount']
        widgets = {
            'data_category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Data Category',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Amount',
                'min': 0,
                'step': 10,
            }),
        }
        labels = {
            'data_category': 'Data Category',
            'amount': 'Amount (in USD)',
        }
        
class buss_data_request_form(forms.ModelForm):
    data_category = forms.ChoiceField(choices=[]) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_category'].choices = [
            (rate.data_category, rate.data_category) for rate in data_rate.objects.all()
        ]

    class Meta:
        model = buss_data_request
        fields = ['data_category', 'no_of_row']
        widgets = {
            'data_category': forms.Select(attrs={'class': 'form-control'}),
            'no_of_row': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class ProductOpinionForm(forms.ModelForm):
    product_type = forms.ChoiceField(choices=trans_categ, widget=forms.Select())

    class Meta:
        model = ProductOpinion
        fields = [
            'product_type',
            'product_name',
            'about_product',
            'suggesions',
            'liked_features',
            'disliked_features',
        ]
        widgets = {
            'about_product': forms.Textarea(attrs={'rows': 3}),
            'suggesions': forms.Textarea(attrs={'rows': 3}),
            'liked_features': forms.Textarea(attrs={'rows': 2}),
            'disliked_features': forms.Textarea(attrs={'rows': 2}),
        }