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
        try:
            name_field = req.get('name', '').strip()
            if not name_field:
                messages.error(request, 'Group field is required')
            if Group.objects.filter(name=name).exists():
                messages.error(request, 'Group is already exists with same name')
            Group.objects.create(name=name)        
        except ValidationError as e:
            messages.error(request, 'Validation error: '+str(e))
    return redirect('groups')
    
def editGroup(request):

    req = request.POST
    name = req.get('name')
    g_id = request.POST.get('id')

    # try:
    #     name_field = req.get('name', '').strip()
    #     if not name_field:
    #         messages.error(request, 'Group field is required')
    #     if Group.objects.exclude(id = g_id).filter(name = name).exists():
    #         messages.error(request, 'Group is already exists with same name')     
    # except:    
    group = Group.objects.get(id=g_id)
    group.name = name
    group.save()
    messages.success(request, 'Group updated successfully')
    return redirect('groups')

def deleteGroup(request):
    
    g_id = request.POST.get('id')
    group = Group.objects.get(id=g_id)
    group.delete()
    
    messages.success(request, 'Group deleted successfully')
    return redirect('groups')




