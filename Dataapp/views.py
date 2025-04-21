from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.utils.timezone import localtime
from datetime import date

import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd
from django.conf import settings
import matplotlib
matplotlib.use('Agg') 

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BrowserHistory

from django.db.models import Sum
from django.db.models import Q
# Create your views here.
def home(request):
    return render(request,'admin/admin_home.html')

def user(request):
    log = request.session['user_id']
    log_instance = get_object_or_404(Login, id=log)
    login_user = get_object_or_404(User, login=log_instance)
    user_wallet, _ = UserWallet.objects.get_or_create(user=login_user, defaults={'balance': 0})

    return render(request, 'user/user_home.html', {
        'user': login_user,
        'user_wallet': user_wallet,
    })
  
def buss(request):
    return render(request,'bussiness/buss_home.html')


#register
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        login_form = LoginForm(request.POST)
        if user_form.is_valid() and login_form.is_valid():
            login_instance = login_form.save(commit=False)
            login_instance.user_type = 'user'
            login_instance.save()
            user_instance = user_form.save(commit=False)
            user_instance.login = login_instance
            user_instance.save()
            return redirect('login')
    else:
        user_form = UserForm()
        login_form = LoginForm()
    return render(request, 'user/register.html', {'user_form': user_form, 'login_form': login_form})

def buss_register(request):
    if request.method == 'POST':
        buss_form = BussinesForm(request.POST)
        login_form = LoginForm(request.POST)
        if buss_form.is_valid() and login_form.is_valid():
            login_instance = login_form.save(commit=False)
            login_instance.user_type = 'bussines'
            login_instance.save()
            buss_instance = buss_form.save(commit=False)
            buss_instance.login = login_instance
            buss_instance.save()
            return redirect('login')
    else:
        buss_form = BussinesForm()
        login_form = LoginForm()
    return render(request, 'bussiness/buss_registration.html', {'buss_form': buss_form, 'login_form': login_form})


def datatable(request):
    users = User.objects.all()
    return render(request, 'admin/datatable.html', {'users': users})

def datatable_buss(request):
    var = Bussines.objects.all()
    return render(request, 'admin/datatable_buss.html', {'var': var})

def buss_accept(request, id): 
    user=get_object_or_404(Bussines, id=id)
    user.status=1
    user.save()
    return redirect('datatable_buss')

def buss_reject(request, id):
    user=get_object_or_404(Bussines, id=id) 
    user.status=2
    user.save() 
    return redirect('datatable_buss')

#login
def login(request):
    if request.method == 'POST':
        form = login_form(request.POST)  # Instantiate the form with POST data
        if form.is_valid():  # Validate the form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Login.objects.get(email=email)
                if user.password == password:
                    if user.user_type == 'bussines' and Bussines.objects.get(login=user).status == 1:
                        request.session['buss_id'] = user.id
                        request.session['email'] = user.email
                        return redirect('buss')
                    elif user.user_type == 'user':
                        request.session['user_id'] = user.id
                        request.session['email'] = user.email
                        return redirect('user')
                    elif user.user_type=='admin':
                        return redirect('home')
                else:
                    messages.error(request, 'Password is incorrect')
            except Login.DoesNotExist:
                messages.error(request, 'Email is incorrect')
    else:
        form = login_form()  # Instantiate an empty form for GET requests
    return render(request, 'login_home.html', {'form': form})


#profile updation
def update_user(request):
    log=request.session['user_id']
    logid=get_object_or_404(Login,id=log)
    user=get_object_or_404(User,login=logid)    
    if request.method=='POST':
        form=UserForm(request.POST,instance=user)
        form2=EmailForm(request.POST,instance=logid)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('user')
    else:
        form=UserForm(instance=user)
        form2=EmailForm(instance=logid)
    return render(request,'user/user_prof_update.html',{'form':form,'form2':form2})
    
def update_buss(request):
    log=request.session['buss_id']
    logid=get_object_or_404(Login,id=log)
    user=get_object_or_404(Bussines,login=logid)    
    if request.method=='POST':
        form=BussinesForm(request.POST,instance=user)
        form2=EmailForm(request.POST,instance=logid)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('user')
    else:
        form=BussinesForm(instance=user)
        form2=EmailForm(instance=logid)
    return render(request,'bussiness/buss_profile_update.html',{'form':form,'form2':form2})

