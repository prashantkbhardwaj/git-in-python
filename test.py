import os
import sys
import pickle
from shutil import copyfile
from os import listdir
import difflib



class Commit(object):

        def __init__(self, commitId, parent, message):
                self.commitId = commitId
                self.parent = parent
                self.message = message

                fo = open(".gitpy/addinfo.txt", "r+")
                change = fo.read()
                change = change.splitlines()

                print change

		if not os.path.exists('.gitpy/' + str(self.commitId)):
                    os.makedirs(".gitpy/" + str(self.commitId))

                for i in change:
                        if i in os.listdir(os.getcwd()):
                                copyfile(os.getcwd()+ "/" + i, os.getcwd()+ "/.gitpy/" + str(self.commitId) + "/" + i)

                

class Branch(object):

        def __init__(self, name, commit):
                self.name = name
                self.commit = commit



class Git(object):

        def __init__(self):
                self.lastcommitId = -1
                self.HEAD = None


        def commit(self, message):
        	self.lastcommitId = self.lastcommitId + 1
                new_commit = Commit(self.lastcommitId, self.HEAD, message)
                self.HEAD = new_commit
                return new_commit

        def log(self):

                commit = self.HEAD
                history = []

                while (commit):
                        history.append(commit)
                        commit = commit.parent


                return history



argument = sys.argv[1]

if len(sys.argv) == 3:
        specific = sys.argv[2]
elif len(sys.argv) == 4:
        message = sys.argv[3]


if argument == "init":
        if not os.path.exists('.gitpy'):
                os.makedirs('.gitpy')
                print "Initialized an empty repositoru in the current working directory"

                files_in_cwd = os.listdir(os.getcwd())
                files_in_gitpy = os.listdir(os.getcwd() + "/.gitpy")

        else:
                print "Already Exists"

elif argument == "add":

        files_in_cwd = os.listdir(os.getcwd())
        files_in_gitpy = os.listdir(os.getcwd() + "/.gitpy")

        if specific:
                if specific == "-A" or specific == "-a":
                        fo = open(".gitpy/addinfo.txt", "wb")

                        for untracked in files_in_cwd:
                                if untracked not in files_in_gitpy and untracked !=".gitpy":
                                        fo.write(untracked + "\n")

elif argument == "commit":

        repo = pickle.load(fo)
        reoi()
        repo = Git()
        
        repo.commit('Hello World')

        fo = open("hello.txt", "wb")
        fo.write("Testing diff")
        fo.close()

        fo = open("hello.txt", "r+")
        string1 = fo.read()
        string1 = string1.splitlines()
        
        fi = open(".gitpy/" + str(repo.HEAD.commitId) + "/hello.txt")
        string2 = fo.read()
        string2 = string2.splitlines()
        
        diff = difflib.unified_diff(string2, string1, lineterm='')
        print '\n'.join(list(diff))
        

        
        print repo.log()

       
        pickle.dump(repo, fo)
        
elif argument == "dump"
        repo = Git()

        # To dump the object
        fo = open("checking.txt", "wb")

        pickle.dump(repo, fo)

        # To load the object back
        fo = open("checking.txt", "r+")

        repo = pickle.load(fo)

        # Now repo.commit("Hello World") will work. It will have previous objects too
        
