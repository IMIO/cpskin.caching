# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory
from cpskin.caching import patch

patch  # flake8
_ = MessageFactory("cpskin.caching")
