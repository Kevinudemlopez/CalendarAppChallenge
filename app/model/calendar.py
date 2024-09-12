from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error


# TODO: Implement Reminder class here
class Reminder:
    date_time: datetime
    type: str = field(default="email")

    EMAIL = "email"
    SYSTEM = "system"

    def __str__(self):
        return f"Reminder on {self.date_time} of type {self.type}"

# TODO: Implement Event class here
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: List[Reminder] = field(default_factory=list)
    id: str = field(default_factory=generate_unique_id)

    def add_reminder(self, date_time: datetime, type_: Optional[str] = Reminder.EMAIL):
        reminder = Reminder(date_time=date_time, type=type_)
        self.reminders.append(reminder)

    def delete_reminder(self, reminder_index: int):
        if 0 <= reminder_index < len(self.reminders):
            del self.reminders[reminder_index]
        else:
            reminder_not_found_error()

    def __str__(self):
        return f"ID: {self.id}\nEvent title: {self.title}\nDescription: {self.description}\nTime: {self.start_at} - {self.end_at}"


# TODO: Implement Day class here
class Day:
    def __init__(self, date_: date):
        self.date_ = date_
        self.slots: Dict[time, Optional[str]] = {}
        self._init_slots()

    def _init_slots(self):
        current_time = time(0, 0)
        while current_time < time(23, 45):
            self.slots[current_time] = None
            current_time = (datetime.combine(date(1, 1, 1), current_time) + timedelta(minutes=15)).time()

    def add_event(self, event_id: str, start_at: time, end_at: time):
        current_time = start_at
        while current_time < end_at:
            if self.slots.get(current_time) is not None:
                slot_not_available_error()
            self.slots[current_time] = event_id
            current_time = (datetime.combine(date(1, 1, 1), current_time) + timedelta(minutes=15)).time()

    def delete_event(self, event_id: str):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None

        current_time = start_at
        while current_time < end_at:
            if self.slots.get(current_time) is not None:


# TODO: Implement Calendar class here
