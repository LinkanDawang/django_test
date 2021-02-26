from django.db import models
from simplepro.components import fields


class BaseModel(models.Model):
    options1 = """
            {
                  shortcuts: [
                  {
                    text: '今天',
                    onClick(picker) {
                      picker.$emit('pick', new Date());
                    }
                  }, 
                  {
                    text: '昨天',
                    onClick(picker) {
                      const date = new Date();
                      date.setTime(date.getTime() - 3600 * 1000 * 24);
                      picker.$emit('pick', date);
                    }
                  }, 
                  {
                    text: '一周前',
                    onClick(picker) {
                      const date = new Date();
                      date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
                      picker.$emit('pick', date);
                    }
                  }]
                }
            """
    STATE_CHOICES = ((0, "无效"), (1, "有效"))
    create_time = fields.DateTimeField(
        options=options1, clearable=False,
        auto_now_add=True, verbose_name='创建时间'
    )
    update_time = fields.DateTimeField(
        options=options1, clearable=False, editable=False,
        auto_now=True, verbose_name='创建时间'
    )
    state = fields.RadioField(choices=STATE_CHOICES, verbose_name='单选框', default=0, help_text='只能选一个')
    # create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # update_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    # state = models.SmallIntegerField(choices=STATE_CHOICES, default=1)

    class Meta:
        abstract = True  # 抽象类,不生成数据表


class VirtualForeignKey(models.ForeignKey):
    """Virtual foreignkey which won't create concret relationship on database level."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("on_delete", models.DO_NOTHING)
        kwargs.setdefault("db_constraint", False)
        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)

