from genericpath import isdir
import platform
import os
from utils.commands_list import *
from pynput.keyboard import *
from pyautogui import typewrite
import calendar
import getpass
import shutil
import datetime
import magic
import time

current_platform = platform.system()

commands_history = []

cur_dir_path = os.getcwd()

if current_platform == 'Windows':
    history_file_path = 'C:/Users/' + getpass.getuser() + '/history.txt'
else:
    history_file_path = '/home/' + getpass.getuser() + '/history.txt'


def main():
    listener = Listener(
        on_press=on_key_press)
    listener.start()
    global visit_history
    visit_history = False
    while True:
        global command
        if visit_history == False:
            command = input("~{}$ ".format(cur_dir_path)).strip('\n')
        if command == 'exit':
            commands_history.append(command)
            with open(history_file_path, 'a') as history_file:
                history_file.write(command + "\n")
            break
        elif command == 'clear':
            commands_history.append(command)
            with open(history_file_path, 'a') as history_file:
                history_file.write(command + "\n")
            if current_platform == 'Windows':
                os.system('cls')
            else:
                os.system('clear')
        elif command == 'help':
            commands_history.append(command)
            with open(history_file_path, 'a') as history_file:
                history_file.write(command + "\n")
            print("pysh: A Cross-Platform Shell written in Python")
        else:
            check_valid(command)


def on_key_press(key):
    if key == Key.up:
        visit_history = True
        typewrite(commands_history[-1])
        command = input("~{}$ ".format(cur_dir_path)).strip('\n')
        return False


def check_valid(command):
    if command != '':
        main_command = command.split()[0]
        if main_command in commands_list:
            commands_history.append(command)
            with open(history_file_path, 'a') as history_file:
                history_file.write(command + "\n")
            execute_commands(command)
        else:
            print("pysh: command not found: {}".format(command))


