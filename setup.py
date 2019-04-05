'''
Bundle into a Windows executable with  `python setup.py build_exe`
'''
from cx_Freeze import setup, Executable

setup(
    name="jackit",
    version="1.0",
    description="Program the game to win!",
    options={
        "build_exe": {
            "includes": [
                "deploy.py"
            ],
            "excludes": [
                "django",
                "jackitio",
                "tests"
            ],
            "packages": [
                "requests",
                "queue",
                "idna"
            ],
            "include_files": [
                ("gen.dump", "lib/gen.dump")
            ]
        }
    },
    executables=[
        Executable("game.py")
    ]
)
