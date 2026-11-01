import unittest
from tools.format_adapters import renpy, webgal, paradox
class AdapterTests(unittest.TestCase):
    def test_renpy(self):
        s='translate chinese strings:\n    old "Hello [name]"\n    new ""\n'
        self.assertIn('你好 [name]',renpy(s,{'Hello [name]':'你好 [name]'}))
    def test_renpy_protection(self):
        with self.assertRaises(ValueError):renpy('translate chinese strings:\n    old "Hello [name]"\n    new ""\n',{'Hello [name]':'你好'})
    def test_webgal(self):
        self.assertEqual(webgal('爱音:你好;\nchangeBg:bg.png;\n',{'1':'早上好'}),'爱音:早上好;\nchangeBg:bg.png;\n')
    def test_webgal_command_guard(self):
        with self.assertRaises(ValueError):webgal('changeBg:bg.png;\n',{'1':'oops'})
    def test_paradox(self):
        self.assertIn('KEY:0 "你好"',paradox('l_english:\n KEY:0 "Hello"\n',{'KEY':'你好'}))
    def test_paradox_unknown(self):
        with self.assertRaises(ValueError):paradox('l_english:\n KEY:0 "Hello"\n',{'X':'oops'})
if __name__=='__main__':unittest.main()
