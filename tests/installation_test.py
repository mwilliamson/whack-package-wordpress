import os
import subprocess
import time

from nose.tools import istest, assert_equals
from starboard import find_local_free_tcp_port as find_port
from selenium import webdriver

from tempdir import create_temporary_dir


@istest
def deploying_wordpress_shows_front_page():
    with create_temporary_dir() as temp_dir:
        port = find_port()
        install_wordpress(temp_dir, port=port)
        process = subprocess.Popen(
            ["bin/httpd", "-DNO_DETACH"],
            cwd=temp_dir
        )
        try:
            assert hello_world_post_is_visible(port=port)
        finally:
            process.terminate()


def install_wordpress(directory, port):
    path = os.path.join(os.path.dirname(__file__), "..")
    subprocess.check_call(["whack", "install", path, directory, "--no-cache"])
    
    conf_path = os.path.join(directory, "conf/httpd.conf")
    with open(conf_path, "r") as conf_file:
        original_conf_contents = conf_file.read()
    conf_contents = original_conf_contents.replace("Listen 80", "Listen {0}".format(port))
    with open(conf_path, "w") as conf_file:
        conf_file.write(conf_contents)

def hello_world_post_is_visible(port):
    url = "http://localhost:{0}/".format(port)
    browser = webdriver.Firefox()
    try:
        browser.get(url)
        browser.find_element_by_link_text("Hello world!")
    finally:
        browser.close()
