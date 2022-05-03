from django.conf import settings

from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


from django.core.validators import RegexValidator

from bases.models import TimeStampBase

GENDER_CHOICES = (
        (0,'female'),
        (1,'male'),
        (2,'Opt out')
    )

STATE_CHOICES=(
    ('AL','Alabama'),('AK','Alaska'),('AZ','Arizona'),('AR','Arkansas'),('CA','California'),('CO','Colorado'),('CT','Connecticut'),('DE','Delaware'),('FL','Florida'),('GA','Georgia'),('HI','Hawaii'),('ID','Idaho'),('IL','Illinois'),('IN','Indiana'),('IA','Iowa'),('KS','Kansas'),('KY','Kentucky'),('LA','Louisiana'),('ME','Maine'),('MD','Maryland'),('MA','Massachusetts'),('MI','Michigan'),('MN','Minnesota'),('MS','Mississippi'),('MO','Missouri'),('MT','Montana'),('NE','Nebraska'),('NA','Nevada'),('NH','New Hampshire'),('NJ','New Jersey'),('NM','New Mexico'),('NY','New York'),('NC','North Carolina'),('ND','North Dakota'),('OH','Ohio'),('OK','Oklahoma'),('OR','Oregon'),('PA','Pennsylvania'),('RI','Rhode Island'),('SC','South Carolina'),('SD','South Dakota'),('TN','Tennessee'),('TX','Texas'),('UT','Utah'),('VT','Vermont'),('VA','Virginia'),('WA','Washington'),('WV','West Virginia'),('WI','Wisconsin'),('WY','Wyoming')
    )

CREDIT_METHOD_CHOICES =(
        ('V','Visa'),
        ('M','Mastercard'),
        ('A','American Express'),
        ('D','Discover'),
    )

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        
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

    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        return self.create_user(
            email = self.normalize_email(email),
            password= password,
            **extra_fields)

class User(AbstractBaseUser,TimeStampBase):
    """
        email
        password
    """
    objects = UserManager()

    email = models.EmailField(verbose_name=_('email address'),unique=True, max_length=255)
    is_staff = models.BooleanField(verbose_name='Is staff',default=False)
    is_active = models.BooleanField(verbose_name='Is active',default=True)
    is_superuser = models.BooleanField(verbose_name='Is superuser',default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    date_joined = None
    last_login = None
    
    def __str__(self):
        return str(self.email)
    
    # @property
    # def is_superuser(self):
    #     return self.is_superuser
    # @property
    # def is_staff(self):
    #     return self.is_staff

    def has_perm(self, perm, obj=None):
        # return self.is_staff
        return True
    def has_module_perms(self, app_label):
        # return self.is_staff
        return True

# class ProfileManager(models.Manager):

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

    gender = models.IntegerField(choices=GENDER_CHOICES,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)

    
    state = models.CharField(max_length=3,choices=STATE_CHOICES,blank=True,null=True)

    zipcodeValidator = RegexValidator(r"^([0-9]{5}(?:-[0-9]{4})?$)",r"Error: Must be Digit 5 E.g. 00000 or 00000-0000")
    zipcode = models.CharField(max_length=12,validators=[zipcodeValidator],blank=True,null=True)

    credit_method = models.CharField(max_length=1, choices=CREDIT_METHOD_CHOICES, blank=True, null=True)

    credit_accountValidator = RegexValidator(r"^([0-9]{15})$",r"Error: credit account number must be Digit 15 numbers.")
    credit_account = models.CharField(max_length=15, validators=[credit_accountValidator], blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE,related_name="profile",null=True)

    def __str__(self):
        return str(self.user)