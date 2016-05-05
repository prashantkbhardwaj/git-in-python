#!/usr/bin/env python
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


files_in_cwd = os.listdir(os.getcwd())

if os.path.exists('.gitpy/'):
        files_in_gitpy = os.listdir(os.getcwd() + "/.gitpy")

        

if argument == "init":
        if not os.path.exists('.gitpy'):
                os.makedirs('.gitpy')
                print "Initialized an empty repository in " + os.getcwd()
        else:
                print "Already Exists"

        repo = Git()
        os.makedirs('.gitpy/dump')
        fo = open(".gitpy/dump/dump.txt", "wb")
        pickle.dump(repo, fo)
        

elif argument == "add":

        fo = open(".gitpy/dump/dump.txt", "r")
        repo = pickle.load(fo)

        if specific:
                if specific == "-A" or specific == "-a":
                        fo = open(".gitpy/dump/addinfo.txt", "wb")

                        for untracked in files_in_cwd: 
                                if not os.path.isdir(os.getcwd()+ "/" + untracked) and untracked!="test.py":
                                        if untracked not in files_in_gitpy:
                                                print untracked
                                                fo.write(untracked + "\n")

elif argument == "commit":

        fo = open(".gitpy/dump/dump.txt", "r")
        repo = pickle.load(fo)
        fo.close()

        try:
                specific
        except NameError:
                print "Provide a message!"
        else:
                repo.commit(specific)

                fo = open(".gitpy/dump/addinfo.txt", "r+")
                change = fo.read()
                fo.close()
                
                change = change.splitlines()

                if change:
                        if not os.path.exists('.gitpy/' + str(repo.HEAD.commitId)):
                                os.makedirs(".gitpy/" + str(repo.HEAD.commitId))

                        for i in change:
                                if i in os.listdir(os.getcwd()):
                                        copyfile(os.getcwd()+ "/" + i, os.getcwd()+ "/.gitpy/" + str(repo.HEAD.commitId) + "/" + i)

                        fo = open(".gitpy/dump/addinfo.txt", 'w').close()
                else:
                        print "Cannot commit before adding"
                
                
        fo = open(".gitpy/dump/dump.txt", "wb")
        pickle.dump(repo,fo)
        fo.close()
        
elif argument == "diff":

        fo = open(".gitpy/dump/dump.txt", "r")
        repo = pickle.load(fo)
        fo.close()

        if repo.HEAD:

                try:
                        specific
                except NameError:

                        for i in files_in_cwd:
                                if not os.path.isdir(os.getcwd()+ "/" + i) and i!="test.py":
                                        fo = open(i, "r+")
                                        string1 = fo.read()
                                        string1 = string1.splitlines()                                       
                                        
                                        fi = open(".gitpy/" + str(repo.HEAD.commitId) + "/" + i, "r+")
                                        string2 = fi.read()
                                        string2 = string2.splitlines()

                                        if string1 != string2:
                                                print 'Printing diff for file:' + i
                                                diff = difflib.unified_diff(string2, string1, lineterm='')
                                                print '\n'.join(list(diff))
                                                print '\n\n\n'

                                                

                                       

                                
                else:
                        fo = open(specific, "r+")
                        string1 = fo.read()
                        string1 = string1.splitlines()

                        fi = open(".gitpy/" + str(repo.HEAD.commitId) + "/" + specific)
                        string2 = fo.read()
                        string2 = string2.splitlines()

                        diff = difflib.unified_diff(string2, string1, lineterm='')
                        print '\n'.join(list(diff))
                        print '\n\n\n'


               
        else:
                print "Cannot compare since no commits in place"


elif argument == "log":

        fo = open(".gitpy/dump/dump.txt", "r")
        repo = pickle.load(fo)
        fo.close()

        print repo.log()

else:
        print "No recognized argument!"
        
                
                
                



        
        
