"""
build.py is a modification of compiling script found on the PyGame wiki (contributors listed in page's history section).
http://pygame.org/wiki/Pygame2exe?action=view

The above script also borrows from the Distutils (Python methodology of creating distributions of programs) tutorial found on the official Python wiki, made by a Donn Ingle.
http://wiki.python.org/moin/Distutils/Tutorial

This script is provided as Public Domain.

This script uses the Python module py2exe, an extension of the Distutils framework, which allows the creation of executable files under the modern Windows enviroments.

A bin (binary) directory will be created after running build.py containing the executable file and data used in the program.

Be sure to modify BuildExe.__init__ below to direct this script to those data (ie images and map files), as well as any meta data you may wish to provide.

Ensure a back-up is made of the code you are compiling in the off-chance the otherwise short compliation process is abrupted mid-way.
"""

try:
    from distutils.core import setup
    import py2exe, pygame
    from modulefinder import Module
    import glob, fnmatch
    import sys, os, shutil
    import operator
except ImportError, message:
    raise SystemExit,  "Unable to load module. %s" % message
 
#hack which fixes the pygame mixer and pygame font
origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll","sdl_ttf.dll"): # "sdl_ttf.dll" added by arit.
            return 0
    return origIsSystemDLL(pathname) # return the orginal function
py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one
 
class pygame2exe(py2exe.build_exe.py2exe): #This hack make sure that pygame default font is copied: no need to modify code for specifying default font
    def copy_extensions(self, extensions):
        #Get pygame default font
        pygamedir = os.path.split(pygame.base.__file__)[0]
        pygame_default_font = os.path.join(pygamedir, pygame.font.get_default_font())
 
        #Add font to list of extension to be copied
        extensions.append(Module("pygame.font", pygame_default_font))
        py2exe.build_exe.py2exe.copy_extensions(self, extensions)
 
class BuildExe:
    def __init__(self):
        
        #Name of starting .py
        self.script = "main.py"
 
        #Name of program
        self.project_name = "Fire Engine"
 
        #Project webpage url
        self.project_url = "https://github.com/MatthewRoyBarber/Fire-Engine/"
 
        #Version of program
        self.project_version = "0.1"
 
        #License of the program
        self.license = "Public Domain"
 
        #Auhor of program
        self.author_name = "Matthew Barber"
        self.author_email = "matthewroydonbarber@gmail.com"
        self.copyright = "Copyright (c) 2016 Matthew Barber"
 
        #Description
        self.project_description = "Game similiar to the Fire Emblem strategy game series"
 
        #Icon file (None will use pygame default icon)
        self.icon_file = 'icon.png'
 
        #Extra files/dirs copied to game
        self.extra_datas = ['player.png', 'basin.png', 'tileset.png', 'example.map']
 
        #Extra/excludes python modules
        self.extra_modules = []
        self.exclude_modules = []
        
        #DLL Excludes
        self.exclude_dll = ['']
        #python scripts (strings) to be included, seperated by a comma
        self.extra_scripts = []
 
        #Zip file name (None will bundle files in exe instead of zip file)
        self.zipfile_name = None
 
        #Dist directory
        self.dist_dir = 'bin'
    
    def opj(self, *args):
        path = os.path.join(*args)
        return os.path.normpath(path)
 
    def find_data_files(self, srcdir, *wildcards, **kw):
        """Get a list of all files under the srcdir matching wildcards, returned in a format to be used for install_data"""
        
        def walk_helper(arg, dirname, files):
            if '.svn' in dirname:
                return
            names = []
            lst, wildcards = arg
            for wc in wildcards:
                wc_name = self.opj(dirname, wc)
                for f in files:
                    filename = self.opj(dirname, f)
 
                    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
            if names:
                lst.append( (dirname, names ) )
 
        file_list = []
        recursive = kw.get('recursive', True)
        if recursive:
            os.path.walk(srcdir, walk_helper, (file_list, wildcards))
        else:
            walk_helper((file_list, wildcards),
                        srcdir,
                        [os.path.basename(f) for f in glob.glob(self.opj(srcdir, '*'))])
        return file_list
 
    def run(self):
        if os.path.isdir(self.dist_dir): #Erase previous destination dir
            shutil.rmtree(self.dist_dir)
        
        #Use the default pygame icon, if none given
        if self.icon_file == None:
            path = os.path.split(pygame.__file__)[0]
            self.icon_file = os.path.join(path, 'pygame.ico')
 
        #List all data files to add
        extra_datas = []
        for data in self.extra_datas:
            if os.path.isdir(data):
                extra_datas.extend(self.find_data_files(data, '*'))
            else:
                extra_datas.append(('.', [data]))
        
        setup(
            cmdclass = {'py2exe': pygame2exe},
            version = self.project_version,
            description = self.project_description,
            name = self.project_name,
            url = self.project_url,
            author = self.author_name,
            author_email = self.author_email,
            license = self.license,
 
            # targets to build
            windows = [{
                'script': self.script,
                'icon_resources': [(0, self.icon_file)],
                'copyright': self.copyright
            }],
            options = {'py2exe': {'optimize': 2, 'bundle_files': 1, 'compressed': True, \
                                  'excludes': self.exclude_modules, 'packages': self.extra_modules, \
                                  'dll_excludes': self.exclude_dll,
                                  'includes': self.extra_scripts} },
            zipfile = self.zipfile_name,
            data_files = extra_datas,
            dist_dir = self.dist_dir
            )
        
        if os.path.isdir('build'): #Clean up build dir
            shutil.rmtree('build')
 
if __name__ == '__main__':
    if operator.lt(len(sys.argv), 2):
        sys.argv.append('py2exe')
    BuildExe().run() #Run generation
    raw_input("Press any key to continue") #Pause to let user see that things ends 
