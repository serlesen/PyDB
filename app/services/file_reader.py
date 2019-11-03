import json
import os.path

class FileReader(object):

    MAX_DOC_PER_FILE = 1000

    def find(self, key, value):
        counter = 0
        while True:
            counter += 1
            fname = 'data/data' + str(counter) + '.txt'
            if os.path.isfile(fname) is False:
                return None
            result = self.find_in_file(fname, key, value)
            if result is not None:
                return result

    def find_in_file(self, fname, key, value):
        file = open(fname, "r")
        for line in file:
            doc = json.loads(line)
            if key in doc and doc[key] == value:
                return doc
        return None

    def append(self, doc):
        counter = 0
        while True:
            counter += 1
            fname = 'data/data' + str(counter) + '.txt'
            if os.path.isfile(fname):
                if self.file_len(fname) > self.MAX_DOC_PER_FILE:
                    continue
            file = open(fname, "a")
            normalized_doc = self.normalize(doc)
            file.write(self.to_str(normalized_doc) + '\n')
            return normalized_doc
        return None

    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def update(self, id, doc):
        counter = 0
        while True:
            counter += 1
            fname = 'data/data' + str(counter) + '.txt'
            if os.path.isfile(fname) is False:
                return None
            result = self.find_in_file(fname, 'id', id)
            if result is not None:
                file = open(fname, "r+")
                lines = file.readlines()
                file.seek(0)
                file.truncate()
                updated = None
                for line in lines:
                    if updated is None:
                        current_doc = json.loads(line)
                        if current_doc["id"] == id:
                            if doc is None:
                                updated = current_doc
                                continue
                            normalized_doc = self.normalize(doc)
                            updated = normalized_doc
                            line = self.to_str(normalized_doc) + '\n'
                    file.write(line)
                return updated

    def normalize(self, doc):
        normalized_doc = {}
        for k in doc.keys():
            normalized_doc[k.lower()] = doc[k]
        return normalized_doc

    def to_str(self, doc):
        return str(doc).replace('\'', '"')
