import json
import os.path
from app.tools.filter_tool import FilterTool

class FileReader(object):

    MAX_DOC_PER_FILE = 100000

    def find(self, search_context):
        counter = 0
        while True:
            counter += 1
            fname = 'data/data' + str(counter) + '.txt'
            if os.path.isfile(fname) is False:
                return None
            results = self.find_in_file(fname, search_context)
            if results not empty:
                return results

    def find_in_file(self, fname, search_context)
        file = open(fname, "r")
        results = []
        for line in file:
            doc = json.loads(line)
            if search_context.filter.match(doc):
                results.append(doc)
                if len(results) == search_context.size:
                    return results
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
            results = self.find_in_file(fname, SearchContext({'filter': {'id', id}, 'size': 1}))
            if results not empty:
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
