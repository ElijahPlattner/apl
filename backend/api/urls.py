from django.urls import path
from . import views
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AnalyzePDFView
from .views import UserAnalyzationHistoryView
from .views import AnalyzationDetailView
from .views import CustomTokenObtainPairView

urlpatterns = [

    #path: http://127.0.0.1:8000/api/hello
    #body: 
        #{}
    path('hello', views.hello_world),

    #path: http://127.0.0.1:8000/api/register
    #method: POST
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
    #method: POST
    #body:
        # {
        # "username": "exampleUsername",
        # "password": "MyStrongPass123!"
        # }
    path('login', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),

    #path:
    #body:
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    #path: http://127.0.0.1:8000/api/analyze
    #method: POST
    #body: file, user_id

    path('analyze', AnalyzePDFView.as_view(), name='analyze'),

    
    #path: http://127.0.0.1:8000/api/analyze/user/<user_id>/history
    #method: GET
    #body: {}
    path('analyze/user/<int:user_id>/history', UserAnalyzationHistoryView.as_view(), name='user_analyzation_history'),

    #path: http://127.0.0.1:8000/api/analyze/analyzation/<analyzation_id>
    #method: GET
    #body: {}

    path('analyze/analyzation/<int:analyzation_id>', AnalyzationDetailView.as_view(), name='analyzation_detail'),

]
