import uuid
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey




# Create your models here.
class Login(models.Model):
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    user_type=models.CharField(max_length=10)

class User(models.Model):
    name=models.CharField(max_length=100)
    contact_no=models.CharField(max_length=10)
    gender=models.CharField(max_length=10)
    uniq= models.CharField(max_length=20, unique=True, editable=False)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.uniq:  # Only generate if not already assigned
          self.uniq = self.generate_unique_mrnumber()
        super().save(*args, **kwargs)
    def generate_unique_mrnumber(self):
            """Generate a unique MR number"""
            while True:
                 new_mrnumber = f"DS-{uuid.uuid4().hex[:5].upper()}"  # Example: MR-AB12CD34E5
                 if not User.objects.filter(uniq=new_mrnumber).exists():
                     return new_mrnumber

class Bussines(models.Model):
    bussines_name=models.CharField(max_length=100)
    bussines_category=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    contact_no=models.CharField(max_length=10)
    status=models.IntegerField(default=0)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)

class Survey(models.Model):
    question=models.CharField(max_length=500)
    option1=models.CharField(max_length=100)
    option2=models.CharField(max_length=100)
    option3=models.CharField(max_length=100,null=True,blank=True)
    option4=models.CharField(max_length=100,null=True,blank=True)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)
    
class UserSurvey(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    survey=models.ForeignKey(Survey,on_delete=models.CASCADE)
    option=models.CharField(max_length=100)

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    dateee = models.DateField(default=now)
    transaction_type = models.CharField(max_length=100, default="0")
    amount = models.CharField(max_length=100, default="0") 
    payment_method = models.CharField(max_length=100, default="0")
    merchant_name = models.CharField(max_length=100, default="0")
    category = models.CharField(max_length=100,default=0)
    upload_date = models.DateField(default=now)
    status = models.IntegerField(default=0)
    login = models.ForeignKey(User, on_delete=models.CASCADE)

class ProductReview(models.Model):
    product_name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 5)])
    positive_feedback = models.TextField(blank=True, null=True) 
    negative_feedback = models.TextField(blank=True, null=True)
    suggestions = models.TextField(blank=True,null=True)
    login=models.ForeignKey(User, on_delete=models.CASCADE)
    login2=models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.product_name} - {self.model_number} - {self.rating}⭐"
    
class EmployeeDetails(models.Model):
    file=models.FileField(upload_to='employee_files/',null=True, blank=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100,default="0")
    salary = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    reason_to_leave_previous_company = models.TextField(blank=True, null=True)
    login=models.ForeignKey(User, on_delete=models.CASCADE,default=0)
    def __str__(self):
        return f"{self.designation} in {self.department}"
    


class EducationDetail(models.Model):
    DEGREE_LEVEL_CHOICES = [
        ('10th', '10th'),
        ('12th', '12th'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('Other', 'Other'),
    ]
    file=models.FileField(upload_to='education_files/',null=True, blank=True)
    degree_level = models.CharField(max_length=10, choices=DEGREE_LEVEL_CHOICES)
    degree_name = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    year_of_passing = models.PositiveIntegerField()
    grade_or_percentage = models.CharField(max_length=20)
    login=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.degree_name} from {self.institution} ({self.year_of_passing})"

class ProductOpinion(models.Model):
    product_type = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    about_product = models.TextField()
    suggesions = models.TextField()
    liked_features = models.TextField(blank=True, null=True)
    disliked_features = models.TextField(blank=True, null=True)
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(auto_now_add=True)

class data_rate(models.Model):
    data_category=models.CharField(max_length=100)
    amount=models.IntegerField()


class buss_data_request(models.Model):
    data_category = models.CharField(max_length=100)
    table_column = models.CharField(max_length=100, blank=True, null=True)
    table_value = models.CharField(max_length=100, blank=True, null=True)
    no_of_row = models.IntegerField()
    cancel_status = models.IntegerField(default=0)
    accept_status = models.IntegerField(default=0)
    current_date = models.DateField(default=now)
    login = models.ForeignKey(Bussines, on_delete=models.CASCADE)
    payment_status = models.IntegerField(default=0)
   



class data_transfer(models.Model):
    data_request = models.ForeignKey('buss_data_request', on_delete=models.CASCADE)
    business = models.ForeignKey(Bussines, on_delete=models.CASCADE,null=True, blank=True)   
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True, blank=True)
    object_id = models.PositiveIntegerField(default=0)
    viewed_object = GenericForeignKey('content_type', 'object_id')

    viewed_at = models.DateTimeField(default=now, null=True, blank=True)

    def __str__(self):
        return f"{self.business.bussines_name} viewed {self.content_type} #{self.object_id} on {self.viewed_at}"
    
class Bank(models.Model):
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20, unique=True)
    ifsc_code = models.CharField(max_length=11, unique=True)
    customer_name = models.CharField(max_length=100)
    cvv = models.CharField(max_length=3)
    expiry_date = models.CharField(max_length=7,null=True,blank=True) 
    total_balance = models.IntegerField(null=True, blank=True)

class Payment(models.Model):
    card_no=models.IntegerField()
    name_card=models.CharField(max_length=100)
    expiry_date=models.CharField(max_length=10)
    cvv=models.IntegerField()
    amount=models.IntegerField()
    login=models.ForeignKey(Bussines,on_delete=models.CASCADE)
    current_date = models.DateField(default=now)

class UserWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

class chatmodel(models.Model):
    sender = models.IntegerField()
    receiver = models.IntegerField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

#image extract
class Transaction(models.Model):
    file = models.FileField(upload_to='ai_extract/')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    dateee = models.DateField(default=now)
    transaction_type = models.CharField(max_length=100, default="0")
    amount = models.CharField(max_length=100, default="0") 
    payment_method = models.CharField(max_length=100, default="0")
    merchant_name = models.CharField(max_length=100, default="0")
    category = models.CharField(max_length=100, default="0")
    upload_date = models.DateField(default=now)
    status = models.IntegerField(default=0)
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    


class BrowserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    title = models.CharField(max_length=255, blank=True, null=True) 
    url = models.URLField()  
    visited_at = models.DateTimeField(auto_now_add=True)