#survey
def add_survey(request):
    if request.method == 'POST':
        log = request.session['buss_id']
        logid = get_object_or_404(Login, id=log)  
        user = get_object_or_404(Bussines, login=logid) 
        form = SurveyForm(request.POST)
        print(form)
        if form.is_valid():
            var = form.save(commit=False)
            var.login = logid  
            var.save()
            return redirect('buss')
    else:
        form = SurveyForm()
    return render(request, 'bussiness/buss_survey.html', {'form': form})

def survey_view(request):
    log=request.session['buss_id']
    users = Survey.objects.filter(login_id=log)
    return render(request, 'bussiness/buss_survey_view.html', {'users': users})

def survey_edit(request, id):
    user=get_object_or_404(Survey, id=id)    
    if request.method=='POST':
        form=SurveyForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('survey_view')
    else:
        form=SurveyForm(instance=user)
    return render(request,'bussiness/buss_survey_edit.html',{'form':form})

def survey_delete(request, id):
    user=get_object_or_404(Survey, id=id)
    user.delete()
    return redirect('survey_view')

def select_bussiness(request):
    surveys = Survey.objects.all()
    business_ids = surveys.values_list('login_id', flat=True)  
    businesses = Bussines.objects.filter(login_id__in=business_ids)  
    return render(request, 'admin/admin_view_sur_company.html', {'buss': businesses})

def admin_survey(request, id):
    users = Survey.objects.filter(login_id=id)
    return render(request, 'admin/admin_survey_view.html', {'users': users})

def select_bussiness_user(request):
    surveys = Survey.objects.all()
    business_ids = surveys.values_list('login_id', flat=True)  
    businesses = Bussines.objects.filter(login_id__in=business_ids)  
    return render(request, 'user/user_sur_buss_view.html', {'buss': businesses})

def user_survey(request, id):
    userid = request.session.get('user_id')
    usr = get_object_or_404(User, login_id=userid)

    # Get all survey questions for this login (business)
    all_questions = Survey.objects.filter(login=id)

    # Filter out only those questions the user has not yet answered
    unanswered_questions = [q for q in all_questions if not UserSurvey.objects.filter(user=usr, survey=q).exists()]

    if not unanswered_questions:
        request.session['quiz_completed'] = True
        return redirect('survey_complete')

    # Always work with the first unanswered question
    current_question = unanswered_questions[0]

    if request.method == 'POST':
        form = UserSurveyForm(request.POST, question=current_question)
        if form.is_valid():
            user_answer = form.save(commit=False)
            user_answer.survey = current_question
            user_answer.user = usr
            user_answer.option = form.cleaned_data['option']
            user_answer.save()
            return redirect('user_survey', id=id)
    else:
        form = UserSurveyForm(question=current_question)

    return render(request, 'user/user_survey_view.html', {'form': form, 'question': current_question})

def survey_complete(request):
    return render(request,'survey_complete.html')

def thank(request):
    return render(request,'thank_you.html')

def survey_view_buss(request):
    log = request.session['buss_id']
    users = Survey.objects.filter(login_id=log)
    res = UserSurvey.objects.filter(survey__in=users).select_related('user', 'survey')
    grouped_responses = {}
    for response in res:
        user_name = response.user.uniq 
        if user_name not in grouped_responses:
            grouped_responses[user_name] = []
        grouped_responses[user_name].append(response.option)  

    return render(request, 'bussiness/buss_sur_res.html', {'grouped_responses': grouped_responses})

def survey_result_admin(request):
    survey_ids = UserSurvey.objects.values_list('survey_id', flat=True)
    users = Survey.objects.filter(id__in=survey_ids)
    res = UserSurvey.objects.filter(survey__in=users).select_related('user', 'survey')
    grouped_responses = []

    for response in res:
        user_id = response.user.id
        business_id = response.survey.login.id
        option = response.option

        # Check if a row with the same user_id and business_id already exists
        existing_row = next((row for row in grouped_responses if row['user_id'] == user_id and row['business_id'] == business_id), None)

        if existing_row:
            existing_row['options'].append(option)
        else:
            grouped_responses.append({
                'user_id': user_id,
                'business_id': business_id,
                'options': [option]
            })

    return render(request, 'admin/admin_survey_result.html', {'grouped_responses': grouped_responses})


