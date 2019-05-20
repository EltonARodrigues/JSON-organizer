from ast import literal_eval
from datetime import datetime, timedelta
from .exception import InvalidMessage
import datetime
import os
import json
import re
import csv


class Message():
    def __init__(self, message):
        self.__message = message
        self.__keys = r'values\d*|sensor\d*'

    def __str__(self):
        return F"INPUT: {self.__message}"

    def _verify_fields(self):
        return "id" in self.__message and re.findall(
            self.__keys, str(self.__message))

    def _get_measurer_key(self):
        return [key for key in self.__message.keys()
                if re.search(self.__keys, key)][0]

    def _define_date(self, date):
        return date - timedelta(minutes=-1)

    def _format_date(self, date):
        return date.strftime("%Y-%m-%d@%H:%M:%S")

    def _count_values(self):
        measurer_key = self._get_measurer_key()
        return len(self.__message[measurer_key]) - 1

    def validate(self):
        try:
            json.loads(self.__message)
            self.__message = literal_eval(self.__message)

            if not self._verify_fields():
                raise InvalidMessage("Invalid filds in a dict")
            return True

        except (ValueError, TypeError):
            raise InvalidMessage("Error with dict")
            return False

    def format_to_api(self):
        api_join_menssage = []

        measurer_key = self._get_measurer_key()
        count = self._count_values()

        date = datetime.datetime.now()

        for i in range(count + 1):
            date = self._define_date(date)
            api_template = {
                'values': self.__message[measurer_key][i],
                'date': self._format_date(date)
            }
            api_join_menssage.append(api_template)
        return api_join_menssage

    def last_value(self):
        measurer_key = self._get_measurer_key()

        last = {
            measurer_key: self.__message[measurer_key][self._count_values()]
        }
        return last

    def format_aws_message(self):
        measurer_key = self._get_measurer_key()

        now = datetime.datetime.now()
        data = now.strftime("%Y-%m-%d %H:%M")
        aws_message = {
            "id": self.__message['id'],
            "vol": self.__message[measurer_key][self._count_values()],
            "data": data
        }
        return aws_message
