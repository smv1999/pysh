commands_list = ['lf', 'ldir', 'pwd', 'cd', 'manual', 'mkdir',
                 'calendar', 'calc', 'whoami', 'echo', 'rm',
                 'cat', 'cp', 'mv', 'date', 'file', 'history',
                 'head', 'tail', 'touch', 'wc']

commands_list_manual = {
    'lf': 'Lists all files in the current directory',
    'ldir': 'Lists all directories in the current directory',
    'pwd': 'Prints the name of the current/working directory',
    'cd': "Changes the current/working directory. \nusage: 'cd [DIRECTORY]'",
    'manual': "Gives information about a command. \nusage: 'manual [COMMAND] \nFor example: manual pwd'",
    'mkdir': 'Make directories - used for creating directories if they do not already exist. \nusage: mkdir [DIRECTORY_NAME]',
    'calendar': "Displays the calendar of a given date. \nusage: 'calendar [YEAR]' or 'calendar [YEAR] [MONTH]' \nFor example: 'calendar 2021' or 'calendar 2021 12'",
    'calc': "Evaluates a mathematical expression. \nusage: 'calc [EXPR]'",
    'whoami': 'Displays the username of the currently logged-in user',
    'echo': "Displays a line of text. \nusage: 'echo [TEXT]'",
    'rm': "Remove files or directories. \nusage: 'rm [DIRECTORY]' or 'rm [FILE]'",
    'cat': "Concatenate files and print on the standard output. \nusage: 'cat [FILE]...'",
    'cp': "Copy files from source to destination. \nDestination file is created if it doesn't already exist. \nusage: 'cp [SOURCE_FILE] [DESTINATION_FILE]' or 'cp [SOURCE_FILE] [DESTINATION_DIRECTORY]'",
    'mv': "Move files from source to destination. \nIf destination file doesn't exist, then source file is renamed to destination file's name. \nIf destination file exists, then contents of source file are copied to destination file and source file is deleted. \n"
    "usage: 'mv [SOURCE_FILE] [DESTINATION_FILE]' or 'mv [SOURCE_FILE] [DESTINATION_DIRECTORY]'",
    'date': "Displays the current date and time. \nusage: 'date'",
    'file': "Determines and displays the file type and other details. \n usage: 'file [FILE]'",
    'history': "Displays the history of the executed commands. \nusage: 'history' - for viewing the local history of the shell's current session. 'history -a' for viewing the global history of the shell's all sessions."
}
