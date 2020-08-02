"""
Populate database with fake data for development purposes

@author: Jad Haddad <jad.haddad92@gmail.com> 2020
"""

from random import randint

import click

from . import Database
from .schema import Apps, Leaderboards, Users


@click.command(context_settings=dict(show_default=True))
@click.option('--num_users', 'numUsers', type=int, default=100,
              help="Number of users")
@click.option('--num_apps', 'numApps', type=int, default=5,
              help="Number of apps")
@click.option('--num_scores_type', 'numScoresType', type=int, default=4,
              help="Number of score type")
@click.option('--reinit', 'reInit', is_flag=None, flag_value=True,
              help="Delete all rows from database before inserting new ones")
def populate(numUsers: int, numApps: int, numScoresType: int, reInit: bool):
    """ Insert Fake data in database
    """
    with Database().transaction() as store:
        if reInit:
            store.query(Users).delete()
            store.query(Apps).delete()
        
        users = [ Users(id=i, nickname=f'user_{i}') for i in range(numUsers) ]
        apps = [ Apps(name=f'app_{i}') for i in range(numApps) ]
        store.bulk_save_objects(apps)
        store.bulk_save_objects(users)
        
        leaderboards = []
        for app in store.query(Apps).all():
            store.merge(app)
            appId = app.id
            for scoreName in range(numScoresType):
                leaderboards.extend(
                    [ Leaderboards(scoreName=f'score{scoreName}', appId=appId,
                                   userId=user.id, value=randint(0, 100))
                      for user in users ]
                )
        store.bulk_save_objects(leaderboards)

if __name__ == '__main__':
    populate() # pylint: disable=no-value-for-parameter