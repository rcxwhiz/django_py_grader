from django.http import HttpResponse
from django.shortcuts import render


def index(request):
	return HttpResponse('This is the index page of the site bro')


def submit(request, assignment_name):
	return HttpResponse(f'You\'re looking at assignment: {assignment_name}')


def create(request):
	return HttpResponse('You\'re looking at the page to create an assignment')


def view_results(request, assignment_name):
	return HttpResponse(f'You\'re looking at the results for: {assignment_name}')
