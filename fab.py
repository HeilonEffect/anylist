__author__ = 'ctulhu'
import os
from fabric.api import run, env, cd, roles

def production_env():
    env.user = 'root'
    env.project_root = '/root/anylist'
    env.shell = '/usr/local/bin/bash -c'
    env.python = '/root/anylist/virt/bin/python'
