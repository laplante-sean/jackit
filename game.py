'''
Sets up site deployment and starts game
'''
import traceback
import os
import sys

if __name__ == "__main__":
    '''
    Any exceptions are printed to a bugreport.txt file
    '''
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
