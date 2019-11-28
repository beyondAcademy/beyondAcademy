##default import
from django.db import models

##imageTest import
from django.urls import reverse



##user imports
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
# Create your models here.



##etc models
class BaseCode(models.Model):
    h_category = models.CharField(max_length=3)
    m_category = models.CharField(max_length=3)
    key = models.CharField(max_length=3)
    val = models.CharField(max_length=40)

    class Meta:
        managed = True
        unique_together = (('h_category', 'm_category', 'key'),)

##trade models
class TradeHeaderModel(models.Model):
    date = models.CharField(max_length=8)
    receipt_no = models.IntegerField()
    trade_type = models.CharField(max_length=3)
    take_price = models.IntegerField()
    give_price = models.IntegerField()
    take_currency = models.CharField(max_length=3)
    give_currency = models.CharField(max_length=3)
    take_user = models.IntegerField()
    give_user = models.IntegerField()
    trade_dttm_webserver = models.DateTimeField()
    trade_dttm_browser = models.DateTimeField()

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

class TradePerUserModel(models.Model):
    date = models.CharField(max_length=8)
    receipt_no = models.IntegerField()
    seq = models.IntegerField()
    user = models.IntegerField()
    trade_flag = models.CharField(max_length=3)
    currency = models.CharField(max_length=3)
    amount = models.IntegerField()
    trade_type = models.CharField(max_length=3)
    trade_dttm_webserver = models.DateTimeField()
    trade_dttm_browser = models.DateTimeField()

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

class TradePointModel(models.Model):
    date = models.CharField(max_length=8)
    receipt_no = models.IntegerField()
    seq = models.IntegerField()
    user = models.IntegerField()
    trade_type = models.CharField(max_length=3)
    cat_h_category = models.CharField(max_length=3)
    cat_m_category = models.CharField(max_length=3)
    cat_key = models.CharField(max_length=3)
    amount = models.IntegerField()
    trade_dttm_webserver = models.DateTimeField()
    trade_dttm_browser = models.DateTimeField()

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

class TradeRequestAnswerModel(models.Model):
    date = models.CharField(max_length=8)
    receipt_no = models.IntegerField()
    currency = models.CharField(max_length=3)
    amount = models.IntegerField()
    take_user = models.IntegerField()
    give_user = models.IntegerField()
    request_no = models.ForeignKey('QuestionRequest', models.DO_NOTHING)
    answer_no = models.ForeignKey('QuestionRequestAnswerModel', models.DO_NOTHING)
    trade_dttm_webserver = models.DateTimeField()
    trade_dttm_browser = models.DateTimeField()

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

# class TradeProposalAnswer(models.Model):
#     date = models.DateTimeField()
#     receipt_no = models.CharField(max_length=5)
#     currency = models.CharField(max_length=1)
#     amount = models.IntegerField()
#     take_user = models.ForeignKey('User', models.DO_NOTHING)
#     give_user = models.ForeignKey('User', models.DO_NOTHING)
#     proposal_id = models.ForeignKey()
#     feedback_id = models.ForeignKey()
#     answer_id = models.ForeignKey()
#     trade_dttm_webserver = models.DateTimeField()
#     trade_dttm_browser = models.DateTimeField()
#
#     delete_yn = models.CharField(default="N", max_length=1)
#     ins_dttm = models.DateTimeField(auto_now_add=True)
#     ins_user = models.CharField(max_length=20, default='ADMIN')
#     upt_dttm = models.DateTimeField(auto_now=True)
#     upt_user = models.CharField(max_length=20, default='ADMIN')

class TradeLiveinterviewSelectModel(models.Model):
    date = models.CharField(max_length=8)
    receipt_no = models.IntegerField()
    currency = models.CharField(max_length=3)
    amount = models.IntegerField()
    take_user = models.IntegerField()
    give_user = models.IntegerField()
    trade_dttm_webserver = models.DateTimeField()
    trade_dttm_browser = models.DateTimeField()

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

##liveinterview models
class LiveinterviewModel(models.Model):
    write_user = models.ForeignKey('User', models.DO_NOTHING)
    write_dttm = models.DateTimeField()
    title = models.CharField(max_length=50)
    content = models.TextField()
    currency = models.CharField(max_length=3)
    amount = models.IntegerField()
    duration = models.IntegerField(default=0)
    read_count = models.IntegerField(default=0)

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

