"""
parses the markdown file and returns the Documentation for the document variables.
It uses pydantic to structure the documentation object that will be used by the LSP.


The parser will take a markdown like this:

```markdown
# Title 

Ignored part 


Optional doc-start marker, if not found it will assume the first `##` is the doc start.
<!-- doc-start -->  

## Variable

> Documentation for the variable

### Variable.Nested
> Documentation for the nested variable

#### Variable.Nested.Nested
> Documentation for the nested nested variable

##### Nested
> Documentation for the Variable.Nested.Nested.Nested variable 

What defines nesting is actually the heading level, so the parser will look for the first heading level that 
is lower than the current one.

## another_variable = 123
> Documentation for the another variable

The text after the `=` on the header is optional and ignored by the parser

## ANOTHER_VARIABLE_WITH_UNDERSCORES
> Documentation for the another variable with underscores

The parser is case insensitive, so `variable` and `Variable` and `VARIABLE` are the same.

## FOO
>>>
This blockquote format is also supported,
this is the FOO variable documentation
>>>

## DATABASES
> This is a dictionary of database configuration, can handle multiple database settings.

### {key}
>>>
The key for the database can be any valid string
it is mandatory that the first one is named `default`
Example:
```py
DATABASES = {
  "default": {
    "NAME": "foo",
    "OPTIONS": {
        "TLS_VERIFICATION": True,
        "TIMEOUT": 30
    }
  }
}
```
>>>

#### NAME
> The name for the database
> if it is sqlite it must be the filename
> if it is a DBMS it must be a full connection string

This one is actualy `DATABASES.default.NAME` or `DATABASES__default__NAME` or `{key}.NAME` or `{key}__NAME`  

The parser only cares about the last fragment on variable name, so `DATABASES.default.NAME` 
is the same as `DATABASES__default__NAME` or `{key}.NAME` or `{key}__NAME`

The parser will split the variable and assume the last fragment as the target.

if the `NAME = "default"` then the parser will first remove everything after the `=` 
then will replace `__` with `.`
and then will split the variable name into `[DATABASES, default, NAME]`
and will take the last element `NAME` as the target
and then will look for the first heading level that is lower than the current one.
which is `###` in this case and will assume this is nested under `DATABASES.{key}`
The placeholders `{key}` and `[item]` can be used to declare dynamic variable name on dict and lists respectively.

#### {key}.OPTIONS
> Arbitrary options passed directly to the DBMS driver as a key:value pair.

As you can see you can use the `PARENT.KEY` or `PARENT__KEY` spec optionally, this one is actually the same 
as simply `OPTIONS` as the heading level already defines the parent.

##### TLS_VERIFICATION
> This boolean marks if TLS verification is on/off

##### TIMEOUT
> This is an integer timeout in seconds

##### {key}.OPTIONS.TIMEOUT = 30
> Time out in seconds

The text after the `=` on the header is optional and ignored by the parser


## authors
>>>
The authors of the blog, this is a dictionary of authors, the key is the author's name and the value is a dictionary of author's data.

Example:

```python
AUTHORS = [
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "url": "https://john.doe.com",
        "avatar": "https://john.doe.com/avatar.png",
        "bio": "John Doe is a software engineer at Example Inc."
    }
]   
```

The `name` is the author's name, the `email` is the author's email, the `url` is the author's URL, the `avatar` is the author's avatar, the `bio` is the author's bio.

>>>

### authors[item].name
> The name of the author.

### authors[item].email
> The email of the author.

### [item].url
> The URL of the author.

### [item].avatar
> The avatar of the author.

### authors[item].bio
> The bio of the author.

---

Optional doc-end marker, if not found it will assume the end of the file is the doc end.
<!-- doc-end -->

Extra content that is ignored by the parser.
```

"""

import re
from typing import Optional
from pydantic import BaseModel


lookup_path = str  # AST path of the variable


class Variable(BaseModel):
    """
    The variable model, this is the model for a variable.
    """

    name: str
    doc: str
    # can optionally take more fields
    # full_name: str
    # type: type (str, dict, list, bool, int, float) taken from default value or header (NAME<type> = 10)
    # default: default value (taken from after the `=` on the header)
    # required: taken from the presence of * on the header (NAME * = 10)
    # choices: taken from the [enum] on the header (NAME [option1, option2, option3] = option1)
    # deprecated: taken from the presence of `DEPRECATED` after name on the header (NAME DEPRECATED = 10)
    parent: Optional["Variable"] = None
    children: list["Variable"] = []


