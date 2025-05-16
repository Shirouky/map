from __future__ import annotations
from datetime import datetime, timedelta
import random
from abc import ABC, abstractmethod


def random_time_between(start_time, end_time):
    start_timestamp = start_time.timestamp()
    end_timestamp = end_time.timestamp()
    random_timestamp = random.uniform(start_timestamp, end_timestamp)
    return datetime.fromtimestamp(random_timestamp)


def time(hour):
    return datetime.strptime(f"{hour}:00 20-04-2025", "%H:%M:%S %d-%m-%Y")


class Factory(ABC):
    @abstractmethod
    def factory_method(self):
        pass

    def create(self) -> str:
        person = self.factory_method()

        return person


class Person:
    places = []
    name = ""

    def __init__(self, name: str, places: list):
        self.name = name
        self.places = places

    def get_places(self):
        return self.places

    def get_name(self):
        return self.name


class DoctorFactory(Factory):
    def factory_method(self) -> Person:
        name = "doctor"
        places = [["amenity", "hospital", "time", random_time_between(time("6:00"), time("8:30"))],
                  ["shop", True, "time", random_time_between(time("17:00"), time("19:30"))],
                  ["building", ["apartments", "residential", "house"], "delta",
                   timedelta(minutes=random.randint(5, 40))]]

        return Person(name, places)


class SchoolChildFactory(Factory):
    def factory_method(self) -> Person:
        name = "schoolchild"
        places = [["building", "school", "time", random_time_between(time("7:00"), time("8:30"))],
                  ["shop", True, "time", random_time_between(time("14:00"), time("16:30"))],
                  ["building", ["apartments", "residential", "house"], "delta",
                   timedelta(minutes=random.randint(5, 20))]]

        return Person(name, places)


class OfficeWorkerFactory(Factory):
    def factory_method(self) -> Person:
        name = "office worker"
        places = [["office", "company", "time", random_time_between(time("7:00"), time("8:30"))],
                  ["leisure", "sports_centre", "time", random_time_between(time("17:00"), time("19:00"))],
                  ["building", ["apartments", "residential", "house"], "delta",
                   timedelta(minutes=random.randint(40, 180))]]

        return Person(name, places)


class CourierFactory(Factory):
    def factory_method(self) -> Person:
        name = "courier"
        places = [["office", "logistics", "time", random_time_between(time("7:30"), time("9:30"))],
                  ["building", ["apartments", "residential", "house"], "delta",
                   timedelta(minutes=random.randint(5, 15))],
                  ["amenity", "fast_food", "delta", timedelta(minutes=random.randint(5, 15))],
                  ["building", "residential", "delta", timedelta(minutes=random.randint(15, 45))],
                  ["office", "logistics", "delta", timedelta(minutes=random.randint(5, 15))],
                  ["building", ["apartments", "residential", "house"], "delta",
                   timedelta(minutes=random.randint(20, 30))]]

        return Person(name, places)


class SalesmanFactory(Factory):
    def factory_method(self) -> Person:
        name = "salesman"
        places = [["shop", True, "time", random_time_between(time("8:00"), time("9:30"))],
                  ["amenity", "pharmacy", "time", random_time_between(time("18:00"), time("19:00"))],
                  ["building", ["apartments", "residential", "house"], "delta",
                   timedelta(minutes=random.randint(5, 20))]]

        return Person(name, places)
