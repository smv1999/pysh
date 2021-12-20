from genericpath import isdir
import platform
import os
from commands_list import *
from pynput.keyboard import *
from pyautogui import typewrite
import calendar
import getpass
import shutil

current_platform = platform.system()

commands_history = []

cur_dir_path = os.getcwd()


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
        typewrite(commands_history[-1])
        command = input("~{}$ ".format(cur_dir_path)).strip('\n')
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
                "pysh: incorrect usage: try 'calendar [YEAR]' or 'calendar [YEAR] [MONTH]'")
    elif main_command == 'calc':
        if len(command_args_opt) == 2:
            try:
                print(eval(command_args_opt[1]))
            except:
                print(
                    "pysh: calc: invalid expression '{}'".format(command_args_opt[1]))
        else:
            print("pysh: incorrect usage: try 'calc [EXPR]'")
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
                    # try:
                    shutil.rmtree(command_args_opt[dir_index])
                    # except:
                    #     print("pysh: rm: cannot remove '{}': No such file or directory".format(
                    #         command_args_opt[dir_index]))
            else:
                print("pysh: rm: cannot remove '{}': No such file or directory".format(
                    command_args_opt[dir_index]))
        else:
            print("pysh: incorrect usage: try 'rm [DIRECTORY]' or 'rm [FILE]'")
    elif main_command == 'cat':
        pass
    elif main_command == 'cp':
        pass
    elif main_command == 'mv':
        pass


main()
