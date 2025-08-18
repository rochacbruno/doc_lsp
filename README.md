# doc_lsp

doc_lsp is a simple specification and LSP (Language Server) that loads comments from a separate file.

Document variables in a separate markdown file and this LSP will show the docs on your editor.

## Standard

Assuming a file named `settings.py` 

```py
SERVER = "localhost"
PORT = 4545
```

Or a `config.conf`

```conf
max_open_windows    true
font_size           18
```

Then the LSP will lookup information about each variable on a separate file.

`settings.py.md`
```markdown
## SERVER
> This variable defines which server the system is connected to,         
> when used together with port this will define the connection string.   
> example: `hostname:port`                                             

## PORT
> Port used to connect ot server

```

`config.conf.md`
```plain
## max_open_windows
> This variable is used to set how many multiple tiles can be opened
> at the same time.

## font_size
> Set the default size for the system font.
```

## Usage

With the LSP Server `conf_doc_lsp` enabled on your editor,
having the variable selected or with cursor focus, trigger the action `view_doc` 
and the editor will show the overlay with the full text from the respective comment file.

`|` = cursor position
```py
SERV|ER = "foo"
```
Trigger `view_doc` (you may have a keybind such as Ctrl+e`)

```plain
SERV|ER = "foo"
    ______ doc_lsp:SERVER ___________________________________________________
    | This variable defines which server the system is connected to,         |
    | when used together with port this will define the connection string.   |
    | example: `hostname:port`                                               |
    _________________________________________________________________________
```

If the `settings.py.md` does not exist, then the action will be NOOP and just emit a INFO `Doc not found for variable`


## Implementation

- The doc_lsp is implemented in Rust
- It is a single binary and zero config
- Just run `doc_lsp` to start calling it
- Lookup is always read direclty from file, so changes on .md imediatelly reflect

## Specs

- doc_lsp is filetype agnostic
- doc_lsp lookup will match `filename.ext` -> `filename.ext.md`
- Lookup is made from the doc_lsp parser
- The last occurence wins in case of duplication

 
See [./examples](examples) 



