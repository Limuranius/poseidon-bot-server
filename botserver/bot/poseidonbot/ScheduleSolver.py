import datetime
from .ConfigManager import ConfigManagerInterface
from typing import Tuple, List

timeInterval = Tuple[datetime.datetime, datetime.datetime]


class ScheduleSolver:
    schedule_json: dict
    config_manager: ConfigManagerInterface

    def __init__(self, config_manager: ConfigManagerInterface):
        self.config_manager = config_manager

    def update_schedule(self, schedule_json: dict):
        """Обновляет расписание, полученное на определённый день"""
        self.schedule_json = schedule_json

    def __getFreeTimeIntervals(self) -> List[timeInterval]:
        """Из расписания для определённой машинки берёт все незанятые временные промежутки"""
        intervals = []
        for interval in self.schedule_json["data"][self.config_manager.MachineNumber]["entries"]:
            if interval["isBusy"]:
                continue
            else:
                start = datetime.datetime.strptime(interval["start"], "%Y/%m/%d %H:%M:%S")  # "2022/03/05 07:00:00"
                max_end = datetime.datetime.strptime(interval["max_end"], "%Y/%m/%d %H:%M:%S")
                intervals.append((start, max_end))
        return intervals

    def __applyPreferredTimeLength(self, intervals: List[timeInterval]) -> List[timeInterval]:
        """Убирает временные промежутки, не подходящие по желаемой длительности"""
        new_intervals = []
        for interval in intervals:
            dt = interval[1] - interval[0]
            if self.config_manager.MinTimeLength <= dt <= self.config_manager.MaxTimeLength:
                new_intervals.append(interval)
        return new_intervals

    def __applyPreferredTimeIntervals(self, intervals: List[timeInterval]) -> List[timeInterval]:
        """Убирает временные промежутки, не подходящие под желаемое время"""
        new_intervals = []
        for interval in intervals:
            start, end = interval
            for pref_interval in self.config_manager.TimeIntervals:
                pref_start, pref_end = pref_interval
                if start >= pref_start or end <= pref_end:  # Если промежутки хоть как-то пересекаются
                    new_intervals.append((max(start, pref_start), min(end, pref_end)))  # Оставляем пересекающуюся часть
        return new_intervals

    def __removeOverlappingIntervals(self, intervals: List[timeInterval]):
        """Убирает временные промежутки, которые полностью перекрываются каким-то промежутком"""
        new_intervals = []
        intervals = sorted(list(set(intervals)))  # Убираем дупликаты
        for i in range(len(intervals)):
            interv1 = intervals[i]
            is_overlapped = False
            for j in range(len(intervals)):
                if i != j:
                    interv2 = intervals[j]
                    if interv2[0] <= interv1[0] and interv1[1] <= interv2[1]:
                        is_overlapped = True
                        break
            if not is_overlapped:
                new_intervals.append(interv1)
        return new_intervals

    def getPerfectMatches(self) -> List[timeInterval]:
        intervals = self.__getFreeTimeIntervals()
        intervals = self.__applyPreferredTimeIntervals(intervals)
        intervals = self.__applyPreferredTimeLength(intervals)
        intervals = self.__removeOverlappingIntervals(intervals)
        return intervals
