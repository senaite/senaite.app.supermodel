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


Test Setup
----------

Needed Imports:

    >>> import transaction
    >>> from DateTime import DateTime
    >>> from bika.lims import api
    >>> from bika.lims.utils.analysisrequest import create_analysisrequest
    >>> from bika.lims.workflow import doActionFor as do_action_for
    >>> from plone.app.testing import TEST_USER_ID
    >>> from plone.app.testing import TEST_USER_PASSWORD
    >>> from plone.app.testing import setRoles
    >>> from senaite.core.supermodel import SuperModel

Functional Helpers:

    >>> def start_server():
    ...     from Testing.ZopeTestCase.utils import startZServer
    ...     ip, port = startZServer()
    ...     return "http://{}:{}/{}".format(ip, port, portal.id)

    >>> def new_sample(services):
    ...     values = {
    ...         "Client": client.UID(),
    ...         "Contact": contact.UID(),
    ...         "DateSampled": date_now,
    ...         "SampleType": sampletype.UID()}
    ...     service_uids = map(api.get_uid, services)
    ...     sample = create_analysisrequest(client, request, values, service_uids)
    ...     transaction.commit()
    ...     return sample

    >>> def get_analysis(sample, id):
    ...     ans = sample.getAnalyses(getId=id, full_objects=True)
    ...     if len(ans) != 1:
    ...         return None
    ...     return ans[0]


Environment Setup
-----------------

Setup the testing environment:

    >>> portal = self.portal
    >>> request = self.request
    >>> setup = portal.bika_setup
    >>> date_now = DateTime().strftime("%Y-%m-%d")
    >>> date_future = (DateTime() + 5).strftime("%Y-%m-%d")
    >>> setRoles(portal, TEST_USER_ID, ['LabManager', ])
    >>> user = api.get_current_user()


LIMS Setup
----------

Setup the Lab for testing:

    >>> setup.setSelfVerificationEnabled(True)
    >>> analysisservices = setup.bika_analysisservices
    >>> client = api.create(portal.clients, "Client", title="Happy Hills", ClientID="HH")
    >>> contact = api.create(client, "Contact", Firstname="Rita", Lastname="Mohale")
    >>> labcontact = api.create(setup.bika_labcontacts, "LabContact", Firstname="Lab", Lastname="Manager")
    >>> department = api.create(setup.bika_departments, "Department", title="Chemistry", Manager=labcontact)
    >>> sampletype = api.create(setup.bika_sampletypes, "SampleType", title="Water", Prefix="Water")


Content Setup
-------------

Create some Analysis Services with unique Keywords:

    >>> Ca = api.create(analysisservices, "AnalysisService", title="Calcium", Keyword="Ca")
    >>> Mg = api.create(analysisservices, "AnalysisService", title="Magnesium", Keyword="Mg")
    >>> Cu = api.create(analysisservices, "AnalysisService", title="Copper", Keyword="Cu")
    >>> Fe = api.create(analysisservices, "AnalysisService", title="Iron", Keyword="Fe")
    >>> Au = api.create(analysisservices, "AnalysisService", title="Aurum", Keyword="Au")

Create a new Sample:

    >>> sample = new_sample([Cu, Fe, Au])

Get the contained Analyses:

    >>> cu = get_analysis(sample, Cu.getKeyword())
    >>> fe = get_analysis(sample, Fe.getKeyword())
    >>> au = get_analysis(sample, Au.getKeyword())


SuperModel
----------

Now we can simply create a new `SuperModel` instance by passing in the Unique ID
(UID) of a content object, a catalog brain or an instance object.

Now a `SuperModel` can be instantiated via the UID::

    >>> uid = api.get_uid(client)
    >>> supermodel1 = SuperModel(uid)

It can be also instantiated via a catalog brain::

    >>> brain = api.get_brain_by_uid(uid)
    >>> supermodel2 = SuperModel(brain)

And it can be instantiated with the content object directly::

    >>> supermodel3 = SuperModel(client)

All of them create new `SuperModel` instances for us::

    >>> supermodel1
    <SuperModel:UID(...)>

    >>> supermodel2
    <SuperModel:UID(...)>

    >>> supermodel3
    <SuperModel:UID(...)>

All of them should be equal::

    >>> supermodel1 == supermodel2 == supermodel3
    True

We have now full access to the `Client` schema::

    >>> supermodel1.Name
    'Happy Hills'

    >>> supermodel1.ClientID
    'HH'

And the `Client` instance as well as the catalog brain of the primary registered
catalog are lazily fetched::

    >>> supermodel1.instance
    <Client at /plone/clients/client-1>

    >>> supermodel1.brain
    <Products.ZCatalog.Catalog.mybrains object at ...>

This gives full access to the catalog metadata and content schema::

    >>> supermodel1.review_state
    'active'

It is also possible to call member functions directly::

    >>> supermodel1.getPhysicalPath()
    ('', 'plone', 'clients', 'client-1')


SuperModel Interface
--------------------

A `SuperModel` provides more or less the same interface as a standard Python dictionary.

    >>> supermodel = SuperModel(sample)

The `keys` method returns all schema fields of the model:

    >>> supermodel.keys()
    ['id', 'title', ...]

The `values` method returns the values of the fields:

    >>> supermodel.values()
    ['Water-0001', 'Water-0001', ...]

The `get` method allows to retrieve a named value:

    >>> supermodel.get("title")
    'Water-0001'



Lazy Loading
------------

The `SuperModel` retrieves the brain/object only if it is requested:

    >>> supermodel = SuperModel(sample.UID())

Accessing the `brain` property fetches the brain from the right catalog:

    >>> supermodel._brain is None
    True

    >>> supermodel.brain
    <Products.ZCatalog.Catalog.mybrains object at ...>

    >>> supermodel._brain is supermodel.brain
    True

The catalog is automatically set to the primary registered catalog of the ArchetypeTool:

    >>> supermodel.catalog
    <BikaCatalogAnalysisRequestListing at /plone/bika_catalog_analysisrequest_listing>

The instance is not fetched yet:

    >>> supermodel._instance is None
    True

But as soon as we access the instance property, it will be waked up:

    >>> supermodel.instance
    <AnalysisRequest at /plone/clients/client-1/Water-0001>

    >>> supermodel._instance is supermodel.instance
    True


Cleanup
-------

Each `SuperModel` cleans up after itself:

    >>> supermodel1 = SuperModel(sample)
    >>> supermodel2 = SuperModel(sample)

    >>> supermodel1.instance
    <AnalysisRequest at /plone/clients/client-1/Water-0001>

    >>> supermodel2.instance
    <AnalysisRequest at /plone/clients/client-1/Water-0001>

Deleting the `SuperModel` will trigger the destrucotr:

    >>> del supermodel1

The wrapped instance object gets ghosted if it was not modified:_

    >>> sample._p_state == -1
    True

And reactivated (loaded into memory) if it is accessed again:

    >>> supermodel2.get("title")
    'Water-0001'

    >>> sample._p_state == 0
    True


Not impressed yet?
------------------

Let's give our previous created Sample super powers and wrap it into a `SuperModel`:

    >>> supermodel = SuperModel(sample)

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
    '3'
