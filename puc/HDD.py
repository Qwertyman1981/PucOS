import os

class HDD
    def __init__(self, storage_dir=Storage)
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def list_files(self)
        return os.listdir(self.storage_dir)

    def read(self, filename)
        path = os.path.join(self.storage_dir, filename)
        if not os.path.exists(path)
            return None
        with open(path, r, encoding=utf-8) as f
            return f.read()

    def write(self, filename, data)
        path = os.path.join(self.storage_dir, filename)
        with open(path, w, encoding=utf-8) as f
            f.write(data)

    def delete(self, filename)
        path = os.path.join(self.storage_dir, filename)
        if os.path.exists(path)
            os.remove(path)
