from setuptools import setup, find_packages

import ast


install_requires = [
    'click == 3.3'
]

test_require = [
    'pytest == 2.6.4',
]

docs_require = [
    'sphinx == 1.2.3',
]

def get_version(filename):
    with open(filename) as f:
        tree = ast.parse(f.read(), filename)
        for node in tree.body:
            if (isinstance(node, ast.Assign) and
                    node.targets[0].id == '__version__'):
                version = ast.literal_eval(node.value)
            if isinstance(version, tuple):
                version = '.'.join([str(x) for x in version])
        return version
    raise Exception('__version__ not found in {}'.format(filename))


setup(
    name='jinja-watcher',
    version=get_version('jinja_watcher/__init__.py'),
    author='Kang Hyojun',
    author_email='admire9@gmail.com',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=test_require,
    extras_require={
        'docs': docs_require,
        'tests': test_require
    },
    entry_points='''
        [console_scripts]
        jinja-watcher = jinja_watcher.cli:cli
    '''
)
