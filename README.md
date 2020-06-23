YASync-CLI -- Yet Another Syncthing CLI Tool
============================================

***YASync-CLI*** provides a command-line tool `yasync-cli` to manipulate a
Syncthing daemon from a terminal. It is supposed to be useful for headless
servers.

Why another Syncthing CLI tool? Because I don't like other similar tools... And
actually, not many of them are still well maintained. To the best of my knowledge,
[Syncthing Tray](https://github.com/Martchus/syncthingtray) is the only one that
is well maintained and has a complete set of features. However, Syncthing Tray
does not separate its CLI tool from GUI components. Its users have to install
all GUI components even if they only need the CLI tool. So I decided to work on
my own version.

This project is still a WIP. Currently, I only add a feature when I need one as
I'm the only user. Feature requests are welcome. And feel free to test it.
`yasync-cli` has never been tested on other machines/systems.

-------------------
## I. Installation

### 1. Prerequisite

`yasync-cli` is implemented with Python only. So modification and expansion is
easy. Currently, the only third-party dependency is
[Requests](https://github.com/psf/requests).

### 2. Installation

It's recommended to install it to a local searchable path with `pip`:

```
$ git clone https://github.com/piyueh/yasync-cli
$ cd yasync-cli
$ pip install --user .
```

By default, the executable, `yasync-cli`, is installed at `~/.local/bin/yasync-cli`.
If `~/.local/bin` is already in `PATH`, then the executable can be executed with
just `$ yasync-cli`. Alternatively, one can choose to use the full path to run
the executable, i.e., `$ ~/.local/bin/yasync-cli`.

Another way to test it without installing is to execute the module with Python:
go into the repository root folder and, when executing the tool, replace
`yasync-cli` with `python -m yasynccli`. But this is not recommended for
production run.

### 3. Removing `pip` installation

```
$ pip uninstall yasynccli
```

---------------------
## II. Example usage

### 1. Help pages

See help with

```
$ yasync-cli --help
```

or see the help of subcommands with

```
$ yasync-cli <subcommand> --help
```

Currently supported subcommands include: `show`, `log`, `check`, `scan`, `get`,
and `post`.


### 2. Show basic info in a configuration file

```
$ yasync-cli show
```

This will print very basic info of the configuration and the monitored folders'
information from the default Syncthing config file (i.e.,
`${HOME}/.config/syncthing/config.xml`).

To show the info of a customized configuration file:

```
$ yasync-cli --config <path to the config file> show
```

### 3. Scan a file/directory to force synchronization

If a monitored folder has many subfolders and files, it may take a while for the
Syncthing daemon to notice new changes, even with *inotify* enabled. Issusing a
scan command to a changed directory or a changed file somehow forces the damemon
to notice the change and synchronize the file/directory with orher devices. The
command is

```
$ yasync-cli scan <PATH>
```
if using the default Syncthing configuration. `<PATH>` is the path to the target
directory or file. If the directory or the file does not belong to any monitored
folder, an error is raised.

### 4. GET and POST endpoints

`yasync-cli` also exposes subcommands for sending GET and POST requests to a
Syncthing server. For example, to rescan a file of a monitored folder (of which
the ID is `abcde-12345`) using a POST request:

```
$ yasync-cli post /db/scan folder=abcde-12345 sub=dir1/dir2/file.txt
```

The folder ID can be obtained from the output of `$ yasunc-cli show`. And
`dir1/dir2/file.txt`is the relative path of the target file to the monitered
folder.

This is just an example usage. Basically, there's no need to use `post` and `get`
for simple tasks like re-scanning because `yasync-cli` already has a `scan`
subcommand. The `get` and `post` subcommands are mainly for debugging purpose and
for my convenience. If anyone finds there's a `get` or `post` request being used
very often, it's better to wrap it as a subcommand of `yasync-cli`.

----------------
## III. Contact

Pi-Yueh Chuang ([pychuang@pm.me](pychuang@pm.me))
