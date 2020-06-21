#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Pi-Yueh Chuang <pychuang@pm.me>
#
# Distributed under terms of the BSD 3-Clause license.

"""Test SyncthingSession class.
"""
import sys
import pathlib
import importlib
import requests
import pytest

# import target module
target = pathlib.Path(__file__).resolve().parents[1].joinpath("yasynccli", "session.py")
spec = importlib.util.spec_from_file_location("session", target)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def create_fake_config(folder):
    """Create a bare-minumum fake config.xml."""

    import xml.etree.ElementTree as ET

    root = ET.Element("configuration", {"version": "30"})
    root.append(ET.Comment("A fake config.xml."))

    # folder 1
    attr = dict(id="abcde-12345", label="folder 1",path=str(pathlib.Path.home()))
    root.append(ET.Element("folder", attr))

    # folder 2
    attr = dict(id="cvbnm-q1w2e", label="folder 2",path=str(pathlib.Path.home().parent))
    root.append(ET.Element("folder", attr))

    # gui
    gui = ET.SubElement(root, "gui")
    address = ET.SubElement(gui, "address")
    address.text = "192.168.1.1:9783"
    apikey = ET.SubElement(gui, "apikey")
    apikey.text = "bMskdeWP293r7f8v3hdsTqwef"

    # write to folder/test_config.xml
    tree = ET.ElementTree(root)
    tree.write(pathlib.Path(folder)/"test_config.xml", "utf-8")

    return pathlib.Path(folder) / "test_config.xml"

def test_SyncthingSession_0():
    """Test init without giving a config file."""
    with pytest.raises(TypeError):
        config = module.SyncthingSession()

def test_SyncthingSession_1():
    """Test init an invalid config file."""
    with pytest.raises(FileNotFoundError):
        config = module.SyncthingSession("./abcdefg.xml")

def test_SyncthingSession_2(tmpdir):
    """Test init with a fake config file."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingSession(p)
    assert config.config == p
    assert config.url == "http://192.168.1.1:9783"
    assert config.apikey == "bMskdeWP293r7f8v3hdsTqwef"
    assert config.headers["X-API-KEY"] == "bMskdeWP293r7f8v3hdsTqwef"

def test_SyncthingSession_3(tmpdir):
    """Test init with a fake config file and url overwritten."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingSession(p, url="123.45.214.11:1234")
    assert config.config == p
    assert config.url == "http://123.45.214.11:1234"
    assert config.apikey == "bMskdeWP293r7f8v3hdsTqwef"

def test_SyncthingSession_4(tmpdir):
    """Test init with a fake config file and api key overwritten."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingSession(p, apikey="nfekFKLE;Qfnklda2143e3")
    assert config.config == p
    assert config.url == "http://192.168.1.1:9783"
    assert config.apikey == "nfekFKLE;Qfnklda2143e3"

def test_SyncthingSession_5(tmpdir):
    """Test init with a fake config file and both url & api key overwritten."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingSession(p, "123.45.214.11:1234", "nekFKLEfnklda2143e3")
    assert config.config == p
    assert config.url == "http://123.45.214.11:1234"
    assert config.apikey == "nekFKLEfnklda2143e3"

def test_SyncthingSession_6(tmpdir):
    """Test init with different URL formats."""
    p = create_fake_config(tmpdir)

    config = module.SyncthingSession(p, url="//123.45.214.11:1234")
    assert config.url == "http://123.45.214.11:1234"

    config = module.SyncthingSession(p, url="http://123.45.214.11:1234")
    assert config.url == "http://123.45.214.11:1234"

    config = module.SyncthingSession(p, url="https://123.45.214.11:1234")
    assert config.url == "https://123.45.214.11:1234"

def test_SyncthingSession_7(tmpdir):
    """Test GET method."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingSession(p, url="123.45.214.11:1234")

    with pytest.raises(RuntimeError):
        config.get("sysfdtem", "bbrowse", timeout=1)
        config.get("dbs", "rescan", timeout=1)

    with pytest.raises(requests.exceptions.ConnectTimeout):
        config.get("system", "browse", timeout=1)
        config.get("system", "config", timeout=1)
        config.get("system", "config", "insync", timeout=1)
        config.get("system", "connections", timeout=1)
        config.get("system", "debug", timeout=1)
        config.get("system", "discovery", timeout=1)
        config.get("system", "error", timeout=1)
        config.get("system", "log", timeout=1)
        config.get("system", "ping", timeout=1)
        config.get("system", "status", timeout=1)
        config.get("system", "upgrade", timeout=1)
        config.get("system", "version", timeout=1)
        config.get("db", "browse", timeout=1)
        config.get("db", "completion", timeout=1)
        config.get("db", "file", timeout=1)
        config.get("db", "ignores", timeout=1)
        config.get("db", "need", timeout=1)
        config.get("db", "status", timeout=1)
        config.get("events", timeout=1)
        config.get("stats", "device", timeout=1)
        config.get("stats", "folder", timeout=1)
        config.get("svc", "deviceid", timeout=1)
        config.get("svc", "lang", timeout=1)
        config.get("svc", "random", "string", timeout=1)
        config.get("svc", "report", timeout=1)

def test_SyncthingSession_8(tmpdir):
    """Test POST method."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingSession(p, url="123.45.214.11:1234")

    with pytest.raises(RuntimeError):
        config.post("sysfdtem", "bbrowse", timeout=1)
        config.post("dbs", "rescan", timeout=1)

    with pytest.raises(requests.exceptions.ConnectTimeout):
        config.post("system", "config", timeout=1)
        config.post("system", "debug", timeout=1)
        config.post("system", "discovery", timeout=1)
        config.post("system", "error", "clear", timeout=1)
        config.post("system", "error", timeout=1)
        config.post("system", "pause", timeout=1)
        config.post("system", "ping", timeout=1)
        config.post("system", "reset", timeout=1)
        config.post("system", "restart", timeout=1)
        config.post("system", "resume", timeout=1)
        config.post("system", "shutdown", timeout=1)
        config.post("system", "upgrade", timeout=1)
        config.post("db", "ignores", timeout=1)
        config.post("db", "override", timeout=1)
        config.post("db", "prio", timeout=1)
        config.post("db", "revert", timeout=1)
        config.post("db", "scan", timeout=1)

def test_SyncthingSession_9(tmpdir):
    """Test invalid method."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingSession(p, url="123.45.214.11:1234")

    with pytest.raises(NotImplementedError):
        config.options("a", "b", timeout=1)
        config.head("a", "b", timeout=1)
        config.put("a", "b", timeout=1)
        config.patch("a", "b", timeout=1)
        config.delete("a", "b", timeout=1)
