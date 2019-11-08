import json
import os.path

from app.tools.filter_tool import FilterTool
from app.tools.search_context import SearchContext
from app.tools.database_context import DatabaseContext

class FileReader(object):

    def find(self, collection, search_context):
        counter = 0
        while True:
            counter += 1
            fname = DatabaseContext.DATA_FOLDER + collection + '/data' + str(counter) + '.txt'
            if os.path.isfile(fname) is False:
                return None
            results = self.find_in_file(fname, search_context)
            if len(results) > 0:
                return results

    def find_in_file(self, fname, search_context):
        with open(fname, "r") as file:
            results = []
            for line in file:
                doc = json.loads(line)
                if search_context.filter.match(doc):
                    results.append(doc)
                    if len(results) == search_context.size:
                        return results
            return results

    def append_bulk(self, collection, docs):
        counter = 0
        while True:
            counter += 1
            fname = DatabaseContext.DATA_FOLDER + collection + '/data' + str(counter) + '.txt'
            if os.path.isfile(fname):
                size = self.file_len(fname)
                if size >= DatabaseContext.MAX_DOC_PER_FILE:
                    continue
            with open(fname, "a") as file:
                for doc in docs:
                    normalized_doc = self.normalize(doc)
                    file.write(json.dumps(normalized_doc) + '\n')
                return "Done"
        return None

    def append(self, collection, doc):
        counter = 0
        while True:
            counter += 1
            fname = DatabaseContext.DATA_FOLDER + collection + '/data' + str(counter) + '.txt'
            if os.path.isfile(fname):
                if self.file_len(fname) >= DatabaseContext.MAX_DOC_PER_FILE:
                    continue
            with open(fname, "a") as file:
                normalized_doc = self.normalize(doc)
                file.write(json.dumps(normalized_doc) + '\n')
                return normalized_doc
        return None

    def file_len(self, fname):
        i = 0
        with open(fname) as f:
            for i, l in enumerate(f, 1):
                pass
        return i

    def update(self, collection, id, doc):
        counter = 0
        while True:
            counter += 1
            fname = DatabaseContext.DATA_FOLDER + collection + '/data' + str(counter) + '.txt'
            if os.path.isfile(fname) is False:
                return None
            results = self.find_in_file(fname, SearchContext({'filter': {'id': id}, 'size': 1}))
            if len(results) > 0:
                with open(fname, "r+") as file:
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
                                line = json.dumps(normalized_doc) + '\n'
                        file.write(line)
                    return updated

    def normalize(self, doc):
        normalized_doc = {}
        for k in doc.keys():
            normalized_doc[k.lower()] = doc[k]
        return normalized_doc

