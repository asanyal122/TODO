from django.shortcuts import render

from .models import Profile,Thread,Group,Todo

def index(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    grps=profile.group_set.all()
    return render(request,'todoapp/index.html',{'Groups':grps,'user':user})

def description(request,id):
    grp=Group.objects.get(id=id)
    todos=grp.todo.all()
    return render(request,'todoapp/description.html',{'Group':grp.gname,'todos':todos})