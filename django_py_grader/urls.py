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

	path('submit/', views.submit, name='submit'),
	path('submit/<str:assignment_name>/', views.submit_assignment, name='submit_assignment'),
	path('test_submit/<str:assignment_name>/', views.test_submit_assignment, name='test_submit_assignment'),

	path('view_assignment_results/', views.view_results, name='view_results'),
	path('view_assignment_results/<str:assignment_name>/', views.view_assignment_results, name='view_assignment_results'),

	path('view_submission_result/', views.view_any_submission_result, name='view_any_submission_result'),
	path('view_submission_result/<int:submission_id>/', views.view_submission_result, name='view_submission_result'),

	path('create_assignment/', views.create_assignment, name='create_assignment'),
	path('add_test_case/<str:assignment_name>', views.add_test_case, name='add_test_case'),

	path('manage_net_ids/', views.manage_net_ids, name='manage_net_ids'),
	path('add_net_id/', views.add_net_id, name='add_net_id'),
	path('remove_net_id/', views.remove_net_id, name='remove_net_id'),
	path('upload_net_id_csv/', views.upload_net_id_csv, name='upload_net_id_csv'),
	path('clear_net_id/', views.clear_net_id, name='clear_net_id'),

	path('grader_login/', views.grader_login, name='grader_login'),

	path('success/', views.success, name='success'),
	path('failure/', views.failure, name='failure')
]
