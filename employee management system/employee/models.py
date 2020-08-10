from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    #OneToOne mean whenever new user is created, a new profile will be created
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length = 20, null = False, blank = False)
    salary = models.IntegerField(null = True, blank = True)
    picture = models.ImageField(upload_to='pictures/%Y/%m/%d/', max_length=255, null = True, blank = True)

    class Meta:
        ordering = ('-salary',)     # - is for descending order

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)

class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(profile__designation='Employee')

#proxy model
# you can't add fields in this model
#we can use all user model properties through employee class
class Employee(User):
    class Meta:
        ordering = ('username', )
        proxy = True

    objects = EmployeeManager()

    def full_name(self):
        return self.first_name + " - " + self.last_name


#if a new user is created, then new profile will automatically be created
# it is called signal receiver system
@receiver(post_save, sender = User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
    else:
        instance.profile.save()