class LiveinterviewCategoryModel(models.Model):
    interview_id = models.ForeignKey('LiveinterviewModel', models.DO_NOTHING)
    seq = models.IntegerField()
    cat_h_category = models.CharField(max_length=3)
    cat_m_category = models.CharField(max_length=3)
    cat_key = models.CharField(max_length=3)

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

class LiveinterviewReplyModel(models.Model):
    interview_id = models.ForeignKey('LiveinterviewModel', models.DO_NOTHING)
    seq = models.IntegerField()
    reply_user = models.ForeignKey('User', models.DO_NOTHING)
    reply_dttm = models.DateTimeField()

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

class LiveinterviewSelectListModel(models.Model):
    user_id = models.ForeignKey('User', models.DO_NOTHING)
    seq = models.IntegerField()
    interview_id = models.ForeignKey('LiveinterviewModel', models.DO_NOTHING)
    select_date = models.CharField(max_length=8)

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True, blank=True, null=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

##question models
####question request models
class QuestionRequest(models.Model):
    user_id = models.ForeignKey('User', models.DO_NOTHING)
    write_date_browser = models.CharField(max_length=8, blank=True, null=True)
    write_date_webserver = models.CharField(max_length=8, blank=True, null=True)
    content = models.TextField()
    finish_yn = models.CharField(default="N", max_length=1)

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')


class QuestionRequestCategory(models.Model):
    request_no = models.ForeignKey('QuestionRequest', models.DO_NOTHING)
    seq = models.IntegerField()
    cat_h_category = models.CharField(max_length=3)
    cat_m_category = models.CharField(max_length=3)
    cat_key = models.CharField(max_length=3)

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True, blank=True, null=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

    unique_together = (('request_no', 'seq'),)

class QuestionRequestAnswerModel(models.Model):
    request_no = models.ForeignKey('QuestionRequest', models.DO_NOTHING)
    seq = models.IntegerField()
    answer_user = models.ForeignKey('User', models.DO_NOTHING)
    write_date = models.CharField(max_length=8, blank=True, null=True)
    content = models.TextField()
    currency = models.CharField(max_length=3)
    amount = models.IntegerField()
    select_yn = models.CharField(default="N", max_length=1)
    select_date = models.CharField(max_length=8, blank=True, null=True)
    finish_yn = models.CharField(default="N", max_length=1)
    delete_yn = models.CharField(default="N", max_length=1)
    finish_yn = models.CharField(default="N", max_length=1)

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True, blank=True, null=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

class QuestionRequestAnswerSelectListModel(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    seq = models.IntegerField()
    answer = models.ForeignKey('QuestionRequestAnswerModel', models.DO_NOTHING)

    delete_yn = models.CharField(default="N", max_length=1)
    ins_dttm = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ins_user = models.CharField(max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(auto_now=True, blank=True, null=True)
    upt_user = models.CharField(max_length=20, default='ADMIN')

##Test Models
##User models
class UserManager(BaseUserManager):
    def create_user(self, username, password, last_name, email, phone, date_of_birth):
        user = self.model(
            username=username,
            last_name = last_name,
            email = self.normalize_email(email),
            phone = phone,
            date_of_birth = date_of_birth,
            date_joined = timezone.now(),
            is_superuser =0,
            is_staff = 0,
            is_active =1
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, last_name, email, phone, date_of_birth, password):
        user = self.create_user(
            username = username,
            password = password,
            last_name = last_name,
            email = email,
            phone = phone,
            date_of_birth = date_of_birth
        )

        user.is_superuser = 1
        user.is_staff = 1
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    password = models.CharField(max_length=128)
    username = models.CharField(unique=True, max_length=150)
    is_superuser = models.IntegerField()
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=254)
    date_of_birth = models.DateTimeField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)
    is_staff = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    credit = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['last_name', 'phone', 'email', 'date_of_birth']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'auth_user'




## test models
class Post(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()

    def __str__(self):
        return self.title



class imageTest(models.Model):
    image = models.ImageField(upload_to='%Y/%m/%d/orig', null=True)
    filtered_image = models.ImageField(upload_to='%Y/%m/%d/filtered', null=True)
    content = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        url = reverse('detail', kwargs={'pk': self.pk})
        return url
