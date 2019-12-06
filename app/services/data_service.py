import _pickle as pickle
import os.path

from app.services.files_reader import FilesReader
from app.tools.collection_locker import CollectionLocker, col_locking
from app.tools.filter_tool import FilterTool
from app.tools.database_context import DatabaseContext

#
# Class to read (without conditions or only some given lines), append and update a data file.
# A bulk append method is created, but only for debug purpose.
#
class DataService(object):

    @col_locking
    def find_all(self, col_meta_data, thread_id):
        results = []
        for fname in col_meta_data.enumerate_data_fnames(thread_id):
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname

            if os.path.exists(pname) == False:
                return results

            results.extend(FilesReader.get_instance().get_file_content(pname))

        return results

    @col_locking
    def find_by_line(self, col_meta_data, lines, thread_id):
        lines_it = iter(lines)
        results = []
        try:
            l = next(lines_it)
            for i, fname in enumerate(col_meta_data.enumerate_data_fnames(None)):
                if self.is_line_in_current_file(l, i) == False:
                    continue
                while self.is_line_in_current_file(l, i):
                    if thread_id == None or ((i + 1) % DatabaseContext.MAX_THREADS) == thread_id:
                        # the desired line is in the current data file for the desired thread
                        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname

                        current_docs = FilesReader.get_instance().get_file_content(pname)
                        
                        while self.is_line_in_current_file(l, i):
                            current_line = l - i * DatabaseContext.MAX_DOC_PER_FILE
                            results.append(current_docs[current_line])
                            l = next(lines_it)
                    else:
                        l = next(lines_it)
        except StopIteration:    
            pass
        return results

    def is_line_in_current_file(self, line, index_file):
        return line >= index_file * DatabaseContext.MAX_DOC_PER_FILE and line < (index_file + 1) * DatabaseContext.MAX_DOC_PER_FILE

    def find_one_in_file(self, pname, filter_tool):
        docs = FilesReader.get_instance().get_file_content(pname)
        
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
            docs = FilesReader.get_instance().get_file_content(pname)
        else:
            docs = []

        for doc in input_docs:
            # FIXME inserts docs until max file is reached
            docs.append(self.normalize(doc))

        FilesReader.get_instance().write_file_content(pname, docs)

        return "Done"

    @col_locking
    def append(self, col_meta_data, doc):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname()
        if self.file_len(pname) >= DatabaseContext.MAX_DOC_PER_FILE:
           pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.next_data_fname() 
 
        if os.path.exists(pname):
            docs = FilesReader.get_instance().get_file_content(pname)
        else:
            docs = []

        normalized_doc = self.normalize(doc)
        docs.append(normalized_doc)

        FilesReader.get_instance().write_file_content(pname, docs)

        return normalized_doc

    def file_len(self, pname):
        if os.path.exists(pname) is False:
            return 0
        
        docs = FilesReader.get_instance().get_file_content(pname)
        return len(docs)

    @col_locking
    def update(self, col_meta_data, id, input_doc):
        for fname in col_meta_data.enumerate_data_fnames(None):
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname
            results = self.find_one_in_file(pname, FilterTool({'$filter': {'id': id}}))
            if results is not None:

                docs = FilesReader.get_instance().get_file_content(pname)

                updated = None
                updated_docs = []
                for i, doc in enumerate(docs):
                    if updated is None and doc["id"] == id:
                        normalized_doc = self.normalize(input_doc)
                        updated = {'line': i, 'doc': normalized_doc}
                        updated_docs.append(normalized_doc)
                    else:
                        updated_docs.append(doc)

                FilesReader.get_instance().write_file_content(pname, updated_docs)

                return updated
        return None

    def normalize(self, doc):
        normalized_doc = {}
        for k in doc.keys():
            normalized_doc[k.lower()] = doc[k]
        return normalized_doc

