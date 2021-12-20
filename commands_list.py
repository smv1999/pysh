commands_list = ['lf', 'ldir', 'pwd', 'cd', 'manual', 'mkdir',
                 'calendar', 'calc', 'whoami', 'echo', 'rm', 'cat', 'cp', 'mv']

commands_list_manual = {
    'lf': 'lists all files in the current directory',
    'ldir': 'lists all directories in the current directory',
    'pwd': 'prints the name of the current/working directory',
    'cd': "changes the current/working directory. \n usage: 'cd [DIRECTORY]'",
    'manual': "gives information about a command. \n usage: 'manual [COMMAND] \n For example: manual pwd'",
    'mkdir': 'make directories - used for creating directories if they do not already exist. \n usage: mkdir [DIRECTORY_NAME]',
    'calendar': "displays the calendar of a given date. \n usage: 'calendar [YEAR]' or 'calendar [YEAR] [MONTH]' \n For example: 'calendar 2021' or 'calendar 2021 12'",
    'calc': "evaluates a mathematical expression. \n usage: 'calc [EXPR]'",
    'whoami': 'displays the username of the currently logged-in user',
    'echo': "displays a line of text. \n usage: 'echo [TEXT]'",
    'rm': "remove files or directories. \n usage: 'rm [DIRECTORY]' or 'rm [FILE]'",
    'cat': "",
    'cp': "",
    'mv': ""
}
