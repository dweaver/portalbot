#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""portalbot - Portals Utility - update widget js and domain css

Usage:
    portalbot upload [options] --domain=<domain> --user=<user>
        [--widgetjs=<file> --portal=<id> --dashboard=<id> --widget=<id>]
        [--domaincss=<file>]
        [--noninteractive]

    Portalbot fills in your username and gives you 60 seconds to enter your
    password.

    portal and dashboard ids can be taken from the dashboard url:

        /view/<portal>/<dashboard>

    Finding your widget id requires inspecting the DOM. In Chrome, right click
    on the down arrow on the top right in the widget and select Inspect
    Element. The id is from the id of that element, e.g. if you see
    <img id="menuicon1" ... the widget id is 1.

    Currently only non-public dashboard ids are supported.

    By default, the browser is left open. Pass --noninteractive to quit when
    upload completes.

Options:
    -h --help     Show this screen
    -v --version  Show version

"""
# Copyright (c) 2013, Exosite, LLC
# All rights reserved
import time

from docopt import docopt
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumApp():
    def __init__(self, baseurl, browser=None):
        self.baseurl = baseurl
        self.br = browser or webdriver.Firefox()

    def css(self, selector):
        return self.br.find_element_by_css_selector(selector)

    def wait(self, wait_selector, wait_sec=60):
        '''Wait for an element'''
        return WebDriverWait(self.br, wait_sec, 0.1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector)))

    def click_wait(self, click_selector, wait_selector, wait_sec=60):
        '''Find an element, click on it, and then wait for another element'''
        self.br.find_element_by_css_selector(click_selector).click()
        self.wait(wait_selector, wait_sec)

    def click(self, click_selector):
        '''Find an element, click on it'''
        self.br.find_element_by_css_selector(click_selector).click()

    def script(self, script):
        self.br.execute_script(script)


class PortalBot(SeleniumApp):
    user = None
    password = None

    def setuser(self, user=None, password=None):
        self.user=user
        self.password=password

    def upload_css(self, cssfile):
        self.login('/admin/theme')
        with open(cssfile) as f:
            css = f.read()
            el = self.css('div.form textarea[Name="Code"]')
            el.clear()
            el.send_keys(css)
            submitel = 'form[enctype="multipart/form-data"] input[type="submit"]'
            self.click_wait(submitel, submitel)

    def upload_js(self, widgetjsfile, portalid, dashboardid, widgetid):
        self.login('views/' + portalid + '/' + dashboardid)
        with open(widgetjsfile) as f:
            js = f.read()
            menuiconcss = '#menuicon' + widgetid
            self.click(menuiconcss)
            textcss = 'span.script textarea'
            self.click_wait('#editmenu' + widgetid, textcss)
            # need to convert the code mirror object to text area mode
            # http://codemirror.net/doc/manual.html#fromTextArea
            self.script(
                'cm = CodeMirror.fromTextArea($("span.script textarea").get(0)); cm.toTextArea()')
            el = self.css(textcss)
            el.clear()
            el.send_keys(js)
            submitel = '#formeditwidget' + widgetid + ' #diveditwidgetsave' + widgetid
            self.click(submitel)
            try:
                notice = self.wait("div.notice", wait_sec=3)
                print(notice.text)
            except TimeoutException:
                self.wait('#divwidget' + widgetid, wait_sec=3)

                # click the "Execute Javascript" button, if it shows up
                js_button_css = 'fieldset.execution button'
                try:
                    self.css(js_button_css)
                    self.click(js_button_css)
                except:
                    pass

            # scroll to the top of the window
            self.script('window.scrollTo(0,0)')

    def login(self, path=None):
        if path:
            path = path[1:] if path[0] == '/' else path
            url = self.baseurl + '/' + path
        else:
            url = self.baseurl

        print url
        self.br.get(url)

        try:
            # log in
            userel = self.css('#login_user')
            if self.user:
                userel.send_keys(self.user)
            if self.password:
                self.css('#login_pass').send_keys(self.password)
            else:
                self.css('#login_pass').click()

            # time login
            t1 = time.time()

            # div.form is necessary on logicpd.exosite.com because there is another
            # matching button outside the div.form. Could also look for the visible
            # one.
            if self.user and self.password:
                self.click_wait('div.form button[type="submit"]', 'div.admin_menu')
            else:
                self.wait('div.admin_menu')

            t2 = time.time()

            print("Took {:0.3f}s to login".format((t2 - t1)))


        except NoSuchElementException:
            # if there's no login element, we were already logged in
            pass


def run_command(p, args):
    t1 = time.time()
    domaincss = args['--domaincss']
    if domaincss is not None:
        p.upload_css(domaincss)

    widgetjs = args['--widgetjs']
    if widgetjs is not None:
        p.upload_js(widgetjs, args['--portal'], args['--dashboard'], args['--widget'])

    if domaincss is None and widgetjs is None:
        print "There was nothing to do!"

    t2 = time.time()
    print("Completed in {:0.3f}s".format((t2 - t1)))


def handle_args(args):
    p = PortalBot('https://' + args['--domain'] + '.exosite.com')
    args['--pass'] = None
    p.setuser(user=args['--user'], password=args['--pass'])

    if args['--noninteractive']:
        # run once
        run_command(p, args)
    else:
        # run forever
        while True:
            # time login
            run_command(p, args)
            try:
                input("Press Enter to send again, Ctrl + C to quit...")
            except KeyboardInterrupt:
                return
            except:
                continue


if __name__ == '__main__':
    args = docopt(__doc__, version="Portals Utility 0.0.2")
    #try:
    handle_args(args)
    #except Exception as ex:
        #print(ex)
        #sys.exit(1)
