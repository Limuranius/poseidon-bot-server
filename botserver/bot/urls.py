from django.urls import path
from .views import IndexView, CreateView, RecordsListView


urlpatterns = [
    path("", IndexView.as_view(), name="index_url"),
    path("create/", CreateView.as_view(), name="create_record_url"),
    path("list/", RecordsListView.as_view(), name="records_list_url"),
]