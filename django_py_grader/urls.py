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
from py_grader.handler import add_grading_methods_to_db

add_grading_methods_to_db()

urlpatterns = [
	# site utils
	path('admin/', admin.site.urls),

	# student pages
	path('', views.index, name='index'),

	path('submit/', views.submit, name='submit'),
	path('submit_get/', views.submit_get, name='submit_get'),
	path('submit/<str:assignment_name>/', views.submit_assignment, name='submit_assignment'),

	path('view_submission_result/', views.view_any_submission_result, name='view_any_submission_result'),
	path('view_submission_result_get/', views.view_any_submission_result_get, name='view_any_submission_result_get'),
	path('view_submission_result/<int:submission_id>/', views.view_submission_result, name='view_submission_result'),

	# grader pages
	path('grader/', views.grader_index, name='grader_index'),

	path('grader/test_submit/', views.test_submit, name='test_submit'),
	path('grader/test_submit_get/', views.test_submit_get, name='test_submit_get'),
	path('grader/test_submit/<str:assignment_name>/', views.test_submit_assignment, name='test_submit_assignment'),

	path('grader/view_assignment_results/', views.view_results, name='view_results'),
	path('grader/view_assignment_results_get/', views.view_results_get, name='view_results_get'),
	path('grader/view_assignment_results/<str:assignment_name>/', views.view_assignment_results,
	     name='view_assignment_results'),

	path('grader/create_assignment/', views.create_assignment, name='create_assignment'),
	path('grader/assignments/', views.assignments, name='assignments'),
	path('grader/add_test_case/', views.add_any_test_case, name='add_any_test_case'),
	path('grader/add_any_test_case_get/', views.add_any_test_case_get, name='add_any_test_case_get'),
	path('grader/add_test_case/<str:assignment_name>', views.add_test_case, name='add_test_case'),

	path('grader/manage_net_ids/', views.manage_net_ids, name='manage_net_ids'),
	path('grader/manage_net_ids/add_net_id/', views.add_net_id, name='add_net_id'),
	path('grader/manage_net_ids/remove_net_id/', views.remove_net_id, name='remove_net_id'),
	path('grader/manage_net_ids/upload_net_id_csv/', views.upload_net_id_csv, name='upload_net_id_csv'),
	path('grader/manage_net_ids/clear_net_id/', views.clear_net_id, name='clear_net_id'),

	path('accounts/', include('django.contrib.auth.urls'))
]
