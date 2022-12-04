from django.shortcuts import render, redirect
from django.views import View
from .forms import RecordForm
from .models import RecordModel
from .BotManagment import BotMonitor


class IndexView(View):
    def get(self, request):
        return render(request, "bot/index.html")


class CreateView(View):
    def get(self, request):
        return render(request, "bot/create_record.html", context={"form": RecordForm()})

    def post(self, request):
        form = RecordForm(request.POST)
        if form.is_valid():
            obj = form.save()  # Сохраняем новую запись в БД
            BotMonitor.update_bot_for_obj(obj)  # Создаём для записи связанного бота
            return redirect("records_list_url")
        else:
            return redirect("create_record_url")



class RecordsListView(View):
    def get(self, request):
        records = RecordModel.objects.all()
        return render(request, "bot/record_list.html", context={"records": records})