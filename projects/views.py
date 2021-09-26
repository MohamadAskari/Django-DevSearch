from projects.models import Project
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects

def projetcs(request):
    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects':projects, 'search_query':search_query, 'custom_range':custom_range }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        project.getVoteCount

        return redirect('project', pk=project.id)

    project = Project.objects.get(id=pk)
    return render(request, 'projects/single project.html', {'project':project, 'form':form})

@login_required(login_url='login')
def createProject(request):

    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = profile
            project.save()
            return redirect('account')

    context = {'form' : form}
    return render(request, 'projects/create project.html', context)

@login_required(login_url='login')
def updateProject(request, pk):

    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projectObj)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=projectObj)
        if form.is_valid():
            form.save()
            return redirect('account')
            
    context = {'form' : form}
    return render(request, 'projects/create project.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):

    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    if request.method == 'POST':
        projectObj.delete()
        return redirect('account')

    context = {'project':projectObj}
    return render(request, 'projects/delete project.html', context)    