#transaction data collection
def upload_file(request):
    if request.method == 'POST':
        log = request.session['user_id']
        log_instance = get_object_or_404(Login, id=log) 
        user_instance = get_object_or_404(User, login=log_instance)  
        form = UploadFileForm(request.POST, request.FILES)
        print
        if form.is_valid():
            var = form.save(commit=False)
            var.login = user_instance  
            var.save()
            return redirect('../user/') 
    else:
        form = UploadFileForm()
    return render(request, 'user/user_data_entry.html', {'form': form})

def admin_transaction_view(request):
    users = UploadedFile.objects.all()
    return render(request, 'admin/admin_tran_details.html', {'users': users})

def admin_review_view(request):
    users = ProductReview.objects.all()
    return render(request, 'admin/admin_review_view.html', {'users': users})

def admin_trans_accept(request, id): 
    user=get_object_or_404(UploadedFile, id=id)
    user.status=1
    user.save()
    return redirect('admin/admin_transaction_view')

def admin_trans_reject(request, id):
    user=get_object_or_404(UploadedFile, id=id) 
    user.status=2
    user.save() 
    return redirect('admin/admin_transaction_view')

def user_transaction_view(request):
    log=request.session['user_id']
    var=get_object_or_404(User,login_id=log)
    users=UploadedFile.objects.filter(login_id=var)
    return render(request,'user/user_trans_view.html',{'users':users})

def tran_del(request,id):
    log=get_object_or_404(UploadedFile,id=id)
    log.delete()
    return redirect('user_transaction_view')

def tran_edit(request,id):
    log=get_object_or_404(UploadedFile,id=id)
    if request.method=='POST':
        form=UploadFileForm(request.POST,request.FILES,instance=log)
        if form.is_valid():
            form.save()
            return redirect('user_transaction_view')
    else:
        form=UploadFileForm(instance=log)
    return render(request,'user/user_trans_view_up.html',{'form':form})


#review data collect
def review_product(request):
    id=request.session['user_id']
    log=get_object_or_404(User,login_id=id)
    users=UploadedFile.objects.filter(login_id=log)
    return render(request,'user/user_review_product.html',{'users':users})  

def review_add(request,id):
    log=get_object_or_404(UploadedFile,id=id)
    var=request.session['user_id']
    log1=get_object_or_404(User,login_id=var)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            inn=form.save(commit=False)
            inn.rating+=1
            inn.login=log1
            inn.login2=log
            inn.save()
            return redirect('../../thank/')
    else:
        form = ProductReviewForm()
    return render(request, 'user/reviewwww.html', {'form': form})

def user_review_view(request):
    log=request.session['user_id']
    var=get_object_or_404(User,login_id=log)
    users=ProductReview.objects.filter(login_id=var)
    return render(request,'user/user_review_view.html',{'users':users})

def review_del(request,id):
    log=get_object_or_404(ProductReview,id=id)
    log.delete()
    return redirect('../../user_review_view/')

def review_edit(request,id):
    log=get_object_or_404(ProductReview,id=id)
    if request.method=='POST':
        form=ProductReviewForm(request.POST,instance=log)
        if form.is_valid():
            form.save()
            return redirect('../../user_review_view/')
    else:
        form=ProductReviewForm(instance=log)
    return render(request,'user/user_review_edit.html',{'form':form})


#employee details
def add_employee_details(request):
    log = request.session['user_id']
    log_instance = get_object_or_404(User,login_id=log)
    if request.method == 'POST':
        form = EmployeeDetailsForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            doo=form.save(commit=False) 
            doo.login = log_instance
            doo.save() 
            return redirect('user/')  
    else:
        form = EmployeeDetailsForm()
    return render(request, 'user/employee_details.html', {'form': form})

def employ_details_view(request):
    log=request.session['user_id']
    var=get_object_or_404(User,login_id=log)
    users=EmployeeDetails.objects.filter(login_id=var)
    return render(request,'user/employ_detils_view.html',{'users':users})

