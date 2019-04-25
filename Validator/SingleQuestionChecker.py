import json
import re

day_month_year_regex = re.compile(r"^([0-2][0-9]|(3)[0-1])(/)(((0)[0-9])|((1)[0-2]))(/)\d{4}$")
month_year_regex = re.compile(r"^(((0)[0-9])|((1)[0-2]))(/)\d{4}$")
year_regex = re.compile(r"^\d{4}$")


class Checker:

    question = None
    question_json = None
    event_types = None
    participant_types = None
    subtasks_types = None
    location_types = None
    time_types = None
    document_name = None

    def __init__(self):
        self.load_event_types()
        self.load_subtasks_types()
        self.load_time_types()
        self.load_participant_types()
        self.load_location_types()

    def load_event_types(self):
        event_types_json = json.loads(open("event_types.json", "r").read())
        self.event_types = event_types_json["event_types"]

    def load_subtasks_types(self):
        subtasks_types_json = json.loads(open("subtasks_types.json", "r").read())
        self.subtasks_types = subtasks_types_json["subtasks"]

    def load_time_types(self):
        time_types_json = json.loads(open("time_types.json", "r").read())
        self.time_types = time_types_json["time_types"]

    def load_participant_types(self):
        participant_types_json = json.loads(open("participant_types.json", "r").read())
        self.participant_types = participant_types_json["participant_types"]

    def load_location_types(self):
        location_types_json = json.loads(open("location_types.json", "r").read())
        self.location_types = location_types_json["location_types"]

    def check_question_valid(self, question):

        self.question = question
        self.question_json = json.loads(self.question)
        self.document_name = list(self.question_json.keys())[0]

        try:
            self.check_question_keys_valid()
        except Exception as e:
            raise Exception("there is an issue with question keys, " + str(e))
        try:
            self.check_question_keys_values_valid()
        except Exception as e:
            raise Exception("there is an issue with question values, " + str(e))

    def check_question_keys_values_valid(self):
        self.check_question_event_type_value()
        self.check_question_subtask_value()
        self.check_question_verbose_question_value()
        self.check_question_time_value()

    def check_question_event_type_value(self):
        if type(self.question_json[self.document_name]["event_type"]) is not str:
            raise Exception("invalid event type value! (" +
                            str(type(self.question_json[self.document_name]["event_type"])) +
                            " instead of str)")
        if self.question_json[self.document_name]["event_type"] not in self.event_types:
            raise Exception("invalid event type value! (" +
                            str(self.question_json[self.document_name]["event_type"]) +
                            ")")

    def check_question_subtask_value(self):
        if type(self.question_json[self.document_name]["subtask"]) is not int:
            raise Exception("invalid subtask value! (" +
                            str(type(self.question_json[self.document_name]["subtask"])) +
                            " instead of int)")
        if self.question_json[self.document_name]["subtask"] not in self.subtasks_types:
            raise Exception("invalid subtask value! (" +
                            str(self.question_json[self.document_name]["subtask"]) +
                            ")")

    def check_question_verbose_question_value(self):
        if type(self.question_json[self.document_name]["verbose_question"]) is not str:
            raise Exception("invalid verbose_question value! (" +
                            str(type(self.question_json[self.document_name]["verbose_question"])) +
                            " instead of str)")

    def check_question_time_value(self):
        if "time" in self.question_json[self.document_name]:
            if list(self.question_json[self.document_name]["time"].keys())[0] not in self.time_types:
                raise Exception("invalid time value! (" +
                                str(list(self.question_json[self.document_name]["time"].keys())[0]) +
                                ")")
            if "day" in self.question_json[self.document_name]["time"]:
                if not day_month_year_regex.match(self.question_json[self.document_name]["time"]["day"]):
                    raise Exception("invalid time value! (" +
                                    str(self.question_json[self.document_name]["time"]["day"]) +
                                    ")")
            elif "month" in self.question_json[self.document_name]["time"]:
                if not month_year_regex.match(self.question_json[self.document_name]["time"]["month"]):
                    raise Exception("invalid time value (" +
                                    str(self.question_json[self.document_name]["time"]["month"]) +
                                    ")")
            elif "year" in self.question_json[self.document_name]["time"]:
                if not year_regex.match(self.question_json[self.document_name]["time"]["year"]):
                    raise Exception("invalid time value (" +
                                    str(self.question_json[self.document_name]["time"]["year"]) +
                                    ")")

    def check_question_keys_valid(self):

        event_properties_number = 0

        self.check_question_document_name_key()
        self.check_question_event_type_key()
        self.check_question_subtask_key()
        event_properties_number = self.check_question_participant_key(event_properties_number)
        event_properties_number = self.check_question_time_key(event_properties_number)
        event_properties_number = self.check_question_location_key(event_properties_number)
        self.check_question_event_properties_number(event_properties_number)
        self.check_question_verbose_question_key()

    def check_question_document_name_key(self):
        if len(list(self.question_json.keys())) is not 1:
            raise Exception("invalid document name key! (number of document name keys is " +
                            str(len(list(self.question_json.keys()))) +
                            " instead of 1)")

    def check_question_event_type_key(self):
        if "event_type" not in self.question_json[self.document_name]:
            raise Exception("invalid event type key! (is missing)")
        elif type(self.question_json[self.document_name]["event_type"]) is not str:
            raise Exception("invalid event type key! (" +
                            str(type(self.question_json[self.document_name]["event_type"])) +
                            " instead of str")

    def check_question_subtask_key(self):
        if "subtask" not in self.question_json[self.document_name]:
            raise Exception("invalid subtask key! (is missing)")

    def check_question_participant_key(self, event_properties_number):
        if "participant" in self.question_json[self.document_name]:
            event_properties_number += 1
            if list(self.question_json[self.document_name]["participant"].keys())[0] not in self.participant_types:
                raise Exception("invalid participant key! (" +
                                str(list(self.question_json[self.document_name]["participant"].keys())[0]) +
                                ")")
        return event_properties_number

    def check_question_time_key(self, event_properties_number):
        if "time" in self.question_json[self.document_name]:
            event_properties_number += 1
            if list(self.question_json[self.document_name]["time"].keys())[0] not in self.time_types:
                raise Exception("invalid time key! (" +
                                str(list(self.question_json[self.document_name]["time"].keys())[0]) +
                                ")")
        return event_properties_number

    def check_question_location_key(self, event_properties_number):
        if "location" in self.question_json[self.document_name]:
            event_properties_number += 1
            if list(self.question_json[self.document_name]["location"].keys())[0] not in self.location_types:
                raise Exception("invalid location key! (" +
                                str(list(self.question_json[self.document_name]["location"].keys())[0]) +
                                ")")
        return event_properties_number

    @staticmethod
    def check_question_event_properties_number(event_properties_number):
        if event_properties_number is not 2:
            raise Exception("invalid the number of properties! (" +
                            str(event_properties_number) +
                            " instead of 2)")

    def check_question_verbose_question_key(self):
        if "verbose_question" not in self.question_json[self.document_name]:
            raise Exception("invalid verbose_question key! (is missing)")

