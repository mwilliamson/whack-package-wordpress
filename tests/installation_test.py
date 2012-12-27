import os
import subprocess

from nose.tools import istest
from selenium import webdriver

from tempdir import create_temporary_dir


@istest
def deploying_wordpress_shows_front_page():
    with create_temporary_dir() as temp_dir:
        install_wordpress(temp_dir, port=54321)
        process = start_apache2(temp_dir)
        try:
            assert hello_world_post_is_visible(port=54321)
        finally:
            process.terminate()

def install_wordpress(directory, port):
    path = os.path.join(os.path.dirname(__file__), "..")
    subprocess.check_call(["whack", "install", path, directory, "-pport={0}".format(port), "--no-cache"])

def start_apache2(temp_dir):
    apache_dir = os.path.join(temp_dir, "apache2")
    return subprocess.Popen(
        ["bin/httpd", "-DNO_DETACH", "-d", apache_dir],
        cwd=apache_dir
    )

def hello_world_post_is_visible(port):
    url = "http://localhost:{0}/".format(port)
    browser = webdriver.Firefox()
    try:
        browser.get(url)
        browser.find_element_by_link_text("Hello world!")
    finally:
        browser.close()
