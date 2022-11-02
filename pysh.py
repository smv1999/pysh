from genericpath import isdir
import platform
import os
import subprocess
from utils.commands_list import *
from utils.boyer_moore_algorithm import BoyerMooreAlgorithm
import calendar
import getpass
import shutil
import datetime
import magic
import time
import socket
import cmd
import dns.resolver
import psutil
import signal
import urllib.request


class Pysh(cmd.Cmd):

    # initialization

    current_platform = platform.system()

    commands_history = []

    cur_dir_path = os.getcwd()

    if current_platform == 'Windows':
        home_path = 'C:/Users/' + getpass.getuser()
        history_file_path = 'C:/Users/' + getpass.getuser() + '/history.txt'
    else:
        home_path = '/home/' + getpass.getuser()
        history_file_path = '/home/' + getpass.getuser() + '/history.txt'

    downloads_path = home_path + '/Downloads/'

    prompt = "~{}$ ".format(cur_dir_path)

    # commands section

    def save_history(self, string):
        self.commands_history.append(string.strip())
        with open(self.history_file_path, 'a') as history_file:
            history_file.write(string.strip() + "\n")

    def do_exit(self, *args):
        gen_args = args[0].split()
        self.save_history("exit " + "".join(gen_args))
        return True

    def do_clear(self, *args):
        gen_args = args[0].split()
        if not gen_args:
            if self.current_platform == 'Windows':
                os.system('cls')
                self.save_history("cls")
            else:
                os.system('clear')
                self.save_history("clear")
        else:
            print("pysh: clear: incorrect usage: try 'clear'")

    def do_lf(self, *args):
        dirs = args[0].split()
        self.save_history("lf " + " ".join(dirs))
        if dirs:
            for dir in dirs:
                if os.path.isdir(dir):
                    files = [f for f in os.listdir(
                        dir) if os.path.isfile(dir + '/' + f)]
                    for f in files:
                        print(f)
                elif not os.path.isdir(dir):
                    print("pysh: lf: directory '{}' does not exist".format(dir))
        else:
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            for f in files:
                print(f)

    def do_ldir(self, *args):
        dirs = args[0].split()
        self.save_history("ldir " + " ".join(dirs))
        if dirs:
            for dir in dirs:
                if os.path.isdir(dir):
                    dirs_list = [d for d in os.listdir(
                        dir) if os.path.isdir(dir + '/' + d)]
                    for d in dirs_list:
                        print(d)
                elif not os.path.isdir(dir):
                    print("pysh: ldir: directory '{}' does not exist".format(dir))
        else:
            dirs_list = [d for d in os.listdir('.') if os.path.isdir(d)]
            for d in dirs_list:
                print(d)

    def do_pwd(self, *args):
        gen_args = args[0].split()
        self.save_history("pwd " + " ".join(gen_args))
        pwd = os.getcwd()
        print(pwd)

    def do_cd(self, *args):
        gen_args = args[0].split()
        self.save_history("cd " + " ".join(gen_args))
        if len(gen_args) <= 1:
            if len(gen_args) == 0:
                self.cur_dir_path = os.path.abspath(self.home_path)
                self.prompt = "~{}$ ".format(self.cur_dir_path)
                os.chdir(self.cur_dir_path)
            else:
                dir = gen_args[0]
                if os.path.isdir(dir):
                    to_dir_path = dir
                    if to_dir_path == '..':
                        parent_dir_path = os.path.dirname(os.getcwd())
                        self.cur_dir_path = parent_dir_path
                        self.prompt = "~{}$ ".format(self.cur_dir_path)
                        os.chdir(os.path.abspath(parent_dir_path))
                    else:
                        self.cur_dir_path = os.path.abspath(to_dir_path)
                        self.prompt = "~{}$ ".format(self.cur_dir_path)
                        os.chdir(self.cur_dir_path)
                elif not os.path.isdir(dir):
                    print("pysh: cd: directory '{}' does not exist".format(dir))
        else:
            print("pysh: cd: too many arguments: try 'cd [DIRECTORY]'")

    def do_mkdir(self, *args):
        dirs = args[0].split()
        self.save_history("mkdir " + " ".join(dirs))
        if len(dirs) != 0:
            for dir in dirs:
                dir_path = os.path.join(os.getcwd(), dir)
                try:
                    os.mkdir(dir_path)
                except FileExistsError:
                    print("pysh: mkdir: cannot create directory '{}': directory exists".format(
                        dir))
        else:
            print("pysh: mkdir: incorrect usage: try 'mkdir [DIRECTORY]...'")

    def do_calendar(self, *args):
        params = args[0].split()
        self.save_history("calendar " + " ".join(params))
        if len(params) == 2:
            try:
                print(calendar.month(
                    int(params[0]), int(params[1])))
            except:
                print(
                    "pysh: calendar: invalid operand(s). \n Try 'help calendar' for more help.")
        elif len(params) == 1:
            try:
                print(calendar.calendar(int(params[0])))
            except:
                print(
                    "pysh: calendar: invalid operand. \n Try 'help calendar' for more help.")
        else:
            print(
                "pysh: calendar: incorrect usage: try 'calendar [YEAR]' or 'calendar [YEAR] [MONTH]'")

    def do_calc(self, *args):
        gen_args = args[0].split()
        self.save_history("calc " + " ".join(gen_args))
        if len(gen_args) == 1:
            expr = gen_args[0]
            try:
                print(eval(expr))
            except:
                print(
                    "pysh: calc: invalid expression '{}'".format(expr))
        else:
            print("pysh: calc: incorrect usage: try 'calc [EXPR]'")

    def do_whoami(self, *args):
        gen_args = args[0].split()
        self.save_history("whoami " + " ".join(gen_args))
        if not gen_args:
            print(getpass.getuser())
        else:
            print("pysh: whoami: incorrect usage: try 'whoami'")

    def do_echo(self, *args):
        text = args[0]
        self.save_history("echo " + "".join(text))
        if text:
            print(text)
        else:
            print("pysh: echo: incorrect usage: try 'echo [TEXT]'")

    def do_rm(self, *args):
        file_dir = args[0].split()
        self.save_history("rm " + " ".join(file_dir))
        if len(file_dir) == 1 or len(file_dir) == 2:
            args_index = -1
            dir_index = 0
            if '-r' in file_dir:
                args_index = file_dir.index('-r')
                dir_index = 1 if (args_index == 0) else 0
            if os.path.isfile(file_dir[dir_index]):
                os.remove(file_dir[dir_index])
            elif os.path.isdir(file_dir[dir_index]):
                if args_index == -1:
                    try:
                        os.rmdir(file_dir[dir_index])
                    except:
                        print("pysh: rm: cannot remove '{}': directory not empty".format(
                            file_dir[dir_index]))
                else:
                    shutil.rmtree(file_dir[dir_index])
            else:
                print("pysh: rm: cannot remove '{}': No such file or directory".format(
                    file_dir[dir_index]))
        else:
            print(
                "pysh: rm: incorrect usage: try 'rm [DIRECTORY]' or 'rm [FILE]'")

    def do_cat(self, *args):
        files = args[0].split()
        self.save_history("cat " + " ".join(files))
        if len(files) != 0:
            for file in files:
                if os.path.isfile(file):
                    with open(file) as f:
                        print(f.read())
                else:
                    print("pysh: cat: file '{}' does not exist".format(file))
        else:
            print("pysh: cat: incorrect usage: try 'cat [FILE]...'")

    def do_cp(self, *args):
        file_dir = args[0].split()
        self.save_history("cp " + " ".join(file_dir))
        if len(file_dir) == 2:
            if os.path.isfile(file_dir[0]):
                if not os.path.isdir(file_dir[1]):
                    if not os.path.isfile(file_dir[1]):
                        # destination file is created if it doesn't already exist
                        with open(file_dir[1], 'w'):
                            pass

                    with open(file_dir[0], 'r') as src_file:
                        src_file_data = src_file.read()
                        with open(file_dir[1], 'w') as dest_file:
                            dest_file.write(src_file_data)
                elif os.path.isdir(file_dir[1]):
                    with open(file_dir[0], 'r') as src_file:
                        src_file_data = src_file.read()
                        with open(file_dir[1] + '/' + file_dir[0], 'w') as dest_file:
                            dest_file.write(src_file_data)
            else:
                print("pysh: cp: cannot copy '{}': No such file or directory".format(
                    file_dir[0]))
        else:
            print(
                "pysh: cp: incorrect usage: try 'cp [SOURCE_FILE] [DESTINATION_FILE]' or 'cp [SOURCE_FILE] [DESTINATION_DIRECTORY]'")

    def do_mv(self, *args):
        file_dir = args[0].split()
        self.save_history("mv " + " ".join(file_dir))
        if len(file_dir) == 2:
            if os.path.isfile(file_dir[0]):
                if not os.path.isdir(file_dir[1]):
                    if not os.path.isfile(file_dir[1]):
                        os.rename(file_dir[0], file_dir[1])

                    else:
                        # copy contents from src to dest and delete src
                        with open(file_dir[0], 'r') as src_file:
                            src_file_data = src_file.read()
                            with open(file_dir[1], 'w') as dest_file:
                                dest_file.write(src_file_data)
                        os.remove(file_dir[0])
                elif os.path.isdir(file_dir[1]):
                    with open(file_dir[0], 'r') as src_file:
                        src_file_data = src_file.read()
                        with open(file_dir[1] + '/' + file_dir[0].split('/')[-1], 'w') as dest_file:
                            dest_file.write(src_file_data)
                    os.remove(file_dir[0])
            else:
                print("pysh: mv: cannot move '{}': No such file or directory".format(
                    file_dir[0]))
        else:
            print(
                "pysh: mv: incorrect usage: try 'mv [SOURCE_FILE] [DESTINATION_FILE]' or 'mv [SOURCE_FILE] [DESTINATION_DIRECTORY]'")

    def do_date(self, *args):
        gen_args = args[0].split()
        self.save_history("date " + " ".join(gen_args))
        if not gen_args:
            print(datetime.datetime.now())
        else:
            print("pysh: date: incorrect usage: try 'date'")

    def do_file(self, *args):
        files = args[0].split()
        self.save_history("file " + " ".join(files))
        if len(files) != 0:
            for file in files:
                file_details = []
                try:
                    file_type = magic.from_file(file, mime=True)
                    # file_details.append(file_type.mime)
                    # file_details.append(file_type.name)
                    file_details.append(file_type)
                    file_details.append(
                        str(os.path.getsize(file)) + ' bytes')
                    file_details.append('Modified: ' + str(time.ctime(
                        os.path.getmtime(file))))
                    file_details.append('Created: ' + str(time.ctime(
                        os.path.getctime(file))))

                    print(', '.join(str(detail) for detail in file_details))
                    print()
                except Exception as ex:
                    print(ex)
                    print("pysh: file: file '{}' does not exist or is inaccessible".format(
                        file))
        else:
            print("pysh: file: incorrect usage: try 'file [FILE]...'")

    def do_history(self, *args):
        options = args[0].split()
        self.save_history("history " + " ".join(options))
        if len(options) == 0:
            for command in self.commands_history:
                print(command)
        elif len(options) == 1:
            if options[0] == "-a":
                with open(self.history_file_path, 'r') as history_file:
                    print(history_file.read())
            else:
                print("pysh: history: incorrect usage: try 'history' or 'history -a'")
        else:
            print("pysh: history: incorrect usage: try 'history' or 'history -a'")

    def do_head(self, *args):
        gen_args = args[0].split()
        self.save_history("head " + " ".join(gen_args))
        if len(gen_args) == 1 or len(gen_args) == 3:
            args_index = -1
            file_index = 0
            no_of_lines = 10
            if '-n' in gen_args:
                args_index = gen_args.index('-n')
                file_index = 2 if (args_index == 0) else 0
                if args_index != 2:
                    no_of_lines = int(gen_args[args_index + 1])
                    if os.path.isfile(gen_args[file_index]):
                        f = open(gen_args[file_index], 'r')
                        count = 0
                        for line in f:
                            if count == no_of_lines:
                                break
                            count += 1
                            print(line.strip())
                    else:
                        print("pysh: head: file '{}' does not exist".format(
                            gen_args[file_index]))
                else:
                    print(
                        "pysh: head: incorrect usage: try 'head [FILE]' or 'head [FILE] -n [NUMBER_OF_LINES]'")
            else:
                if os.path.isfile(gen_args[file_index]):
                    f = open(gen_args[file_index], 'r')
                    count = 0
                    for line in f:
                        if count == no_of_lines:
                            break
                        count += 1
                        print(line.strip())
                else:
                    print("pysh: head: file '{}' does not exist".format(
                        gen_args[file_index]))
        else:
            print(
                "pysh: head: incorrect usage: try 'head [FILE]' or 'head [FILE] -n [NUMBER_OF_LINES]'")

    def do_tail(self, *args):
        gen_args = args[0].split()
        self.save_history("tail " + " ".join(gen_args))
        if len(gen_args) == 1 or len(gen_args) == 3:
            args_index = -1
            file_index = 0
            no_of_lines = 10
            text_lines = []
            if '-n' in gen_args:
                args_index = gen_args.index('-n')
                file_index = 2 if (args_index == 0) else 0
                if args_index != 2:
                    no_of_lines = int(gen_args[args_index + 1])
                    if os.path.isfile(gen_args[file_index]):
                        f = open(gen_args[file_index], 'r')
                        for line in f:
                            text_lines.append(line.strip())
                        if len(text_lines) < no_of_lines:
                            result_lines = text_lines
                        else:
                            result_lines = text_lines[(
                                len(text_lines) - no_of_lines):]
                        print(*result_lines, sep='\n')
                    else:
                        print("pysh: tail: file '{}' does not exist".format(
                            gen_args[file_index]))
                else:
                    print(
                        "pysh: tail: incorrect usage: try 'tail [FILE]' or 'tail [FILE] -n [NUMBER_OF_LINES]'")
            else:
                if os.path.isfile(gen_args[file_index]):
                    f = open(gen_args[file_index], 'r')
                    for line in f:
                        text_lines.append(line.strip())
                    if len(text_lines) < no_of_lines:
                        result_lines = text_lines
                    else:
                        result_lines = text_lines[(
                            len(text_lines) - no_of_lines):]
                    print(*result_lines, sep='\n')
                else:
                    print("pysh: tail: file '{}' does not exist".format(
                        gen_args[file_index]))
        else:
            print(
                "pysh: tail: incorrect usage: try 'tail [FILE]' or 'tail [FILE] -n [NUMBER_OF_LINES]'")

    def do_touch(self, *args):
        files = args[0].split()
        self.save_history("touch " + " ".join(files))
        if len(files) != 0:
            for file in files:
                if not os.path.isfile(file):
                    with open(file, 'w') as new_file:
                        pass
                elif os.path.isfile(file):
                    os.utime(
                        file, (datetime.datetime.now().timestamp(), datetime.datetime.now().timestamp()))
        else:
            print("pysh: touch: incorrect usage: try 'touch [FILE]...'")

    def do_wc(self, *args):
        files = args[0].split()
        self.save_history("wc " + " ".join(files))
        if len(files) != 0:
            for file in files:
                number_of_lines = 0
                word_count = 0
                char_count = 0
                if os.path.isfile(file):
                    with open(file, 'r') as f:
                        for line in f:
                            number_of_lines += 1
                            word_count += len(line.split())
                            for ch in line:
                                char_count += 1
                        print("{} {} {} {}".format(
                            number_of_lines, word_count, char_count, file))
                else:
                    print("pysh: wc: '{}': No such file or directory".format(file))
        else:
            print("pysh: wc: incorrect usage: try 'wc [FILE]...'")

    def do_ip(self, *args):
        gen_args = args[0].split()
        self.save_history("ip")
        if not gen_args:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            print("{} {}".format(hostname, ip_address))
        else:
            print("pysh: ip: incorrect usage: try 'ip'")

    def do_host(self, *args):
        gen_args = args[0].split()
        self.save_history("host " + " ".join(gen_args))
        if len(gen_args) == 1:
            try:
                res = dns.resolver.Resolver()
                result = res.resolve(gen_args[0], 'A')
                for val in result:
                    print(val)
            except:
                print("pysh: host: invalid arguments: try 'host [DOMAIN]'")
        else:
            print("pysh: host: incorrect usage: try 'host [DOMAIN]'")

    def do_arch(self, *args):
        gen_args = args[0].split()
        self.save_history("arch")
        if not gen_args:
            print(platform.platform())
            print(platform.system())
            print(platform.processor())
            print(platform.architecture())
        else:
            print("pysh: arch: incorrect usage: try 'arch'")

    def do_ps(self, *args):
        gen_args = args[0].split()
        self.save_history("ps " + " ".join(gen_args))
        if not gen_args:
            for proc in psutil.process_iter():
                try:
                    process_name = proc.name()
                    process_id = proc.pid
                    print(process_name, ":::", process_id)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    print("Internal Error")

        else:
            print("pysh: ps: incorrect usage: try 'ps'")

    def do_wget(self, *args):
        url = args[0]
        self.save_history("wget " + " ".join(url))
        if len(url) != 0:
            try:
                with urllib.request.urlopen(url) as response, open(self.downloads_path + 'temp', 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
            except (urllib.error.HTTPError):
                print("Internal Error")
        else:
            print("pysh: wget: incorrect usage: try 'wget [URL]'")

    def do_kill(self, *args):
        gen_args = args[0].split()
        self.save_history("kill " + " ".join(gen_args))
        if len(gen_args) == 1:
            try:
                os.kill(int(gen_args[0]), signal.SIGTERM)
            except:
                print("Internal Error")

        else:
            print("pysh: kill: incorrect usage: try 'kill [PID]'")

    def do_diff(self, *args):
        gen_args = args[0].split()
        self.save_history("diff " + " ".join(gen_args))
        if len(gen_args) == 2:
            if os.path.isfile(gen_args[0]) and os.path.isfile(gen_args[1]):
                with open(gen_args[0], 'r') as file1:
                    with open(gen_args[1], 'r') as file2:
                        line_nos = []
                        file1_total_lines = 0
                        file2_total_lines = 0
                        file1_dict = {}
                        file2_dict = {}
                        index = 1
                        for line in file1:
                            file1_total_lines += 1

                        for line in file2:
                            file2_total_lines += 1

                        file1.seek(0)
                        file2.seek(0)

                        if file1_total_lines != 0:
                            for ln1 in file1:
                                file1_dict[index] = ln1.strip()
                                index += 1

                        index = 1

                        if file2_total_lines != 0:
                            for ln2 in file2:
                                file2_dict[index] = ln2.strip()
                                index += 1

                        min_index = max(file1_total_lines, file2_total_lines)

                        for ind in range(1, min_index + 1):
                            if ind in file1_dict.keys() and ind in file2_dict.keys():
                                if file1_dict[ind] != file2_dict[ind]:
                                    line_nos.append(ind)
                            elif ind not in file1_dict.keys():
                                line_nos.append(ind)
                                file1_dict[ind] = 'NA'
                            elif ind not in file2_dict.keys():
                                line_nos.append(ind)
                                file2_dict[ind] = 'NA'

                        file1.seek(0)
                        file2.seek(0)

                        if line_nos:
                            file1_line_nos = []
                            for number in line_nos:
                                if number <= file1_total_lines:
                                    file1_line_nos.append(number)

                            file2_line_nos = []
                            for number in line_nos:
                                if number <= file2_total_lines:
                                    file2_line_nos.append(number)

                            for line_no in file1_line_nos:
                                file1.seek(0)
                                file2.seek(0)
                                line_counter = 0
                                for line in file1:
                                    line_counter += 1
                                    if line_counter == line_no:
                                        if line.strip() != 'NA':
                                            print('< ' + line.strip())

                            print("---")
                            for line_no in file2_line_nos:
                                file1.seek(0)
                                file2.seek(0)
                                line_counter = 0
                                for line in file2:
                                    line_counter += 1
                                    if line_counter == line_no:
                                        if line.strip() != 'NA':
                                            print('< ' + line.strip())
            else:
                if not os.path.isfile(gen_args[0]):
                    print("pysh: diff: {}: No such file or directory".format(
                        gen_args[0]))
                if not os.path.isfile(gen_args[1]):
                    print("pysh: diff: {}: No such file or directory".format(
                        gen_args[1]))
        else:
            print("pysh: diff: incorrect usage: try 'diff [FILE1] [FILE2]'")

    def do_grep(self, *args):
        commands = args[0].split()
        self.save_history("grep " + " ".join(commands))
        if len(commands) <= 1:
            print(
                "pysh: chmod: incorrect usage: try 'grep pattern [FILES] [OPTIONS]'")
            return
        pattern = BoyerMooreAlgorithm(commands[0])

        if '-f' in commands:
            if os.path.exists(os.getcwd() + '/' + commands[commands.index('-f') - 1]):
                with open(commands[commands.index('-f') - 1], 'r') as file:
                    line_number = 1
                    for line in file:
                        pattern.find_pattern(
                            line.split(' '), True, line_number)
                        line_number += 1
            else:
                print("pysh: grep: {}: No such file or directory".format(
                    commands[commands.index('-f') - 1]))

        else:
            pattern.find_pattern(commands[1:])

    def do_chmod(self, *args):
        gen_args = args[0].split()
        
        HELP_MESSAGE = "pysh: chmod: incorrect usage:\nValid Use:\n\t'chmod [PERMISSIONS] [FILES]'\n\t'chmod -c [PERMISSIONS] [FILES]'\n\t'chmod -C [PERMISSIONS] [FILES]'"
        if len(gen_args) <= 1:
            print(HELP_MESSAGE)
            return
    
        cascade = 0 # no cascade
        
        if gen_args[0] == '-c':
            cascade = 1 # cascade only once
            permissions, files = gen_args[1], gen_args[2:]
        elif gen_args[0] == '-C':
            cascade = 2 # cascade for all directories and subdirectories
            permissions, files = gen_args[1], gen_args[2:]
        else:
            permissions, files = gen_args[0], gen_args[1:]

        permission_decimal = 0
        if permissions.isnumeric():

            if len(permissions) != 3 or not all(['0' <= digit <= '7' for digit in permissions]):
                print(
                    f"pysh: chmod: {permissions}: Invalid access permission bits")
                return

            for digit in permissions:
                permission_decimal = 8 * permission_decimal + int(digit)

            for file in files:
                try:
                    if os.path.isfile(file):
                        oldPerms = oct(os.stat(file).st_mode)[-4:]
                        os.chmod(file, permission_decimal)
                        newPerms = oct(os.stat(file).st_mode)[-4:]
                        print(f"pysh: chmod: {file} Permissions changed from {oldPerms} to {newPerms}")

                    elif os.path.isdir(file):
                        oldPerms = oct(os.stat(file).st_mode)[-4:]
                        os.chmod(file, permission_decimal)
                        newPerms = oct(os.stat(file).st_mode)[-4:]
                        print(f"pysh: chmod: {file} Permissions changed from {oldPerms} to {newPerms}")
                        if cascade == 1:
                            dir_files = ' '.join( [os.path.join(file, subfile) for subfile in os.listdir(file)] )
                            self.do_chmod(f'{permissions} {dir_files}')
                        elif cascade == 2:
                            dir_files = ' '.join( [os.path.join(file, subfile) for subfile in os.listdir(file)] )
                            self.do_chmod(f'-C {permissions} {dir_files}')

                    else:
                        print(
                            f"pysh: chmod: {file}: No such file or directory")
                except PermissionError:
                    print("Internal Error")
        else:
            if len(permissions) <= 1 or len(permissions) > 4 or permissions[0] not in ['+', '-'] or any([flag not in ['r', 'w', 'x'] for flag in permissions[1:]]):
                print(HELP_MESSAGE)
                return

            permission_bitmask = 0
            if 'r' in permissions:
                permission_bitmask += (1 << 2) * ((1 << 6) + (1 << 3) + 1)
            if 'w' in permissions:
                permission_bitmask += (1 << 1) * ((1 << 6) + (1 << 3) + 1)
            if 'x' in permissions:
                permission_bitmask += (1) * ((1 << 6) + (1 << 3) + 1)

            if permissions[0] == '+':
                for file in files:
                    try:
                        if os.path.isfile(file) or os.path.isdir(file):
                            oldPerms = (os.stat(file).st_mode &
                                        ((1 << 10) - 1))
                            newPermDecimal = oldPerms | permission_bitmask
                            oldPerms = oct(os.stat(file).st_mode)[-4:]
                            os.chmod(file, newPermDecimal)
                            newPerms = oct(os.stat(file).st_mode)[-4:]
                            print(
                                f"pysh: chmod: {file} Permissions changed from {oldPerms} to {newPerms}")
                        else:
                            print(
                                f"pysh: chmod: {file}: No such file or directory")
                    except PermissionError:
                        print("Internal Error")

            else:  # permissions[0] == '-'
                for file in files:
                    try:
                        if os.path.isfile(file) or os.path.isdir(file):
                            oldPerms = (os.stat(file).st_mode & ((1 << 10) - 1)) # masling last 9 bits to extract file mods

                            newPermDecimal = oldPerms & (((1 << 10) - 1) - permission_bitmask)
                            
                            oldPerms = oct(os.stat(file).st_mode)[-4:]
                            
                            os.chmod(file, newPermDecimal)
                            newPerms = oct(os.stat(file).st_mode)[-4:]
                            print(
                                f"pysh: chmod: {file} Permissions changed from {oldPerms} to {newPerms}")
                        else:
                            print(
                                f"pysh: chmod: {file}: No such file or directory")
                    except PermissionError:
                        print("Internal Error")

    def do_tree(self, *gen_args):
        gen_args = gen_args[0].split()
        INVALID_SYNTAX = "pysh: tree: Incorrect Usage: try 'tree' or 'tree [DIRECTORY_PATH]...'"

        if  len(gen_args) > 1:  # found multiple directories
            for dir_path in gen_args:
                self.do_tree(dir_path)
            return
        elif len(gen_args) == 1: # single directory path found
            dir_path = gen_args[0]
        else: # current directory tree call
            dir_path = '.'

        # if path is not dir or dir does not have read permission
        if not os.path.isdir(dir_path) or not os.access(dir_path, os.R_OK):
            print(f"{dir_path} [error opening dir]")
            print("\n0 (sub)directories, 0 files\n")
            return

        def helper(indentCount): # recursive helper function
            fileCount, dirCount = 0, 0
            content = [ file for file in os.listdir('.') if file[0] != '.' ] # avoiding '.', '..', and hidden files/folders

            for path in content: 
                if os.path.isdir(path): # if path is directory, then recursively print that directory's tree
                    dirCount += 1
                    if os.access(path, os.R_OK): # directory has read permission ?
                        print(indentCount * '|    ' + '|' + '----' + path)
                        os.chdir(path)
                        fCount, dCount = helper(indentCount + 1)
                        fileCount += fCount
                        dirCount += dCount
                        os.chdir('..')
                    else:
                        print(indentCount * '|    ' + '|' + '----' + path, '[error opening dir]')
                else:
                    fileCount += 1
                    print(indentCount * '|    ' + '|' + '----' + path)

            return dirCount, fileCount
        
        cwd = os.getcwd()
        os.chdir(dir_path)
        print(dir_path)
        dir_count, file_count = helper(0)
        os.chdir(cwd)
        print(f"\n{dir_count} (sub)directories, {file_count} files\n")

    # help section

    def help_exit(self):
        print(commands_list_manual['exit'])

    def help_clear(self):
        print(commands_list_manual['clear'])

    def help_lf(self):
        print(commands_list_manual['lf'])

    def help_ldir(self):
        print(commands_list_manual['ldir'])

    def help_pwd(self):
        print(commands_list_manual['pwd'])

    def help_cd(self):
        print(commands_list_manual['cd'])

    def help_mkdir(self):
        print(commands_list_manual['mkdir'])

    def help_calendar(self):
        print(commands_list_manual['calendar'])

    def help_calc(self):
        print(commands_list_manual['calc'])

    def help_whoami(self):
        print(commands_list_manual['whoami'])

    def help_echo(self):
        print(commands_list_manual['echo'])

    def help_rm(self):
        print(commands_list_manual['rm'])

    def help_cat(self):
        print(commands_list_manual['cat'])

    def help_cp(self):
        print(commands_list_manual['cp'])

    def help_mv(self):
        print(commands_list_manual['mv'])

    def help_date(self):
        print(commands_list_manual['date'])

    def help_file(self):
        print(commands_list_manual['file'])

    def help_history(self):
        print(commands_list_manual['history'])

    def help_head(self):
        print(commands_list_manual['head'])

    def help_tail(self):
        print(commands_list_manual['tail'])

    def help_touch(self):
        print(commands_list_manual['touch'])

    def help_wc(self):
        print(commands_list_manual['wc'])

    def help_ip(self):
        print(commands_list_manual['ip'])

    def help_host(self):
        print(commands_list_manual['host'])

    def help_arch(self):
        print(commands_list_manual['arch'])

    def help_ps(self):
        print(commands_list_manual['ps'])

    def help_wget(self):
        print(commands_list_manual['wget'])

    def help_kill(self):
        print(commands_list_manual['kill'])

    def help_diff(self):
        print(commands_list_manual['diff'])

    def help_grep(self):
        print(commands_list_manual['grep'])

    def help_chmod(self):
        print(commands_list_manual['chmod'])

    def help_tree(self):
        print(commands_list_manual['tree'])

    def default(self, line: str) -> bool:
        self.stdout.write("pysh: command not found: {}\n".format(line))

    def complete_help(self, *args):
        return super().complete_help(*args)


if __name__ == '__main__':
    Pysh().cmdloop()
