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
                raise ConfigError("Invalid boolean value: {}".format(value))
            elif value.lower() in ("1", "true", "t", "yes", "on"):
                return True
            else:
                return False
        elif isinstance(value, bool):
            return value
        else:
            raise ConfigError("Unknown type for object. Expecting bool, got {}".format(
                type(value)
            ))

    def validate_uint(self, value):
        '''
        Validate an unsigned integer
        '''
        value = self.validate_int(value)
        if value < 0:
            raise ConfigError("Expected an unsigned integer. Got a negative number")
        return value

    def validate_int(self, value):
        '''
        Validate an integer value
        '''
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                raise ConfigError("Invalid integer value: {}".format(value))
        elif isinstance(value, int):
            return value
        else:
            raise ConfigError("Unknown type object. Expecting 'int', got: {}".format(
                type(value)
            ))

class JackitConfigCodeEditor(JsonConfig):
    '''
    Class for configuring and validating code editor settings
    '''
    def __init__(self):
        super(JackitConfigCodeEditor, self).__init__()
        self.bg_alpha = 235
        self.bg_color = (0, 0, 0) # Black
        self.font_antialiasing = True
        self.font_color = (0, 255, 0) # Green
        self.key_repeat_delay = 500 # Delay before first repeated key
        self.key_repeat_interval = 30 # Dealy between each repeated key after first
        self.cursor_color = (255, 255, 255) # White
        self.cursor_alpha = 175
        self.tab_size = 4 # Number of spaces for tab
        self.font_size = 16

    def from_json(self, raw):
        '''
        Load the object from JSON laoded from config file
        '''
        self.bg_alpha = self.validate_ubyte(raw.get("bg_alpha", 235))
        self.bg_color = self.validate_color(raw.get("bg_color", (0, 0, 0)))
        self.font_antialiasing = self.validate_bool(raw.get("font_antialiasing", True))
        self.font_color = self.validate_color(raw.get("font_color", (0, 255, 0)))
        self.key_repeat_delay = self.validate_uint(raw.get("key_repeat_delay", 500))
        self.key_repeat_interval = self.validate_uint(raw.get("key_repeat_interval", 30))
        self.cursor_color = self.validate_color(raw.get("cursor_color", (255, 255, 255)))
        self.cursor_alpha = self.validate_ubyte(raw.get("cursor_alpha", 175))
        self.tab_size = self.validate_uint(raw.get("tab_size", 4))
        self.font_size = self.validate_uint(raw.get("font_size", 16))

    def to_json(self):
        '''
        Return a dict representation of the object
        '''
        return {
            "bg_alpha": self.bg_alpha,
            "bg_color": self.bg_color,
            "font_antialiasing": self.font_antialiasing,
            "font_color": self.font_color,
            "key_repeat_delay": self.key_repeat_delay,
            "key_repeat_interval": self.key_repeat_interval,
            "cursor_color": self.cursor_color,
            "cursor_alpha": self.cursor_alpha,
            "tab_size": self.tab_size,
            "font_size": self.font_size
        }

    def validate_ubyte(self, value):
        '''
        Validate an unsigned byte value
        '''
        value = self.validate_int(value)
        if value < 0 or value > 255:
            raise ConfigError("Unsigned byte must be between 0 and 255 inclusive")
        return value

    def validate_color(self, value):
        '''
        Validate a color value from the config
        '''
        if isinstance(value, tuple) or isinstance(value, list):
            if len(value) != 3:
                raise ConfigError("Colors must be tuples of 3 values representing R, G, B")

            new_list = []
            for color_val in value:
                new_list.append(self.validate_ubyte(color_val))

            return tuple(new_list)
        else:
            raise ConfigError("Colors must be a list or tuple of 3 unsigned byte values")


class JackitConfigControls(JsonConfig):
    '''
    Class for configuring and validating Jackit controls
    '''
    def __init__(self):
        super(JackitConfigControls, self).__init__()
        self.up = pygame.K_w
        self.down = pygame.K_s
        self.left = pygame.K_a
        self.right = pygame.K_d
        self.jump = pygame.K_SPACE
        self.interact = pygame.K_e
        self.push = pygame.K_LSHIFT
        self.reset_code = pygame.K_q
        self.toggle_sound = pygame.K_m
        self.kill_self = pygame.K_k

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
        self.push = raw.get("push", getattr(pygame, "K_LSHIFT"))
        self.reset_code = raw.get("reset_code", getattr(pygame, "K_q"))
        self.toggle_sound = raw.get("toggle_sound", getattr(pygame, "K_m"))
        self.kill_self = raw.get("kill_self", getattr(pygame, "K_k"))

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
            'interact': self.interact,
            'push': self.push,
            'reset_code': self.reset_code,
            'toggle_sound': self.toggle_sound,
            'kill_self': self.kill_self
        }

class JackitLeaderboard(JsonConfig):
    '''
    Config for connection to the leaderboard
    '''
    def __init__(self):
        super(JackitLeaderboard, self).__init__()
        self.submission_url = "https://www.jackit.io/leaderboard/submit/"

    def to_json(self):
        '''
        Return a dict representation of the object
        '''
        return {
            'submission_url': self.submission_url
        }

    def from_json(self, raw):
        '''
        Parse the config from JSON
        '''
        self.submission_url = raw.get("submission_url", "https://www.jackit.io/leaderboard/submit/")

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
        self.accurate_framerate = True
        self.sound_enabled = True
        self.controls = JackitConfigControls()
        self.code_editor = JackitConfigCodeEditor()
        self.leaderboard = JackitLeaderboard()

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
        self._width = self.validate_uint(value)

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
        self._height = self.validate_uint(value)

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
        self._framerate = self.validate_uint(value)

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
            "controls": self.controls.to_json(),
            "code_editor": self.code_editor.to_json(),
            "accurate_framerate": self.accurate_framerate,
            "leaderboard": self.leaderboard.to_json(),
            "sound_enabled": self.sound_enabled
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
        self.code_editor.from_json(raw.get("code_editor", self.code_editor.to_json()))
        self.accurate_framerate = self.validate_bool(raw.get("accurate_framerate", True))
        self.leaderboard.from_json(raw.get("leaderboard", self.leaderboard.to_json()))
        self.sound_enabled = self.validate_bool(raw.get("sound_enabled", True))

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
