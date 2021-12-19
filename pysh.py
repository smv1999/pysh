from genericpath import isdir
import platform
import os
from commands_list import *
from pynput.keyboard import *


current_platform = platform.system()

commands_history = []

cur_dir_path = os.getcwd()


def main():
    listener = Listener(
        on_press=on_key_press)
    listener.start()
    while True:
        global command, visit_history
        if visit_history == False:
            command = input("~{}$ ".format(cur_dir_path))
        if command == 'exit':
            commands_history.append(command)
            break
        elif command == 'clear':
            commands_history.append(command)
            if current_platform == 'Windows':
                os.system('cls')
            else:
                os.system('clear')
        elif command == 'help':
            commands_history.append(command)
            print("pysh: A Cross-Platform Shell written in Python")
        else:
            check_valid(command)


def on_key_press(key):
    if key == Key.up:
        visit_history = True
        command = input("~{}$ {}".format(cur_dir_path, commands_history[-1]))
        return False


def check_valid(command):
    if command != '':
        main_command = command.split()[0]
        if main_command in commands_list:
            commands_history.append(command)
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


main()
