#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Pi-Yueh Chuang <pychuang@pm.me>
#
# Distributed under terms of the BSD 3-Clause license.

"""Test SyncthingConfig class.
"""
import sys
import pathlib
import importlib
import pytest

# import target module
target = pathlib.Path(__file__).resolve().parents[1].joinpath("yasynccli", "config.py")
spec = importlib.util.spec_from_file_location("config", target)
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

def test_SyncthingConfig_init_0():
    """Test init without giving a config file."""
    with pytest.raises(TypeError):
        config = module.SyncthingConfig()

def test_SyncthingConfig_init_1():
    """Test init an invalid config file."""
    with pytest.raises(FileNotFoundError):
        config = module.SyncthingConfig("./abcdefg.xml")

def test_SyncthingConfig_init_2(tmpdir):
    """Test init with a fake config file."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingConfig(p)
    assert config._config == p
    assert config._url == "http://"+"192.168.1.1:9783"
    assert config._apikey == "bMskdeWP293r7f8v3hdsTqwef"

def test_SyncthingConfig_init_3(tmpdir):
    """Test init with a fake config file and url overwritten."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingConfig(p, url="123.45.214.11:1234")
    assert config._config == p
    assert config._url == "http://"+"123.45.214.11:1234"
    assert config._apikey == "bMskdeWP293r7f8v3hdsTqwef"

def test_SyncthingConfig_init_4(tmpdir):
    """Test init with a fake config file and api key overwritten."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingConfig(p, apikey="nfekFKLE;Qfnklda2143e3")
    assert config._config == p
    assert config._url == "http://"+"192.168.1.1:9783"
    assert config._apikey == "nfekFKLE;Qfnklda2143e3"

def test_SyncthingConfig_init_5(tmpdir):
    """Test init with a fake config file and both url & api key overwritten."""
    p = create_fake_config(tmpdir)
    config = module.SyncthingConfig(p, "123.45.214.11:1234", "nekFKLEfnklda2143e3")
    assert config._config == p
    assert config._url == "http://"+"123.45.214.11:1234"
    assert config._apikey == "nekFKLEfnklda2143e3"
