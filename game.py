'''
Sets up site deployment and starts game
'''
import traceback
import os
import sys
import argparse

if __name__ == "__main__":
    '''
    Any exceptions are printed to a bugreport.txt file
    '''
    parser = argparse.ArgumentParser(description='JackIT! The Game!')
    parser.add_argument(
        '--sdl2', action="store_true", help="Run using pygame_sdl2 if it's installed")
    args = parser.parse_args()

    if args.sdl2:
        print("Using pygame SDL2")
        try:
            import pygame_sdl2
            pygame_sdl2.import_as_pygame()
        except ImportError as e:
            print("Unable to load pygame_sdl2: ", str(e))
            print("Is it installed? See https://github.com/renpy/pygame_sdl2 for instructions")
            print("Default pygame will be used")
    else:
        print("Using pygame")

    try:
        from deploy import SiteDeployment
        from jackit import JackitGame
        from jackit.config import ConfigError
        SiteDeployment.setup_config()
        JackitGame.run()
    except ConfigError as e:
        print("Invalid config: {}. Please fix {}".format(str(e), SiteDeployment.config_path))
    except BaseException as e:
        print("Exception during game execution. See {}\nException: {}".format(
            os.path.join(SiteDeployment.base_path, "bugreport.txt"), str(e)
        ))

        with open(os.path.join(os.path.dirname(__file__), "bugreport.txt"), 'w') as f:
            traceback.print_exc(file=f)
        sys.exit(1)
    sys.exit(0)
