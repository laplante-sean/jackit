# JackIT!!! The Game

2D Side Scroller platforming game where you have to modify the game's source code to complete levels

### Install

1. clone repo
2. have python 3.5
3. `pip install -r requirements.txt`
4. `python3 game.py`

### Playing

1. Once the game loads there will be a welcome screen. Press enter to start playing
1. Controls are "A" for left, "D" for right, "SPACE" for jump, "E" for interact, and "ESC" to get out of a code editor
1. In the code editor use the arrow keys to move the cursor and the keyboard to type.
1. All the code you type is run by the game. There are some protections but it's not perfect. You can pretty much do anything.
1. a config file `site.cfg.json` is created in the root of the repo when the game is run. You can modify this file, but I wouldn't. A lot of the config options have only been tested with their default values.

#### If you want to use pygame_sdl2 (optional)

_This is not optional on Mac OS X 10.12.2 because of a bug in pygame_
_https://bitbucket.org/pygame/pygame/issues/320/wont-start-on-mac-os-x-10122-on-python-352#comment-33011207_

1. clone https://github.com/renpy/pygame_sdl2
1. Follow installation instructions for your OS
1. Run jackit with `python3 game.py --sdl2`

### Web Leaderboard

#### Running the dev server

1. Run migrations

```
python3 manage.py migrate
```

1. Create the superuser

```
python3 manage.py createsuperuser
```

1. Run the dev server

```
python3 manage.py runserver
```

#### Updating database with changes to the DB models

1. Make migrations

```
python3 manage.py makemigrations leaderboard
```

1. Optionally, look at what will change with `migrate`

```
python3 manage.py sqlmigrate leaderboard <id_from_makemigrations>
```

1. Finally, run `migrate` to actually commit the changes

```
python3 manage.py migrate
```
