import _pickle as pickle
import os.path

from app.tools.filter_tool import FilterTool
from app.tools.database_context import DatabaseContext

class FileReader(object):

    def find_all(self, col_meta_data):
        results = []
        for fname in col_meta_data.enumerate_data_fnames():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname
            with open(pname, "rb") as file:
                results.extend(pickle.load(file))
        return results

    def find_one_in_file(self, pname, filter_tool):
        with open(pname, "rb") as file:
            docs = pickle.load(file)
            for doc in docs:
                if filter_tool.match(doc):
                    return doc
            return None

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

    # TODO also update the index
    def update(self, col_meta_data, id, input_doc):
        for fname in col_meta_data.enumerate_data_fnames():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname
            results = self.find_one_in_file(pname, FilterTool({'$filter': {'id': id}, 'size': 1}))
            if results is not None:
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
        return []

    def normalize(self, doc):
        normalized_doc = {}
        for k in doc.keys():
            normalized_doc[k.lower()] = doc[k]
        return normalized_doc

