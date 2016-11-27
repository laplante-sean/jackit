'''
Handles initial setup and tracking of useful globals
'''

import os

from jackit.config import JackitConfig

class SiteDeploymentSingleton:
    '''
    Handles initial setup, config loading, and logging
    '''

    _instance = None

    @classmethod
    def instance(cls):
        '''
        Get instance of SiteDeploymentSingleton
        '''
        if cls._instance is None:
            cls._instance = SiteDeploymentSingleton()
            return cls._instance
        return cls._instance

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.resource_dir = os.path.join(self.base_path, "jackit", "resources")
        self.config_path = os.path.join(self.base_path, "site.cfg.json")
        self.config = None

    def setup_config(self):
        '''
        Setup the config file
        '''
        self.config = JackitConfig(self.config_path)
        if not os.path.exists(self.config_path):
            self.config.save()

        self.config.load()

SiteDeployment = SiteDeploymentSingleton.instance()
