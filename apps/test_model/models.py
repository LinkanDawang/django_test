from apps.utils.model import BaseModel

from django.db import models


class StudentsInfoModel(BaseModel):
    GRADE_CHOICES = (
        (1, '一年级'),
        (2, '二年级'),
        (3, '三年级'),
        (4, '四年级'),
        (5, '五年级'),
        (6, '六年级'),
    )
    GENDER_CHOICES = (
        (0, '女性'),
        (1, '男性'),
        (2, 'others'),
    )

    name = models.CharField(max_length=10, verbose_name='学生姓名')
    grade = models.SmallIntegerField(choices=GRADE_CHOICES, default=0, verbose_name='年级')
    c_lass = models.SmallIntegerField(db_column='class', verbose_name='班级')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, verbose_name='性别')

    class Meta:
        db_table = 't_students'
        verbose_name = verbose_name_plural = '学生信息'

