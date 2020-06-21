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

By default, an executable should be installed to `${HOME}/.local/bin/yasync-cli`.
If `${HOME}/.local/bin` is already in `PATH`, then the executable can be
executed with `yasync-cli`. Alternatively, one can choose to use the full path
to run the executable, i.e., `${HOME}/.local/bin/yasync-cli`.


## Removing `pip` installation
------------------------------

```
$ pip uninstall yasynccli
```


## Usage
--------


### Help pages

See help with

```
$ yasync-cli --help
```

or see the help of subcommands with

```
$ yasync-cli <subcommand> --help
```

Currently supported subcommands include: `show`, `get`, and `post`.


### Show basic info in the default configuration file

```
$ yasync-cli show
```

This will print very basic info of the configuration and the folders'
information.


### GET and POST endpoints

This tool also exposes subcommands to send GET and POST requests. For example,
to rescan a Syncthing-monitoring folder (of which the ID is `abcde-12345`):

```
$ yasync-cli post /db/scan folder=abcde-12345
```

And the folder ID can be obtained from `$ yasunc-cli show`.

The `get` and `post` subcommands are for debugging purpose only and for
convenience.


## Contact
----------
Pi-Yueh Chuang ([pychuang@pm.me](pychuang@pm.me))
