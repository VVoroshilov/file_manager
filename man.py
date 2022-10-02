import os


class Terminal(object):

    def __init__(self, path):
        """
        При инициации класса запоминаем директорию из настроек, как корневую.
        Создаём атрибут, хранящий текущую директорию для отностельной адресации.
        По умолчания текущая директория является корневой
         """

        self.root = path
        self.cur_path = path

    def corrector(self, name):
        """
        Метод corrector испоьзуется для преобразования имени файла по следующим критериям:
        1. Специальный символ ".." для возврата к предыдущей директории (man cd)
        2. Символы "~" и разделитель (в Linux - "/", в Windows - '\\' для обращения к корневой директории)
        3. Относительная адресация (добавляется путь до текущей директории)
        4. Полная адресация: добавляется путь из настроек программы.
        """

        if name == '..':
            return name

        if name == "~" or name == os.sep:
            return self.root

        if name[0] != os.sep:
            name = self.cur_path + os.sep + name
            
        if self.root in name:
            return name
        else:
            name = self.root + name
        return name

    def mkdir(self, name):
        """
        NAME
         mkdir -- make directories

        SYNOPSIS
             mkdir directory_name

        DESCRIPTION
             The mkdir utility creates the directories.
        """
        name = self.corrector(name)

        if not os.path.isdir(name):
            os.mkdir(name)
        else:
            print(f"Directory {name} already exists")

    def rmdir(self, name):
        """
        NAME
         rmdir -- delete directories

        SYNOPSIS
             rmdir directory_name

        DESCRIPTION
             The rmdir utility deletes the directories.
             If directory is not empty, rmdir deletes directory including content.
        """
        name = self.corrector(name)

        if os.path.isdir(name):
            ls = os.listdir(name)
            if len(ls) != 0:
                for file in ls:
                    file_name = name + os.sep + file
                    if os.path.isfile(file_name):
                        os.remove(file_name)
                    else:
                        self.rmdir(file_name)
            os.rmdir(name)
        else:
            print(f"{name} is not directory or does not exist")

    def cd(self, name):
        """
        NAME
         cd -- change directories

        SYNOPSIS
             cd directory_name

        DESCRIPTION
             The cd utility changes the directories.
             Use cd .. to go to parent directory
             Use cd ~ to go to root directory

             Windows:
             Use cd \\ to go to root directory

             Linux:
             Use cd / to go to root directory
        """
        name = self.corrector(name)

        if name == "..":
            if self.cur_path != self.root and self.root in self.cur_path:
                os.chdir(os.path.dirname(self.cur_path))
                self.cur_path = os.path.dirname(self.cur_path)
        elif os.path.isdir(name):
            os.chdir(name)
            self.cur_path = name
        else:
            print(f"Directory {name} does not exist")

    def touch(self, name):
        """
        NAME
         touch -- create empty file

        SYNOPSIS
             touch file_name

        DESCRIPTION
             The touch utility creates empty file.
             Doing nothing if file exists.
        """
        name = self.corrector(name)

        if not os.path.isfile(name):
            new_file = open(name, "w")
            new_file.close()
        else:
            print(f"{name} already exists")

    def write(self, name):
        """
        NAME
         write -- write to file

        SYNOPSIS
             write file_name

        DESCRIPTION
             The write utility writes in file.
             If file is not empty, utility appends text.
             If file doesn't exist, utility creates new file.
        """
        name = self.corrector(name)

        print("Ctrl+D to stop\n")
        with open(name, "a") as file:
            while True:
                try:
                    string = input() + "\n"
                except EOFError:
                    break
                file.write(string)

    def cat(self, name):
        """
        NAME
         cat -- open file

        SYNOPSIS
             cat file_name

        DESCRIPTION
             The cat utility opens file.
        """
        name = self.corrector(name)

        if os.path.isfile(name):
            with open(name, "r") as file:
                for row in file.readlines():
                    print(row)
        else:
            print(f"{name} does not exist")

    def rm(self, name):
        """
        NAME
         rm -- remove file

        SYNOPSIS
             rm file_name

        DESCRIPTION
             The rm utility removes file.
        """
        name = self.corrector(name)

        if os.path.isfile(name):
            os.remove(name)
        else:
            print(f"{name} does not exist")

    def cp(self, name, direc):
        """
        NAME
         cp -- copy file

        SYNOPSIS
             cp file_name dir_name

        DESCRIPTION
             The cp utility copies file or directory including content.Text file only.
        """
        name = self.corrector(name)
        file_name = name.split(os.sep)[-1]
        direc = self.corrector(direc)

        if os.path.isfile(name):
            with open(name, "r") as file:
                file_copy = file.read()
            with open(direc + os.sep + file_name, "w") as file_cp:
                file_cp.write(file_copy)
        elif os.path.isdir(name):
            os.mkdir(direc + os.sep + file_name)
            for file in os.listdir(name):
                self.cp(name + os.sep + file, direc + os.sep + file_name)
        else:
            print(f"{name} does not exist")

    def move(self, name, new_path):
        """
        NAME
         move -- move file

        SYNOPSIS
             move file_name new_dir

        DESCRIPTION
             The move utility moves file or directory including content.
        """
        name = self.corrector(name)
        file_name = name.split(os.sep)[-1]
        new_path = self.corrector(new_path)

        if self.root not in new_path:
            print("Wrong directory")
        else:
            if os.path.isfile(name) or os.path.isdir(name):
                os.replace(name, new_path + os.sep + file_name)
            else:
                print(f"{name} does not exist")

    def rename(self, name, new_name):
        """
        NAME
         rename -- rename file

        SYNOPSIS
             rename file_name new_name

        DESCRIPTION
             The rename utility renames file or directory.
        """
        new_name = new_name.replace(os.sep, ":")

        if os.sep in name:
            original_path = name[:name.rindex(os.sep) + 1]
            new_name = original_path + new_name

        name = self.corrector(name)
        new_name = self.corrector(new_name)

        if os.path.isfile(name) or os.path.isdir(name):
            os.rename(name, new_name)
        else:
            print(f"{name} does not exist")

    def ls(self, path=None):
        """
        NAME
         ls -- list directory contents

        SYNOPSIS
             ls directory_name

        DESCRIPTION
             The ls utility shows list of content of given directory.
        """
        if path is None:
            path = self.cur_path
        else:
            path = self.corrector(path)
        print(*os.listdir(path), sep='\n')

    def pwd(self):
        """
        NAME
         pwd -- show current directory

        SYNOPSIS
             pwd

        DESCRIPTION
             The pwd utility shows current directory.
        """
        pwd = self.cur_path.replace(self.root, "")
        if pwd == "":
            pwd = os.sep
        print(pwd)

    def r_pwd(self):
        """Версия pwd для отображения пригласительного сообщения."""
        pwd = self.cur_path.replace(self.root, "")
        if pwd == "":
            return os.sep
        return pwd

    def man(self, func_name):
        """
        NAME
         man - an interface to the system reference manuals

        SYNOPSIS
             man utility_name

        DESCRIPTION
             The man utility shows help information about utility.
        """
        if func_name in dir(self):
            print(getattr(self, func_name).__doc__)
        else:
            print(f"{func_name} is not defined")


def main():
    with open('config.txt', 'r') as cfg:
        path = cfg.readline().strip()
    terminal = Terminal(path)
    funcs = [method for method in dir(Terminal) if not method.startswith('__')]

    while True:
        try:
            user_input = input(f"{terminal.r_pwd()}> ").split()
        except EOFError:
            break
        else:

            try:
                if user_input[0] not in funcs:
                    print(f"{user_input[0]} is not defined.\nList of functions: ", end='')
                    print(*funcs, sep=', ', end='.\n')
                    continue
                else:
                    try:
                        getattr(terminal, user_input[0])(*user_input[1:])
                    except Exception as exc:
                        print(f"Some error: {exc}")
                        continue
            except IndexError:
                continue


if __name__ == "__main__":
    main()
