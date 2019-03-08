import sys, os
import yaml
import jinja2 as j2

def loadfile(file):
    try:
        with open(file, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as e:
                print(e)
    except IOError, e:
        print("Error: No such file '"+file+"'")
        exit(1)

def template(dicc):
    template = j2.Environment(loader=j2.FileSystemLoader(os.path.dirname(sys.argv[0])), trim_blocks=True).get_template('Vagrantfile.j2')
    return template.render(clusters=dicc)

def writefile(content, file):
    try:
        with open(file, 'w') as file:
            file.write(content)
    except IOError, e:
        print("Error writing file '"+file+"'")
        exit(1)

if __name__ == "__main__":
    if len(sys.argv)<=1:
        print("Error: It needs a YAML file")
        exit(1)
    FILE_NAME = sys.argv[1]
    yaml = loadfile(FILE_NAME)
    vf = template(yaml)
    writefile(vf, "Vagrantfile")
    exit(0)
