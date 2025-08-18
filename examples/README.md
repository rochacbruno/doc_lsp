# App Config

This is the general app config file, this headline (h1) here is ignored by `doc-lsp` but may be useful for publishing the docs on another markdown parser. e.g: Github, static site, docs site etc.

doc-lsp only cares about the heading levels starting from `##` that can be infinite number  
and the first blockquote after it.

All other content after the first blockquote is ignored by doc-lsp, so any markdown formatting can be used.

- doc-lsp will take variable name such as `FOO` and look for `## FOO` or `## Foo` or `## foo` case insensitive.
- doc-lsp will also lookup for nesting variables, if triggered from `server: {ho|st: }` it will first lookup for `## Server` and all its one level children, then will lookup for any of `### host`, `### server.host`, `### server__host` (it will actually take the heading, split for `.` then split for `__` and then take last element) the first that matches `host` will be the returnedvalue.
- The nesting lookup will be made using AST for supported languages (Python, YAML, JSON, TOML) and for generic text files it will use a simple parser that will simply try to match the current line tokens with the variable name in the header, this will be done by tokenizing the line and then trying to match from full to partial by poping the last token until it matches, at the end it will match the first element that is the root of the variable name.
- doc-lsp will read only the first blockquote inside that header, consecutive `>` or lines wrapped between `>>>` and `>>>`.
- doc-lsp will ignore all the markdown after the first blockquote  

doc-lsp built-in parser is really simple, it only cares about

- Find the doc-start/doc-end markers or set it as first `##` and `EOF`
- Capture all markdown headers with its contents (but it allows unlimited number of #)
- Capture the first blockquote inside each header (consecutie `>` or `>>>` wrapped text)

Adding `<!-- doc-start -->` will optionally tell doc-lsp where the documentation lookup must stop, so the lines before are ignored, if not found then it will assume the first `##` is the doc start.

<!-- doc-start -->

## SERVER
> This is the comment for the `SERVER` variable, the format here must keep simple to be effective  
on the LSP overlay window. 
> it can span multiple lines.

This part is ignored by doc-lsp, the editor will show only the text above the line, so here you can have
any advanced markdown you want.

### SERVER.HOST

> This is the comment for `SERVER.HOST` variable 


As you can see, this is a nested attribute documentation

### PORT

> This is the port used for connection

As you can see the SERVER prefix can be omited, what matters is that the levels are right `###`

### SERVER__OPTIONS

> This is the server options

Dunder (double underscore) can also be used as a separator, useful for Dynaconf style settings

#### TLS_VERIFICATION

> This boolean marks if TLS verification is on/off

#### TIMEOUT

> This is an integer timeout in seconds

## variable

> Variables must be a full match on the respective file

### nested1

> This is for VARIABLE.NESTED1

#### nested2

> This is for VARIABLE.NESTED1.nested2


##### nested3

> This is for VARIABLE.NESTED1.nexted2.nexted3

###### nested4

> This is for VARIABLE.NESTED1.nexted2.nexted3.nested4

####### nested5

> This is for VARIABLE.NESTED1.nexted2.nexted3.nested4.nested5


######## nested6

> This is for VARIABLE.NESTED1.nexted2.nexted3.nested4.nested5.nexted6


---

<!-- doc-end -->

Adding `<!-- doc-end -->` will optionally tell doc-lsp where the documentation lookup must stop, so the rest of markdown is ignored.

```mermaid
graph LR
A --> B
```
