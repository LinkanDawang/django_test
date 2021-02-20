from django.db import models


class VirtualForeignKey(models.ForeignKey):
    """Virtual foreignkey which won't create concret relationship on database level."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("on_delete", models.DO_NOTHING)
        kwargs.setdefault("db_constraint", False)
        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)