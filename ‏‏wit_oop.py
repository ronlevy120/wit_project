# upload  177

from distutils.dir_util import copy_tree
import itertools
from os import listdir
import os.path
from pathlib import Path
import random
import shutil
from shutil import copyfile
import sys

from graphviz import Digraph


class Wit:
    def __init__(self):
        """making a directory named "wit" and directory named "images"""
        self.wit_name = ".wit"
        self.img_name = "images"
        self.staging_name = 'staging_area'
        self.wit_parent = os.getcwd()
        self.wit_path = Path(os.path.join(self.wit_parent, self.wit_name))
        self.img_path = Path(os.path.join(self.wit_path, self.img_name))
        self.staging = os.path.join(self.wit_path, self.staging_name)
        if '.wit' not in listdir(self.wit_parent):
            os.mkdir(self.wit_path)  # Create wit dir
            os.mkdir(self.img_path)
            os.mkdir(self.staging)
        os.chdir(self.wit_path)
        with open("activated.txt", "w") as f:
            f.write("master")
            f.close()

    def copytree(self, src, dst, symlinks=False, ignore=None):
        '''To copy file to another folder'''
        if os.path.isdir(src):
            for item in os.listdir(src):
                if item != 'desktop.ini':
                    s = os.path.join(src, item)
                    d = os.path.join(dst, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, symlinks, ignore)
                    else:
                        shutil.copy2(s, d)
        else:
            copyfile(src, dst)

    def copy_dir(self, src, dst):
        """To copy directory to another directory"""
        path, file = os.path.split(src)
        os.chdir(dst)  # set dst to current path
        if not os.path.exists(file):
            os.mkdir(file)
            self.copytree(src, (os.path.join(dst, file)))
        else:
            paths = []
            path_list = []
            for path, _, files in os.walk(dst):
                for i in files:
                    if i != 'desktop.ini':
                        paths = Path(os.path.join(path, i))
                        path_list.append(paths)
            for p in path_list:
                small_path = os.path.split(p)[0]
                dirname = os.path.split(small_path)[1]
                if dirname == file:
                    if os.path.isfile(file):
                        os.remove(file)
                        self.copytree(src, (os.path.join(dst, file)))
                    else:
                        shutil.rmtree(small_path, ignore_errors=True)
                        os.mkdir(file)
                        self.copytree(src, (os.path.join(dst, file)))

    def add(self):
        src = sys.argv[2]
        dst = self.staging
        path = Path(os.getcwd())  # path is the current working directory
        onlyfiles = []
        status = False
        while not status:  # While there is not parent 'wit' directory
            if os.path.isdir(path):
                for f in listdir(path):
                    onlyfiles.append(f)  # if the current path is a dir, list all file inside
            else:
                onlyfiles = [path]  # make a list with the one file
            if ".wit" in onlyfiles:
                if os.path.isdir(src):
                    self.copy_dir(src, dst)
                    status = True
        #
                else:
                    filename = os.path.split(src)[1]
                    if os.path.exists(os.path.join(dst, filename)):
                        os.remove(os.path.join(dst, filename))
                        shutil.copy(src, dst)
                    else:
                        shutil.copy(src, dst)
                    status = True  # stop iteration
            #
            #
            else:
                path = path.parent  # move to parent dir
                if len(str(path)) <= 3:  # no more parent directory
                    raise ValueError("no .wit directory found")

    def commit(self):
        path = Path(os.getcwd())  # path is the current working directory
        onlyfiles = []
        status = False
        wit = False
        while not status:
            '''Until you find .wit file'''
            if os.path.isdir(path):
                for f in listdir(path):
                    onlyfiles.append(f)
            else:
                onlyfiles = [path]
            if ".wit" in onlyfiles:
                wit = True
                status = True
            else:
                path = path.parent
                if len(str(path)) <= 3:
                    raise ValueError("no .wit directory found")
        if wit:  # if there is parent .wit file
            img_files = []
            already_have = False  # image dir is empty
            for f in listdir(self.img_path):  # check all files in img dir
                img_files.append(f)
            for file in img_files:
                img_file_path = os.path.join(self.img_path, file)
                if os.path.isdir(img_file_path) and len(file) == 40:
                    already_have = True  # if condition true, img dir is not empty

            if already_have:  # if img dir already had files
                self.before_status()
                os.chdir(self.wit_path)
                with open("references.txt", "r") as txt_file:
                    txt_file = txt_file.read().split('\n')
                    parent = txt_file[0].split('=')
                    parent = parent[1]  # geting the parent from line HEAD

                with open("references.txt", "r") as txt_file:
                    txt_file = txt_file.read().split('\n')
                    txt_file = list(filter(None, txt_file))
                    if len(txt_file) < 3:
                        new_branch = txt_file[1].split('=')[1]
                        branch = txt_file[1].split('=')[0]
                        if self.master == self.head and new_branch == self.head:
                            with open("references.txt", "w") as f:
                                '''references file to .wit'''
                                f.write(f"HEAD={parent}\nmaster={parent}\n{branch}={new_branch}")
                                f.close()
                        else:
                            with open("references.txt", "w") as f:
                                f.write(f"HEAD={parent}\nmaster={self.master}")
                                f.close()
                    else:
                        with open("references.txt", "w") as f:
                            f.write(f"HEAD={parent}\nmaster={self.master}")
                            f.close()

            else:
                parent = 'parent'

            idx_list = []
            d_chr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f']
            for _ in range(40):
                temp = random.randrange(len(d_chr))
                idx_list.append(temp)
            name = ''
            for i in idx_list:
                name += d_chr[i]
            new_path = os.path.join(self.img_path, name)
            os.chdir(self.img_path)
            os.mkdir(new_path)  # make new direcoty with 'name' title
            os.chdir(new_path)
            with open(f"{name}.txt", "w") as f:
                f.write(f"parent={parent}\ndate=Sat Aug 26 19:00:20 2020 +0300\nmessage={sys.argv[2]}")
                f.close()

            onlyfiles = []
            for f in listdir(self.staging):
                '''copying files to new dir'''
                onlyfiles.append(f)
            for f in onlyfiles:
                f_path = Path(os.path.join(self.staging, f))
                if os.path.isfile(f_path):
                    shutil.copy(f_path, new_path)

                else:
                    self.copy_dir(f_path, new_path)

            os.chdir(self.wit_path)

            with open("references.txt", "w") as f:
                f.write(f"HEAD={name}\nmaster={name}")
                f.close()

    def before_status(self):
        global wit
        path = Path(os.getcwd())
        onlyfiles = []
        status = False
        while not status:
            '''looking for parent .wit files'''
            if os.path.isdir(path):
                for f in listdir(path):
                    onlyfiles.append(f)
            else:
                onlyfiles = [path]
            if ".wit" in onlyfiles:
                wit = True
                status = True

            else:
                path = path.parent
                if len(str(path)) <= 3:
                    raise ValueError("no .wit directory found")
        if wit:
            os.chdir(self.wit_path)
            with open("references.txt", "r") as txt_file:
                '''last comit id from HEAD (references files)'''
                self.txt_file = txt_file.read().split('\n')
                master = self.txt_file[1].split('=')
                self.master = master[1]
                head = self.txt_file[0].split('=')
                self.head = head[1]

            # looking for files that has been added but not commited
            img_files_list = []
            img_path_list = []
            for path, _, files in os.walk(self.img_path):
                for i in files:
                    if i != 'desktop.ini':
                        img_path_list.append(Path(os.path.join(path, i)))
                        if 40 > len(i) > 0:
                            img_files_list.append(i)
            self.img_files_set = set(img_files_list)

            staging_list = []
            staging_path_list = []
            for path, _, files in os.walk(self.staging):
                for i in files:
                    if i != 'desktop.ini':
                        staging_path_list.append(Path(os.path.join(path, i)))
                        staging_list.append(i)
            self.staging_set = set(staging_list)

            self.changes_to_be_committed = []
            for file in self.staging_set:
                if file not in self.img_files_set:
                    self.changes_to_be_committed.append(file)

            # Changes not staged for commit
            self.added_and_commited = []
            self.changes_not_staged_for_commit = []
            for file in self.staging_set:
                if file in self.img_files_set:
                    self.added_and_commited.append(file)

                staging_dicti = {}
                for p in staging_path_list:
                    filename = os.path.split(p)[1]
                    if filename in self.added_and_commited:
                        with open(p, encoding="utf8") as staging_file:
                            staging_file = staging_file.read()
                            if 'Google\\Drive\\googledrivesync.exe' not in staging_file:
                                staging_dicti.update({filename: staging_file})

                parent_dicti = {}
                wit_parent_list = []
                for path, _, files in os.walk(self.wit_parent):
                    for i in files:
                        if i != 'desktop.ini':
                            wit_parent_list.append(Path(os.path.join(path, i)))

                for p in wit_parent_list:
                    filename = os.path.split(p)[1]
                    if filename in self.added_and_commited:
                        with open(p, encoding="utf8") as parent_file:
                            parent_file = parent_file.read()
                            if 'Google\\Drive\\googledrivesync.exe' not in parent_file:
                                parent_dicti.update({filename: parent_file})

                for filename, full_file in staging_dicti.items():
                    if filename in parent_dicti:
                        if not full_file == parent_dicti[filename]:
                            self.changes_not_staged_for_commit.append(filename)
            self.changes_not_staged_for_commit = list(set(self.changes_not_staged_for_commit))

            # Untracked files
            wit_files = []
            exclude = []
            for __, _, files in os.walk(self.wit_path):
                for i in files:
                    exclude.append(i)
            for _, dirs, __ in os.walk(self.wit_parent):
                for i in dirs:
                    if os.path.isfile(i):
                        if i not in exclude and i != 'desktop.ini':
                            wit_files.append(i)
                    else:
                        if i not in exclude:
                            i_path_isdir = Path(os.path.join(self.wit_parent, i))
                            for __, _, d_files in os.walk(i_path_isdir):
                                for j in d_files:
                                    wit_files.append(j)
            for i in listdir(self.wit_parent):
                    wit_files.append(i)

            wit_set = set(wit_files)
            # global untracked_files
            self.untracked_files = []
            for file in wit_set:
                if file not in self.staging_set:
                    self.untracked_files.append(file)

        self.the_status = f'''------ Status: ------
    Current commit id: {self.head}
    Changes to be committed: {self.changes_to_be_committed }
    changes not staged for commit: {self.changes_not_staged_for_commit}
    Untracked files: {self.untracked_files}'''

    def status(self):
        self.before_status()
        print(self.the_status)

    def rm(self):
        file_to_delete = sys.argv[2]
        os.chdir(self.staging)
        self.file_path = Path(os.path.join(self.staging, file_to_delete))
        if os.path.exists(self.file_path):
            if os.path.isdir(self.file_path):
                shutil.rmtree(self.file_path, ignore_errors=True)
            else:
                os.remove(self.file_path)

    def checkout(self):
        self.before_status()
        if sys.argv[2] == 'master':
            commit_id = self.txt_file[1]
            commit_id = commit_id.split('=')[1]
        else:
            if len(sys.argv) == 40:
                commit_id = sys.argv[2]
            else:
                with open("references.txt", "r") as txt_file:
                    txt_file = txt_file.read().split('\n')
                    txt_file = list(filter(None, txt_file))
                    if len(txt_file) < 3:
                        commit_id = txt_file[1].split('=')[1]
        status = False
        wit = False
        path = Path(os.getcwd())
        onlyfiles = []
        while not status:
            '''Until you find .wit file'''
            if os.path.isdir(path):
                for f in listdir(path):
                    onlyfiles.append(f)
            else:
                onlyfiles = [path]
            if ".wit" in onlyfiles:
                wit = True
                status = True
            else:
                path = path.parent
                if len(str(path)) <= 3:
                    raise ValueError("no .wit directory found")
        if wit:
            if len(self.changes_to_be_committed) == 0 or len(self.changes_not_staged_for_commit) == 0:
                dont_touch_files = []
                for __, _, files in os.walk(self.wit_parent):
                    for i in files:
                        if i in self.untracked_files:
                            dont_touch_files.append(i)

                wit_files = []
                for __, _, files in os.walk(self.wit_path):
                    for i in files:
                        wit_files.append(i)

                for filename in os.listdir(self.wit_parent):
                    file_path = os.path.join(self.wit_parent, filename)
                    if os.path.isfile(file_path):
                        if file_path not in wit_files and filename not in self.untracked_files:
                            os.remove(file_path)

                # remove empty folders
                folders = list(os.walk(self.wit_parent))[:1]
                folders = folders[0][1]
                for folder in folders:
                    if folder != '.wit':
                        result = any(elem in self.untracked_files for elem in listdir(os.path.join(self.wit_parent, folder)))
                        if not result:
                            the_p = os.path.join(self.wit_parent, folder)
                            shutil.rmtree(the_p, ignore_errors=True)
                data_src = os.path.join(self.img_path, commit_id)
                copy_tree(data_src, self.wit_parent)

                os.chdir(self.wit_path)
                with open("references.txt", "r") as txt_file:
                    txt_file = txt_file.read().split('\n')
                    txt_file = list(filter(None, txt_file))
                    if len(txt_file) < 3:
                        new_branch = txt_file[1].split('=')[1]
                    else:
                        new_branch = "NAME"
                with open("activated.txt ", 'w') as file:
                    file.write(new_branch)

            else:
                print("changes not staged for commit and changes to be committed must ne empty")

            os.chdir(self.wit_path)
            with open("references.txt", "w") as f:
                f.write(f"HEAD={commit_id}\nmaster={self.master}")
                f.close()

            shutil.rmtree(self.staging)
            copy_tree(os.path.join(self.img_path, commit_id), self.staging)

    def graph(self):
        self.before_status()
        if len(sys.argv) > 2 and sys.argv[2] == '--all':
                the_all = True
        else:
            the_all = False

        status = False
        wit = False
        path = Path(os.getcwd())
        onlyfiles = []
        while not status:
            '''Until you find .wit file'''
            if os.path.isdir(path):
                for f in listdir(path):
                    onlyfiles.append(f)
            else:
                onlyfiles = [path]
            if ".wit" in onlyfiles:
                wit = True
                status = True
            else:
                path = path.parent
                if len(str(path)) <= 3:
                    raise ValueError("no .wit directory found")
        if wit:
            commit_list = []
            for _, dirs, __ in os.walk(self.img_path):
                for d_dir in dirs:
                    for file in listdir(os.path.join(self.img_path, d_dir)):
                        if len(file) == 44:
                            with open(os.path.join(self.img_path, d_dir, file), 'r') as f:
                                parent = f.read().split('\n')[0]
                                parent = parent.split('=')[1]
                                commit_list.append([file, parent])
            commit_list.sort()
            commit_list = [commit_list for commit_list, _ in itertools.groupby(commit_list)]
            if the_all:
                g = Digraph('G', filename='all digraph', format='png')
                for i in commit_list:
                    child = i[0][:40]
                    parent = i[1]
                    g.edge(child, parent)
                g.view()

            else:
                the_parent = ''
                for i in commit_list:
                    if self.head == i[0][:40]:
                        the_parent = i[1]
                g = Digraph('G', filename='parent digraph', format='png')
                g.edge('head', self.head)
                g.edge('master', self.head)
                g.edge(self.head, the_parent)

                g.view()

    def branch(self):
        status = False
        wit = False
        path = Path(os.getcwd())
        onlyfiles = []
        while not status:
            '''Until you find .wit file'''
            if os.path.isdir(path):
                for f in listdir(path):
                    onlyfiles.append(f)
            else:
                onlyfiles = [path]
            if ".wit" in onlyfiles:
                wit = True
                status = True
            else:
                path = path.parent
                if len(str(path)) <= 3:
                    raise ValueError("no .wit directory found")
        if wit:
            self.before_status()
            branch = sys.argv[2]
            os.chdir(self.wit_path)
            with open("references.txt", "r") as txt_file:
                txt_file = txt_file.read().split('\n')
                txt_file = list(filter(None, txt_file))
                if len(txt_file) < 3:
                    is_name = False
                else:
                    is_name = True
            if is_name:
                txt_file = txt_file[:1]
                txt_file.append(f"{branch} = {self.head}")
                string = ''
                for i in txt_file:
                    string += i + '\n'
                with open("references.txt", "w") as f:
                    f.write(string)
                    f.close()
            else:
                with open("references.txt", "a") as f:
                    f.write(f"\n{branch} = {self.head}")
                    f.close()

    def merge(self):
        self.before_status()
        branch_name = sys.argv[2]
        branch_commit_list = []
        parent_list = []
        os.chdir(self.wit_path)
        if len(branch_name) < 40:
            with open("references.txt", "r") as txt_file:
                txt_file = txt_file.read().split('\n')
                txt_file = list(filter(None, txt_file))
                branch_commit = txt_file[2].split('=')[1]
                branch_commit = branch_commit.replace(" ", "")
                branch_commit_list.append(branch_commit)
        else:
            branch_commit = branch_name
            branch_commit_list.append(branch_commit)

        os.chdir(os.path.join(self.img_path, self.head))
        with open(self.head + '.txt', 'r') as parent_file:
            parent = parent_file.read().split('\n')[0].split('=')[1]
            parent = parent.replace(" ", "")
            parent_list.append(parent)

        while not any(i in parent_list for i in branch_commit_list) or parent == 'parent' and branch_name == 'parent':
            if branch_commit != 'parent':
                os.chdir(os.path.join(self.img_path, branch_commit))
                with open(branch_commit + '.txt', 'r') as branch_file:
                    branch_commit = branch_file.read().split('\n')[0].split('=')[1]
                    branch_commit_list.append(branch_commit)
            if parent != 'parent':
                    os.chdir(os.path.join(self.img_path, parent))
                    with open(parent + '.txt', 'r') as parent_file:
                        parent = parent_file.read().split('\n')[0].split('=')[1]
                    parent_list.append(parent)
        merge_list = parent_list + branch_commit_list
        merge_list = list(set(merge_list))
        for i in merge_list:
            if i == 'parent':
                merge_list.remove(i)
        idx_list = []
        the_chr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f']
        for _ in range(40):
            temp = random.randrange(len(the_chr))
            idx_list.append(temp)
        name = ''
        for i in idx_list:
            name += the_chr[i]
        new_folder = os.path.join(self.img_path, name)
        os.mkdir(new_folder)
        for commit in merge_list:
            for file in listdir(os.path.join(self.img_path, commit)):
                shutil.copy(os.path.join(self.img_path, commit, file), new_folder)
        # #
        for i in listdir(new_folder):
            if i[-3:] == 'txt':
                try:
                    os.remove(i)
                except OSError:
                    pass

        for __, _, files in os.walk(self.staging):
            for i in files:
                if i in listdir(new_folder):
                    try:
                        os.remove(i)
                    except OSError:
                        pass
        for __, _, files in os.walk(new_folder):
            for i in files:
                shutil.copy(os.path.join(new_folder, i), self.staging)


if __name__ == "__main__":
    w = Wit()
    if sys.argv[1] == 'add':
        w.add()
    elif sys.argv[1] == 'commit':
        w.commit()
    elif sys.argv[1] == 'status':
        w.status()
    elif sys.argv[1] == 'rm':
        w.rm()
    elif sys.argv[1] == 'checkout':
        w.checkout()
    elif sys.argv[1] == 'graph':
        w.graph()
    elif sys.argv[1] == 'branch':
        w.branch()
    elif sys.argv[1] == 'merge':
        w.merge()

# Reupload 177
