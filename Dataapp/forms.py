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
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Select your date of birth',
        })
    )
    contact_no = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your contact number',
        })
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your city',
        })
    )
    state = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your state',
        })
    )
    country = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your country',
        })
    )

    class Meta:
        model = User
        fields = ['name', 'gender', 'dob', 'contact_no', 'city', 'state', 'country']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
        }
        labels = {
            'dob': 'Date of Birth',
            'contact_no': 'Contact Number',
        }

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Login
        fields = ['email', 'password']

class BussinesForm(forms.ModelForm):
    class Meta:
        model = Bussines
        fields = ['bussines_name', 'bussines_category', 'address', 'district', 'city', 'contact_no']
        widgets = {
            'bussines_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your business name',
                'style': 'font-size: 16px;',
            }),
            'bussines_category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your business category',
                'style': 'font-size: 16px;',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your business address',
                'style': 'resize: none; font-size: 14px;',
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your district',
                'style': 'font-size: 14px;',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city',
                'style': 'font-size: 14px;',
            }),
            'contact_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your contact number',
                'style': 'font-size: 14px;',
            }),
        }
        labels = {
            'bussines_name': 'Business Name',
            'bussines_category': 'Business Category',
            'address': 'Business Address',
            'district': 'District',
            'city': 'City',
            'contact_no': 'Contact Number',
        }

class login_form(forms.Form):
    email=forms.EmailField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput())

class EmailForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
        })
    )

    class Meta:
        model = Login
        fields = ['email']
        labels = {
            'email': 'Email Address',
        }

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['question', 'option1', 'option2', 'option3', 'option4']
        widgets = {
            'question': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter the survey question here...',
                'style': 'resize: none; font-size: 16px;',
            }),
            'option1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option 1',
                'style': 'font-size: 14px;',
            }),
            'option2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option 2',
                'style': 'font-size: 14px;',
            }),
            'option3': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option 3',
                'style': 'font-size: 14px;',
            }),
            'option4': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option 4',
                'style': 'font-size: 14px;',
            }),
        }
        labels = {
            'question': 'Survey Question',
            'option1': 'First Option',
            'option2': 'Second Option',
            'option3': 'Third Option',
            'option4': 'Fourth Option',
        }

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
        fields = [
            'file', 
            'department', 
            'designation', 
            'company_name', 
            'salary', 
            'location', 
            'date_of_joining', 
            'reason_to_leave_previous_company'
        ]
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'border: 2px solid #ced4da; padding: 10px;',
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your department',
                'style': 'font-size: 14px; border-radius: 5px;',
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your designation',
                'style': 'font-size: 14px; border-radius: 5px;',
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your company name',
                'style': 'font-size: 14px; border-radius: 5px;',
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your salary',
                'style': 'font-size: 14px; border-radius: 5px;',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your location',
                'style': 'font-size: 14px; border-radius: 5px;',
            }),
            'date_of_joining': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'font-size: 14px; border-radius: 5px;',
            }),
            'reason_to_leave_previous_company': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Explain your reason for leaving the previous company',
                'style': 'resize: none; font-size: 14px; border-radius: 5px;',
            }),
        }
        labels = {
            'file': 'Upload File',
            'department': 'Department',
            'designation': 'Designation',
            'company_name': 'Company Name',
            'salary': 'Salary',
            'location': 'Location',
            'date_of_joining': 'Date of Joining',
            'reason_to_leave_previous_company': 'Reason for Leaving Previous Company',
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

    class Meta:
        model = buss_data_request
        fields = ['data_category', 'table_column', 'table_value', 'no_of_row']
        widgets = {
            'data_category': forms.Select(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            'no_of_row': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'style': 'width: 95%;'}),
            'table_value': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            'table_column': forms.Select(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_category'].choices = [
            (rate.data_category, rate.data_category) for rate in data_rate.objects.all()
        ]
        if 'table_column' in self.data:
            selected_column = self.data.get('table_column')
            self.fields['table_column'].choices = [(selected_column, selected_column)]
        else:
            self.fields['table_column'].choices = []


class ProductOpinionForm(forms.ModelForm):
    product_type = forms.ChoiceField(
        choices=trans_categ,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'font-size: 14px; border-radius: 5px;',
        })
    )

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
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product name',
                'style': 'font-size: 14px; border-radius: 5px;',
            }),
            'about_product': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts about the product',
                'style': 'resize: none; font-size: 14px; border-radius: 5px;',
            }),
            'suggesions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Provide your suggestions',
                'style': 'resize: none; font-size: 14px; border-radius: 5px;',
            }),
            'liked_features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'What features did you like?',
                'style': 'resize: none; font-size: 14px; border-radius: 5px;',
            }),
            'disliked_features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'What features did you dislike?',
                'style': 'resize: none; font-size: 14px; border-radius: 5px;',
            }),
        }
        labels = {
            'product_type': 'Product Type',
            'product_name': 'Product Name',
            'about_product': 'About the Product',
            'suggesions': 'Suggestions',
            'liked_features': 'Liked Features',
            'disliked_features': 'Disliked Features',
        }

class chatmodelform(forms.ModelForm):
    class Meta:
        model = chatmodel
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }

class UploadInvoiceForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['file']

class TransactionEditForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['login', 'upload_date', 'status', 'file']