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
        writer
        writerstate
        bool_only

    lots of default dict methods still remain to be implemented
    implementations for options provided in constructor also not done yet.
    should experiment with searcher toggling as well.

    URGENT: opening without providing bool_only argument should open with the correct mode and act accordingly. mode currently saved to file.
    '''

    def __init__(self, in_folder='testing_index', bool_only=False, from_file = None, with_dict = None, with_index = None, custom_schema = None):
        ''' 
        implement optional stuff
        '''
        self.indexdir = in_folder

        '''if custom_schema:
            self._schema = custom_schema'''

        self.bool_only = bool_only

        self._schema = Schema(keystring = TEXT(stored=not self.bool_only), valuestring = TEXT(stored=not self.bool_only))

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

        if os.path.exists(self.indexdir + '/ixIsTruthy'):
            ixinfofile = open(self.indexdir + '/ixIsTruthy','rb')
            ixinfo = ixinfofile.readline()
            if ixinfo == '1':
                ixinfo = True
            elif ixinfo == '0':
                ixinfo = False
            if ixinfo != self.bool_only:
                raise Exception('cannot open existing index in a different bool_only mode. change it or add to argument and set as true')
            ixinfofile.close()
        else:
            ixinfofile = open(self.indexdir + '/ixIsTruthy', 'wb')
            if self.bool_only:
                ixinfofile.write('1')
            else:
                ixinfofile.write('0')
            ixinfofile.close()


        self.writer = self.ix.writer()

        if with_dict:
            for key in with_dict:
                writer.add_document(keystring = unicode(key), valuestring = unicode(with_dict[key]) )

        self.writer.commit()

    def writerToggleClose(self):
        if not self.writer.is_closed:
            self.writer.commit()

    def writerToggleOpen(self):
        if self.writer.is_closed:
            self.writer = self.ix.writer()

    def __len__(self):
        self.writerToggleClose()
        with self.ix.searcher() as searcher:
            self.doc_count = searcher.doc_count()
            return self.doc_count


    def __getitem__(self,key):
        self.writerToggleClose()
        with self.ix.searcher() as searcher:
            self.result = searcher.search( Term('keystring',unicode(key)), limit = 1 )
            if self.bool_only:
                if len(self.result) == 0:
                    return False
                else:
                    return True
            else:
                return str( self.result[0]['valuestring'] ) #return, for the top result, the value for the given key

    def __setitem__(self,key,value):
        self.writerToggleOpen()
        self.writer.add_document(keystring = unicode(key), valuestring = unicode(value))

    def __delitem__(self,key):
        self.writerToggleOpen()
        self.writer.delete_by_term('keystring', unicode(key))

    def __iter__(self):
        if not self.bool_only:
            self.writerToggleClose()
            with self.ix.searcher() as searcher:
                all_results = searcher.search(query.Every(),reverse=True)
                res_count = len(all_results)
                if res_count > 0:
                    for i in xrange(res_count):
                        yield str(all_results[i]['valuestring'])
        else:
            raise Exception('cannot get text from a whooshed_dict object initialized with bool_only = True')

    def __contains__(self, item):
        self.writerToggleClose()
        if self.has_key(key=item):
            return True
        elif self.has_value(value=item):
            return True
        return False

    def keys(self):
        if not self.bool_only:
            self.writerToggleClose()
            keylist = []
            with self.ix.searcher() as searcher:
                all_results = searcher.search(query.Every(),reverse=True)
                res_count = len(all_results)
                if res_count > 0:
                    for i in xrange(res_count):
                        keylist.append( str(all_results[i]['keystring']) )
            return keylist
        else:
            raise Exception('cannot get text from a whooshed_dict object initialized with bool_only = True')

    def has_key(self, key):
        self.writerToggleClose()
        with self.ix.searcher() as searcher:
            self.result = searcher.search( Term('keystring',unicode(key)), limit = 1 )
            if len(self.result) > 0: 
                return True 
            else:
                return False

    def has_value(self, value):
        self.writerToggleClose()
        with self.ix.searcher() as searcher:
            self.result = searcher.search( Term('valuestring',unicode(value)), limit = 1 )
            if len(self.result) > 0: 
                return True 
            else:
                return False


    def clear(self):
        self.writerToggleClose()
        shutil.rmtree(self.indexdir)



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

