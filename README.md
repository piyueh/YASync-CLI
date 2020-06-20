YASync-CLI -- Yet Another Syncthing CLI Tool
============================================

YASync-CLI provides a command-line tool `yasync-cli` to manipulate a Syncthing
daemon from terminal. It is supposed to be useful for headless servers.

The project is still a WIP. Currently, I only add features when I need ones
as I'm the only user. Feature requests are welcome. And feel free to test it.
`yasync-cli` has never been tested on other machines/systems.


## Installation
---------------

This is still a develop version. To install it to a local searchable path with
`pip`:

```
$ git clone https://github.com/piyueh/yasync-cli
$ cd yasync-cli
$ pip install --user .
```

By default, an executable should be installed at `${HOME}/.local/bin/yasync-cli`.
Execute `${HOME}/.local/bin/yasync-cli --help` to see help. If
`${HOME}/.local/bin` is in a user's `PATH`, then the user can just execute
`yasync-cli` instead of using the full path.


## Removing `pip` installation
------------------------------

```
$ pip uninstall yasynccli
```

## Usage
--------

See help with

```
$ ${HOME}/.local/bin/yasync-cli --help
```


## Contact
----------
Pi-Yueh Chuang ([pychuang@pm.me](pychuang@pm.me))
