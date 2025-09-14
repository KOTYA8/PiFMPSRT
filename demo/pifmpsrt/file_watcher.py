import os
import time

class FileWatcher:
    def __init__(self, filename="file.txt"):
        self.filename = filename
        self.last_content = ""
        self.last_mtime = 0
        self.last_update_time = 0  # время последнего изменения текста

    def read(self):
        """Читает файл и возвращает текст. Следит за изменениями"""
        try:
            mtime = os.path.getmtime(self.filename)
            if mtime != self.last_mtime:
                with open(self.filename, "r", encoding="utf-8") as f:
                    content = f.read().strip("\n\r")
                self.last_content = content
                self.last_mtime = mtime
                self.last_update_time = time.time()
        except FileNotFoundError:
            return ""
        return self.last_content

    def changed_recently(self, expire_time=None):
        """True если файл менялся в пределах expire_time"""
        if expire_time is None:
            return True
        return (time.time() - self.last_update_time) <= expire_time
