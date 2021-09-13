import os
import re
from datetime import datetime

from flask import Flask, render_template, request

app = Flask(__name__)
# Название файла в котором хранятся данные, через название самого файла
last_modification = dict()
modification_history = dict()

notes_dir = "notes/"
modification_history_dir = "modification_histories/"


def get_current_dir():
    file_dir = os.path.abspath(__file__)
    index = file_dir.rfind('/')
    return file_dir[0:index + 1]


def get_notes_dir():
    return get_current_dir() + notes_dir


def get_modification_history_dir():
    return get_current_dir() + modification_history_dir


def list_all_notes():
    dir_name = get_notes_dir()
    res = list()
    for note_name in os.listdir(dir_name):
        if note_name.endswith(".txt"):
            res.append(note_name)
    return res


def remove_useless_prefix_suffix(line):
    start_index = re.search("\d", line).start()
    finish_index = re.search("\.", line).start()
    return line[start_index:finish_index]


def get_creation_time(file_name):
    file_path = get_modification_history_dir() + file_name
    my_file = open(file_path, "r")
    line = remove_useless_prefix_suffix(my_file.readline())
    my_file.close()
    return line


def get_all_creation_times():
    result = list()
    dir_name = get_modification_history_dir()
    for file_name in os.listdir(dir_name):
        result.append(get_creation_time(file_name))
    return result


def get_last_modification_time(file_name):
    file_path = get_modification_history_dir() + file_name
    my_file = open(file_path, "r")
    line = remove_useless_prefix_suffix(my_file.readlines()[-1])
    my_file.close()
    return line


def get_all_last_modification_times():
    result = list()
    dir_name = get_modification_history_dir()
    for file_name in os.listdir(dir_name):
        result.append(get_last_modification_time(file_name))
    return result


@app.route('/')
def start_menu():
    print(len(list_all_notes()))
    return render_template('menu.html', sz=int(len(list_all_notes())), result_1=list_all_notes(),
                           result_2=get_all_creation_times(),
                           result_3=get_all_last_modification_times())


@app.route('/', methods=['POST', 'GET'])
def main_menu():
    if request.form:
        action_type, file_name, text = "", "", ""
        for key, value in request.form.items():
            if file_name == "":
                file_name = value
            else:
                action_type = key
                text = value
        if action_type == "create" or action_type == "edit":
            file_path = get_notes_dir() + file_name
            my_file = open(file_path, "w+")
            my_file.write(text)
            my_file.close()
            current_datetime = datetime.now()
            file_path = get_modification_history_dir() + file_name
            if action_type == 'create':
                my_file = open(file_path, "w+")
                my_file.write("Created at: ")
            else:
                my_file = open(file_path, "a+")
                my_file.write("Modified at: ")
            my_file.write(str(current_datetime))
            my_file.write("\n")
            my_file.close()
        elif file_name != "":
            file_path = get_notes_dir() + file_name
            os.remove(file_path)
            file_path = get_modification_history_dir() + file_name
            os.remove(file_path)
    return render_template('menu.html', sz=int(len(list_all_notes())), result_1=list_all_notes(),
                           result_2=get_all_creation_times(),
                           result_3=get_all_last_modification_times())


@app.route('/read', methods=['POST', 'GET'])
def read():
    if request.method == 'POST':
        chosen_note = ""
        for key, value in request.form.items():
            chosen_note = value
        list_of_notes = list_all_notes()
        try:
            with open(get_notes_dir() + chosen_note) as f:
                data = f.read()
            return render_template("read.html", name=chosen_note, result=data)
        except:
            pass
        return 0


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        chosen_note = ""
        for key, value in request.form.items():
            chosen_note = value
        list_of_notes = list_all_notes()
        try:
            with open(get_notes_dir() + chosen_note) as f:
                data = f.read()
            return render_template("edit.html", name=chosen_note, result=data)
        except:
            pass
        return 0


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        chosen_note = ""
        for key, value in request.form.items():
            chosen_note = value
        return render_template("add.html", name=chosen_note)
    return 0


@app.route('/history', methods=['POST', 'GET'])
def history():
    if request.method == 'POST':
        chosen_note, data = "", ""
        for key, value in request.form.items():
            chosen_note = value
        with open(get_modification_history_dir() + chosen_note) as f:
            data = f.readlines()
        print(data)
        return render_template("history.html", name=chosen_note, sz=len(data), result=data)
    return 0


if __name__ == '__main__':
    app.run(debug=True)
