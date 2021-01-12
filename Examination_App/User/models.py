from django.db import models
# Create your models here.

# 用户信息表
class T_user_info(models.Model):
    user_id = models.CharField(primary_key=True,max_length=12)
    wechat_id = models.CharField(null=True,max_length=32)
    user_real_name = models.CharField(max_length=20,null=True)
    phone_number = models.CharField(default=0,null=False,unique=True,max_length=11)
    identity_card = models.CharField(null=False, unique=True, max_length=18,default=None)
    permission = models.CharField(null=False,max_length=1,default=0)
    login_state = models.CharField(null=False,max_length=1,default=0)
    registration_date = models.DateTimeField(null=False,default=None)



#购买状态表
class T_purchase_state(models.Model):
    purchase_state_id = models.CharField(primary_key=True,max_length=18)
    user = models.ForeignKey("User.T_user_info",
                                related_name="T_purchase_state_user_id",on_delete=models.DO_NOTHING,null=False,default=None)
    question_category = models.ForeignKey('Examination.T_question_category',
                                             related_name="T_purchase_state_question_category_id",
                                          on_delete=models.DO_NOTHING,null=False,default=None)
    expiry_date = models.DateField(auto_now=False,null=False,default=None)
    current_state = models.CharField(max_length=10,null=False,default='0')

class T_purchase_history(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User.T_user_info",
                                related_name="T_purchase_history_user_id",on_delete=models.DO_NOTHING,null=False,default=None)
    question_category = models.ForeignKey("Examination.T_question_category",
                                             related_name="T_purchase_history_question_category_id",
                                          on_delete=models.DO_NOTHING, null=False,default=None)
    purchase_date = models.DateField(auto_now=False,null=False,default=None)

#模拟答题信息表
class T_test_info(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_paper = models.ForeignKey("Examination.T_test_paper",
                                      related_name="test_paper",on_delete=models.DO_NOTHING,null=False,default=None)
    user = models.ForeignKey("T_user_info",
                                      related_name="user",on_delete=models.DO_NOTHING,null=False,default=None)
    question_category = models.ForeignKey("Examination.T_question_category",
                                      related_name="question_category",on_delete=models.DO_NOTHING,null=False,default=None)
    test_date = models.DateTimeField(null=False,default=None)
    score = models.CharField(max_length=3,null=False,default=None)