
import os
import subprocess
import datetime



class Note():
    def __init__(self, name: str, created=datetime.datetime.now().strftime('%m/%d/%Y, %H:%M'), tag = '', changed = None):
        self.name = name
        self.created = created

    def open_note(self, change=False):

        try:
            print(f"Opening note '{self.name}'...")
            subprocess.call(['open', '-a', 'TextEdit', f'.//notes//{self.name}.txt'])
        except:
            try:
                subprocess.call(['notepad', f'.//notes//{self.name}.txt'])
            except FileNotFoundError:
                print("Text editor not found")
        if change:
            self.changed = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M')

    def change_note(self):
        self.changed = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M')
        self.open_note(True)

    def remove_note(self):
        path = os.path.join('.', 'notes', f'{self.name}.txt')
        if os.path.isfile(path):
            try:
                os.remove(path)
            except OSError as e:
                print(f"Error removing file: {e}")
        else:
            print(f"File not found: {path}")

    def change_tag(self, tag):
        self.tag = tag

    def remove_tag(self):
        self.tag = ''



