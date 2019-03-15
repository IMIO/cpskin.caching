# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import cpskin.caching


class CpskinCachingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=cpskin.caching)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "cpskin.caching:default")


CPSKIN_CACHING_FIXTURE = CpskinCachingLayer()


CPSKIN_CACHING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_CACHING_FIXTURE,), name="CpskinCachingLayer:IntegrationTesting"
)


CPSKIN_CACHING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CPSKIN_CACHING_FIXTURE,), name="CpskinCachingLayer:FunctionalTesting"
)


CPSKIN_CACHING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(CPSKIN_CACHING_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CpskinCachingLayer:AcceptanceTesting",
)
