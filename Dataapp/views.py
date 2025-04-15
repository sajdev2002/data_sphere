from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BrowserHistory


# Create your views here.
def home(request):
    return render(request,'admin/admin_home.html')

def user(request):
    return render(request,'user/user_home.html')

def buss(request):
    return render(request,'bussiness/buss_home.html')

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
            return redirect('home')
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
            return redirect('home')
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

def add_survey(request):
    if request.method == 'POST':
        log = request.session['buss_id']
        logid = get_object_or_404(Login, id=log)  
        user = get_object_or_404(Bussines, login=logid) 
        form = SurveyForm(request.POST)
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
    questions = Survey.objects.filter(login=id)
    if 'quiz_progress' not in request.session or request.session.get('quiz_completed'):
        request.session['quiz_progress'] = {'question_index': 0}
        request.session['quiz_completed'] = False

    user_progress = request.session['quiz_progress']
    question_index = user_progress['question_index']

    if question_index >= len(questions):
        request.session['quiz_completed'] = True
        return redirect('survey_complete')

    current_question = questions[question_index]
    if UserSurvey.objects.filter(user=usr, survey=current_question).exists():
        return redirect('survey_complete')
    else:
        if request.method == 'POST':
            form = UserSurveyForm(request.POST, question=current_question)
            if form.is_valid():
                user_answer = form.save(commit=False)
                user_answer.survey = current_question
                user_answer.user = usr
                user_answer.option = form.cleaned_data['option']
                user_answer.save()
                user_progress['question_index'] += 1
                request.session['quiz_progress'] = user_progress
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

def add_education_detail(request):
    log = request.session['user_id']
    log_instance = get_object_or_404(User, id=log)  # Ensure you're using the correct field for lookup
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

def payment_transfer(request,id):
    jj = get_object_or_404(buss_data_request, id=id)
    var=jj.data_category
    row=jj.no_of_row
    amd=get_object_or_404(data_rate, data_category=var)
    amount=amd.amount*row
    if request.method == 'POST':
        log = request.session['buss_id']
        log_instance = get_object_or_404(Bussines, login_id=log)  
        form = PaymentForm(request.POST)

        if form.is_valid():
            var = form.save(commit=False)
            var.login = log_instance 
            var.save()

            jj.payment_status=1
            jj.save()
            return redirect('buss') 
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

def admin_data_tranfer(request, id):
    data_request = get_object_or_404(buss_data_request, id=id)
    data_request.transfer_status = 1
    data_request.save()
    data_transfer.objects.create(req_login=data_request)
    return redirect('../../admin_request_view') 

def buss_data_view(request, id):
    data_request = get_object_or_404(buss_data_request, id=id)
    data = None
    fields = []

    if data_request.data_category == 'Employee Details':
        data = EmployeeDetails.objects.filter(login_id=data_request.login_id)[:data_request.no_of_row]
        fields = ['ID', 'Department', 'Designation', 'Company Name', 'Salary', 'Location', 'Date of Joining', 'Reason to Leave Previous Company']
    elif data_request.data_category == 'Transaction Details':
        data = UploadedFile.objects.filter(login_id=data_request.login_id)[:data_request.no_of_row]
        fields = ['ID','Transaction ID', 'Date', 'Transaction Type', 'Amount', 'Payment Method', 'Merchant Name', 'Category']
    elif data_request.data_category == 'Education Details':
        data = EducationDetail.objects.filter(login_id=data_request.login_id)[:data_request.no_of_row]
        fields = ['ID','Degree Level', 'Degree Name', 'Institution', 'Year of Passing', 'Grade or Percentage']
    else:
        fields = ['No data available for this category']

    return render(request, 'bussiness/buss_data_view.html', {'data': data, 'fields': fields, 'data_category': data_request.data_category})
    
def add_opennion(request):
    log = request.session['user_id']
    log_instance = get_object_or_404(User, id=log)  
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

# @csrf_exempt
# def save_browser_history(request):
#     if request.method == 'POST':
#         # Parse the JSON data sent by the extension
#         username = request.POST.get('username')  
#         url = request.POST.get('url')
#         title = request.POST.get('title')

#         # Get the user and save the data
#         user = User.objects.get(username=username)
#         BrowserHistory.objects.create(user=user, url=url, title=title)

#         return JsonResponse({'status': 'success', 'message': 'Browser history saved successfully.'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})