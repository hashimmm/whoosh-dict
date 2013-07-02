#whooshed dict
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, DATETIME
import whoosh.index as index
import os
from shutil import rmtree
from whoosh.fields import *
from whoosh.query import *
from whoosh import query

'''
making a generic dictionary indexing class. not completed yet.
'''

class whooshed_dict:
    '''
    properties:
        ix
        result (may be removed. Is there since I think I can use it for optimization)
        indexdir
        _schema
        doc_count (may be removed. Is there since I think I can use it for optimization)
    lots of default dict methods still remain to be implemented
    implementations for options provided in constructor also not done yet.
    '''

    def __init__(self, in_folder='testing_index', from_file = None, with_dict = None, with_index = None, custom_schema = None):
        ''' 
        implement optional stuff
        '''
        self.indexdir = in_folder

        '''if custom_schema:
            self._schema = custom_schema'''

        self._schema = Schema(keystring = TEXT(stored=True), valuestring = TEXT(stored=True))


        if not index.exists_in(self.indexdir):
            #logging.info("index does not exist in indexdir, will create")
            if not os.path.exists(self.indexdir):
                #logging.info("indexdir does not exist, will create")
                os.mkdir(self.indexdir)
                #logging.info("created indexdir")        
            self.ix = index.create_in(self.indexdir, self._schema)
            #logging.info("created index in indexdir")
        else:
            self.ix = index.open_dir(self.indexdir)
            #logging.info("found and opened existing index in indexdir")

        writer = self.ix.writer()

        if with_dict:
            for key in with_dict:
                writer.add_document(keystring = unicode(key), valuestring = unicode(with_dict[key]) )

        writer.commit()

    def __len__(self):
        with self.ix.searcher() as searcher:
            self.doc_count = searcher.doc_count()
            return self.doc_count


    def __getitem__(self,key):
        with self.ix.searcher() as searcher:
            self.result = searcher.search( Term('keystring',unicode(key)), limit = 1 )
            return str( self.result[0]['valuestring'] ) #return, for the top result, the value for the given key

    def __setitem__(self,key,value):
        writer = self.ix.writer()
        writer.add_document(keystring = unicode(key), valuestring = unicode(value))
        writer.commit()

    def __delitem__(self,key):
        writer = self.ix.writer()
        writer.delete_by_term('keystring', unicode(key))
        writer.commit()

    def __iter__(self):
        with self.ix.searcher() as searcher:
            all_results = searcher.search(query.Every(),reverse=True)
            res_count = len(all_results)
            if res_count > 0:
                for i in xrange(res_count):
                    yield str(all_results[i]['valuestring'])

    def __contains__(self, item):
        if self.has_key(key=item):
            return True
        elif self.has_value(value=item):
            return True
        return False

    def keys(self):
        keylist = []
        with self.ix.searcher() as searcher:
            all_results = searcher.search(query.Every(),reverse=True)
            res_count = len(all_results)
            if res_count > 0:
                for i in xrange(res_count):
                    keylist.append( str(all_results[i]['keystring']) )
        return keylist

    def has_key(self, key):
        with self.ix.searcher() as searcher:
            self.result = searcher.search( Term('keystring',unicode(key)), limit = 1 )
            if len(self.result) > 0: 
                return True 
            else:
                return False

    def has_value(self, value):
        with self.ix.searcher() as searcher:
            self.result = searcher.search( Term('valuestring',unicode(value)), limit = 1 )
            if len(self.result) > 0: 
                return True 
            else:
                return False


    def clear(self): shutil.rmtree(self.indexdir)



    ''' IMPLEMENT/correct THE FOLLOWING METHODS

    def __eq__(self, other): pass #whoosh.index doesn't have __eq__ :/ make it?

    def copy(self):                             
        if self.__class__ is whooshed_dict:          
            return self.indexdir         
        import copy                             
        return copy.copy(self)

    
    def update(self, with_dict = None, with_index = None):
        if with_dict:
            pass

        if with_index:
            pass


    def keys(self): 

    def items(self):  

    def values(self):  '''

