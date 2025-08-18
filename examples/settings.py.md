# App configuration

This is the configuration documentation for the **APP**,
Here you can get detailed information about how to configure the application.  

The documentation written here is also available on the code editor via `doc-lsp`

## SERVER
> This variable defines which server the system is connected to,         
> when used together with port this will define the connection string.   
> example: `hostname:port`                                             

This part of the docs are here to be read on github or any other markdown rendered content
but the code editor will see only what is on the first blockquote above.

## PORT = 1234
> Port used to connect to server

This can optionally have the default value added to the header.
just for displaying reasons, doc-lsp will actually strip everything after the `=`

## DEBUG = True
> Enable or disable debugging mode

## ALLOW_RESOURCE_MANAGEMENT = True
> When disabled it will not allow Creation, Update, Deletion of resources
> in the application.

## DEFAULT_ORG
> New users will be assigned to this organization
> If this organization does not exist it will be created at app startup

## DATABASES
>>>
A dictionary of database configuration, can handle multiple database settings.
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

As you can see, blockquotes can also be defined using `>>>`

### {key}
>>>
The key for the database can be any valid string
it is mandatory that the first one is named `default`
Example:
```py
DATABASES = {"foo": {"NAME": "mydb", ...}}
``` 
>>>

#### NAME
> The name for the database
> if it is sqlite it must be the filename
> if it is a DBMS it must be a full connection string

#### {key}.OPTIONS
> Arbitrary options passed directly to the DBMS driver as a key:value pair.

As you can see you can use the `PARENT.KEY` or `PARENT__KEY` spec optionally.

##### TLS_VERIFICATION
> Enables or disables TLS verification

This is implicitly `{key}.OPTIONS.TLS_VERIFICATION` and the nesting is resolved by `#####` heading level  
so explicitly using the FQKP (Full qualified key path) is optional.

##### {key}.OPTIONS.TIMEOUT = 30
> Time out in seconds

<!-- doc-end -->

The part of the doc that is read by doc-lsp ended, here any markdown or text can be added, doc-lsp ignores it.
