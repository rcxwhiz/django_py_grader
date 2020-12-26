"""django_py_grader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from py_grader import views

urlpatterns = [
	path('admin/', admin.site.urls),

	path('', views.index, name='index'),

	path('submit', views.submit, name='submit'),
	path('submit/<str:assignment_name>/', views.submit_assignment, name='submit_assignment'),
	path('view_assignment_results/<str:assignment_name>', views.view_assignment_results, name='view_assignment_results'),
	path('view_submission_result/<int:submission_id>', views.view_submission_result, name='view_submission_result'),
	path('create_assignment', views.create_assignment, name='create_assignment')
]
