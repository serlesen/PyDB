import _pickle as pickle
import os.path

from app.tools.collection_locker import CollectionLocker, col_locking
from app.tools.filter_tool import FilterTool
from app.tools.database_context import DatabaseContext

class FileReader(object):

    @col_locking
    def find_all(self, col_meta_data):
        results = []
        for fname in col_meta_data.enumerate_data_fnames():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname

            if os.path.exists(pname) == False:
                return results

            with open(pname, "rb") as file:
                results.extend(pickle.load(file))
        return results

    @col_locking
    def find_by_line(self, col_meta_data, lines):
        lines_it = iter(lines)
        results = []
        try:
            l = next(lines_it)
            for i, fname in enumerate(col_meta_data.enumerate_data_fnames()):
                if l > (i + 1) * DatabaseContext.MAX_DOC_PER_FILE:
                    continue
                pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname
                with open(pname, "rb") as file:
                    current_docs = pickle.load(file)
                    while l < (i + 1) * DatabaseContext.MAX_DOC_PER_FILE:
                        current_line = l - i * DatabaseContext.MAX_DOC_PER_FILE
                        results.append(current_docs[current_line])
                        l = next(lines_it)
        except StopIteration:    
            return results

    def find_one_in_file(self, pname, filter_tool):
        with open(pname, "rb") as file:
            docs = pickle.load(file)
            for doc in docs:
                if filter_tool.match(doc):
                    return doc
            return None

    @col_locking
    def append_bulk(self, col_meta_data, input_docs):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname()
        if self.file_len(pname) >= DatabaseContext.MAX_DOC_PER_FILE:
           pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.next_data_fname() 

        if os.path.exists(pname):
            with open(pname, 'rb') as file:
                docs = pickle.load(file)
        else:
            docs = []
           
        CollectionLocker.lock_file(pname)

        with open(pname, 'wb') as file:
            for doc in input_docs:
                # FIXME inserts docs until max file is reached
                docs.append(self.normalize(doc))
            file.write(pickle.dumps(docs))

        CollectionLocker.unlock_file(pname)

        return "Done"

    @col_locking
    def append(self, col_meta_data, doc):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname()
        if self.file_len(pname) >= DatabaseContext.MAX_DOC_PER_FILE:
           pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.next_data_fname() 
 
        if os.path.exists(pname):
            with open(pname, 'rb') as file:
                docs = pickle.load(file)
        else:
            docs = []

        CollectionLocker.lock_file(pname)

        with open(pname, "wb") as file:
            normalized_doc = self.normalize(doc)
            docs.append(normalized_doc)
            file.write(pickle.dumps(docs))

        CollectionLocker.unlock_file(pname)

        return normalized_doc

    def file_len(self, pname):
        if os.path.exists(pname) is False:
            return 0
        with open(pname, 'rb') as file:
            docs = pickle.load(file)
            return len(docs)

    @col_locking
    def update(self, col_meta_data, id, input_doc):
        for fname in col_meta_data.enumerate_data_fnames():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname
            results = self.find_one_in_file(pname, FilterTool({'$filter': {'id': id}}))
            if results is not None:

                CollectionLocker.lock_file(pname)

                with open(pname, "rb+") as file:
                    docs = pickle.load(file)
                    file.seek(0)
                    file.truncate()
                    updated = None
                    for doc in docs:
                        if updated is None:
                            if doc["id"] == id:
                                docs.remove(doc)
                                normalized_doc = self.normalize(input_doc)
                                updated = normalized_doc
                                docs.append(normalized_doc)
                    file.write(pickle.dumps(docs))

                CollectionLocker.unlock_file(pname)

                return updated
        return []

    def normalize(self, doc):
        normalized_doc = {}
        for k in doc.keys():
            normalized_doc[k.lower()] = doc[k]
        return normalized_doc

