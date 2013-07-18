from lettuce import *
import whooshed_dict as wd

@before.all
def define_stuff():
    world.wd = wd.whooshed_dict(in_folder='test_index')
    world.strkey = 'strkey'
    world.strval = 'strval'
    world.keylist = ['listKey1','listKey2']
    world.vallist = ['listVal1','listVal2']

#------------------------------------------------------------------------------------------------
@step(u'Store a string key and string value')
def store_str_k_v(step):
    world.wd.clear()
    world.wd = wd.whooshed_dict(in_folder='test_index')
    world.wd[world.strkey] = world.strval

@step(u'Retrieve via key for string key and string value')
def retrieve_via_key_both_str(step):
    try:
        world.wd[world.strkey]
    except Exception as ee:
        assert False, ee

#------------------------------------------------------------------------------------------------

@step(u'Store a listOfStrings element as key and string as value')
def store_listE_k_str_val(step):
    world.wd.clear()
    world.wd = wd.whooshed_dict(in_folder='test_index')
    world.wd[world.keylist[0]] = world.strval
    print "-%s-%s"%(repr(world.strval), repr(world.wd.keys()))
    pass

@step(u'Retrieve via key for string-list-element key and string value')
def retrieve_listStr_k_str_v(step):
    try:
        world.wd[world.keylist[0]]
    except Exception as ee:
        assert False, ee

#------------------------------------------------------------------------------------------------

@step(u'Store a string as key and listOfStrings element as value')
def store_listE_k_str_val(step):
    world.wd.clear()
    world.wd = wd.whooshed_dict(in_folder='test_index')
    world.wd[world.strkey] = world.vallist[0]

@step(u'Retrieve via key for string key and string-list-element value')
def retrieve_listStr_k_str_v(step):
    try:
        world.wd[world.strkey]
    except Exception as ee:
        assert False, ee

#------------------------------------------------------------------------------------------------