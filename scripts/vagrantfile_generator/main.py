import sys, os
import yaml
import jinja2 as j2
import subprocess

def loadfile(file):
    try:
        with open(file, 'r') as stream:
            try:
                return yaml.load(stream, Loader=yaml.BaseLoader)
            except yaml.YAMLError as e:
                print(e)
    except IOError as e:
        print("Error: No such file '"+file+"'")
        exit(1)

def template(dicc):
    template = j2.Environment(loader=j2.FileSystemLoader(os.path.dirname(sys.argv[0])), trim_blocks=True).get_template('Vagrantfile.j2')
    return template.render(clusters=dicc)

def template_inventory(dicc):
    template = j2.Environment(loader=j2.FileSystemLoader(os.path.dirname(sys.argv[0])), trim_blocks=True).get_template('docker_inventory.j2')
    return template.render(hosts=dicc)

def sshconfig(stdout):
    sshconfig = stdout.decode("utf-8").split("\n")
    inventory = []
    host_tmp = {}
    for elem in sshconfig:
        obj = elem.lstrip().split(" ")
        if 'Host ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'HostName ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'User ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'Port ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'UserKnownHostsFile ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'StrictHostKeyChecking ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'PasswordAuthentication ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'IdentitiesOnly ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'LogLevel ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif '' == elem:
            if len(host_tmp) > 0:
                inventory.append(host_tmp)
                host_tmp = {}
    return inventory

def writefile(content, file):
    try:
        with open(file, 'w') as file:
            file.write(content)
    except IOError as e:
        print("Error writing file '"+file+"'")
        exit(1)

if __name__ == "__main__":
    if len(sys.argv)<=1:
        print("Error: It needs a YAML file")
        exit(1)
    if sys.argv[1] == "--template":
        try:
            with open('vagrant-template.yaml', 'r') as fh:
                print("Error: Template file already exists")
                exit(1)
        except FileNotFoundError:
            try:
                with open(os.path.dirname(sys.argv[0])+'/vagrant-config.yaml', 'r') as vf:
                    writefile(vf.read(), "vagrant-template.yaml")
            except FileNotFoundError:
                print(os.path.dirname(sys.argv[0])+'/vagrant-config.yaml', 'r')
                print("Error: Template config not exists")
                exit(1)
    elif sys.argv[1] == "--ansible-inventory":
        inventory = sshconfig(subprocess.run(['vagrant','ssh-config'], stdout=subprocess.PIPE).stdout)
        di = template_inventory(inventory)
        writefile(di, "inventory")
    else:
        FILE_NAME = sys.argv[1]
        yaml = loadfile(FILE_NAME)
        vf = template(yaml)
        writefile(vf, "Vagrantfile")
    exit(0)
