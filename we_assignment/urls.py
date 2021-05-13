from django.urls   import path,include

from posting.views import PasswordCheckView

urlpatterns = [
    path('post',include('posting.urls')),
    path('checkpw/<int:posting_id>',PasswordCheckView.as_view())
]