def emp_del(request,id):
    log=get_object_or_404(EmployeeDetails,id=id)
    log.delete()
    return redirect('../../employ_details_view/')

def emp_edit(request, id):
    log = get_object_or_404(EmployeeDetails, id=id)
    if request.method == 'POST':
        form = EmployeeDetailsForm(request.POST, request.FILES, instance=log)
        if form.is_valid():
            form.save()
            return redirect('employ_details_view')  # Use named URL pattern for better maintainability
    else:
        form = EmployeeDetailsForm(instance=log)
    return render(request, 'user/employee_detail_edit.html', {'form': form})


#education details
def add_education_detail(request):
    log = request.session['user_id']
    log_instance = get_object_or_404(User, login_id=log)  
    if request.method == 'POST':
        form = EducationDetailForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            doo = form.save(commit=False)
            doo.login = log_instance
            doo.save()
            return redirect('../user/') 
    else:
        form = EducationDetailForm()
    return render(request, 'user/education_details.html', {'form': form})

def education_details_view(request):
    log=request.session['user_id']
    var=get_object_or_404(User,login_id=log)
    users=EducationDetail.objects.filter(login_id=var)
    return render(request,'user/education_details_view.html',{'users':users})

def edu_del(request,id):
    log=get_object_or_404(EducationDetail,id=id)
    log.delete()
    return redirect('../../education_details_view/')

def edu_edit(request,id):
    log=get_object_or_404(EducationDetail,id=id)
    if request.method=='POST':
        form=EducationDetailForm(request.POST,request.FILES,instance=log)
        if form.is_valid():
            form.save()
            return redirect('../../education_details_view/')
    else:
        form=EducationDetailForm(instance=log)
    return render(request,'user/edu_details_edit.html',{'form':form})


#opinion details
def add_opennion(request):
    log = request.session['user_id']
    log_instance = get_object_or_404(User, login_id=log)  
    if request.method == 'POST':
        form = ProductOpinionForm(request.POST)
        if form.is_valid():
            doo = form.save(commit=False)
            doo.login = log_instance
            doo.save()
            return redirect('../user/') 
    else:
        form = ProductOpinionForm()
    return render(request, 'user/openinion_details.html', {'form': form})

def opinion_details_view(request):
    log=request.session['user_id']
    var=get_object_or_404(User,login_id=log)
    users=ProductOpinion.objects.filter(login_id=var)
    return render(request,'user/openinion_details_view.html',{'users':users})

def opinion_del(request,id):
    log=get_object_or_404(ProductOpinion,id=id)
    log.delete()
    return redirect('../../opinion_details_view/')

def opinion_edit(request,id):
    log=get_object_or_404(ProductOpinion,id=id)
    if request.method=='POST':
        form=ProductOpinionForm(request.POST,request.FILES,instance=log)
        if form.is_valid():
            form.save()
            return redirect('../../opinion_details_view/')
    else:
        form=ProductOpinionForm(instance=log)
    return render(request,'user/openinion_details_edit.html',{'form':form})


#admin view
def admin_employee_view(request):
    users = EmployeeDetails.objects.all()
    return render(request, 'admin/admin_employee.html', {'users': users})

def admin_edu_view(request):
    users = EducationDetail.objects.all()
    return render(request, 'admin/admin_edu.html', {'users': users})

def admin_opinion_view(request):
    users = ProductOpinion.objects.all()
    return render(request, 'admin/admin_opinion.html', {'users': users})


