#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Pi-Yueh Chuang <pychuang@pm.me>
#
# Distributed under terms of the BSD 3-Clause license.

"""Provides SyncthingConfig class.
"""
import re
import copy
import pathlib
import logging
import xml.etree.ElementTree

# get a logger with dummy handler if the caller does not have logging config
logger = logging.getLogger("yasynccli.config")
logger.addHandler(logging.NullHandler())

class SyncthingConfig:
    """An object holding Syncthing configurations.

    SyncthingConfig is an object that parses Syncthing's configuration XML file
    and holds info for communicating with the Syncthing server. This object can
    be passed to action functions an information holder.

    Construcgtor args:
    ------------------
        config: a str or Path object of the path to a config file.
        url: a str; address to server; supersede the one in the config file.
        apikey: a str; API Key; supersede the one in the config file.
    """

    def __init__(self, config, url=None, apikey=None):
        """SyncthingConfig constructor.

        Args:
        -----
            config: a str or Path object of the path to a config file.
            url: a str; address to server; supersede the one in the config file.
            apikey: a str; API Key; supersede the one in the config file.
        """

        logger.debug("Initializing a SyncthingConfig instance.")

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
            self._folders[folder.attrib["path"]] = {
                "label": folder.attrib["label"], "id": folder.attrib["id"]}

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
            s += col1.format(idnt+"- "+key) + "\n"
            s += "{}{}ID: {}\n".format(idnt, idnt, value["id"])
            s += "{}{}Label: {}\n".format(idnt, idnt, value["label"])

        logger.debug("Done preparing __repr__ string")

        return s

    @property
    def config(self): # read-only attribute
        """Path to the config file saved in this instance."""
        return copy.deepcopy(self._config)

    @property
    def apikey(self): # read-only attribute
        """API key saved in this instance."""
        return copy.deepcopy(self._apikey)

    @property
    def folders(self): # read-only attribute
        """Folders' info stored in this instance."""
        return copy.deepcopy(self._folders)

    @property
    def header(self): # read-only attribute
        """Header for HTTP requests to a Syncthing server."""
        return {"X-API-KEY": self.apikey}

    @property
    def url(self, *args): # read-only attribute
        """Syncthing GUI server address."""
        return "{}://{}:{}".format(self._proto, self._host, self._port)

    def endpoint(self, *args):
        """HTTP REST base URL of the Syncthing server."""
        address = self.url + "/rest"
        for arg in args:
            address += "/{}".format(arg)
        return address
