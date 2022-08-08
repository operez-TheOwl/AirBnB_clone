#!/usr/bin/python3
"""console : entry point to the commad interpreter
It defines a custom shell to control the airbnb application
"""
import cmd

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage

class HBNBCommand(cmd.Cmd):
    """Definition of the custom shell command interpreter
    Attributes:
        /* public class attributes */
        intro (str) : the message that is print at the launch of the console
        prompt (str) : the prompt on every line of the console
        file () : i don't know

        /* private class attribute */
        __class_list (dict) : list of all classes

    Functions:
        /* public instance methods */
        help()
        do_quit()
        do_EOF()
        emptyline()
        precmd()

        do_create()
        do_show()
        do_destroy()
        do_all()
        do_update()

    """

    prompt = "(hbnb) "
    __class_list = {'BaseModel': BaseModel, 'User': User, 'State': State,
                    'City': City, 'Amenity': Amenity, 'Place': Place,
                    'Review': Review}

#    time_pat = re.compile(
#                r'^\d{4}(\-\d{2}){2}T(\d{2}:){2}\d{2}(\.\d{6})?$')
#    uuid_pat = re.compile(
#                r'^[\da-f]{8}(\-[\da-f]{4}){3}\-[\da-f]{12}$')

    err_msg1 = "** class name missing **"
    err_msg2 = "** class doesn't exist **"
    err_msg3 = "** instance id missing **"
    err_msg4 = "** no instance found **"
    err_msg5 = "** attribute name missing **"
    err_msg6 = "** value missing **"

    def do_create(self, line):
        """Command create : Creates a new object given its class
        and prints its id
        Usage : $ create <class name>
                $ create User
        Args:
            line (str) : console line holding the class name of the object
        """
        if (line == ""):
            print(self.err_msg1)
            return
        for key in self.__class_list.keys():
            if (key == line):
                obj = self.__class_list[key]()
                obj.save()
                print(obj.id)
                return
        print(self.err_msg2)

    def do_show(self, line):
        """Command show : prints the string representation of an object
        Usage : $ show <class name> <id>
                $ show BaseModel 1234-1234-1234
        Args:
            line (str) : console line holding the object's class name and id
        """
        args = line.split()
        if (len(args) == 0):                  # checks if a class is given
            print(self.err_msg1)
            return
        for key1 in self.__class_list.keys():  # checks if class exist
            if (args[0] == key1):
                if (len(args) == 1):          # checks if an id is given
                    print(self.err_msg3)
                    return
                obj_key = args[0] + "." + args[1]
                # checks if the object exists currently and prints it
                for (key2, obj) in storage.all().items():
                    if (obj_key == key2):
                        print(obj)
                        return
                print(self.err_msg4)
                return
        print(self.err_msg2)

    def do_destroy(self, line):
        """Command destroy : deletes an object given its class name and id
        Usage : $ destroy <class name> <id>
                $ destroy BaseModel 1234-1234-1234
        Args:
            line (str) : console line holding the object's class name and id
        """
        args = line.split()
        if (len(args) == 0):                  # checks if a class is given
            print(self.err_msg1)
            return
        for key1 in self.__class_list.keys():  # checks if class exist
            if (args[0] == key1):
                if (len(args) == 1):          # checks if an id is given
                    print(self.err_msg3)
                    return
                obj_key = args[0] + "." + args[1]
                # checks if the object exists currently and deletes it
                for (key2, obj) in storage.all().items():
                    if (obj_key == key2):
                        del(storage.all()[key2])
                        storage.save()
                        return
                print(self.err_msg4)
                return
        print(self.err_msg2)

    def do_all(self, line):
        """Command all : prints all objects string representaion
        Usage : $ all [<class name>]
                $ all BaseModel or  $ all
        Args:
            line (str) : console line holding the class name of the objects
        """
        if (line == ""):
            for key in storage.all().keys():
                print(storage.all()[key])
            return
        if (line in self.__class_list.keys()):
            for obj in storage.all().values():
                if (line == obj.__class__.__name__):
                    print(obj)
            return
        print(self.err_msg2)

    def do_update(self, line):
        """Command update : updates an object given its class name,id,
        attribute and new value
        Usage : $ update <class name> <id> <attribute name> "<value>"
                $ update BaseModel 1234-1234-1234 email "name@example.com"
        Args:
            line (str) : console line holding the object's class name and id
        """
        args = line.split()
        if (len(args) == 0):                  # checks if a class is given
            print(self.err_msg1)
            return
        for key1 in self.__class_list.keys():  # checks if class exist
            if (args[0] == key1):
                if (len(args) == 1):          # checks if an id is given
                    print(self.err_msg3)
                    return
                obj_key = args[0] + "." + args[1]
                # checks if the object exists currently
                for (key2, obj) in storage.all().items():
                    if (obj_key == key2):
                        if (len(args) == 2):  # cheks if an attribute is given
                            print(self.err_msg5)
                            return
                        if (len(args) == 3):  # cheks if a value is given
                            print(self.err_msg6)
                            return
                        # adds the new attribute to the object
                        if (args[2] not in
                            ['id', 'created_at', 'updated_at', '__class__']):
                            # find type of attribute and remove its limiter
                            if (args[3][0] in ["'", '"']:
                                    args[3] = parse_str(args)
                            cast = type(eval(args[3]))
                            new_arg = args[3].strip("'")
                            new_arg = new_arg.strip('"')
                            obj.__setattr__(args[2], cast(new_arg))
                            storage.save()
                            return
                print(self.err_msg4)
                return
        print(self.err_msg2)

    def do_count(self, line):
        """Command count : counts number of object of a given class
        Usage : $ <class name>.count()
                $ User.count()
        Args:
            line (str) : console line holding the class name
        """
        if (line == ""):
            print(self.err_msg1)
            return
        for key in self.__class_list.keys():
            if (key == line):
                i = 0
                for obj in storage.all().values():
                    if (obj.__class__.__name__ == line):
                        i += 1
                print(i)
                return
        print(self.err_msg2)

    def do_quit(self, line):
        """Command quit : exits the console
        """
        return (True)

    def do_EOF(self, line):
        """Command EOF : exits the console when "CTRL-D"
        """
        print()
        return (True)

    def emptyline(self):
        """does nothing when an empty line is entered
        """
        return

    def precmd(self, line):
        """modify the line before command execution
        """
        if ("." in line and line.split(".")[1][:5] == "show("):
            args = line.split(".")
            line = args[1][:4] + " " + args[0] + " " + args[1][6:-2]
        elif ("." in line and line.split(".")[1][:8] == "destroy("):
            args = line.split(".")
            line = args[1][:7] + " " + args[0] + " " + args[1][9:-2]
        elif ("." in line and line.split(".")[1][:7] == "update("):
            args = line.split(".")
            line = args[1][:6] + " " + args[0] + " "
            args = args[1][7:-2].split(",")
            if (args[1][1] != "{"):
                line = (line + args[0][1:-1] + " "
                        + args[1][2:-1] + " " + args[2][1:])
            else:
                line = line + args[0][1:-1] + " " + args[1]
        elif ("." in line and line[-2:] == "()"):
            args = line.split(".")
            line = args[1][:-2] + " " + args[0]
        print(line)
        return (line)


def parse_str(args):
    """Transforms string attribute with space into one string
    Args:
        args (list) : list of str from the split of the console line
    """
    try:
        i = 1
        while (args[3][-1] not in ["'", '"']):
            args[3] = args[3] + " " + args[3 + i]
            i += 1
        return (args[3])
    except IndexError:
        print("string value must be quoted")

if __name__ == '__main__':
    HBNBCommand().cmdloop()