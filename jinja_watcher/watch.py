import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .util import render

__all__ = 'start', 'JinjaFileEventHandler',

class JinjaFileEventHandler(FileSystemEventHandler):

    def __init__(self, dest, env, excludes, verbose=False):
        super(JinjaFileEventHandler, self).__init__()
        self.dest = dest
        self.env = env
        self.excludes = excludes
        self.verbose = verbose

    def log(self, event, name):
        what = 'directory' if event.is_directory else 'file'
        if self.verbose:
            print('{} {} {}'.format(what, event.src_path, name))

    def on_moved(self, event):
        super(JinjaFileEventHandler, self).on_moved(event)
        self.log(event, 'moved')

    def on_created(self, event):
        super(JinjaFileEventHandler, self).on_created(event)
        self.log(event, 'created')

    def on_deleted(self, event):
        super(JinjaFileEventHandler, self).on_deleted(event)
        self.log(event, 'deleted')

    def on_modified(self, event):
        super(JinjaFileEventHandler, self).on_modified(event)
        if event.is_directory:
            render(event.src_path, self.dest, self.env, self.excludes)
            if self.verbose:
                print('compiled')


def start(path, handler):
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
