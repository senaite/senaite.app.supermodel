SENAITE CORE SUPERMODEL
=======================

The SENAITE SUPERMODEL is a content wrapper for objects and catalog brains in
SENAITE and provides a unified dictionary interface to access the schema fields,
methods and metadata.

Running this test from the buildout directory::

    bin/test test_doctests -t SUPERMODEL


Introduction
------------

The purpose of this SUPERMODEL is to help coders to access the data from content
objects. It also ensures that the most effective and efficient method is used to
achieve a task.

Import it first::

    >>> from senaite.core.supermodel import SuperModel

Now we can simply create a new `SuperModel` instance by passing in the Unique ID
(UID) of a content object, a catalog brain or an instance object.

So let's create a client for that::

    >>> from senaite import api
    >>> portal = api.get_portal()

    >>> client = api.create(portal.clients, "Client", title="Happy Hills", ClientID="HH")
    >>> client
    <Client at /plone/clients/client-1>

     >>> client.getName()
     'Happy Hills'

     >>> client.getClientID()
     'HH'

Now a `SuperModel` can be instantiated via the UID::

    >>> uid = api.get_uid(client)
    >>> supermodel = SuperModel(uid)

It can be also instantiated via a catalog brain::

    >>> uid_catalog = api.get_tool("uid_catalog")
    >>> brain = uid_catalog({"UID": uid})[0]
    >>> supermodel2 = SuperModel(brain)

And it can be instantiated with the content object directly::

    >>> supermodel3 = SuperModel(client)

All of them create new `SuperModel` instances for us::

    >>> supermodel
    <SuperModel:UID(...)>

    >>> supermodel2
    <SuperModel:UID(...)>

    >>> supermodel3
    <SuperModel:UID(...)>

All of them should be equal::

    >>> supermodel == supermodel2 == supermodel3
    True

    >>> supermodel.catalog == supermodel2.catalog == supermodel3.catalog
    True


We have now full access to the `Client` schema::

    >>> supermodel.Name
    'Happy Hills'

    >>> supermodel.ClientID
    'HH'

And the `Client` instance as well as the catalog brain of the primary registered
catalog are lazily fetched::

    >>> supermodel.instance
    <Client at /plone/clients/client-1>

    >>> supermodel.brain
    <Products.ZCatalog.Catalog.mybrains object at ...>

This gives full access to the catalog metadata and content schema::

    >>> supermodel.review_state
    'active'

It is also possible to call member functions directly::

    >>> supermodel.getPhysicalPath()
    ('', 'plone', 'clients', 'client-1')


Not impressed yet?
------------------

Ok, this seems not like a big deal so far, so let's create some more complex
content structure:

Needed Imports::

    >>> from DateTime import DateTime

    >>> from senaite import api
    >>> from bika.lims.utils.analysisrequest import create_analysisrequest

Functional Helpers::

    >>> def timestamp(format="%Y-%m-%d"):
    ...     return DateTime().strftime(format)

Variables::

    >>> date_now = timestamp()
    >>> portal = self.portal
    >>> request = self.request
    >>> setup = portal.bika_setup
    >>> sampletypes = setup.bika_sampletypes
    >>> samplepoints = setup.bika_samplepoints
    >>> analysiscategories = setup.bika_analysiscategories
    >>> analysisservices = setup.bika_analysisservices

Test user::

We need certain permissions to create and access objects used in this test,
so here we will assume the role of Lab Manager.

    >>> from plone.app.testing import TEST_USER_ID
    >>> from plone.app.testing import setRoles
    >>> setRoles(portal, TEST_USER_ID, ['Manager',])

To create a new AR, a `Contact` is needed::

    >>> contact = api.create(client, "Contact", Firstname="Marylin", Surname="Monroe")
    >>> contact
    <Contact at /plone/clients/client-1/contact-1>

A `SampleType` defines how long the sample can be retained, the minimum volume
needed, if it is hazardous or not, the point where the sample was taken etc.::

    >>> sampletype = api.create(sampletypes, "SampleType", Prefix="water", MinimumVolume="100 ml")
    >>> sampletype
    <SampleType at /plone/bika_setup/bika_sampletypes/sampletype-1>

A `SamplePoint` defines the location, where a `Sample` was taken::

    >>> samplepoint = api.create(samplepoints, "SamplePoint", title="Lake Liberty")
    >>> samplepoint
    <SamplePoint at /plone/bika_setup/bika_samplepoints/samplepoint-1>

An `AnalysisCategory` categorizes different `AnalysisServices`::

    >>> analysiscategory = api.create(analysiscategories, "AnalysisCategory", title="Water")
    >>> analysiscategory
    <AnalysisCategory at /plone/bika_setup/bika_analysiscategories/analysiscategory-1>

An `AnalysisService` defines a analysis service offered by the laboratory::

    >>> analysisservice = api.create(analysisservices, "AnalysisService", title="PH", ShortTitle="ph", Category=analysiscategory, Keyword="PH")
    >>> analysisservice
    <AnalysisService at /plone/bika_setup/bika_analysisservices/analysisservice-1>

Finally, the `AnalysisRequest` can be created::

    >>> values = {
    ...     'Client': client.UID(),
    ...     'Contact': contact.UID(),
    ...     'SamplingDate': date_now,
    ...     'DateSampled': date_now,
    ...     'SampleType': sampletype.UID(),
    ...     'Priority': '1',
    ... }

    >>> service_uids = [analysisservice.UID()]
    >>> ar = create_analysisrequest(client, request, values, service_uids)
    >>> ar
    <AnalysisRequest at /plone/clients/client-1/water-0001-R01>

Let's give this Analysis Request now super powers and wrap it into a `SuperModel`::

    >>> supermodel = SuperModel(ar.UID())

Now we try to fetch the client from the AR::

    >>> supermodel.Client
    <SuperModel:UID(...)>

Ok, why did we get another `SuperModel` here?

A `SuperModel` gives transparent access to reference fields and makes it
therefore possible to traverse schema fields from referenced objects directly::

    >>> supermodel.Client.Name
    'Happy Hills'

Furthermore, all fields that were accessed once are internally cached. Another
fetch would therefore return the cached value instead of getting the attribute
from the database object::

    >>> supermodel.Client.data
    {'Name': 'Happy Hills'}

    >>> supermodel.Client.ClientID
    'HH'

    >>> sorted(supermodel.Client.data.items())
    [('ClientID', 'HH'), ('Name', 'Happy Hills')]

A `SuperModel` can also return all content fields as a dictionary::

    >>> data = supermodel.to_dict()

    >>> data.get("ClientTitle")
    'Happy Hills'

    >>> data.get("Priority")
    '1'
