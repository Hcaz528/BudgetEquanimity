from django.urls import path
from budget_app import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('goodbye', views.goodbye_world, name='goodbye_world'),
    path('test', views.test_sql_query, name='test_sql_query'),

    # API v0
    path('api/0/account/<int:pk>', views.account_detail),
    path('api/0/budget/<int:pk>', views.budget_detail),
    path('api/0/budget/<int:pk>/<int:year>/<int:month>',
         views.budget_detail_filtered),
    # path('api/0/budget/<int:pk>', views.budget_detail),

    # 404 Stuff
    path('404', views.NotFound404, name='NotFound404'),
    path('<path:resource>', views.NotFound404, name='NotFound404'),
]
