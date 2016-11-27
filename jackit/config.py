'''
Config for jackit
'''

import json

class ConfigError(Exception):
    '''
    Error during loading/saving/parsing of JSON config
    '''
    pass

class JackitConfig:
    '''
    Jackit config class
    '''

    def __init__(self, path):
        super(JackitConfig, self).__init__()
        self.path = path
        self.resolution = (800, 600)
        self._mode = "production"

    @property
    def mode(self):
        '''
        Handles getting the value of mode
        '''
        return self._mode

    @mode.setter
    def mode(self, value):
        '''
        Handles setting mode and validating the value
        '''

        if value not in ("production", "development", "dev", "debug"):
            raise ConfigError(
                "Invalid mode {}. Expected one of: production, development, dev, or debug".format(
                    value
                )
            )

        self._mode = value

    def to_json(self):
        '''
        JSON representation of config options
        '''
        return {
            "width": self.resolution[0],
            "height": self.resolution[1],
            "mode": self.mode
        }

    def from_json(self, raw):
        '''
        Load values from JSON
        '''
        self.mode = raw.get("mode", "production")
        self.resolution = (raw.get("width", 800), raw.get("height", 600))

    def load(self):
        '''
        Load config file
        '''
        try:
            with open(self.path, 'r') as f:
                self.from_json(json.loads(f.read()))
        except json.JSONDecodeError:
            raise ConfigError("Unable to load config file. Invalid JSON")
        except IOError as e:
            raise ConfigError("Could not access file {}. {}".format(self.path, str(e)))
        except BaseException as e:
            raise ConfigError("Unkown error loading config: {}".format(str(e)))

    def save(self):
        '''
        Save config file
        '''
        try:
            with open(self.path, 'w') as f:
                f.write(json.dumps(
                    self.to_json(),
                    sort_keys=True,
                    separators=(',', ': '),
                    indent=4
                ))
        except IOError as e:
            raise ConfigError("Could not access file {}. {}".format(self.path, str(e)))
        except BaseException as e:
            raise ConfigError("Unknown error saving config: {}".format(str(e)))

    def is_development_mode(self):
        '''
        Check if the current config is development
        '''
        return self.mode in ("development", "debug", "dev")
