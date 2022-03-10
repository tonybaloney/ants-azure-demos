"""
Tortoise Models
"""
from tortoise import fields
from tortoise.models import Model


class DBUser(Model):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=255, null=True)
    password = fields.CharField(max_length=128, null=True)

    class Meta:
        table="users"

    class PydanticMeta:
        exclude = ["password"]


class DBLocation(Model):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)
    private = fields.BooleanField(null=False, default=False)

    class Meta:
        table="locations"
