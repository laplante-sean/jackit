'''
Config for jackit
'''

import json
import pygame

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

class JackitConfigControls:
    '''
    Class for configuring and validating Jackit controls
    '''

    def __init__(self):
        self.up = pygame.K_w
        self.down = pygame.K_s
        self.left = pygame.K_a
        self.right = pygame.K_d
        self.jump = pygame.K_SPACE
        self.interact = pygame.K_e

    def from_json(self, raw):
        '''
        Load the object from JSON loaded from config file
        '''

        # First pass make sure all are valid
        for key in raw:
            if isinstance(raw[key], str):
                if not hasattr(pygame, raw[key]):
                    raise ConfigError(
                        "Invalid control for {}. Must be a valid pygame key constant".format(key)
                    )
                else:
                    raw[key] = getattr(pygame, raw[key])
            elif isinstance(raw[key], int):
                pass
            else:
                raise ConfigError(
                    "Controls must be a valid pygame key constant as a string or integer"
                )

        # Check for duplicates
        values = list(raw.values())
        values_set = set(values)

        if len(values) != len(values_set):
            raise ConfigError("Cannot have duplicate controls")

        self.up = raw.get('up', getattr(pygame, 'K_w'))
        self.down = raw.get('down', getattr(pygame, 'K_s'))
        self.left = raw.get('left', getattr(pygame, 'K_a'))
        self.right = raw.get('right', getattr(pygame, 'K_d'))
        self.jump = raw.get('jump', getattr(pygame, 'K_SPACE'))
        self.interact = raw.get('interact', getattr(pygame, 'K_e'))

    def to_json(self):
        '''
        Return a dict representation of the object
        '''
        return {
            'up': self.up,
            'down': self.down,
            'left': self.left,
            'right': self.right,
            'jump': self.jump,
            'interact': self.interact
        }

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
        self.controls = JackitConfigControls()

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
            "controls": self.controls.to_json()
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
        self.controls = JackitConfigControls()
        self.controls.from_json(raw.get('controls', self.controls.to_json()))

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
