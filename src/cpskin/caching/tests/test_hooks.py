#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import zope.component.testing
from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import provideAdapter
from zope.component import provideHandler
from zope.component import provideUtility
from zope.event import notify
from zope.interface import alsoProvides
from zope.interface import implements
from plone.registry.interfaces import IRegistry
from plone.registry import Registry
from plone.cachepurging.interfaces import IPurger
from plone.cachepurging.interfaces import ICachePurgingSettings
from plone.cachepurging.tests.test_hooks import FauxRequest

from plone.registry.fieldfactory import persistentFieldAdapter

from ZPublisher.pubevents import PubSuccess
from cpskin.caching.hooks import purge
from cpskin.caching.testing import CPSKIN_CACHING_INTEGRATION_TESTING  # noqa


class TestPurgeHandler(unittest.TestCase):
    def setUp(self):
        provideAdapter(AttributeAnnotations)
        provideAdapter(persistentFieldAdapter)
        provideHandler(purge)

    def tearDown(self):
        zope.component.testing.tearDown()

    def test_purge_no_config(self):
        request = FauxRequest()
        alsoProvides(request, IAttributeAnnotatable)

        IAnnotations(request)["plone.cachepurging.urls"] = set(["/foo", "/bar"])

        registry = Registry()
        registry.registerInterface(ICachePurgingSettings)
        provideUtility(registry, IRegistry)
        settings = registry.forInterface(ICachePurgingSettings)
        settings.enabled = True

        class FauxPurger(object):
            implements(IPurger)

            def __init__(self):
                self.purged = []

            def purgeAsync(self, url, httpVerb="PURGE"):
                self.purged.append(url)

        purger = FauxPurger()
        provideUtility(purger)

        notify(PubSuccess(request))

        self.assertEquals([], purger.purged)

    def test_purge_with_config(self):
        request = FauxRequest()
        alsoProvides(request, IAttributeAnnotatable)

        IAnnotations(request)["plone.cachepurging.urls"] = set(["/foo", "/bar"])

        registry = Registry()
        registry.registerInterface(ICachePurgingSettings)
        provideUtility(registry, IRegistry)

        settings = registry.forInterface(ICachePurgingSettings)
        settings.enabled = True

        class FauxPurger(object):
            implements(IPurger)

            def __init__(self):
                self.purged = []

            def purgeAsync(self, url, httpVerb="PURGE"):
                self.purged.append(url)

        purger = FauxPurger()
        provideUtility(purger)
        os.environ["CACHING_SERVERS"] = "http://localhost:1234 http://10.0.100.1:1235"
        notify(PubSuccess(request))

        self.assertEquals(
            [
                "http://localhost:1234/foo",
                "http://10.0.100.1:1235/foo",
                "http://localhost:1234/bar",
                "http://10.0.100.1:1235/bar",
            ],
            purger.purged,
        )


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
