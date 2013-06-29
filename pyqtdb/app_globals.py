# -*- coding: utf-8 -*-

import os

from . import XSettings

docs_gen =  os.environ.get('__GEN_DOCS__', None)
"""Flag to indicate Sphinx docs gen, Quirk of ReadTheDocs.org"""

settings = XSettings.XSettings()
"""Global settings instance of :py:class:`~pyqtdb.XSettings.XSettings` """





