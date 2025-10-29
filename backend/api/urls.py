from django.urls import path
from . import views
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AnalyzePDFView
from .views import UserAnalyzationHistoryView

urlpatterns = [

    #path: http://127.0.0.1:8000/api/hello
    #body: 
        #{}
    path('hello', views.hello_world),

    #path: http://127.0.0.1:8000/api/register
    #body: 
        # {
        # "username": "exampleUsername",
        # "email": "example@example.com",
        # "password": "MyStrongPass123!",
        # "password2": "MyStrongPass123!",
        # "first_name": "Example",
        # "last_name": "User"
        # }

    path('register', RegisterView.as_view(), name='register'),

    #path: http://127.0.0.1:8000/api/login
    #body:
        # {
        # "username": "exampleUsername",
        # "password": "MyStrongPass123!"
        # }
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    #path:
    #body:
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    #path: http://127.0.0.1:8000/api/analyze
    #body: file, user_id

    path('analyze', AnalyzePDFView.as_view(), name='analyze'),

    #path: http://127.0.0.1:8000/api/analyze/<user_id>/history
    #body: {}
    path('analyze/<int:user_id>/history', UserAnalyzationHistoryView.as_view(), name='user_analyzation_history'),

]
