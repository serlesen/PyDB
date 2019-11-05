import json
import os.path
from app.tools.query_tool import QueryTool

class FileReader(object):

    MAX_DOC_PER_FILE = 100000

    def find(self, query):
        counter = 0
        while True:
            counter += 1
            fname = 'data/data' + str(counter) + '.txt'
            if os.path.isfile(fname) is False:
                return None
            results = self.find_in_file(fname, query)
            if len(results) > 0:
                return results

    def find_in_file(self, fname, query):
        file = open(fname, "r")
        results = []
        for line in file:
            doc = json.loads(line)
            if query.match(doc):
                results.append(doc)
        return results

    def append_bulk(self, docs):
        counter = 0
        while True:
            counter += 1
            fname = 'data/data' + str(counter) + '.txt'
            if os.path.isfile(fname):
                size = self.file_len(fname)
                if size > self.MAX_DOC_PER_FILE:
                    continue
            file = open(fname, "a")
            for doc in docs:
                normalized_doc = self.normalize(doc)
                file.write(self.to_str(normalized_doc) + '\n')
            return "Done"
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
            results = self.find_in_file(fname, QueryTool({'filter': {'id', id}}))
            if len(results) > 0:
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
