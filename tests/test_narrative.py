import unittest
from tools.narrative import validate,export,patch_json
class NarrativeTests(unittest.TestCase):
    def setUp(self):
        self.scene={'start':'a','nodes':{'a':{'type':'line','speaker':'anon','text':'你好','next':'b'},'b':{'type':'end'}}}
    def test_valid(self):self.assertEqual(validate(self.scene)[0],[])
    def test_export(self):self.assertIn('label gns_node_a:',export(self.scene))
    def test_missing_target(self):
        self.scene['nodes']['a']['next']='missing'
        self.assertTrue(validate(self.scene)[0])
    def test_unreachable(self):
        self.scene['nodes']['c']={'type':'end'}
        self.assertTrue(validate(self.scene)[1])
    def test_patch(self):
        self.assertEqual(patch_json({'lines':[{'id':'1','text':'Hi [name]'}]},{'1':'你好 [name]'})['lines'][0]['text'],'你好 [name]')
    def test_patch_guard(self):
        with self.assertRaises(ValueError):patch_json({'lines':[{'id':'1','text':'Hi [name]'}]},{'1':'你好'})
if __name__=='__main__':unittest.main()
