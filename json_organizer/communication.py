import requests
import json
import csv


class APICommunication():

    def __init__(self, username, password, auth_basic):
        self.__username = username
        self.__password = password
        self.__access_token = ''
        self.__auth_basic = auth_basic

    def auth(self, address):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.__auth_basic,
        }

        params = (
            ('grant_type', 'password'),
            ('username', self.__message),
            ('password', self.__password),
        )

        response = (requests.post(address,
                                  headers=headers,
                                  params=params)).json()

        if 'error_description' in response:
            print(response['error_description'])
            return False
        self.__access_token = response['access_token']
        print("authenticated")
        return True

    def post(self, message, id_measurer, address):

        headers = {
            'Authorization': "Bearer " + str(self.__access_token),
            'Content-Type': 'application/json',
        }
        response = requests.request(
            "POST",
            address,
            data=json.dumps(message),
            headers=headers)

        print(response.text)


class APICommunicationDojot():
    def __init__(self, address, username, password):
        self.__message = username
        self.__password= password
        self.__address = address
        self.__access_token = ''

    def api_auth(self):
        headers = {
            'Content-Type': 'application/json',
        }

        params = {
            "username": self.__message,
            "passwd": self.password
        }

        response = (requests.post(self.__address + ':8000/auth',
                                  headers=headers,
                                  data=json.dumps(params))).json()

        if 'error_description' in response:
            return response['error_description']

        self.__access_token = response['jwt']

        return "authenticated"

    def api_send(self, menssage):
        pass

    def api_receive(self, atribute, last_N):
        headers = {
            'Authorization': 'Bearer ' + self.__access_token,
            'Fiware-Service': 'admin',
            'Fiware-ServicePath': '/',
        }
        response = requests.get(
            self.__address,
            headers=headers).json()
        for c in range(last_N):
            data = str(response['contextResponses'][0]['contextElement']
                       ['attributes'][0]['values'][c]['recvTime'])
            value = (response['contextResponses'][0]['contextElement']
                     ['attributes'][0]['values'][c]['attrValue'])
            print(value)

            with f:
                writer = csv.writer(f)
                writer.writerow(value)
