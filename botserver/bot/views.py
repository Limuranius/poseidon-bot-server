from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecordForm
from .models import RecordModel
from .BotManagment import BotMonitor


class IndexView(View):
    def get(self, request):
        return render(request, "bot/index.html")


class CreateRecordView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "bot/create_record.html", context={"form": RecordForm()})

    def post(self, request):
        form = RecordForm(request.POST)
        if form.is_valid():
            # Сохраняем новую запись в БД
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            BotMonitor.update_bot_for_obj(obj)  # Создаём для записи связанного бота
            return redirect("records_list_url")
        else:
            return redirect("create_record_url")


class RecordsListView(View):
    def get(self, request):
        records = RecordModel.objects.all()
        return render(request, "bot/record_list.html", context={"records": records})


class RecordView(View):
    def get(self, request, record_id: int):
        record = get_object_or_404(RecordModel, pk=record_id)
        return render(request, "bot/record_info.html", context={"record": record})
