'''
Handles initial setup and tracking of useful globals
'''

import os

from jackit.config import JackitConfig

class SiteDeploymentError(Exception):
    '''
    Raised if there is an issue in the SiteDeploymentSingleton
    '''
    pass

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
        self._config = None

    @property
    def config(self):
        '''
        Getter for the config instance variable
        '''
        if self._config:
            return self._config
        else:
            raise SiteDeploymentError("Config not setup")

    @config.setter
    def config(self, value):
        if isinstance(value, JackitConfig):
            self._config = value
        else:
            raise SiteDeploymentError(
                "Unknown config object type. Expected JackitConfig, got {}".format(
                    type(value)
                )
            )

    def setup_config(self):
        '''
        Setup the config file
        '''
        self.config = JackitConfig(self.config_path)
        if not os.path.exists(self.config_path):
            self.config.save()

        self.config.load()

SiteDeployment = SiteDeploymentSingleton.instance()
