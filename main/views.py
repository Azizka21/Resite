from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from random import choice

from .serializers import (
    ListSerializer,
    ListDetailsSerializer,
    CreateListSerializer,
)

from .models import List
from .forms import ListSelectionForm, ListEditForm
from .utils import initialize_list_data, resit_by_template, generate_templates

def index(request):
    if request.user.is_authenticated:
        user_lists = List.objects.filter(owner=request.user)
        return render(request, 'index.html', {'lists': user_lists})
    else:
        return redirect('/login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in new user and redirect to home page
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def result(request):
    if request.method == "POST":
        list_id = request.POST.get('selected_list')
        if not list_id:
            return redirect('home')
        selected_list = get_object_or_404(List, id=list_id, owner=request.user)
        # If all seating options have already been used, we generate a new ones
        if not selected_list.templates:
            selected_list.templates = generate_templates(selected_list.item_count)
            selected_list.save()

        template = choice(selected_list.templates)
        selected_list.templates.remove(template)

        result = resit_by_template(selected_list.people_array, template)
        selected_list.last_result = result
        selected_list.save()
        return render(request, 'result.html', {'pairs': result})

    # If user accessed this view directly (GET), redirect to home
    return redirect('home')

def edit_list(request, list_id):
    list_item = get_object_or_404(List, pk=list_id, owner=request.user)
    if request.method == 'POST':
        # Processing the submitted form
        form = ListEditForm(request.POST, instance=list_item)
        if form.is_valid():
            list_item = form.save(commit=False)
            # Saving a shuffled version of the list (to make element order irrelevant)
            initialize_list_data(list_item)
            form.save()
            return redirect('home')
    else:
        # Displaying the form when opening the page for the first time
        # Fill the form with the existing contents of the list
        form = ListEditForm(instance=list_item)

    return render(request, 'edit_list.html', {'form': form, 'list': list_item})

def add_list(request):
    if request.method == 'POST':
        # Processing the submitted form
        form = ListEditForm(request.POST)
        if form.is_valid():
            list_item = form.save(commit=False)
            list_item.owner = request.user
            # Saving a shuffled version of the list (to make element order irrelevant)
            initialize_list_data(list_item)
            list_item.save()
            return redirect('home')
    else:
        # Displaying the form when opening the page for the first time
        form = ListEditForm()

    return render(request, 'edit_list.html', {'form': form})


def delete_list(request, list_id):
    list_item = get_object_or_404(List, pk=list_id, owner=request.user)
    list_item.delete()
    return redirect('home')

# API endpoint for working with the user's lists:
# - GET: returns all lists owned by the user
# - POST: creates a new list for the user
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def my_lists(request):
    if request.method == 'GET':
        lists = List.objects.filter(owner=request.user)
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CreateListSerializer(data=request.data)
        if serializer.is_valid():
            list_item = serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API endpoint for a specific list by ID:
# - GET: retrieve details of the list
# - DELETE: delete the list
# - PUT: fully update the list
# - PATCH: partially update the list
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def get_list(request, list_id):
    list_item = get_object_or_404(List, pk=list_id, owner=request.user)
    if request.method == 'GET':
        serializer = ListDetailsSerializer(list_item)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        list_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CreateListSerializer(instance=list_item, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = CreateListSerializer(instance=list_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API endpoint to generate one possible result (pairing) for a list
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_result(request, list_id):
    list_item = get_object_or_404(List, pk=list_id, owner=request.user)
    if not list_item.templates:
        list_item.templates = generate_templates(list_item.item_count)
        list_item.save()

    template = choice(list_item.templates)
    list_item.templates.remove(template)

    result = resit_by_template(list_item.people_array, template)
    list_item.last_result = result
    list_item.save()
    return Response({'pairs': result})