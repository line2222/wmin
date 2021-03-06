# coding=utf-8

import time
import requests
from random import randint
from . import result
from sys import version_info
import socket

if version_info.major == 3:
    from .printf.py3 import printf, printweb
    from urllib.parse import urlparse
    import queue
else:
    from .printf.py2 import printf, printweb
    from urlparse import urlparse
    input = raw_input
    import Queue as queue


class Url:
    """Url is the most important part of wmin,
    this class include the scan and get website information"""
    def __init__(self, url, dictionary, timeout,
                 proxy, delay, ua, ignore_text, method):
        self.url_deal(url)
        self.dictionary = self.deal_dictionary(dictionary)
        self.timeout = timeout
        self.proxy = list(map(self.build_proxy, proxy))
        self.ua = list(map(self.build_ua, ua))
        self.delay = delay
        self.ignore_text = ignore_text
        self.method = self.filter_method(method)
        self.fail_url = queue.Queue()

    def deal_dictionary(self, dictionary):
        self.dict_line = queue.Queue()

        def add_dictline(filename):
            try:
                with open(filename) as dic:
                    for line in dic.readlines():
                        if not line.startswith("#"):
                            # allow use '#' as note
                            if line.startswith("/"):
                                self.dict_line.put(line.strip("\n"))
                            else:
                                self.dict_line.put("/" + line.strip("\n"))
            except UnicodeDecodeError:
                printf("Coding error,please convert file to utf-8", "error")
                exit()
            except FileNotFoundError:
                self.dict_line = None

        if isinstance(dictionary, list):
            # dictionarys folder list
            for filename in dictionary:
                add_dictline(filename)
        else:
            # single dictionary file
            add_dictline(dictionary)

    def url_deal(self, url):
        protocol = urlparse(url).scheme
        if protocol:
            purl = url
            hostname = urlparse(url).netloc

            if url.endswith("/"):
                purl = url[:-1]
                hostname = url[:-1]

            self.url = purl
            self.hostname = hostname
        else:
            printf("Please enter url with protocl", "warning")
            exit()

    def filter_method(self, method):
        if method.lower() not in ["get", "post", "head"]:
            return None
        else:
            return method.lower()

    def build_ua(self, ua):
        if "" == ua:
            return None
        else:
            return dict({"User-Agent": ua})

    def build_proxy(self, proxy):
        if "" != proxy:
            if ":" and "@" in proxy:
                # proxy type : ip:port@type
                proxy = dict({proxy.split("@")[1]: proxy.split(":")[0]
                              + ":" + proxy.split("@")[0].split(":")[1]})
                return proxy
            else:
                printf("Type wrong!", "warning")
                return None
        else:
            return None

    def build_report_file(self):
        self.report_filename = result.init_html(self.hostname)

    def scan(self):
        url = self.url + self.dict_line.get_nowait()

        try:
            # use appoint method
            kwargs = {"url": url,
                      "timeout": self.timeout,
                      "proxies": self.proxy[randint(0, len(self.proxy)-1)],
                      "headers": self.ua[randint(0, len(self.ua)-1)],
                      "allow_redirects": False}

            if "get" == self.method:
                response = requests.get(**kwargs)
            elif "post" == self.method:
                response = requests.post(**kwargs)
            else:
                response = requests.head(**kwargs)

            code = response.status_code
            html = response.text

            def deal_result():
                if code != 404:
                    printweb(code, url)
                    result.export_html(self.report_filename,
                                       url, url + "\t" + str(code))

            if "" != self.ignore_text:
                if self.ignore_text not in html:
                    deal_result()
            else:
                deal_result()

        except KeyboardInterrupt:
            exit()
        except Exception as e:
            self.fail_url.put(url.replace(self.url, ""))
            printf(url + "\tConnect error", "error")
        time.sleep(self.delay)
        # delay time

    def get_info(self):

        printf("Domain:\t" + self.url, "normal")
        try:
            try:
                printf("Server:\t" + requests.get
                       (self.url, timeout=self.timeout,
                        proxies=self.proxy[
                            randint(0, len(self.proxy)-1)],
                        headers=self.ua[randint(0, len(self.ua)-1)],
                        allow_redirects=False).headers["Server"], "normal")
            except:
                printf("Can\'t get server,Connect wrong", "error")
            try:
                printf("IP:\t" +
                       socket.gethostbyname(self.hostname), "normal")
            except:
                printf("Can\'t get ip,Connect wrong", "error")
            printf("")
        except KeyboardInterrupt:
            exit()

    def run(self):
        self.build_report_file()
        for i in range(self.dict_line.qsize()):
            self.scan()
        self.reconnect()

    def reconnect(self):
        while 0 != self.fail_url.qsize():
            try:
                if input("Reconnect failed url?[Y/n]") in [
                        "n", "no", "No", "NO"]:
                    break
                else:
                    self.dict_line = self.fail_url
                    self.fail_url = queue.Queue()
                    self.run()
            except:
                exit()
