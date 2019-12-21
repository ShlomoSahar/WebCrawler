from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DirectoryWatcher(FileSystemEventHandler):

    patterns = ["*.*"]

    def __init__(self, path, handler):
        self.observer = Observer()
        self.observer.schedule(self, path = path)
        self.handler = handler

    def start(self):
        self.observer.start()

    def process(self, event):
        self.handler.handle(event.src_path, event.event_type, event.is_directory)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)
