from easyprocess import EasyProcess, EasyProcessCheckError
from nose.tools import eq_
from unittest import TestCase
import time


class Test(TestCase):
    def test_call(self):
        eq_(EasyProcess('ls -la').call().return_code, 0)
        eq_(EasyProcess(['ls', '-la']).call().return_code, 0)
    
    def test_check(self):
        eq_(EasyProcess('ls -la').check(), True)
        eq_(EasyProcess(['ls', '-la']).check(), True)
        
        self.assertRaises(EasyProcessCheckError, lambda :  EasyProcess('xxxxx').check())
        self.assertRaises(EasyProcessCheckError, lambda :  EasyProcess('sh -c xxxxx').check())


    def test_start(self):
        p = EasyProcess('ls -la').start()
        time.sleep(0.2)
        eq_(p.stop().return_code, 0)
    
    def test_alive(self):
        eq_(EasyProcess('ping 127.0.0.1 -c 2').is_alive(), False)
        eq_(EasyProcess('ping 127.0.0.1 -c 2').start().is_alive(), True)
        eq_(EasyProcess('ping 127.0.0.1 -c 2').start().stop().is_alive(), False)
        eq_(EasyProcess('ping 127.0.0.1 -c 2').call().is_alive(), False)
        
    def test_std(self):
        eq_(EasyProcess('echo hello').call().stdout, 'hello')
        
    def test_wait(self):
        eq_(EasyProcess('echo hello').wait().return_code, None)
        eq_(EasyProcess('echo hello').wait().stdout, None)
        
        eq_(EasyProcess('echo hello').start().wait().return_code, 0)
        eq_(EasyProcess('echo hello').start().wait().stdout, 'hello')
        
        
        
