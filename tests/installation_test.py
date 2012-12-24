import os
import subprocess

from nose.tools import istest
from selenium import webdriver

from tempdir import create_temporary_dir


@istest
def deploying_wordpress_shows_front_page():
    with create_temporary_dir() as temp_dir:
        deploy_wordpress(temp_dir, port=54321)
        assert hello_world_post_is_visible(port=54321)

def deploy_wordpress(directory, port):
    path = os.path.join(os.path.dirname(__file__), "..")
    subprocess.check_call(["whack", "install", path, directory, "-pport={0}".format(port), "--no-cache"])
    
def hello_world_post_is_visible(port):
    url = "http://localhost:{0}/".format(port)
    browser = webdriver.Firefox()
    try:
        browser.get(url)
        browser.find_element_by_link_text("Hello world!")
    finally:
        browser.close()
