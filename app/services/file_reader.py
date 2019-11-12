import json
import os.path

from app.tools.filter_tool import FilterTool
from app.tools.search_context import SearchContext
from app.tools.database_context import DatabaseContext

class FileReader(object):

    def find(self, col_meta_data, search_context):
        for fname in col_meta_data.enumerate_data_fnames():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname
            results = self.find_in_file(pname, search_context)
            if len(results) > 0:
                return results
        return None

    def find_in_file(self, pname, search_context):
        with open(pname, "r") as file:
            results = []
            for line in file:
                doc = json.loads(line)
                if search_context.filter.match(doc):
                    results.append(doc)
                    if len(results) == search_context.size:
                        return results
            return results

    def append_bulk(self, col_meta_data, docs):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname()
        if self.file_len(pname) >= DatabaseContext.MAX_DOC_PER_FILE:
           pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.next_data_fname() 
           
        with open(pname, "a") as file:
            for doc in docs:
                # FIXME inserts docs until max file is reached
                normalized_doc = self.normalize(doc)
                file.write(json.dumps(normalized_doc) + '\n')
        return "Done"

    def append(self, col_meta_data, doc):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname()
        if self.file_len(pname) >= DatabaseContext.MAX_DOC_PER_FILE:
           pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.next_data_fname() 
 
        with open(pname, "a") as file:
            normalized_doc = self.normalize(doc)
            file.write(json.dumps(normalized_doc) + '\n')
        return normalized_doc

    def file_len(self, pname):
        if os.path.exists(pname) is False:
            return 0
        i = 0
        with open(pname) as f:
            for line in f:
                i += 1
        return i

    def update(self, col_meta_data, id, doc):
        for fname in col_meta_data.enumerate_data_fnames():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname
            results = self.find_in_file(pname, SearchContext({'$filter': {'id': id}, 'size': 1}))
            if len(results) > 0:
                with open(pname, "r+") as file:
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
                if self.file_len(pname) == 0:
                    col_meta_data.remove_last_data_file()
                return updated
        return None

    def normalize(self, doc):
        normalized_doc = {}
        for k in doc.keys():
            normalized_doc[k.lower()] = doc[k]
        return normalized_doc