#payment
def payment_transfer(request, id):
    jj = get_object_or_404(buss_data_request, id=id)
    var = jj.data_category
    row = jj.no_of_row
    amd = get_object_or_404(data_rate, data_category=var)
    amount = amd.amount * row

    if request.method == 'POST':
        log = request.session.get('buss_id')
        log_instance = get_object_or_404(Bussines, login_id=log)  
        form = PaymentForm(request.POST)

        if form.is_valid():
            card_no = form.cleaned_data['card_no']
            name_card = form.cleaned_data['name_card']
            expiry_input = form.cleaned_data['expiry_date']
            cvv = form.cleaned_data['cvv']

            # Validate expiry_input
            if not expiry_input:
                messages.error(request, "Expiry date is required.")
                return render(request, 'payment.html', {'form': form, 'amount': amount})

            # Check expiry format MM/YY
            try:
                expiry_date = datetime.strptime(expiry_input, "%m/%y").date().replace(day=1)
            except ValueError:
                messages.error(request, "Invalid expiry date format. Use MM/YY.")
                return render(request, 'payment.html', {'form': form, 'amount': amount})

            try:
               
                bank = Bank.objects.get(
                    card_number=card_no,
                    cvv=cvv
                )

                if bank.customer_name != name_card:
                    messages.error(request, "Customer name does not match.")
                    return render(request, 'payment.html', {'form': form, 'amount': amount})

                # if bank.expiry_date != expiry_input:
                #     messages.error(request, "Expiry date does not match.")
                #     return render(request, 'payment.html', {'form': form, 'amount': amount})

            except Bank.DoesNotExist:
                messages.error(request, "Bank details not found or incorrect.")
                return render(request, 'payment.html', {'form': form, 'amount': amount})

            if bank.total_balance < amount:
                messages.error(request, "Insufficient balance.")
                return render(request, 'payment.html', {'form': form, 'amount': amount})

            # Deduct amount
            bank.total_balance -= amount
            bank.save()

            # Save payment
            payment = form.save(commit=False)
            payment.login = log_instance
            payment.current_date = now()
            payment.save()

            # Update request status
            jj.payment_status = 1
            jj.save()

            messages.success(request, "Payment successful.")
            return redirect('../../buss_data_request_view')
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'form': form, 'amount': amount})

def admin_rate_set(request):
    if request.method == 'POST':
        form = data_rate_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../home')
    else:
        form = data_rate_form()
    return render(request, 'admin/admin_data_rate.html', {'form': form})

def admin_rate_view(request):
    users = data_rate.objects.all()
    return render(request, 'admin/admin_rate_view.html', {'users': users})

def admin_rate_edit(request,id):
    log=get_object_or_404(data_rate,id=id)
    if request.method=='POST':
        form=data_rate_form(request.POST,instance=log)
        if form.is_valid():
            form.save()
            return redirect('../admin_rate_view/')
    else:
        form=data_rate_form(instance=log)
    return render(request,'admin/admin_rate_edit.html',{'form':form})


#data request
def bussiness_data_request(request):
    log = request.session['buss_id']
    log_instance = get_object_or_404(Bussines, login_id=log)
    if request.method == 'POST':
        form = buss_data_request_form(request.POST)
        if form.is_valid():
            doo = form.save(commit=False)
            doo.login = log_instance
            doo.save()
            return redirect('buss')  
    else:
        form = buss_data_request_form()
    return render(request, 'bussiness/busss_data_request.html', {'form': form})

def get_category_columns(request):
    category = request.GET.get('category')
    columns = []

    if category == 'Employee Details':
        columns = ['Department', 'Designation', 'Company Name', 'Salary', 'Location']
    elif category == 'Transaction Details':
        columns = ['Date', 'Transaction Type', 'Amount', 'Payment Method', 'Merchant Name', 'Category']
    elif category == 'Education Details':
        columns = [ 'Degree Level', 'Degree Name', 'Institution', 'Year of Passing', 'Grade or Percentage']
    elif category == 'Product Review':
        columns = ['Product Name', 'Model Number', 'Rating']
    elif category == 'User Data':
        columns = ['Gender', 'DOB', 'City', 'State', 'Country']
    elif category == 'Openion':
        columns = ['Product type', 'Product Name']

    return JsonResponse({'columns': columns})

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

DEGREE_LEVEL_CHOICES = [
    ('10th', '10th'),
    ('12th', '12th'),
    ('UG', 'Undergraduate'),
    ('PG', 'Postgraduate'),
    ('Other', 'Other'),
]

def get_column_choices(request):
    column = request.GET.get('column')
    choices = []

    if column == 'Transaction Type':
        choices = trans_CHOICES
    elif column == 'Payment Method':
        choices = payment_CHOICES
    elif column == 'Category':
        choices = trans_categ
    elif column == 'Degree Level':
        choices = DEGREE_LEVEL_CHOICES
    elif column == 'Gender':
        choices = GENDER_CHOICES

    return JsonResponse({'choices': choices})

