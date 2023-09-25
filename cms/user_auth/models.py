from django.db import models
from django.core.validators import RegexValidator,EmailValidator
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import jwt
import uuid
import re
from datetime import datetime,timedelta


def get_phone_regex():
    return RegexValidator(
        regex=r'^[6-9]\d{9}$', message=_(
            'Enter a valid phone number'
        )
    )


def validate_length(value):
    length = len(str(value))
    if length != 6:
        raise ValidationError(
            _('%(value)s is an invalid pincode')
        )

def get_password_regex(password):
    if re.fullmatch(r'[A-Za-z0-9]{8,}', password):
        return True
    return False

class userManager(UserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class role(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=15,null=False)    


class rootUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(max_length=254, validators=[EmailValidator], null=False)
    full_name =  models.CharField(max_length=125)
    phone = models.CharField(max_length=15, validators=[get_phone_regex()], null=False)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=125,null=True,blank=True)
    state = models.CharField(max_length=125,null=True,blank=True)
    country = models.CharField(max_length=125,null=True,blank=True)
    pincode = models.IntegerField(validators=[validate_length])
    role = models.ForeignKey(role,on_delete=models.CASCADE,null=False)
    
    objects = userManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    
    @property
    def token(self):
        token = jwt.encode(
            {'id': self.id.hex,
            'email': self.email,
            'phone': self.phone,
            'exp': datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY, algorithm='HS256')

        return token
                
    class Meta:
        db_table = 'root_users'
        
        
class userToken(models.Model):
    id = models.UUIDField(primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    authToken = models.CharField(max_length=256,null=True, blank=True)
    
    class Meta:
        db_table = 'root_users_token'