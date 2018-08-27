from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import code_generator, create_gid
from django.db.models import Q

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=15)

    def __str__(self):
        return str(self.user.username)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Todo(models.Model):
    title=models.CharField(max_length=15)
    description=models.TextField()
    author=models.ForeignKey(Profile)
    end_date=models.DateTimeField(blank=True)
    active= models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return str(self.title)

class Group(models.Model):
    gid=models.CharField(max_length=10,blank=True)
    gname=models.CharField(max_length=15)
    members=models.ManyToManyField(Profile)
    todo=models.ManyToManyField(Todo,blank=True)
    invite_link=models.CharField(max_length=100,blank=True)

    def save(self, *args, **kwargs):
        if self.gid is None or self.gid == "":
            self.gid = create_gid(self)
            self.invite_link = 'https://www.todo.herokuapp.com/todoapp/invite/'+str(self.gname)+'-'+str(self.gid)
        super(Group, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.gname)
    


class ThreadManager(models.Manager):
    def get_or_new(self,grp):
        qlookup=Q(group=grp)
        qs=self.get_queryset().filter(qlookup)
        if qs.exists():
            return qs[0]
        else:
            Klass=grp.__class__
            grpobj=Klass.objects.get(id=grp.id)
            obj=self.model(group=grpobj)
            obj.save()
            return obj


class Thread(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE)

    objects=ThreadManager()

    def __str__(self):
        return str(self.group.gid)