from distutils.debug import DEBUG
from secrets import choice
from signal import raise_signal
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.forms import MultipleChoiceField

from django.core.validators import RegexValidator

from bases.models import TimeStampBase



class UserManager(BaseUserManager):

    def create_user(self, email, password):
        
        if not email:
            raise ValueError('must have user email.')
        if not password:
            raise ValueError('must have user password.')
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        
        user = self.create_user(
            email = self.normalize_email(email),
            password= password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,TimeStampBase):
    email = models.EmailField(verbose_name='email address',unique=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



class Profile(TimeStampBase):
    """
        first name
        Last name
        gender
        address
        city
        state
        zipcode
        pay account
        user - foreign key
    """
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    GENDER_CHOICES = (
        (0,'female'),
        (1,'male'),
        (2,'Opt out')
    )
    gender = models.IntegerField(choices=GENDER_CHOICES,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)

    STATE_CHOICES=(
    ('AL','Alabama'),
    ('AK','Alaska'),
    ('AZ','Arizona'),
    ('AR','Arkansas'),
    ('CA','California'),
    ('CO','Colorado'),
    ('CT','Connecticut'),
    ('DE','Delaware'),
    ('FL','Florida'),
    ('GA','Georgia'),
    ('HI','Hawaii'),
    ('ID','Idaho'),
    ('IL','Illinois'),
    ('IN','Indiana'),
    ('IA','Iowa'),
    ('KS','Kansas'),
    ('KY','Kentucky'),
    ('LA','Louisiana'),
    ('ME','Maine'),
    ('MD','Maryland'),
    ('MA','Massachusetts'),
    ('MI','Michigan'),
    ('MN','Minnesota'),
    ('MS','Mississippi'),
    ('MO','Missouri'),
    ('MT','Montana'),
    ('NE','Nebraska'),
    ('NA','Nevada'),
    ('NH','New Hampshire'),
    ('NJ','New Jersey'),
    ('NM','New Mexico'),
    ('NY','New York'),
    ('NC','North Carolina'),
    ('ND','North Dakota'),
    ('OH','Ohio'),
    ('OK','Oklahoma'),
    ('OR','Oregon'),
    ('PA','Pennsylvania'),
    ('RI','Rhode Island'),
    ('SC','South Carolina'),
    ('SD','South Dakota'),
    ('TN','Tennessee'),
    ('TX','Texas'),
    ('UT','Utah'),
    ('VT','Vermont'),
    ('VA','Virginia'),
    ('WA','Washington'),
    ('WV','West Virginia'),
    ('WI','Wisconsin'),
    ('WY','Wyoming'),
    )
    state = models.CharField(max_length=3,choices=STATE_CHOICES,blank=True,null=True)

    zipcodeValidator = RegexValidator(r"^([0-9]{5}(?:-[0-9]{4})?$)","Error: Must be Digit 5 E.g. 00000 or 00000-0000")
    zipcode = models.CharField(max_length=12,validators=zipcodeValidator,blank=True,null=True)
    CREDIT_METHOD_CHOICES =(
        ('V','Visa'),
        ('M','Mastercard'),
        ('A','American Express'),
        ('D','Discover'),
    )
    credit_method = models.CharField(max_length=1, choices=CREDIT_METHOD_CHOICES, blank=True, null=True)
    credit_account = models.CharField(max_length=15, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=CASCADE,related_name="profile",null=True)