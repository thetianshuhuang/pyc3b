# pyc3b

Python PC3b Assembler

![](https://github.com/thetianshuhuang/pyc3b/blob/master/wide.png)

## Dependencies
- Python 3
- [print](https://github.com/thetianshuhuang/print)

## Usage
```shell
$ python assemble.py source [output] [-flags]
```

### Arguments
- ```source```: Source LC3b assembly file
- ```output```: Optional output file; defaults to the same name as source, except with a ```.obj``` extension

### Flags
- ```-p```: Print out assembled files
- ```-t```: Print out symbol table