class Document(BaseModel):
    variables: dict[lookup_path, Variable]

    def get_variable(self, path: lookup_path) -> Variable | None:
        """Get the variable from the document.

        This must be able to perform dynamic lookup from what is received from the LSP,
        so it must be able to handle `SERVER.HOST` and `SERVER__HOST` and `SERVER__HOST__OPTIONS`
        the lookup_path can be a simple str to match or a specific AST path for instant lookup.
        """
        # Try exact match first (case insensitive)
        path_lower = path.lower()
        for key, var in self.variables.items():
            if key.lower() == path_lower:
                return var

        # Try matching just the variable name (last part)
        parts = path.replace("__", ".").split(".")
        target = parts[-1].lower()

        for key, var in self.variables.items():
            var_name = key.split(".")[-1].lower()
            if var_name == target:
                return var

        return None


class Header(BaseModel):
    """
    The block model, this is the model for a block.
    """

    level: int
    title: str
    content: str
    parent: Optional["Header"] = None
    children: list["Header"] = []


class HeaderTree(BaseModel):
    """Stores all headers parsed from the markdown file

    taken from the document start to the document end.

    Document start == First `##` or `<!-- doc-start -->`
    Document end == First `<!-- doc-end -->` or `EOF`
    """

    headers: list[Header] = []


def parse_header_tree(markdown: str) -> HeaderTree:
    """Parse the markdown file and return the parsed markdown."""
    lines = markdown.split("\n")
    headers = []
    stack = []  # Stack to keep track of parent headers

    # Find document start
    doc_started = False
    doc_start_idx = 0
    doc_end_idx = len(lines)

    for i, line in enumerate(lines):
        if "<!-- doc-start -->" in line:
            doc_started = True
            doc_start_idx = i + 1
            break
        elif line.startswith("## "):
            doc_started = True
            doc_start_idx = i
            break

    if not doc_started:
        return HeaderTree(headers=[])

    # Find document end
    for i, line in enumerate(lines[doc_start_idx:], doc_start_idx):
        if "<!-- doc-end -->" in line:
            doc_end_idx = i
            break

    i = doc_start_idx
    while i < doc_end_idx:
        line = lines[i]

        # Check if it's a header
        if re.match(r"^#{2,6} ", line):
            # Count the level (## = level 1, ### = level 2, etc.)
            level = len(re.match(r"^(#{2,6}) ", line).group(1)) - 1

            # Extract title (remove # and everything after =)
            title = re.sub(r"^#{2,6} ", "", line)
            if "=" in title:
                title = title.split("=")[0].strip()

            # Extract content (blockquote immediately after)
            content = ""
            j = i + 1

            # Skip empty lines
            while j < doc_end_idx and not lines[j].strip():
                j += 1

            # Check for >>> style blockquote
            if j < doc_end_idx and lines[j].strip() == ">>>":
                j += 1
                content_lines = []
                while j < doc_end_idx and lines[j].strip() != ">>>":
                    content_lines.append(lines[j])
                    j += 1
                content = "\n".join(content_lines).strip()
                i = j
            # Check for > style blockquote
            elif j < doc_end_idx and lines[j].startswith(">"):
                content_lines = []
                while j < doc_end_idx and lines[j].startswith(">"):
                    content_lines.append(lines[j][1:].strip())
                    j += 1
                content = "\n".join(content_lines)
                i = j - 1

            # Create header object
            header = Header(level=level, title=title, content=content)

            # Manage parent-child relationships based on level
            while stack and stack[-1].level >= level:
                stack.pop()

            if stack:
                header.parent = stack[-1]
                stack[-1].children.append(header)

            headers.append(header)
            stack.append(header)

        i += 1

    return HeaderTree(headers=headers)


def parse_document(markdown: str) -> Document:
    """Parse the markdown file and return the parsed document.

    This creates a HeaderTree and then with all the elements structured as a tree,
    parses the tree to create a Document object.
    """
    header_tree = parse_header_tree(markdown)
    variables = {}

    def process_header(header: Header, parent_path: str = ""):
        # Clean the title to get the variable name
        title = header.title

        # Remove placeholders like {key} or [item]
        title = re.sub(r"\{[^}]+\}", "", title)
        title = re.sub(r"\[[^\]]+\]", "", title)

        # Remove parent path prefix if present
        title = title.split(".")[-1].strip()

        # Build the full path
        if parent_path:
            full_path = f"{parent_path}.{title}"
        else:
            full_path = title

        # Create variable
        var = Variable(name=title, doc=header.content)

        # Store with both the full path and just the name
        if title:  # Only add if title is not empty
            variables[full_path] = var
            variables[title] = var

        # Process children
        for child in header.children:
            process_header(child, full_path if title else parent_path)

    # Process all top-level headers
    for header in header_tree.headers:
        if header.parent is None:
            process_header(header)

    return Document(variables=variables)
