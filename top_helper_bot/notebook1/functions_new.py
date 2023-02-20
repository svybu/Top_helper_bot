from .classes_new import Note
from .decorator import input_error
from .db import db, table

"""*****************основна логіка роботи та функції*****************"""

"""*******вітання та відповідь на помилкові команди********"""

@input_error
def hello(a):
    return 'How can I help you?'

def wrong_command():
    return 'Wrong command('

def show_all(args):
    table.show_all(db)

"""*******парсер введеного тексту з обробкою********"""
#@input_error
def parser_string(u_input):
    command, *args = u_input.split()
    if args:
        if ((command + ' ' + args[0]).lower()) in ['show all', 'good bye']:
            command = (command + ' ' + args[0]).lower()
        handler = OPTIONS.get(command.lower(), wrong_command)
    else:
        handler = OPTIONS.get(command.lower(), wrong_command)
    return handler, args

#@input_error
def add_note(args):
    name = ' '.join(args)
    ex_note = Note(name)
    if db.check_name(ex_note.name):
        r = f'note with this name already exists'
    else:
        db.add_record(ex_note)
        ex_note.open_note()
        r = f'{ex_note.name} added'
    return r

#@input_error
def change_note(args):
    name = str(args)
    if db.check_name(name) == False :
        raise FileNotFoundError
    else:
        ex_note = Note(name)
        db.change_record(ex_note)
        ex_note.open_note(True)
        return f'{ex_note.name} changed'


#@input_error
def remove_note(args):
    name = str(args)
    if db.check_name(name) == False :
        raise FileNotFoundError
    else:
        ex_note = Note(name)
        ex_note.remove()
        db.remove_record(ex_note.name)
        return f'{ex_note.name} removed'


#@input_error
def add_tags(args):
    name = str(args)
    if db.check_name(name):
        note = Note(name)
        tags = input('Enter tags ')
        db.add_tag(note.change_tag(tags))
    else:
        raise FileNotFoundError
    return f'added tags to {note.name} '


#@input_error
def remove_tags(args):
    name = str(args)
    if db.check_name(name):
        note = Note(name)
        note.remove_tag()
    else:
        raise FileNotFoundError
    return f'removed tags to {note.name} '


#@input_error
def filter(args):
    tag = str(args)
    table.filter(db, tag)

#@input_error
def sort(args):
    table.sort(db)



OPTIONS = {"hello": hello,
           "add": add_note,
           'change': change_note,
           'delete': remove_note,
           'remove': remove_note,
           'show all': show_all,
           "tag_add": add_tags,
           'tag_delete': remove_tags,
           'tag_remove': remove_tags,
           'filter': filter,
           'sort': sort,
           'good bye': exit,
           'close': exit,
           'exit': exit,
           '.': exit
           }