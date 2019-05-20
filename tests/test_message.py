from datetime import datetime, timedelta
from json_organizer.message import Message
from json_organizer.exception import InvalidMessage

from unittest import TestCase
import datetime


class Testmessage(TestCase):

    def setUp(self):
        input = '''{"id":"fce176","topic":"bancada",
                    "countpkt":"2","sensor3":[159.99,174.47,
                    189.03,203.51,218.07,232.55,247.03,261.50,
                    275.98,290.55]}'''

        self.message = Message(input)
        self.validate = self.message.validate()

    def test_message_validation_is_true(self):
        self.assertTrue(self.validate)

    def test_message_validation_is_false(self):
        with self.assertRaises(InvalidMessage):
            self.message = Message(input)
            self.validate = self.message.validate()

    def test_message_validation_is_true(self):
        self.assertEqual(True, self.validate)

    def test_message_validation_is_false(self):
        with self.assertRaises(InvalidMessage):
            wrong_message = Message('{"id":"fce176')
            validade = wrong_message.validate()

    def test_format_to_api(self):
        output = self.message.format_to_api()

        self.assertEqual(type(output), list)

    def test_format_to_api(self):
        output = self.message.format_to_api()

        self.assertEqual(type(output), list)

    def test_last_value(self):
        output = self.message.last_value()
        value_test = {"sensor3": 290.55}

        self.assertEqual(output, value_test)

    def test_aws_message(self):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M")

        value = {
            'id': 'fce176',
            'vol': 290.55,
            'data': date
        }

        output = self.message.format_aws_message()
        self.assertEqual(output, value)