column_mapping = {
    'Date': 'dateee',
    'Transaction Type': 'transaction_type',
    'Amount': 'amount',
    'Merchant Name': 'merchant_name',
    'Payment Method': 'payment_method',
    'Category': 'category',

    'Product Name': 'product_name',
    'Model Number': 'model_number',
    'Rating': 'rating',

    'Department': 'department',
    'Designation': 'designation',
    'Company Name': 'company_name',
    'Salary': 'salary',
    'Location': 'location',

    'Degree Level': 'degree_level',
    'Degree Name': 'degree_name',
    'Institution': 'institution',
    'Year of Passing': 'year_of_passing',
    'Grade or Percentage': 'grade_or_percentage',

    'Gender': 'gender',
    'DOB': 'dob',
    'City': 'city',
    'State': 'state',
    'Country': 'country',
    'Product type': 'product_type'
}

def get_available_row_count(request):
    category = request.GET.get('category')
    column = request.GET.get('column')
    value = request.GET.get('value')
    model = None

    # Match category to model
    if category == 'Transaction Details':
        model = UploadedFile
    elif category == 'Employee Details':
        model = EmployeeDetails
    elif category == 'Education Details':
        model = EducationDetail
    elif category == 'Product Review':
        model = ProductReview
    elif category == 'Openion':
        model = ProductOpinion
    elif category == 'User Data':
        model = User

    if not model:
        return JsonResponse({'count': 0})

    # Exclude already purchased
    content_type = ContentType.objects.get_for_model(model)
    bought_ids = data_transfer.objects.filter(content_type=content_type).values_list('object_id', flat=True)
    queryset = model.objects.exclude(id__in=bought_ids)

    # Apply filter
    if column and value:
        model_field = column_mapping.get(column)
        if model_field:
            filter_kwargs = {f"{model_field}__iexact": value}
            queryset = queryset.filter(**filter_kwargs)

    count = queryset.count()
    return JsonResponse({'count': count})

def buss_data_request_view(request):
    log=request.session['buss_id']
    log_instance = get_object_or_404(Bussines, login_id=log)
    users = buss_data_request.objects.filter(login_id=log_instance)
    return render(request, 'bussiness/buss_data_req_view.html', {'users': users})

def request_cancel(request,id):
    log=get_object_or_404(buss_data_request,id=id)
    log.cancel_status=1
    log.save()
    return redirect('../../buss_data_request_view/')

def admin_request_view(request):
    users = buss_data_request.objects.all()
    return render(request, 'admin/admin_buss_req_view.html', {'users': users})

def admin_request_accept(request, id): 
    user=get_object_or_404(buss_data_request, id=id)
    user.accept_status=1
    user.save()
    return redirect('../../admin_request_view')

#preview
def buss_trans_preview(request):
    users = UploadedFile.objects.all()
    total_rows = users.count()  # Calculate the total number of rows
    return render(request, 'bussiness/buss_transaction_prev.html', {'users': users, 'total_rows': total_rows})

def buss_review_preview(request):
    users = ProductReview.objects.all()
    total_rows = users.count()  # Calculate the total number of rows
    return render(request, 'bussiness/buss_review_prev.html', {'users': users, 'total_rows': total_rows})


#chart
def survey_view_chart(request):
    log=request.session['buss_id']
    users = Survey.objects.filter(login_id=log)
    return render(request, 'bussiness/survey_chart.html', {'users': users})

