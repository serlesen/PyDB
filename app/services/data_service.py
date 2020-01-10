import _pickle as pickle
import os.path

from app.services.files_reader import FilesReader
from app.tools.collection_locker import CollectionLocker, col_locking
from app.tools.filter_tool import FilterTool
from app.tools.database_context import DatabaseContext

class DataService(object):
    """ Class to read (without conditions or only some given lines), append and update a data file. """

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
    def append(self, col_meta_data, input_docs):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname()
        if self.file_len(pname) >= DatabaseContext.MAX_DOC_PER_FILE:
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.next_data_fname() 
 
        if os.path.exists(pname):
            docs = FilesReader.get_instance().get_file_content(pname)
        else:
            docs = []
            
        docs_to_iterate = input_docs
        output_docs = []
        
        remaining_capacity = DatabaseContext.MAX_DOC_PER_FILE - len(docs)
        while len(docs_to_iterate) > 0:
            normalized_docs = self.normalize(docs_to_iterate[:remaining_capacity])
            docs.extend(normalized_docs)
            output_docs.extend(normalized_docs)

            docs_to_iterate = docs_to_iterate[remaining_capacity:]
            
            FilesReader.get_instance().write_file_content(pname, docs)
            if len(docs_to_iterate) > 0:
                docs = []
                pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.next_data_fname() 
                remaining_capacity = DatabaseContext.MAX_DOC_PER_FILE

        return output_docs

    def file_len(self, pname):
        if os.path.exists(pname) is False:
            return 0
        
        docs = FilesReader.get_instance().get_file_content(pname)
        return len(docs)

    @col_locking
    def update(self, col_meta_data, ids, input_docs):
        updated = []
        counter = 0
        line_counter = 0

        docs = None
        try:
            id = ids[counter]
            input_doc = input_docs[counter]
            counter += 1

            for fname in col_meta_data.enumerate_data_fnames(None):
                pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname
                
                results = self.find_one_in_file(pname, FilterTool({'$filter': {'id': id}}))

                docs = None
                if results is not None:
    
                    if docs is None:
                        docs = FilesReader.get_instance().get_file_content(pname)

                    updated_docs = []
                    for i, doc in enumerate(docs):
                        if bool(doc) and doc["id"] == id:
                            normalized_doc = self.normalize([input_doc])
                            updated.append({'line': i + line_counter, 'doc': normalized_doc[0]})
                            updated_docs.extend(normalized_doc)

                            if counter < len(ids):
                                id = ids[counter]
                                input_doc = input_docs[counter]
                                counter += 1
                        else:
                            updated_docs.append(doc)
    
                    FilesReader.get_instance().write_file_content(pname, updated_docs)
                line_counter += DatabaseContext.MAX_DOC_PER_FILE
        except StopIteration:
            if docs is not None:
                FilesReader.get_instance().write_file_content(pname, updated_docs)
    
        return updated

    def normalize(self, docs):
        normalized_docs = []
        for doc in docs:
            normalized_doc = {}
            for k in doc.keys():
                normalized_doc[k.lower()] = doc[k]
            normalized_docs.append(normalized_doc)
        return normalized_docs

