from django.db import models
from apps.utils.model import BaseModel, VirtualForeignKey
from django.contrib.postgres.fields import JSONField

# from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from simplecus.components import fields


class TestModel(models.Model):
    conf = models.CharField(max_length=50, null=True, blank=True, verbose_name='联系人信息')

    class Meta:
        verbose_name = verbose_name_plural = '表'
        db_table = "test_table"


class Test2Model(models.Model):
    conf = models.CharField(max_length=50, null=True, blank=True, verbose_name='联系人信息')

    class Meta:
        verbose_name = verbose_name_plural = '表'
        managed = False
        db_table = "test2_table"


class Supplier(BaseModel):
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name="名称")
    fname = models.CharField(max_length=128, null=True, blank=True, verbose_name="简称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "供应商表"
        managed = True
        db_table = "supplier"


def get_supplier_queryset():
    return Supplier.objects.order_by('-pk')[:10]


class UploadFile(BaseModel):
    TYPE_CHOICES = (
        (0, '全部'),
        (1, '小的'),
        (2, '大的'),
        (3, '长的'),
    )
    STATE_CHOICES = ((0, "无效"), (1, "有效"))
    school_choices = (
        (0, '北大'),
        (1, '清华'),
        (2, '复旦'),
        (3, '交大'),
        (4, '厦大'),
        (5, '深大'),
        (6, '中山大学'),
        (7, '东南大学'),
        (8, '南开大学'),
    )
    options1 = """
        {
              shortcuts: [{
                text: '今天',
                onClick(picker) {
                  picker.$emit('pick', new Date());
                }
              }, {
                text: '昨天',
                onClick(picker) {
                  const date = new Date();
                  date.setTime(date.getTime() - 3600 * 1000 * 24);
                  picker.$emit('pick', date);
                }
              }, {
                text: '一周前',
                onClick(picker) {
                  const date = new Date();
                  date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
                  picker.$emit('pick', date);
                }
              }]
            }
        """
    file = models.FileField(upload_to="upload/", null=True, blank=True, verbose_name="上传文件")
    file_temp = models.CharField(max_length=1024, verbose_name="文件路径")

    # 复选框字段
    category = fields.CheckboxField(
        max_length=12, choices=TYPE_CHOICES, default=0, help_text='我是提示', verbose_name="类别"
    )
    # 单选框字段
    # state = fields.RadioField(choices=STATE_CHOICES, verbose_name='单选框', default=0, help_text='只能选一个')
    # Switch字段
    isgood = fields.SwitchField(default=False, help_text='点我切换', verbose_name='切换')
    # Int输入框
    int_input = fields.InputNumberField(
        max_value=100, min_value=1, default=1,
        help_text='数字输入', verbose_name='InputNumber计数器'
    )
    # 滑动改变数值
    int_slide = fields.SliderField(
        # show_input 展示输入框
        show_input=True, max_value=100, min_value=1, step=1,
        input_size='large', show_tooltip=True, default=1,
        help_text='滑动改变数值', verbose_name='Slider滑块'
        )

    # 图片
    # file_icon = fields.ImageField(
    #     drag=True, action="/images",
    #     max_length=128, null=True, blank=True, verbose_name='图片上传'
    # )

    # 基础类型 int字段，如果有choices属性就会渲染成Select 没有就渲染成普通的输入框
    school = fields.IntegerField(verbose_name='学校', choices=school_choices, default=0)

    # 评分类型
    point = fields.RateField(max_value=5, allow_half=True, show_score=True, verbose_name='评分')

    str_input = fields.CharField(max_length=128, show_word_limit=True, verbose_name='输入框')
    supplier = fields.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True,
        help_text='选择一个人', clearable=True, placeholder='看什么',
        queryset=get_supplier_queryset,
        # 这里这里可以传入function，但是返回的必须是个queryset，也可以传入queryset
        limit=10,
    )

    class Meta:
        verbose_name = verbose_name_plural = "示例"
        managed = True
        db_table = "files"