def survey_results(request, id):
    chart_type = request.GET.get('chart', 'bar')  

    survey = Survey.objects.get(id=id)
    responses = UserSurvey.objects.filter(survey=survey)

    counts = {
        'option1': responses.filter(option='option1').count(),
        'option2': responses.filter(option='option2').count(),
        'option3': responses.filter(option='option3').count(),
        'option4': responses.filter(option='option4').count(),
    }

    labels = []
    values = []
    if survey.option1:
        labels.append(survey.option1)
        values.append(counts['option1'])
    if survey.option2:
        labels.append(survey.option2)
        values.append(counts['option2'])
    if survey.option3:
        labels.append(survey.option3)
        values.append(counts['option3'])
    if survey.option4:
        labels.append(survey.option4)
        values.append(counts['option4'])

    df = pd.DataFrame({'Option': labels, 'Votes': values})

    # Plot generation
    plt.figure(figsize=(8, 5))
    sns.set_style("whitegrid")

    if chart_type == 'bar':
        sns.barplot(data=df, x='Option', y='Votes', hue='Option', palette='Blues_d', legend=False)
    elif chart_type == 'line':
        sns.lineplot(data=df, x='Option', y='Votes', marker='o')
    elif chart_type == 'pie':
        plt.pie(values, labels=labels, autopct='%1.1f%%', colors=sns.color_palette('Blues_d'))
        plt.axis('equal')  # Pie chart is a circle

    plt.title(survey.question)
    if chart_type != 'pie':
        plt.ylabel('Number of Votes')
        plt.xlabel('Options')

    chart_path = os.path.join(settings.MEDIA_ROOT, f'survey_{id}.png')
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    chart_url = settings.MEDIA_URL + f'survey_{id}.png'

    return render(request, 'bussiness/survey_results_chart.html', {
        'survey': survey,
        'chart_url': chart_url,
    })


#wallet
def buss_data_view(request, id):
    data_request = get_object_or_404(buss_data_request, id=id)
    business = data_request.login
    num_rows = data_request.no_of_row

    model_class = None
    fields = []

    # Mapping UI labels to actual model fields
    column_mapping = {
        'Date': 'dateee',
        'Transaction Type': 'transaction_type',
        'Amount': 'amount',
        'Merchant Name': 'merchant_name',
        'Payment Method': 'payment_method',
        'Category': 'category',

        'Product Name': 'product_name',
        'Model Number': 'model_number',
        'Rating': 'rating',

        'Department': 'department',
        'Designation': 'designation',
        'Company Name': 'company_name',
        'Salary': 'salary',
        'Location': 'location',
        
        'Degree Level': 'degree_level',
        'Degree Name': 'degree_name',
        'Institution': 'institution',
        'Year of Passing': 'year_of_passing',
        'Grade or Percentage': 'grade_or_percentage',
        
        'Product type': 'product_type',
        'Product Name': 'product_name',
       
        'Gender': 'gender',
        'DOB': 'dob',
        'City': 'city',
        'State': 'state',
        'Country': 'country',
    }

    if data_request.data_category == 'Employee Details':
        model_class = EmployeeDetails
        fields = ['ID', 'Department', 'Designation', 'Company Name', 'Salary', 'Location', 'Date of Joining', 'Reason to Leave Previous Company']

    elif data_request.data_category == 'Transaction Details':
        model_class = UploadedFile
        fields = ['ID', 'Transaction ID', 'Date', 'Transaction Type', 'Amount', 'Payment Method', 'Merchant Name', 'Category']

    elif data_request.data_category == 'Education Details':
        model_class = EducationDetail
        fields = ['ID', 'Degree Level', 'Degree Name', 'Institution', 'Year of Passing', 'Grade or Percentage']

    elif data_request.data_category == 'Product Review':
        model_class = ProductReview
        fields = ['ID', 'Product Name', 'Model Number Type', 'Rating', 'Positive Feedback', 'Negative Feedback', 'Suggestions']

    else:
        return render(request, 'bussiness/buss_data_view.html', {
            'data': [],
            'fields': ['No data available for this category'],
            'data_category': data_request.data_category
        })

    content_type = ContentType.objects.get_for_model(model_class)

    # Start filtering
    filter_kwargs = {}
    column_ui = data_request.table_column
    column_value = data_request.table_value

    if column_ui in column_mapping and column_value:
        model_field = column_mapping[column_ui]
        filter_kwargs[model_field] = column_value

    # Check if this request already has stored records
    already_viewed = data_transfer.objects.filter(
        business=business,
        data_request=data_request,
        content_type=content_type
    ).order_by('id')

    if already_viewed.exists():
        object_ids = already_viewed.values_list('object_id', flat=True)
        data = model_class.objects.filter(id__in=object_ids)
    else:
        all_viewed_ids = data_transfer.objects.filter(
            business=business,
            content_type=content_type
        ).values_list('object_id', flat=True)

        query = model_class.objects.exclude(id__in=all_viewed_ids)
        if filter_kwargs:
            query = query.filter(**filter_kwargs)

        data = query.order_by('id')[:num_rows]

        for item in data:
            transfer = data_transfer.objects.create(
                business=business,
                data_request=data_request,
                content_type=content_type,
                object_id=item.id
            )
            update_user_wallet(transfer)

    return render(request, 'bussiness/buss_data_view.html', {
        'data': data,
        'fields': fields,
        'data_category': data_request.data_category
    })

