#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Pi-Yueh Chuang <pychuang@pm.me>
#
# Distributed under terms of the BSD 3-Clause license.

"""Provides SyncthingSession class.
"""
import re
import copy
import pathlib
import logging
import xml.etree.ElementTree
import requests

# get a logger with dummy handler if the caller does not have logging config
logger = logging.getLogger("yasynccli.session")
logger.addHandler(logging.NullHandler())

class SyncthingSession(requests.Session):
    """Syncthing communication session.

    SyncthingSession is an derived requests.Session class that also parses
    Syncthing's configuration XML file and holds info for communication with the
    Syncthing server. This object can be used as an configuration holder also
    a requests.Session.

    Construcgtor args:
    ------------------
        config: a str or Path object of the path to a config file.
        url: a str; address to server; supersede the one in the config file.
        apikey: a str; API Key; supersede the one in the config file.
    """

    # legal GET APIs
    _get_apis = [
        "/system/browse", "/system/config", "/system/config/insync",
        "/system/connections", "/system/debug", "/system/discovery",
        "/system/error", "/system/log", "/system/ping", "/system/status",
        "/system/upgrade", "/system/version", "/db/browse", "/db/completion",
        "/db/file", "/db/ignores", "/db/need", "/db/status", "/events",
        "/stats/device", "/stats/folder", "/svc/deviceid", "/svc/lang",
        "/svc/random/string", "/svc/report"
    ]

    # legal POST APIs
    _post_apis = [
        "/system/config", "/system/debug", "/system/discovery",
        "/system/error/clear", "/system/error", "/system/pause", "/system/ping",
        "/system/reset", "/systemart", "/system/resume", "/system/shutdown",
        "/system/upgrade", "/db/ignores", "/db/override", "/db/prio",
        "/db/revert", "/db/scan"
    ]


    def __init__(self, config, url=None, apikey=None):
        """SyncthingConfig constructor.

        Args:
        -----
            config: a str or Path object of the path to a config file.
            url: a str; address to server; supersede the one in the config file.
            apikey: a str; API Key; supersede the one in the config file.
        """

        logger.debug("Initializing a SyncthingConfig instance.")
        super(SyncthingSession, self).__init__()

        # read and parse the config file
        self._config = pathlib.Path(config).resolve()
        tree = xml.etree.ElementTree.parse(self._config)

        # get url and apikey from GUI info
        gui = tree.find("gui")
        self._url = gui.find("address").text if url is None else url

        # to consider some possible ways to specify URL
        pattern = r"(?://|(?P<proto>.*)://|)(?P<host>.*):(?P<port>\d+?)(?:$|/)"
        match = re.search(pattern, self._url)
        self._host, self._port = match.group("host"), match.group("port")
        self._proto = "http" if match.group("proto") is None else match.group("proto")

        # api key
        self._apikey = gui.find("apikey").text if apikey is None else apikey

        # get folders
        self._folders = {}

        for folder in tree.iterfind("folder"):
            p = pathlib.Path(folder.attrib["path"]).expanduser().resolve()
            self._folders[p] = {
                "label": folder.attrib["label"], "id": folder.attrib["id"]}

        # update attributes inhirented from the parent
        self.headers.update({"X-API-KEY": self._apikey})

        logger.debug("Done initializing a SyncthingConfig instance.")

    def __repr__(self): # overriding __repr__

        logger.debug("Preparing __repr__ string")

        col1 = "{:28s}"
        idnt = "  "

        s = "\n"
        s += col1.format("[Config path]") + "\n\n"
        s += idnt + str(self.config) + "\n"

        s += "\n"
        s += col1.format("[GUI info]") + "\n\n"
        s += col1.format(idnt+"Address: ") + self.url + "\n"
        s += col1.format(idnt+"API Key: ") + self.apikey + "\n"

        s += "\n"
        s += col1.format("[Folders]") +"\n"
        for key, value in self.folders.items():
            s += "\n"
            s += col1.format(idnt+"- "+str(key)) + "\n"
            s += "{}{}ID: {}\n".format(idnt, idnt, value["id"])
            s += "{}{}Label: {}\n".format(idnt, idnt, value["label"])

        logger.debug("Done preparing __repr__ string")

        return s

    @property
    def config(self): # read-only attribute
        """Path to the config file saved in this instance."""
        return copy.deepcopy(self._config)

    @property
    def url(self, *args): # read-only attribute
        """Syncthing GUI server address."""
        return "{}://{}:{}".format(self._proto, self._host, self._port)

    @property
    def apikey(self): # read-only attribute
        """API key saved in this instance."""
        return copy.deepcopy(self._apikey)

    @property
    def folders(self): # read-only attribute
        """Folders' info stored in this instance."""
        return copy.deepcopy(self._folders)

    def get(self, *args, **kwargs):
        """GET method with URL embeded in.

        Args:
        -----
            args: positional arguments; each one represents a fregment in the
                REST API endpoint URL. For example, session.get("system", "config")
                will send a GET request to http://<server>/rest/system/config.
            kwargs: optional arguments that a request takes.

        Returns:
        --------
            A request.Response; response from the server.
        """

        action = ""
        for arg in args:
            action += "/{}".format(arg.strip("/"))

        # check if the api is ligal
        if not action in self._get_apis:
            logger.error("{} is not a legal GET endpoint.".format(action))
            raise RuntimeError("{} is not a legal GET endpoint.".format(action))

        action = self.url + "/rest" + action
        return super(SyncthingSession, self).get(action, **kwargs)

    def post(self, *args, data=None, json=None, **kwargs):
        """POST method with URL embeded in.

        Args:
        -----
            args: positional arguments; each one represents a fregment in the
                REST API endpoint URL. For example, session.post("system", "config")
                will send a POST request to http://<server>/rest/system/config.
            data: Dictionary, list of tuples, bytes, or file-like object to send
                in the body of the `requests.Request`.
            json: json to send in the body of the `requests.Request`.
            kwargs: Optional arguments that a `requests.Reques` takes.

        Returns:
        --------
            A request.Response; response from the server.
        """

        action = ""
        for arg in args:
            action += "/{}".format(arg.strip("/"))

        # check if the api is ligal
        if not action in self._post_apis:
            logger.error("{} is not a legal POST endpoint.".format(action))
            raise RuntimeError("{} is not a legal POST endpoint.".format(action))

        action = self.url + "/rest" + action
        return super(SyncthingSession, self).post(action, data=data, json=json, **kwargs)

    def options(self, *args, **kwargs):
        raise NotImplementedError

    def head(self, *args, **kwargs):
        raise NotImplementedError

    def put(self, *args, data=None, **kwargs):
        raise NotImplementedError

    def patch(self, *args, data=None, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError
