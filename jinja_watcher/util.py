import os
import errno
import json

from jinja2 import FileSystemLoader, Environment

__all__ = 'ensure_directory', 'context_from_file', 'render',


def read_from_json(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())


def ensure_directory(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass


def context_from_file(filename):
    config = {}
    with open(filename) as context_file:
        exec(compile(context_file.read(), filename, 'exec'), config)
        return dict((k, v) for k, v in config.items() if k.isupper())


def find_templates(path):
    for root, dir_, tempnames in os.walk(path):
        for tempname in tempnames:
            root_without_par = os.path.join(root.replace(path, ''))
            if root_without_par.startswith('/'):
                root_without_par = root_without_par[1:]
            if tempname.endswith('.html'):
                yield os.path.join(root_without_par, tempname)


def render(path, out=None, context={}, excludes=[]):
    if not out:
        out = path
    out = os.path.abspath(out)
    env = Environment(loader=FileSystemLoader(path))
    for template in find_templates(path):
        temp = env.get_template(template)
        out_file = os.path.join(out, template)
        ensure_directory(os.path.dirname(out_file))
        with open(out_file, 'w') as f:
            if not template in excludes:
                f.write(temp.render(context))
