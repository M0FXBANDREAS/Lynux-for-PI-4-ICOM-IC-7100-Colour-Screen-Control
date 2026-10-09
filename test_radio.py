import unittest
from types import SimpleNamespace
from server import encode_frequency, decode_frequency, Radio

class SerialFake:
    def __init__(self): self.reply=b''; self.sent=[]
    def reset_input_buffer(self): self.reply=b''
    def write(self, frame):
        self.sent.append(frame)
        self.reply=frame+b'\xfe\xfe\xe0\x88\xfb\xfd'
    def read(self,n): result=self.reply; self.reply=b''; return result

class Tests(unittest.TestCase):
    def test_frequency_wire_order(self):
        self.assertEqual(encode_frequency(14200000),bytes.fromhex('00 00 20 14 00'))
        self.assertEqual(decode_frequency(bytes.fromhex('00 00 20 14 00')),14200000)
    def test_receive_range(self):
        for hz in (0,200000000,399999999,471000000):
            with self.assertRaises(ValueError): encode_frequency(hz)
    def test_invalid_bcd(self):
        with self.assertRaises(ValueError): decode_frequency(bytes.fromhex('aa 00 00 00 00'))
    def test_echo_skipped_ack_received(self):
        radio=Radio(SimpleNamespace(port=None,address=0x88,audio_device=None))
        radio.port=SerialFake()
        self.assertEqual(radio.exchange(5,encode_frequency(14200000)),b'')
        self.assertEqual(radio.port.sent[0],bytes.fromhex('fe fe 88 e0 05 00 00 20 14 00 fd'))
    def test_no_transmit_api(self):
        radio=Radio(SimpleNamespace(port=None,address=0x88,audio_device=None))
        with self.assertRaises(ValueError): radio.set({'ptt':True})
        with self.assertRaises(ValueError): radio.set({'mode':'invalid'})

if __name__=='__main__': unittest.main()
