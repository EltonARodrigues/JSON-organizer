from ast import literal_eval
from datetime import datetime, timedelta
from .exception import InvalidMessage
import os
import datetime
import json
import re
import csv


class Message():
    def __init__(self, message):
        self.__message = message
        self.__keys = r'values\d*|sensor\d*'

    def __str__(self):
        return F"INPUT: {self.__message}"

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

    def _verify_fields(self):
        return "id" in self.__message and re.findall(self.__keys, str(self.__message))


    def formt_to_api(self):
        api_template = {}
        measurer_key = [key for key in self.__message.keys()
                        if re.search(self.__keys, key)][0]
        count_v = len(self.__message[measurer_key])
        api_join_menssage = []
        date = datetime.datetime.now()
        for i in range(count_v):
            date_format = date - timedelta(minutes=(count_v - (i + 1)))
            api_template["values"] = self.__message[measurer_key][i]
            api_template["date"] = date_format.strftime("%Y-%m-%d@%H:%M:%S")
            api_join_menssage.append(dict(api_template))
        return api_join_menssage

    def last_value(self):
        message_to_send = {}
        formatada = self.__message
        measurer_key = [key for key in self.__message.keys()
                        if re.search(self.__keys, key)][0]

        return "{\"" + str(measurer_key) + "\":\"" + str(
            self.__message[measurer_key][(len(self.__message[measurer_key]) - 1)]) + "\"}"

    def format_dojot_message(self):
        measurer_key = [key for key in self.__message.keys()
                        if re.search(self.__keys, key)][0]
        count_v = len(list(filter(None, self.__message[measurer_key])))
        api_template = "{" + measurer_key + ": "" }"
        date = datetime.datetime.now()
        for i in range(int(10)):
            date_format = date - timedelta(minutes=(count_v - (i + 1)))
            api_template['values'] = self.__message[measurer_key][i]
            api_template['date'] = date_format.strftime('%Y-%m-%d@%H:%M:%S')
        print(api_template)
        return api_template

    # AWS
    def format_aws_message(self):
        measurer_key = [key for key in self.__message.keys()
                        if re.search(self.__keys, key)][0]
        json_m = self.__message
        now = datetime.datetime.now()
        data = now.strftime("%Y-%m-%d %H:%M")
        fmessage = {"id": (json_m["id"]), "vol": (
            json_m[measurer_key][(len(self.__message[measurer_key]) - 1)]), "data": data}

        return (fmessage)