def update_user_wallet(transfer):
    content_model = transfer.content_type.model_class()
    model_name = content_model.__name__
    obj = content_model.objects.get(id=transfer.object_id)
    user_obj1=obj.login
    usr=user_obj1.id
    data_category = transfer.data_request.data_category
    rate_obj = data_rate.objects.filter(data_category=data_category).first()
    amount = rate_obj.amount
    user_instance = get_object_or_404(User, id=usr) 
    print(user_instance)
    wallet, created = UserWallet.objects.get_or_create(user=user_instance, defaults={'balance': 0})
    wallet.balance += amount
    wallet.save()

def user_wallet_view(request):
    log = request.session['user_id']
    log_instance = get_object_or_404(Login, id=log)
    login_user = get_object_or_404(User, login=log_instance)

    user_wallet, created = UserWallet.objects.get_or_create(user=login_user, defaults={'balance': 0})
    
    user_transfers = data_transfer.objects.all()
    category_earnings = {}

    for transfer in user_transfers:
        if not transfer.content_type:
            continue

        content_model = transfer.content_type.model_class()
        try:
            obj = content_model.objects.get(id=transfer.object_id)
            if obj.login == login_user:
                category = transfer.data_request.data_category
                rate_obj = data_rate.objects.filter(data_category=category).first()
                if rate_obj:
                    if category not in category_earnings:
                        category_earnings[category] = 0
                    category_earnings[category] += rate_obj.amount
        except content_model.DoesNotExist:
            continue

    return render(request, 'user/wallet_view.html', {
        'user_wallet': user_wallet,
        'user': login_user,
        'category_earnings': category_earnings,
    })


#chat

def chat(request):
    user_id = request.session.get('buss_id')
    admin = Login.objects.get(user_type='admin')

    # Fetch chat messages between user and admin
    messages = chatmodel.objects.filter(
        sender__in=[user_id, admin.id],
        receiver__in=[user_id, admin.id]
    ).order_by('timestamp')

    chat_data = []
    for msg in messages:
        local_timestamp = localtime(msg.timestamp)  # Convert to local time
        if local_timestamp.date() == date.today():
            display_time = local_timestamp.strftime("%I:%M %p, Today")
        else:
            display_time = local_timestamp.strftime("%I:%M %p, %b %d")

        chat_data.append({
            'message': msg.message,
            'sender': 'You' if msg.sender == user_id else 'Admin',
            'timestamp': display_time  # Pass the formatted timestamp
        })

    context = {
        'messages': chat_data,
        'today': date.today()
    }

    return render(request, 'bussiness/chat_set.html', context)

def send_message(request):
    if request.method == 'POST':
        user_id = request.session.get('buss_id')
        admin = Login.objects.get(user_type='admin')
        message = request.POST.get('message')

        new_chat = chatmodel.objects.create(
            sender=user_id,
            receiver=admin.id,
            message=message
        )

        # Get local timestamp
        local_timestamp = localtime(new_chat.timestamp)
        current_date = date.today()

        if local_timestamp.date() == current_date:
            display_time = local_timestamp.strftime("Today, %I:%M %p")
        else:
            display_time = local_timestamp.strftime("%b %d, %I:%M %p")

        return JsonResponse({
            'message': new_chat.message,
            'timestamp': display_time,
            'sender': 'You'
        })
    
def admin_chat_buss(request):
    return render(request, 'admin/chat_buss.html')



#brower
def save_browser_history(request):
    if request.method == 'POST':
        # Parse the JSON data sent by the extension
        username = request.POST.get('username')  
        url = request.POST.get('url')
        title = request.POST.get('title')

        # Get the user and save the data
        user = User.objects.get(username=username)
        BrowserHistory.objects.create(user=user, url=url, title=title)

        return JsonResponse({'status': 'success', 'message': 'Browser history saved successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})