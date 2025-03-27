from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'admin_home.html')

def user(request):
    return render(request,'user_home.html')

def buss(request):
    return render(request,'buss_home.html')

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
    return render(request, 'register.html', {'user_form': user_form, 'login_form': login_form})

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
    return render(request, 'buss_registration.html', {'buss_form': buss_form, 'login_form': login_form})

def datatable(request):
    users = User.objects.all()
    return render(request, 'datatable.html', {'users': users})

def datatable_buss(request):
    var = Bussines.objects.all()
    return render(request, 'datatable_buss.html', {'var': var})

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
    return render(request,'user_prof_update.html',{'form':form,'form2':form2})
    
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
    return render(request,'user_prof_update.html',{'form':form,'form2':form2})

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
    return render(request, 'buss_survey.html', {'form': form})

def survey_view(request):
    log=request.session['buss_id']
    users = Survey.objects.filter(login_id=log)
    return render(request, 'buss_survey_view.html', {'users': users})

def survey_edit(request, id):
    user=get_object_or_404(Survey, id=id)    
    if request.method=='POST':
        form=SurveyForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('survey_view')
    else:
        form=SurveyForm(instance=user)
    return render(request,'buss_survey_edit.html',{'form':form})

def survey_delete(request, id):
    user=get_object_or_404(Survey, id=id)
    user.delete()
    return redirect('survey_view')

def select_bussiness(request):
    surveys = Survey.objects.all()
    business_ids = surveys.values_list('login_id', flat=True)  
    businesses = Bussines.objects.filter(login_id__in=business_ids)  
    return render(request, 'admin_view_sur_company.html', {'buss': businesses})

def admin_survey(request, id):
    users = Survey.objects.filter(login_id=id)
    return render(request, 'admin_survey_view.html', {'users': users})

def select_bussiness_user(request):
    surveys = Survey.objects.all()
    business_ids = surveys.values_list('login_id', flat=True)  
    businesses = Bussines.objects.filter(login_id__in=business_ids)  
    return render(request, 'user_sur_buss_view.html', {'buss': businesses})


def user_survey(request, id):
        userid=request.session['user_id']
        usr=get_object_or_404(User, login=userid)
        sur=get_object_or_404(Bussines, login=id)
        user_progress=request.session.get('quiz_progress',{'question_index':0})
        question_index=user_progress['question_index']
        questions=Survey.objects.filter(login=id)
        if question_index >= len(questions):
                request.session['quiz_completed']=True
                return redirect('survey_complete')
   
        current_question=questions[question_index]
        if request.method=='POST':
            form=UserSurveyForm(request.POST,question=current_question)
            if form.is_valid():
                user_answer=form.save(commit=False)
                user_answer.survey=current_question
                user_answer.user=usr
                user_answer.option=form.cleaned_data['option']
                user_answer.save()
                user_progress['question_index']+=1
                request.session['quiz_progress']=user_progress
                return redirect('user_survey',id=id)

        else:
            form=UserSurveyForm(question=current_question)
        return render(request, 'user_survey_view.html', {'form':form,'question':current_question})

def survey_complete(request):
    return render(request,'survey_complete.html')