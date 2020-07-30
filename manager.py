import os

import typer

manager = typer.Typer()


@manager.command()
def isort():
    os.system('pipenv run isort src')


@manager.command()
def flake8():
    os.system('pipenv run flake8 src')


@manager.command()
def yapf():
    os.system('pipenv run yapf -i -r src')


if __name__ == "__main__":
    manager()
