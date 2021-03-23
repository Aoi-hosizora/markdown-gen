# markdown-gen (mdg)

+ A command line tool that can generate markdown using some options.

### Dependencies

+ [md-toc](https://pypi.org/project/md-toc/)

### Install

+ Linux

```bash
sudo pip3 install md-toc
chmod +x cli.py
sudo ln -s /usr/bin/mdg /xxx/cli.py
```

+ Windows

```bash
# waiting...
```

### Usage

```bash
$ mdg generate --help

# Usage: mdg generate [OPTIONS] INPUT_FILE
#
#   Generate markdown by options.
#
# Options:
#   -o, --output TEXT  Output file path.  [required]
#   --force            Force to save.
#   --center_image     Make images center.
#   --en_punctuation   Use English punctuations.
#   --katex_image      Use image for katex equation.
#   --add_toc          Add table of content.
#   --copy_image       Copy image to current folder.
#   --help             Show this message and exit.
```

### Reference

+ [Building Beautiful Command Line Interfaces with Python](https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df)
+ [uetchy/math-api](https://github.com/uetchy/math-api)
+ [frnmst/md-toc](https://github.com/frnmst/md-toc)
  