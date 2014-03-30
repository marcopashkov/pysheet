import os
import project as p

class MetaProject(type):
    """Metaclass for a project, which contains some convienience methods"""

    __ext__ = 'pys_proj'
    __path__ = '.'

    # { name: class } - every class instance registers itself here
    __project_instances__ = {}

    @property
    def all(cls):
        """Return all projects as generator"""
        # setup
        path = MetaProject.__path__
        files = os.listdir(path) 
        fullpath = lambda path, filename : os.path.join(path, filename)

        # filter the project folders
        projects = (_f for _f in files if os.path.isdir(fullpath(path, _f)))
        projects = (p for p in projects if p.endswith(MetaProject.__ext__))
        projects = (fullpath(path, p) for p in projects)
        projects = (p.Project(path=path) for path in projects)
        return projects

    def __create_new_project_folder__(cls, name):
        """Create a new project path"""
        foldername = '{0}_{1}'.format(name, MetaProject.__ext__)
        path = os.path.join(MetaProject.__path__, foldername)

        # TODO: catch, so user can be notified if project already exists
        os.mkdir(path) # create a new folder
        base_file = os.path.join(path, '__init__.py')
        open(base_file, 'w').close() # create a new file
        return path

    def create_new_project(cls, name):
        """Create a new project (incl. folder structure) and return its
        object representation"""
        path = cls.__create_new_project_folder__(name)
        return p.Project(path=path)

    def get(cls, name):
        """Return the Project by its name"""
        return (p for p in cls.all if p.name == name).next()

    def register(cls, klass):
        """Project-instances register itself here"""
        cls.__project_instances__[klass.package_name] = klass

    def get_project_klass(cls, package_name):
        """Return project-instance by package_name"""
        return cls.__project_instances__.get(package_name)
