from django.shortcuts import render, redirect
from Menu.models import Group
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
# Create your views here.

def index(request):

    groups_list = Group.objects.all()
    groups = Paginator(groups_list,15)
    page = request.GET.get('page')
    s = groups.get_page(page)
    nums = 'a' * s.paginator.num_pages
    groupsCount = Group.objects.count()

    return render(request, 'pages/groups/index.html', {"groups": s,'nums':nums, 'groupsCount': groupsCount})

def addGroup(request):

    if request.method == "POST":
        req = request.POST
        name = req.get('name')
        if not name:
            messages.warning(request, 'Please provide a name for the Group.')
        else:

            try:
                Group.objects.get(name=name)
                messages.warning(request,'Group already exists with same name')
            except Group.DoesNotExist:
                Group.objects.create(name=name)
                messages.success(request,'new Group created')

    return redirect('groups')
    
def editGroup(request):
    if request.method == "POST":
        req = request.POST
        name = req.get('name')
        g_id = req.get('id')

        try:
            group = Group.objects.get(id=g_id)
            name_field = name.strip()
            if not name_field:
                messages.warning(request, 'Group name field is required')
            elif Group.objects.exclude(id=g_id).filter(name=name).exists():
                messages.warning(request, 'Group already exists with the same name')
            else:
                group.name = name
                group.save()
                messages.success(request, 'Group updated successfully')
        except Group.DoesNotExist:
            messages.warning(request, 'Group not found')

    return redirect('groups')


def deleteGroup(request):
    
    g_id = request.POST.get('id')
    group = Group.objects.get(id=g_id)
    group.delete()
    
    messages.success(request, 'Group deleted successfully')
    return redirect('groups')




