import datetime
import os
import subprocess
from pathlib import Path
import pandas as pd


def save():
    df.to_csv('df.csv', index=False, sep=';')
def create_df():
    try:
        df = pd.read_csv('df.csv', delimiter=';')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['tags', 'name', 'created', 'changed', 'note'])
    if os.path.exists('notes')==False:
        os.mkdir('notes')
    return df


df = create_df()

class Notebook(pd.DataFrame):
    def add_note(self, note):
        self.loc[len(self), ['name', 'created', 'note']] = [note.name.value, note.created, note]
        save()
    def change_note(self, note,changed=datetime.datetime.now().strftime('%m/%d/%Y, %H:%M')):
        self.loc[df['name'] == note.name.value, ['changed']] = changed
        save()

    def remove_note(self, note):
        self = self.loc[self['name'] != note.name.value]
        save()

class Field:
    def __init__(self, value):
        self._value = str(value)
        self.value = str(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    @Field.value.setter
    def value(self, value):
        try:
            fle = Path(f'.//notes//{value}.txt')
            fle.touch(exist_ok=False)
            self.value = str(value)
        except FileExistsError:
            return f'Note with this name already exists'


class Tag(Field):
    @Field.value.setter
    def value(self, value):
        self.value = str(value)
        try:
            self.value = value.lower()
        except:
            pass


class Note():
    def __init__(self, name, tags='', created=datetime.datetime.now().strftime('%m/%d/%Y, %H:%M')):
        self.name = Name(name)
        self.tags = tags
        self.created = created


    def add_tags(self, new_tag):
        self.tags = new_tag
        df.loc[df['name'] == self.name.value, ['tags']] = self.tags



    def delete_tags(self):
        self.tags = ''
        df.loc[df['name'] == self.name.value, ['tags']] = ''

    def add_note(self):
        try:
            subprocess.call(['open', '-a', 'TextEdit', f'.//notes//{self.name.value}.txt'])
            df.loc[len(df), ['name', 'created']] = [self.name.value, self.created]
        except:
            try:
                subprocess.call(['notepad', f'.//notes//{self.name.value}.txt'])
                df.loc[len(df), ['name', 'created']] = [self.name.value, self.created]
            except FileNotFoundError:
                print("Text editor not found")

    def change_note(self, changed=datetime.datetime.now().strftime('%m/%d/%Y, %H:%M')):
        try:
            subprocess.call(['open', '-a', 'TextEdit', f'.//notes//{self.name.value}.txt'])
            df.loc[df['name'] == self.name.value, ['changed']] = changed
        except:
            try:
                subprocess.call(['notepad', f'.//notes//{self.name.value}.txt'])
                df.loc[df['name'] == self.name.value, ['changed']] = changed
            except FileNotFoundError:
                print("Text editor not found")

    def remove(self):
        global df
        os.remove(f'.//notes//{self.name.value}.txt')
        df = df.loc[df['name'] != self.name.value]
        return df



def synk():
    global df
    names = os.listdir('notes')
    names = [i[:-4] for i in names]
    for name in names:
        if df['name'].isin([name]).any()==False:
            ex_note = Note(name)
            df.loc[len(df), ['name', 'created']] = [ex_note.name.value, ex_note.created]
    save()
    df = df.loc[df['name'].isin(names)==True]
    save()



synk()   # ---------------  ??? обязательно сразу синхронизировать


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'No contact with this name, try again'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'Seems, some mistake. Please, try again'
        except TypeError as exception:
            return "Sorry, I didn't understand this command, please try again"
        except AttributeError as exception:
            return "Sorry, no such attribute("
        except FileExistsError:
            return 'note with this name  already exists'
        except FileNotFoundError:
            return 'there is no note with this name'

    return inner

# from classes import Note, df, synk, create_df
# from decorator import input_error
# from classes import save
"""*****************основна логіка роботи та функції*****************"""

"""*******вітання та відповідь на помилкові команди********"""
@input_error
def hello(a):
    return 'How can I help you?'


def wrong_command():
    return 'Wrong command('


def show_all(a):
    synk()
    df = create_df()
    result = df
    return result


"""*******парсер введеного тексту з обробкою********"""
@input_error
def parser_string(u_input):
    command, *args = u_input.split()
    if args:
        if ((command + ' ' + args[0]).lower()) in ['show all', 'good bye']:
            command = (command + ' ' + args[0]).lower()
        handler = OPTIONS.get(command.lower(), wrong_command)
    else:
        handler = OPTIONS.get(command.lower(), wrong_command)
    return handler, args

@input_error
def add_note(args):
    df = create_df()
    name = str(args[0])
    if df['name'].isin([name]).any():
        raise FileExistsError
    else:
        ex_note = Note(name)
        ex_note.add_note()
        save()
    return f'{ex_note.name.value} added'

@input_error
def change_note(args):
    synk()
    df = create_df()
    name = str(args[0])
    if df['name'].isin([name]).any() == False:
        raise FileNotFoundError
    else:
        ex_note = Note(name)
        ex_note.change_note()
        save()
        return f'{ex_note.name.value} changed'

@input_error
def remove_note(args):
    synk()
    df = create_df()
    name = args[0]
    if df['name'].isin([name]).any() == False:
        raise FileNotFoundError
    else:
        ex_note = Note(name)
        df = ex_note.remove()
        save()
        return f'{ex_note.name.value} removed'

@input_error
def add_tags(args):
    synk()
    df = create_df()
    name = args[0]
    if df['name'].isin([name]).any():
        ex_note = Note(name)
        tags = input('Enter tags ')
        ex_note.add_tags(tags)
        save()
    else:
        raise FileNotFoundError
    return f'added tags to {ex_note.name.value} '


@input_error
def remove_tags(args):
    df = create_df()
    name = args[0]
    if df['name'].isin([name]).any():
        ex_note = Note(name)
        ex_note.delete_tags()
        save()
    else:
        raise FileNotFoundError
    return f'removed tags to {ex_note.name.value} '


@input_error
def filter(args):
    df = create_df()
    tag = args[0]
    #df_filtered=df[df.tags.str.contains(tag, na=False).any()]
    df_filtered = df[df.tags.str.contains('|'.join(tag),na=False)]
    print(df_filtered)

@input_error
def sort(a):
    df = create_df()
    flag = int(input('Input 1 for sort by date of creation or 2 - by date of change '))
    if flag == 1:
        df_sorted=df.sort_values(by='created', ascending=False)
    else:
        df_sorted = df.sort_values(by='changed',ascending=False)
    print(df_sorted)

OPTIONS = {"hello": hello,
           "add": add_note,
           'change': change_note,
           'delete': remove_note,
           'remove': remove_note,
           'show all': show_all,
           "tag_add": add_tags,
           'tag_delete': remove_tags,
           'tag_remove': remove_tags,
           'filter':filter,
           'sort':sort,
           'good bye': exit,
           'close': exit,
           'exit': exit,
           '.': exit
           }


















# from functions import parser_string, wrong_command
# from decorator import input_error
# from classes import synk, save


@input_error
def main():
    try:
        while True:
            u_input = input('Enter command ')
            handler, *args = parser_string(u_input)
            if handler == wrong_command:
                print('Wrong command(')
            elif handler == exit:
                print("Good bye!")
                break
            else:
                result = handler(*args)
                print(result)
    finally:
        save()


if __name__ == '__main__':
    synk()
    print('Welcome to NoteBook')
    main()

