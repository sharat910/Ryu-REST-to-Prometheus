from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_config(filename):
    with open("configs/%s.yml" % filename) as f:
        config = load(f,Loader=Loader)
    return config
