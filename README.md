YASync-CLI -- Yet Another Syncthing CLI Tool
============================================

YASync-CLI provides a command-line tool `yasync-cli` to manipulate a Syncthing
daemon from a terminal. It is supposed to be useful for headless servers.

Why another Syncthing CLI tool? Because I don't like other similar tools... And
actually, not many such tools are still well maintained. To my best knowledge,
the one that is well maintained and has complete features is
[Syncthing Tray](https://github.com/Martchus/syncthingtray).
However, Syncthing Tray does not separate its CLI tools and GUI components.
So users have to installed all GUI components even if we only need the CLI tools,
which is the reason I decided to work on my own CLI tools.

This project is still a WIP. Currently, I only add features when I need ones
as I'm the only user. Feature requests are welcome. And feel free to test it.
`yasync-cli` has never been tested on other machines/systems.


## I. Installation
------------------

This is still a developing version. To install it to a local searchable path with
`pip`:

```
$ git clone https://github.com/piyueh/yasync-cli
$ cd yasync-cli
$ pip install --user .
```

By default, the executable is installed at `${HOME}/.local/bin/yasync-cli`.
If `${HOME}/.local/bin` is already in `PATH`, then the executable can be
executed with `yasync-cli`. Alternatively, one can choose to use the full path
to run the executable, i.e., `${HOME}/.local/bin/yasync-cli`.


## II. Removing `pip` installation
----------------------------------

```
$ pip uninstall yasynccli
```


## III. Usage
-------------


### 1. Help pages

See help with

```
$ yasync-cli --help
```

or see the help of subcommands with

```
$ yasync-cli <subcommand> --help
```

Currently supported subcommands include: `show`, `scan`, `get`, and `post`.


### 2. Show basic info in the default configuration file

```
$ yasync-cli show
```

This will print very basic info of the configuration and the monitored folders'
information.

### 3. Scan a file/directory to force synchronization

If a monitored folder has many subfolders and files, it may take a while for the
Syncthing daemon to notice new changes, even with *inotify* enabled. Issusing a
scan command to a changed directory or a changed file somehow forces the damemon
to notice the change and synchronize the file/directory with orher devices. The
command is

```
$ yasync-cli scan <PATH>
```

where `<PATH>` is the path to the target directory or file. If the directory or
the file does not belong to any monitored folder, an error is raised.

### 4. GET and POST endpoints

`yasync-cli` also exposes subcommands to send GET and POST requests. For example,
to rescan a monitored folder (of which the ID is `abcde-12345`):

```
$ yasync-cli post /db/scan folder=abcde-12345
```

The folder ID can be obtained from the output of `$ yasunc-cli show`.

The `get` and `post` subcommands are for debugging purpose only and for
my convenience.


## IV. Contact
--------------
Pi-Yueh Chuang ([pychuang@pm.me](pychuang@pm.me))
