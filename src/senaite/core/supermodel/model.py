# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.SUPERMODEL.
#
# SENAITE.CORE.SUPERMODEL is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2020 by it's authors.
# Some rights reserved, see README and LICENSE.

import json

from bika.lims import api
from DateTime import DateTime
from Products.CMFPlone.utils import safe_callable
from Products.CMFPlone.utils import safe_hasattr
from Products.CMFPlone.utils import safe_unicode
from Products.ZCatalog.Lazy import LazyMap
from senaite.core.supermodel import logger
from senaite.core.supermodel.decorators import returns_super_model
from senaite.core.supermodel.interfaces import ISuperModel
from zope.interface import implements

_marker = object()


class SuperModel(object):
    """Generic wrapper for content objects

    This wrapper exposes the schema fields of the wrapped content object as
    attributes. The schema field values are looked up by their accessors.

    If the primary catalog of the wrapped object contains a metadata column
    with the same name as the accessor, the metadata colum value is used
    instead.

    Note: Adapter lookup is done by `portal_type` name, e.g.:

    >>> portal_type = api.get_portal_type(self.context)
    >>> adapter = queryAdapter(uid, ISuperModel, name=portal_type)
    """
    implements(ISuperModel)

    def __init__(self, thing):

        # Type based initializers
        if isinstance(thing, basestring) and thing == "0":
            self.init_with_instance(api.get_portal())
        elif api.is_uid(thing):
            self.init_with_uid(thing)
        elif api.is_brain(thing):
            self.init_with_brain(thing)
        elif api.is_object(thing):
            self.init_with_instance(thing)
        else:
            raise TypeError(
                "Can not initialize a SuperModel with '{}'".format(
                    repr(thing)))

    def init_with_uid(self, uid):
        """Initialize with an UID
        """
        self._brain = None
        self._catalog = None
        self._data = {}
        self._instance = None
        self._uid = uid

    def init_with_brain(self, brain):
        """Initialize with a catalog brain
        """
        self._brain = brain
        self._catalog = self.get_catalog_for(brain)
        self._data = {}
        self._instance = None
        self._uid = api.get_uid(brain)

    def init_with_instance(self, instance):
        """Initialize with an instance object
        """
        self._brain = None
        self._catalog = self.get_catalog_for(instance)
        self._data = {}
        self._instance = instance
        self._uid = api.get_uid(instance)

    def __del__(self):
        """Destructor

        Terminates all references for garbage collection
        """
        logger.debug("Destroying {}".format(repr(self)))

        # https://zodb.readthedocs.io/en/latest/api.html#persistent.interfaces.IPersistent
        if self._instance is not None:
            changed = getattr(self._instance, "_p_changed", 0)
            # Object is either in the "Ghost" or in the "Saved" state and can
            # be safely deactivated
            if not changed:
                self._instance._p_deactivate()

        self._brain = None
        self._catalog = None
        self._data = None
        self._instance = None
        self._uid = None

    def __repr__(self):
        return "<{}:UID({})>".format(
            self.__class__.__name__, self.uid)

    def __str__(self):
        return self.uid

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, other):
        return self.uid == other.uid

    def __getitem__(self, key):
        value = self.get(key, _marker)
        if value is not _marker:
            return value
        raise KeyError(key)

    def __getattr__(self, name):
        value = self.get(name, _marker)
        if value is not _marker:
            return value
        # tab completion in pdbpp
        if name == "__members__":
            return self.keys()
        raise AttributeError(name)

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        for k in self.keys():
            yield k

    def keys(self):
        fields = api.get_fields(self.instance).keys()
        return filter(lambda f: not f.startswith("_"), fields)

    def iteritems(self):
        for k in self:
            yield (k, self[k])

    def iterkeys(self):
        return self.__iter__()

    def values(self):
        return [v for _, v in self.iteritems()]

    def items(self):
        return list(self.iteritems())

    def get_field(self, name, default=None):
        accessor = getattr(self.instance, "getField", None)
        if accessor is None:
            return default
        return accessor(name)

    def get(self, name, default=None):
        # Internal lookup in the data dict
        value = self.data.get(name, _marker)

        # Return the value immediately
        if value is not _marker:
            return self.data[name]

        # Field lookup on the instance
        field = self.get_field(name)

        if field is None:
            # expose non-private members of the instance/brain to have access
            # to e.g. self.absolute_url (function object) or self.review_state
            if not name.startswith("_") or not name.startswith("__"):
                # check if the instance contains this attribute
                instance = self.instance
                instance_value = getattr(instance, name, _marker)
                if instance_value is not _marker:
                    return instance_value

                # check if the brain contains this attribute
                brain = self.brain
                brain_value = getattr(brain, name, _marker)
                if brain_value is not _marker:
                    return brain_value

            return default
        else:
            # Retrieve field value by accessor name
            accessor = field.getAccessor(self.instance)
            accessor_name = accessor.__name__

            # Metadata lookup by accessor name
            value = getattr(self.brain, accessor_name, _marker)
            if value is _marker:
                logger.debug("Add metadata column '{}' to the catalog '{}' "
                             "to increase performance!"
                             .format(accessor_name, self.catalog.__name__))
                value = accessor()

        # Process value for publication
        value = self.process_value(value)

        # Store value in the internal data dict
        self._data[name] = value

        return value

    def process_value(self, value):
        """Process publication value
        """
        # UID -> SuperModel
        if api.is_uid(value):
            # Do not process "0" as the portal object
            # -> Side effect in specifications when the value is "0"
            if value == "0":
                return "0"
            return self.to_super_model(value)
        # Content -> SuperModel
        elif api.is_object(value):
            return self.to_super_model(value)
        # String -> Unicode
        elif isinstance(value, basestring):
            return safe_unicode(value).encode("utf-8")
        # DateTime -> DateTime
        elif isinstance(value, DateTime):
            return value
        # Process list values
        elif isinstance(value, (LazyMap, list, tuple)):
            return map(self.process_value, value)
        # Process dict values
        elif isinstance(value, (dict)):
            return {k: self.process_value(v) for k, v in value.iteritems()}
        # Process function
        elif safe_callable(value):
            return self.process_value(value())
        # Always return the unprocessed value last
        return value

    @property
    def uid(self):
        """UID of the wrapped object
        """
        return self._uid

    @property
    def data(self):
        """Internal data cache
        """
        if not isinstance(self._data, dict):
            self._data = {}
        return self._data

    @property
    def instance(self):
        """Content instance of the wrapped object
        """
        if self._instance is None:
            logger.debug("SuperModel::instance: *Wakup object*")
            self._instance = api.get_object(self.brain)
        return self._instance

    @property
    def brain(self):
        """Catalog brain of the wrapped object
        """
        if self._brain is None:
            logger.debug("SuperModel::brain: *Fetch catalog brain*")
            self._brain = self.get_brain_by_uid(self.uid)
        return self._brain

    @property
    def catalog(self):
        """Primary registered catalog for the wrapped portal type
        """
        if self._catalog is None:
            logger.debug("SuperModel::catalog: *Fetch catalog*")
            self._catalog = self.get_catalog_for(self.brain)
        return self._catalog

    def get_catalog_for(self, brain_or_object):
        """Return the primary catalog for the given brain or object
        """
        if not api.is_object(brain_or_object):
            raise TypeError("Invalid object type %r" % brain_or_object)
        catalogs = api.get_catalogs_for(brain_or_object, default="uid_catalog")

        return catalogs[0]

    def get_brain_by_uid(self, uid):
        """Lookup brain from the right catalog
        """
        if uid == "0":
            return api.get_portal()

        # ensure we have the primary catalog
        if self._catalog is None:
            brain = api.get_brain_by_uid(uid, default=_marker)
            if brain is _marker:
                raise ValueError("No object found for UID '{}'".format(uid))
            # Retrieve the first registered catalog for the brain
            self._catalog = self.get_catalog_for(brain)

        # Fetch the brain with the primary catalog
        results = self.catalog({"UID": uid})
        if not results:
            raise ValueError("No results found for UID '{}'".format(uid))
        if len(results) != 1:
            raise ValueError("Found more than one object for UID '{}'"
                             .format(uid))
        return results[0]

    @returns_super_model
    def to_super_model(self, thing):
        """Wraps an object into a Super Model
        """
        if api.is_uid(thing):
            return SuperModel(thing)
        if not api.is_object(thing):
            raise TypeError("Expected a portal object, got '{}'"
                            .format(type(thing)))
        return thing

    def is_valid(self):
        """Self-check
        """
        try:
            self.brain
        except ValueError:
            return False
        return True

    def stringify(self, value):
        """Convert value to string

        This method is used to generate a simple JSON representation of the
        object (without dereferencing objects etc.)
        """
        # SuperModel -> UID
        if ISuperModel.providedBy(value):
            return str(value)
        # DateTime -> ISO8601 format
        elif isinstance(value, (DateTime)):
            return value.ISO8601()
        # Image/Files -> filename
        elif safe_hasattr(value, "filename"):
            return value.filename
        # Dict -> convert_value_to_string
        elif isinstance(value, dict):
            return {k: self.stringify(v) for k, v in value.iteritems()}
        # List -> convert_value_to_string
        if isinstance(value, (list, tuple, LazyMap)):
            return map(self.stringify, value)
        # Callables
        elif safe_callable(value):
            return self.stringify(value())
        elif isinstance(value, unicode):
            value = value.encode("utf8")
        try:
            return str(value)
        except (AttributeError, TypeError, ValueError):
            logger.warn("Could not convert {} to string".format(repr(value)))
            return None

    def to_dict(self, converter=None):
        """Returns a copy dict of the current object

        If a converter function is given, pass each value to it.
        Per default the values are converted by `self.stringify`.
        """
        if converter is None:
            converter = self.stringify
        out = dict()
        for k, v in self.iteritems():
            out[k] = converter(v)
        return out

    def to_json(self):
        """Returns a JSON representation of the current object
        """
        return json.dumps(self.to_dict())

    def flush(self):
        """Flush the internal data cache
        """
        self._data = {}
