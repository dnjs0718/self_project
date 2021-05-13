from django.urls   import path
from posting.views import PostingView,PostingListView

urlpatterns = [
    path('/<int:posting_id>',PostingView.as_view()),
    path('',PostingView.as_view()),
    path('/list',PostingListView.as_view())
]