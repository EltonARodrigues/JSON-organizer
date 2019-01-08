from json_organizer.message import Message
from json_organizer.exception import InvalidMessage

from unittest import TestCase


class Testmessage(TestCase):

    def setUp(self):
        self.input = '{"id":"fce176","topic":"bancada","countpkt":"2","sensor3":[159.99,174.47,189.03,203.51,218.07,232.55,247.03,261.50,275.98,290.55]}'

    def test_message_validation_is_true(self):
        message = Message(self.input)
        validator = message.validate()
        self.assertEqual(True, validator)

    def test_message_validation_is_false(self):
        with self.assertRaises(InvalidMessage):
            message = Message('{"id":"fce176')
            validator = message.validate()
