'''
Test the JackitConfig class
'''

import os
import unittest
from deploy import SiteDeployment, SiteDeploymentError
from jackit.config import JackitConfig

class TestSiteDeployment(unittest.TestCase):
    '''
    Test the JackitConfig methods
    '''
    def setUp(self):
        '''
        Called before each test method is run
        '''
        self.test_base_path = os.path.dirname(os.path.abspath(__file__))
        self.test_config_path = os.path.join(self.test_base_path, "test.cfg.json")
        self.config = JackitConfig(self.test_config_path)

    def tearDown(self):
        '''
        Called after each test method is run
        '''
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)

    def test_valid_config(self):
        '''
        Test SiteDeployment with a valid config object
        '''
        SiteDeployment.config = self.config

    def test_invalid_config(self):
        '''
        Test SiteDeployment with an invalid config object
        '''
        with self.assertRaises(SiteDeploymentError):
            SiteDeployment.config = []

    def test_invalid_config_access(self):
        '''
        Test accessing the config prior to setup
        '''
        with self.assertRaises(SiteDeploymentError):
            test = SiteDeployment.config
