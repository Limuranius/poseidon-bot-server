from django.urls import path
from .views import IndexView, CreateRecordView, RecordsListView, RecordView


urlpatterns = [
    path("", IndexView.as_view(), name="index_url"),
    path("create/", CreateRecordView.as_view(), name="create_record_url"),
    path("records/", RecordsListView.as_view(), name="records_list_url"),
    path("records/<int:record_id>", RecordView.as_view(), name="record_url")
]