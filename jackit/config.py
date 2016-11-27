'''
Config for jackit
'''

import json

class ConfigError(Exception):
    '''
    Error during loading/saving/parsing of JSON config
    '''
    pass

class JsonConfig:
    '''
    Base class for config
    '''
    def __init__(self):
        pass

    def validate_bool(self, value):
        '''
        Validate a boolean value
        '''
        if isinstance(value, str):
            if value.lower() not in ("1", "0", "true", "false", "t", "f", "yes", "no", "on", "off"):
                raise ConfigError("Invalid boolean value for option 'fullscreen': {}".format(value))
            elif value.lower() in ("1", "true", "t", "yes", "on"):
                return True
            else:
                return False
        elif isinstance(value, bool):
            return value
        else:
            raise ConfigError("Unknown type for option 'fullscreen'. Expecting bool, got {}".format(
                type(value)
            ))

    def validate_int(self, value):
        '''
        Validate an integer value
        '''
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                raise ConfigError("Invalid integer value for option 'width': {}".format(value))
        elif isinstance(value, int):
            return value
        else:
            raise ConfigError("Unknown type for option 'width'. Expecting int, got {}".format(
                type(value)
            ))

class JackitConfig(JsonConfig):
    '''
    Jackit config class
    '''
    def __init__(self, path):
        super(JackitConfig, self).__init__()
        self.path = path
        self._width = 800
        self._height = 600
        self._framerate = 60
        self._mode = "production"
        self._fullscreen = False

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

    @property
    def fullscreen(self):
        '''
        Get current value of fullscreen
        '''
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        '''
        Set the value of fullscreen and validate
        '''
        self._fullscreen = self.validate_bool(value)

    @property
    def width(self):
        '''
        Get the current value of width
        '''
        return self._width

    @width.setter
    def width(self, value):
        '''
        Set the value of width and validate
        '''
        self._width = self.validate_int(value)

    @property
    def height(self):
        '''
        Get the value of height
        '''
        return self._height

    @height.setter
    def height(self, value):
        '''
        Set the value of height and validate
        '''
        self._height = self.validate_int(value)

    @property
    def framerate(self):
        '''
        Get the value of framerate
        '''
        return self._framerate

    @framerate.setter
    def framerate(self, value):
        '''
        Set the value of framerate and validate
        '''
        self._framerate = self.validate_int(value)

    def to_json(self):
        '''
        JSON representation of config options
        '''
        return {
            "resolution": {
                "width": self.width,
                "height": self.height
            },
            "mode": self.mode,
            "fullscreen": self.fullscreen,
            "framerate": self.framerate,
        }

    def from_json(self, raw):
        '''
        Load values from JSON
        '''
        self.mode = raw.get("mode", "production")
        res = raw.get("resolution", {"width":800, "height":600})
        self.width = res.get("width", 800)
        self.height = res.get("height", 600)
        self.fullscreen = raw.get("fullscreen", False)
        self.framerate = raw.get("framerate", 60)

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
