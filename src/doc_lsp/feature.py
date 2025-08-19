from __future__ import annotations

import re
from lsprotocol import types
from pygls.capabilities import get_capability
from pygls.workspace import TextDocument


class HoverTrigger:
    """Define when the feature's hover method should be called."""

    patterns: list[re.Pattern]
    """A list of regular expressions to try"""

    languages: set[str] = set()
    """Languages in which the trigger should fire.

    If empty, the document's language will be ignored.
    """

    def __call__(
        self,
        uri: str,
        params: types.HoverParams,
        document: TextDocument,
        language: str,
        client_capabilities: types.ClientCapabilities,
    ) -> HoverContext | None:
        """Determine if this hover trigger should fire.

        Parameters
        ----------
        uri
           The uri of the document in which the request was made

        params
           The definition params sent from the client

        document
           The document in which the request was made

        language
           The language at the point where the request was made

        client_capabilities
           The client's capabilities

        Returns
        -------
        Optional[HoverContext]
           A hover context, if this trigger has fired
        """

        if len(self.languages) > 0 and language not in self.languages:
            return None

        try:
            line = document.lines[params.position.line]
        except IndexError:
            line = ""

        for pattern in self.patterns:
            for match in pattern.finditer(line):
                # Only trigger if the position of the request is within the match.
                start, stop = match.span()
                if not (start <= params.position.character <= stop):
                    continue

                return HoverContext(
                    uri=uri,
                    doc=document,
                    match=match,
                    position=params.position,
                    language=language,
                    capabilities=client_capabilities,
                )

        return None


class HoverContext:
    """Captures the context within which a hover request has been made."""

    uri: str
    """The uri for the document in which the hover request was made"""

    doc: TextDocument
    """The document within which the hover request was made"""

    match: re.Match
    """The match object describing the site of the hover request."""

    position: types.Position
    """The position at which the hover request was made."""

    language: str
    """The language where the hover request was made."""

    capabilities: types.ClientCapabilities
    """The client's capabilities."""

    def __repr__(self):
        p = f"{self.position.line}:{self.position.character}"
        return f"HoverContext<{self.uri}:{p} ({self.language}) -- {self.match}>"

    @property
    def content_format(self) -> list[types.MarkupKind]:
        """The list of supported markup formats the client supports (if known).
        Order indicates the client's preference"""

        hover: types.HoverClientCapabilities | None
        hover = get_capability(self.capabilities, "text_document.hover", None)
        if hover is None:
            return []

        return list(hover.content_format or [])

    @property
    def markdown_parser(self) -> tuple[str, str | None] | None:
        """The markdown parser used by the client (if known)"""

        markdown: types.MarkdownClientCapabilities | None
        markdown = get_capability(self.capabilities, "general.markdown", None)
        if markdown is None:
            return None

        return (markdown.parser, markdown.version)

    @property
    def markdown_allowed_tags(self) -> list[str]:
        """The list of allowed html tags the client will allow in markdown text (if
        known)"""

        markdown: types.MarkdownClientCapabilities | None
        markdown = get_capability(self.capabilities, "general.markdown", None)
        if markdown is None:
            return []

        return list(markdown.allowed_tags or [])
