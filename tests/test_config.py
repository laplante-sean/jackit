'''
Test the JackitConfig class
'''

import os
import unittest
from jackit.config import JackitConfig, JsonConfig, ConfigError, JackitConfigControls,\
    JackitConfigCodeEditor

class TestJsonConfig(unittest.TestCase):
    '''
    Test the JSON config methods
    '''
    def setUp(self):
        '''
        Called before each test method is run
        '''
        self.config = JsonConfig()

    def test_valid_int(self):
        '''
        Test the validate_int method
        '''
        self.assertEqual(self.config.validate_int("10"), 10)
        self.assertEqual(self.config.validate_int(10), 10)

    def test_valid_uint(self):
        '''
        Test the validate_uint method
        '''
        self.assertEqual(self.config.validate_uint("10"), 10)
        self.assertEqual(self.config.validate_uint(10), 10)

    def test_invalid_int(self):
        '''
        Test the validate_int method with invalid values
        '''
        with self.assertRaises(ConfigError):
            self.config.validate_int([1, 2, 3, 4, 5])

        with self.assertRaises(ConfigError):
            self.config.validate_int("Invalid Int")

    def test_invalid_uint(self):
        '''
        Test the validate_uint method with invalid values
        '''
        with self.assertRaises(ConfigError):
            self.config.validate_uint("-1")

        with self.assertRaises(ConfigError):
            self.config.validate_uint(-1)

    def test_valid_bool(self):
        '''
        Test the validate_bool method
        '''
        self.assertEqual(self.config.validate_bool(False), False)
        self.assertEqual(self.config.validate_bool(True), True)

        for true_check in ("1", "true", "yes", "on", "t", "TRUE", "YES", "ON", "T"):
            self.assertEqual(self.config.validate_bool(true_check), True)

        for false_check in ("0", "false", "no", "off", "f", "FALSE", "NO", "OFF", "F"):
            self.assertEqual(self.config.validate_bool(false_check), False)

    def test_invalid_bool(self):
        '''
        Test the validate_bool method with invalid values
        '''
        with self.assertRaises(ConfigError):
            self.config.validate_bool(10)

        with self.assertRaises(ConfigError):
            self.config.validate_bool("boo")

class TestJackitConfig(unittest.TestCase):
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

    def test_valid_mode(self):
        '''
        Test all valid mode strings
        '''
        for valid_mode in ("production", "development", "dev", "debug"):
            self.config.mode = valid_mode

    def test_invalid_mode(self):
        '''
        Test mode setter with invalid mode values
        '''
        with self.assertRaises(ConfigError):
            self.config.mode = "boo"

class TestJackitConfigControls(unittest.TestCase):
    '''
    Test the JackitConfigControls methods
    '''
    def setUp(self):
        '''
        Called each time a test method is run
        '''
        self.controls = JackitConfigControls()

    def test_invalid_controls(self):
        '''
        Test from_json() with invalid control values
        '''
        with self.assertRaises(ConfigError):
            raw = {
                'up': 'blah',
                'down': 'blah1',
                'left': 'blah2',
                'right': 'blah3',
                'jump': 'blah4'
            }
            self.controls.from_json(raw)

    def test_duplicate_controls(self):
        '''
        Test from_json() with duplicate control values
        '''

        with self.assertRaises(ConfigError):
            raw = {
                'up': 'K_a',
                'down': 'K_a',
                'left': 'K_a',
                'right': 'K_d',
                'jump': 'K_SPACE'
            }
            self.controls.from_json(raw)

class TestJackitConfigCodeEditor(unittest.TestCase):
    '''
    Test the JackitConfigControls methods
    '''
    def setUp(self):
        '''
        Called each time a test method is run
        '''
        self.code_editor = JackitConfigCodeEditor()

    def test_valid_ubyte(self):
        '''
        Test the validate_ubyte method
        '''
        self.assertEqual(self.code_editor.validate_ubyte(200), 200)
        self.assertEqual(self.code_editor.validate_ubyte("200"), 200)

    def test_invalid_ubyte(self):
        '''
        Test the validate_ubyte method with invalid values
        '''
        with self.assertRaises(ConfigError):
            self.code_editor.validate_ubyte(256)

        with self.assertRaises(ConfigError):
            self.code_editor.validate_ubyte("256")

    def test_valid_color(self):
        '''
        Test the validate_color method
        '''
        self.assertEqual(self.code_editor.validate_color((0, 0, 0)), (0, 0, 0))
        self.assertEqual(self.code_editor.validate_color([0, 0, 0]), (0, 0, 0))
        self.assertEqual(self.code_editor.validate_color(("0", "0", "0")), (0, 0, 0))

    def test_invalid_color(self):
        '''
        Test the validate_color method with invalid colors
        '''
        with self.assertRaises(ConfigError):
            self.code_editor.validate_color(10)

        with self.assertRaises(ConfigError):
            self.code_editor.validate_color(("-1", 0, 10))
