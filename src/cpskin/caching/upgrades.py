# -*- coding: utf-8 -*-


def reload_registry_xml(context):
    context.runImportStepFromProfile(
        'profile-cpskin.workflow:default', 'plone.app.registry')
