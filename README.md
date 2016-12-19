# JackIT!!! The Game

#### Install

1. clone
2. have python 3.5
3. `pip install -r requirements.txt`
4. `python game.py`

#### Leaderboard

##### Running the dev server

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
