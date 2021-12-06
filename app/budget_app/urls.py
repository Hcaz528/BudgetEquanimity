from django.urls import path
from budget_app import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('goodbye', views.goodbye_world, name='goodbye_world'),
    path('test', views.test_sql_query, name='test_sql_query'),
    path('404', views.NotFound404, name='NotFound404'),
    path('<path:resource>', views.NotFound404, name='NotFound404'),
    # path('ad', views.hello_world_scripts_one, name='app_one'),
    # path('app.js', views.hello_world_scripts_two, name='app'),
]