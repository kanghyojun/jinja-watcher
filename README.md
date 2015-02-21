# jinja-watcher

compile and watch jinja2 template files.

## Usage

    $ jinja-watcher -w --dest ./out ./in

`src` can be eithr directory or json file. if `src` is a json it should be like
below.


    {
      "dest": "./out",
      "verbose": true,
      "watch": true,
      "excludes": ["layout.html", "user/layout.html"],
      "env": "./env.py"
    }
