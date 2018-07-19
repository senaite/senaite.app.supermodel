# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.SUPERMODEL
#
# Copyright 2018 by it's authors.

from senaite import api
from senaite.core.supermodel.interfaces import ISuperModel
from zope.component import queryAdapter


def returns_super_model(func):
    """Wraps an object into a SuperModel
    """

    def to_super_model(obj):
        # avoid circular imports
        from senaite.core.supermodel import SuperModel

        # Object is already a Publication Object, return immediately
        if isinstance(obj, SuperModel):
            return obj

        # Only portal objects are supported
        if not api.is_object(obj):
            raise TypeError("Expected a portal object, got '{}'"
                            .format(type(obj)))

        # Wrap the object into a specific Publication Object Adapter
        uid = api.get_uid(obj)
        portal_type = api.get_portal_type(obj)

        adapter = queryAdapter(uid, ISuperModel, name=portal_type)
        if adapter is None:
            return SuperModel(uid)
        return adapter

    def decorator(*args, **kwargs):
        obj = func(*args, **kwargs)
        if isinstance(obj, (list, tuple)):
            return map(to_super_model, obj)
        return to_super_model(obj)

    return decorator
