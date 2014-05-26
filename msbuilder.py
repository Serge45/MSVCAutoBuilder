# -*- coding: utf-8 -*-
import os, subprocess

class Msbuilder:
    def __init__(self, \
                 sln_path = r".\\", \
                 prj_name = "", \
                 build_config = r"Release", \
                 devenv_path = ""):

        self.possible_msbuild_path = []
        self.msbuild_path = None
        self.sln_path = sln_path
        self.prj_name = prj_name
        self.build_config = build_config
        self.build_command = r'/Build'

        if devenv_path != None:
            if len(devenv_path):
                self.possible_msbuild_path.append(devenv_path)

        self.possible_msbuild_path.append(\
            r"C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\devenv.exe")

        for path in self.possible_msbuild_path:
            if os.path.exists(path):
                self.msbuild_path = path
                break;

        if self.msbuild_path == None:
            raise Exception("devenv.exe not found.")


    def build(self, rebuild = False):
        if not os.path.isfile(self.msbuild_path):
            raise Exception("devenv.exe not found.")

        if rebuild:
            self.build_command = r'/Rebuild'

        arg1 = self.build_command
        arg2 = self.build_config
        arg3 = ""
        arg4 = ""
        arg5 = ""
        arg6 = ""

        if self.prj_name != None:
            if len(self.prj_name):
                arg3 = r'/project'
                arg4 = self.prj_name
                arg5 = r'/projectconfig'
                arg6 = self.build_config

        #Modify this line for git or delete it if you do not need update.
        p = subprocess.call([r'svn', r'update', os.path.dirname(os.path.realpath(self.sln_path))])

        if not p:
            print 'Version updated.'
            print 'Start building...'
            print 'Build config: %s' %(self.build_config)

            p = subprocess.call([self.msbuild_path, self.sln_path, arg1, arg2, arg3, \
                                                               arg4, arg5, arg6])
        else:
            print 'svn updating failed.'
            return False

        if not p:
            print 'Build sucessfully.'
            return True

        else:
            print "Build failed"
            return False

#Example
if __name__ == '__main__':
    msbuilder = Msbuilder(r'D:\projects\mp7600\mp7600.sln', r"MP7600Calibration", r'Release')
    msbuilder.build(rebuild = False)
