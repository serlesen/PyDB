import _pickle as pickle
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
        with open(pname, "rb") as file:
            results = []
            docs = pickle.load(file)
            for doc in docs:
                if search_context.filter.match(doc):
                    results.append(doc)
                    if len(results) == search_context.size:
                        return results
            return results

    def append_bulk(self, col_meta_data, input_docs):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname()
        if self.file_len(pname) >= DatabaseContext.MAX_DOC_PER_FILE:
           pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.next_data_fname() 

        if os.path.exists(pname):
            with open(pname, 'rb') as file:
                docs = pickle.load(file)
        else:
            docs = []
           
        with open(pname, 'wb') as file:
            for doc in input_docs:
                # FIXME inserts docs until max file is reached
                docs.append(self.normalize(doc))
            file.write(pickle.dumps(docs))
        return "Done"

    def append(self, col_meta_data, doc):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname()
        if self.file_len(pname) >= DatabaseContext.MAX_DOC_PER_FILE:
           pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.next_data_fname() 
 
        if os.path.exists(pname):
            with open(pname, 'rb') as file:
                docs = pickle.load(file)
        else:
            docs = []

        with open(pname, "wb") as file:
            normalized_doc = self.normalize(doc)
            docs.append(normalized_doc)
            file.write(pickle.dumps(docs))
        return normalized_doc

    def file_len(self, pname):
        if os.path.exists(pname) is False:
            return 0
        with open(pname, 'rb') as file:
            docs = pickle.load(file)
            return len(docs)

    def update(self, col_meta_data, id, input_doc):
        for fname in col_meta_data.enumerate_data_fnames():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname
            results = self.find_in_file(pname, SearchContext({'$filter': {'id': id}, 'size': 1}))
            if len(results) > 0:
                with open(pname, "rb+") as file:
                    docs = pickle.load(file)
                    file.seek(0)
                    file.truncate()
                    updated = None
                    for doc in docs:
                        if updated is None:
                            if doc["id"] == id:
                                docs.remove(doc)
                                if input_doc is None:
                                    updated = doc
                                else:
                                    normalized_doc = self.normalize(input_doc)
                                    updated = normalized_doc
                                    docs.append(normalized_doc)
                    file.write(pickle.dumps(docs))

                if input_doc is None and self.file_len(pname) == 0:
                    col_meta_data.remove_last_data_file()
                return updated
        return None

    def normalize(self, doc):
        normalized_doc = {}
        for k in doc.keys():
            normalized_doc[k.lower()] = doc[k]
        return normalized_doc

