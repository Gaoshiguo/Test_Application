from django.db import models

# Create your models here.
#题目类型表
class T_question_type(models.Model):
    question_type_id = models.CharField(primary_key=True,max_length=1)
    question_type_name = models.CharField(null=False,max_length=10)
#题目类别表
class T_question_category(models.Model):
    question_category_id = models.CharField(primary_key=True,max_length=6)
    question_category_name = models.CharField(null=False,max_length=20)

#题目第一级别类别表
class T_category_one(models.Model):
    category_one_id = models.CharField(primary_key=True,max_length=2)
    category_one_name = models.CharField(null=False,max_length=20,default=" ")

#题目第二级别类别表
class T_category_two(models.Model):
    category_two_id = models.CharField(primary_key=True,max_length=2)
    category_two_name = models.CharField(null=False,max_length=20,default=" ")

#题目第三级别类别表
class T_category_three(models.Model):
    category_three_id = models.CharField(primary_key=True,max_length=2)
    category_three_name = models.CharField(null=False,max_length=20,default=" ")

#模拟试卷表
class T_test_paper(models.Model):
    test_paper_id = models.CharField(primary_key=True,max_length=8)
    test_paper_name = models.CharField(null=False,max_length=50,default=None)
    question_category = models.ForeignKey("T_question_category",related_name="T_test_paper_question_category_id",
                                             on_delete=models.DO_NOTHING,null=False,default=None)
#模拟答题信息表
class T_test_info(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_paper = models.ForeignKey("T_test_paper",
                                   related_name="T_test_info_test_paper",
                                      on_delete=models.CASCADE,null=False,default=None)
    user = models.ForeignKey("User.T_user_info",
                                related_name="T_test_info_user_id",on_delete=models.CASCADE,null=False,default=None)
    question_category = models.ForeignKey("T_question_category",
                                          related_name="T_test_info_question_category_id",
                                             on_delete=models.CASCADE,null=False,default=None)
    test_date = models.DateTimeField(null=False,default=None)
    score = models.IntegerField(null=False,default=None)
#题目信息表
class T_question_info(models.Model):
    # 题目编号
    question_id = models.AutoField(primary_key=True)
    # 题目难度
    question_difficulty = models.CharField(null=True,max_length=4)
    # 题目类别，外键约束于题目类型表
    question_category = models.ForeignKey("T_question_category",
                                          related_name="T_question_info_question_category_id",
                                             on_delete=models.DO_NOTHING,null=False,default=None)
    question_type = models.ForeignKey("T_question_type",
                                      related_name="T_question_info_question_type_id",
                                         on_delete=models.DO_NOTHING,null=False,default=None)
    test_paper = models.ForeignKey("T_test_paper",
                                   related_name="T_question_info_test_paper_id",
                                      on_delete=models.DO_NOTHING,null=False,default=None)
    question_content = models.TextField(null=False)
    right_option = models.CharField(max_length=4,null=False)
    option_A=models.TextField(null=False)
    option_B = models.TextField(null=False)
    option_C = models.TextField(null=True)
    option_D = models.TextField(null=True)
    option_E = models.TextField(null=True)
    option_F = models.TextField(null=True)
    question_analysis = models.TextField(null=True)