def execute_commands(command):
    command_args_opt = command.split()
    main_command = command_args_opt[0]
    if main_command == 'lf':
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            print(f)
    elif main_command == 'ldir':
        dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
        for d in dirs:
            print(d)
    elif main_command == 'pwd':
        pwd = os.getcwd()
        print(pwd)
    elif main_command == 'cd':
        global cur_dir_path
        to_dir_path = command_args_opt[1]
        if to_dir_path == '..':
            parent_dir_path = os.path.dirname(os.getcwd())
            cur_dir_path = parent_dir_path
            os.chdir(os.path.abspath(parent_dir_path))
        else:
            cur_dir_path = to_dir_path
            os.chdir(os.path.abspath(to_dir_path))
    elif main_command == 'manual':
        if len(command_args_opt) == 2:
            if command_args_opt[1] in commands_list:
                print(commands_list_manual[command_args_opt[1]])
            else:
                print('No manual entry for {}'.format(command_args_opt[1]))
        else:
            print("What manual page do you want? \n For example, try 'man cdir'")
    elif main_command == 'mkdir':
        dir_path = os.path.join(os.getcwd(), command_args_opt[1])
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            print("pysh: mkdir: cannot create directory '{}': Directory exists".format(
                command_args_opt[1]))
    elif main_command == 'calendar':
        if len(command_args_opt) == 3:
            try:
                print(calendar.month(
                    int(command_args_opt[1]), int(command_args_opt[2])))
            except:
                print(
                    "pysh: calendar: invalid operand(s). \n Try 'manual calendar' for more help.")
        elif len(command_args_opt) == 2:
            try:
                print(calendar.calendar(int(command_args_opt[1])))
            except:
                print(
                    "pysh: calendar: invalid operand. \n Try 'manual calendar' for more help.")
        else:
            print(
                "pysh: calendar: incorrect usage: try 'calendar [YEAR]' or 'calendar [YEAR] [MONTH]'")
    elif main_command == 'calc':
        if len(command_args_opt) == 2:
            try:
                print(eval(command_args_opt[1]))
            except:
                print(
                    "pysh: calc: invalid expression '{}'".format(command_args_opt[1]))
        else:
            print("pysh: calc: incorrect usage: try 'calc [EXPR]'")
    elif main_command == 'whoami':
        print(getpass.getuser())
    elif main_command == 'echo':
        print(' '.join(text for text in command_args_opt[1:]))
    elif main_command == 'rm':
        if len(command_args_opt) == 2 or len(command_args_opt) == 3:
            args_index = -1
            dir_index = 1
            if '-r' in command_args_opt:
                args_index = command_args_opt.index('-r')
                dir_index = 2 if (args_index == 1) else 1
            if os.path.isfile(command_args_opt[1]):
                os.remove(command_args_opt[dir_index])
            elif os.path.isdir(command_args_opt[dir_index]):
                if args_index == -1:
                    try:
                        os.rmdir(command_args_opt[dir_index])
                    except:
                        print("pysh: rm: cannot remove '{}': directory not empty".format(
                            command_args_opt[dir_index]))
                else:
                    shutil.rmtree(command_args_opt[dir_index])
            else:
                print("pysh: rm: cannot remove '{}': No such file or directory".format(
                    command_args_opt[dir_index]))
        else:
            print(
                "pysh: rm: incorrect usage: try 'rm [DIRECTORY]' or 'rm [FILE]'")
    elif main_command == 'cat':
        if len(command_args_opt) != 1:
            for file in command_args_opt[1:]:
                with open(file) as f:
                    print(f.read())
        else:
            print("pysh: cat: incorrect usage: try 'cat [FILE]...'")
    elif main_command == 'cp':
        if len(command_args_opt) == 3:
            if os.path.isfile(command_args_opt[1]):
                if not os.path.isdir(command_args_opt[2]):
                    if not os.path.isfile(command_args_opt[2]):
                        # destination file is created if it doesn't already exist
                        with open(command_args_opt[2], 'w'):
                            pass

                    with open(command_args_opt[1], 'r') as src_file:
                        src_file_data = src_file.read()
                        with open(command_args_opt[2], 'w') as dest_file:
                            dest_file.write(src_file_data)
                elif os.path.isdir(command_args_opt[2]):
                    with open(command_args_opt[1], 'r') as src_file:
                        src_file_data = src_file.read()
                        with open(command_args_opt[2] + '/' + command_args_opt[1], 'w') as dest_file:
                            dest_file.write(src_file_data)
            else:
                print("pysh: cp: cannot copy '{}': No such file or directory".format(
                    command_args_opt[1]))
        else:
            print(
                "pysh: cp: incorrect usage: try 'cp [SOURCE_FILE] [DESTINATION_FILE]' or 'cp [SOURCE_FILE] [DESTINATION_DIRECTORY]'")
    elif main_command == 'mv':
        if len(command_args_opt) == 3:
            if os.path.isfile(command_args_opt[1]):
                if not os.path.isdir(command_args_opt[2]):
                    if not os.path.isfile(command_args_opt[2]):
                        os.rename(command_args_opt[1], command_args_opt[2])

                    else:
                        # copy contents from src to dest and delete src
                        with open(command_args_opt[1], 'r') as src_file:
                            src_file_data = src_file.read()
                            with open(command_args_opt[2], 'w') as dest_file:
                                dest_file.write(src_file_data)
                        os.remove(command_args_opt[1])
                elif os.path.isdir(command_args_opt[2]):
                    with open(command_args_opt[1], 'r') as src_file:
                        src_file_data = src_file.read()
                        with open(command_args_opt[2] + '/' + command_args_opt[1], 'w') as dest_file:
                            dest_file.write(src_file_data)
                    os.remove(command_args_opt[1])
            else:
                print("pysh: mv: cannot move '{}': No such file or directory".format(
                    command_args_opt[1]))
        else:
            print(
                "pysh: mv: incorrect usage: try 'mv [SOURCE_FILE] [DESTINATION_FILE]' or 'mv [SOURCE_FILE] [DESTINATION_DIRECTORY]'")
    elif main_command == 'date':
        if len(command_args_opt) == 1:
            print(datetime.datetime.now())
        else:
            print("pysh: date: incorrect usage: try 'date'")
    elif main_command == 'file':
        if len(command_args_opt) == 2:
            file_details = []
            try:
                file_type = magic.detect_from_filename(command_args_opt[1])
                file_details.append(file_type.mime_type)
                file_details.append(file_type.name)
                file_details.append(
                    str(os.path.getsize(command_args_opt[1])) + ' bytes')
                file_details.append('Modified: ' + str(time.ctime(
                    os.path.getmtime(command_args_opt[1]))))
                file_details.append('Created: ' + str(time.ctime(
                    os.path.getctime(command_args_opt[1]))))

                print(', '.join(str(detail) for detail in file_details))
            except:
                print("pysh: file: file '{}' does not exist or is inaccessible".format(
                    command_args_opt[1]))
        else:
            print("pysh: file: incorrect usage: try 'file [FILE]'")
    elif main_command == 'history':
        if len(command_args_opt) == 1:
            for command in commands_history:
                print(command)
        elif len(command_args_opt) == 2:
            if command_args_opt[1] == "-a":
                with open(history_file_path, 'r') as history_file:
                    print(history_file.read())
            else:
                print("pysh: history: incorrect usage: try 'history' or 'history -a'")
        else:
            print("pysh: history: incorrect usage: try 'history' or 'history -a'")
    elif main_command == 'head':
        pass
    elif main_command == 'tail':
        pass


main()
