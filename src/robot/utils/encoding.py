#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import sys

from .encodingsniffer import get_console_encoding, get_system_encoding
from .misc import isatty
from .unic import safe_str

CONSOLE_ENCODING = get_console_encoding()
SYSTEM_ENCODING = get_system_encoding()
CUSTOM_ENCODINGS = {"CONSOLE": CONSOLE_ENCODING, "SYSTEM": SYSTEM_ENCODING}
PYTHONIOENCODING = os.getenv("PYTHONIOENCODING")


def console_decode(string, encoding=CONSOLE_ENCODING):
    """Decodes bytes from console encoding to Unicode.

    Uses the system console encoding by default, but that can be configured
    using the `encoding` argument. In addition to the normal encodings,
    it is possible to use case-insensitive values `CONSOLE` and `SYSTEM` to
    use the system console and system encoding, respectively.

    If `string` is already Unicode, it is returned as-is.
    """
    if isinstance(string, str):
        return string
    encoding = CUSTOM_ENCODINGS.get(encoding.upper(), encoding)
    try:
        return string.decode(encoding)
    except UnicodeError:
        return safe_str(string)


def console_encode(
    string,
    encoding=None,
    errors="replace",
    stream=sys.__stdout__,
    force=False,
):
    """Encodes the given string so that it can be used in the console.

    If encoding is not given, determines it based on the given stream and system
    configuration. In addition to the normal encodings, it is possible to use
    case-insensitive values `CONSOLE` and `SYSTEM` to use the system console
    and system encoding, respectively.

    Decodes bytes back to Unicode by default, because Python 3 APIs in general
    work with strings. Use `force=True` if that is not desired.
    """
    if not isinstance(string, str):
        string = safe_str(string)
    if encoding:
        encoding = CUSTOM_ENCODINGS.get(encoding.upper(), encoding)
    else:
        encoding = _get_console_encoding(stream)
    if encoding.upper() != "UTF-8":
        encoded = string.encode(encoding, errors)
        return encoded if force else encoded.decode(encoding)
    return string.encode(encoding, errors) if force else string


def _get_console_encoding(stream):
    encoding = getattr(stream, "encoding", None)
    if isatty(stream):
        return encoding or CONSOLE_ENCODING
    if PYTHONIOENCODING:
        return PYTHONIOENCODING
    return encoding or SYSTEM_ENCODING


def system_decode(string):
    return string if isinstance(string, str) else safe_str(string)


def system_encode(string):
    return string if isinstance(string, str) else safe_str(string)
