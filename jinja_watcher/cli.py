""" :mod:`jinja_watcher.cli` --- command line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import click

from .watch import JinjaFileEventHandler, start
from .util import render, read_from_json, context_from_file

__all__ = 'cli',

@click.command()
@click.option('--dest', 'dest', default='.',
              type=click.Path(exists=True),
              help='destination of compiled file')
@click.option('--env', 'env', default={})
@click.option('--excludes', '-E', 'excludes', multiple=True,
              default=['layout.html'])
@click.option('--verbose', '-v', is_flag=True)
@click.option('--watch', '-w', 'watch', is_flag=True)
@click.argument('src', type=click.Path(exists=True))
def cli(dest, env, src, excludes, verbose, watch):
    if src.endswith('.json'):
        config = read_from_json(src)
        src = config['src']
        dest = config.get('dest', dest)
        excludes = config.get('excludes', excludes)
        env = config.get('env', env)
        watch = config.get('watch', watch)
        verbose = config.get('verbose', verbose)
    if env:
        env = context_from_file(env)
    render(src, dest, env, excludes)
    if watch:
        handler = JinjaFileEventHandler(dest, env, excludes, verbose)
        start(src, handler)
