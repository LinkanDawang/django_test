from django.db import models


class BaseModel(models.Model):
    STATE_CHOICES = ((0, "无效"), (1, "有效"))
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=1)

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

