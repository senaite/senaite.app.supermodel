Supermodel with Dexterity and Archetypes
========================================

Supermodel provides same behavior regardless of the underlying framework of
the content types, this being Archetypes or Dexterity.

Running this test from the buildout directory:

    bin/test test_doctests -t dx_vs_at

Test Setup
----------

    >>> from bika.lims import api
    >>> from plone.app.testing import TEST_USER_ID
    >>> from plone.app.testing import setRoles
    >>> from senaite.app.supermodel.model import SuperModel
    >>> from senaite.core.catalog import SETUP_CATALOG

Variables:

    >>> portal = self.portal
    >>> request = self.request
    >>> setup = portal.setup
    >>> bika_setup = portal.bika_setup

Test special attrs title and description
----------------------------------------

CamelCase is the convention used for field names in AT content types. The
system automatically generates the accessors for them. As an example, for a
field `CommercialName`, the system generates automagically the accessors
`getCommercialName()` and `setCommercialName()`. This is true for AT types
except for the fields `title` and `description`, that are declared in lowercase
and for which the framework automatically generates the accessors `Title()`
and `Description()`.

On the other hand, snake case is the convention used for field names in DX
content types. However, we use explicit accessors that follow CamelCase
convention to get them. Therefore, if the field name is `commercial_name` we
expect the accessors `getCommercialName()` and `setCommercialName()`. As
for AT types, field `title` and `description` are special and are commonly
accessed with the auto-generated getters `Title()` and `Description()`.

The rule of thumb is that **supermodel must behave like an instance**. This
means, that `model.Title` or `model.Description` must return the methods
instead of the value, while `model.title` and `model.description` should return
the values instead of the functions.

Likewise, `model.getCommercialName` must return the method and `CommercialName`
the value, regardless of the underlying type of the object. Note therefore,
that for a DX type, SuperModel will try first to rely on a getter.

Create one Archetype and one Dexterity objects:

    >>> at = api.create(portal.clients, "Client", title="Archetype object",
    ...                 description="My AT description", ClientID="AT")
    >>> dx = api.create(setup.departments, "Department", title="Dexterity object",
    ...                 description="My DX description", department_id="DX")

    >>> api.is_at_content(at)
    True

    >>> api.is_dexterity_content(dx)
    True

And their SuperModel counterparts:

    >>> at_sm = SuperModel(at)
    >>> dx_sm = SuperModel(dx)

We expect same behavior with `title` and `description` attributes:

    >>> at_sm.title
    'Archetype object'

    >>> at_sm.description
    'My AT description'

    >>> dx_sm.title
    'Dexterity object'

    >>> dx_sm.description
    'My DX description'

And same behavior with `Title` and `Description` getters:

    >>> at_sm.Title()
    'Archetype object'

    >>> at_sm.Title
    <bound method Client.Title of <Client at /plone/clients/client-1>>

    >>> dx_sm.Title()
    'Dexterity object'

    >>> dx_sm.Title
    <bound method Department.Title of <Department at /plone/setup/departments/department-1>>

    >>> at_sm.Description()
    'My AT description'

    >>> at_sm.Description
    <bound method Client.Description of <Client at /plone/clients/client-1>>

    >>> dx_sm.Description()
    'My DX description'

    >>> dx_sm.Description
    <bound method Department.Description of <Department at /plone/setup/departments/department-1>>

While we expect SuperModel to behave the same with fields:

    >>> at_sm.ClientID
    'AT'

    >>> at_sm.getClientID
    <bound method Client.getClientID of <Client at /plone/clients/client-1>>

    >>> at_sm.getClientID()
    'AT'

    >>> dx_sm.department_id
    'DX'

    >>> dx_sm.getDepartmentID
    <bound method Department.getDepartmentID of <Department at /plone/setup/departments/department-1>>

    >>> dx_sm.getDepartmentID()
    'DX'

However, note that for dexterity types, system will rely on a getter if there
is no field set with the given name:

    >>> dx_sm.DepartmentID
    'DX'

Same principles apply when using brains:

    >>> cat = api.get_tool(SETUP_CATALOG)
    >>> brain = cat(UID=dx.UID())[0]
    >>> brain_sm = SuperModel(brain)

    >>> brain_sm.title
    'Dexterity object'

    >>> brain_sm.Title()
    'Dexterity object'

    >>> brain_sm.Title
    <bound method Department.Title of <Department at /plone/setup/departments/department-1>>

    >>> brain_sm.description
    'My DX description'

    >>> brain_sm.Description()
    'My DX description'

    >>> brain_sm.Description
    <bound method Department.Description of <Department at /plone/setup/departments/department-1>>

    >>> brain_sm.department_id
    'DX'

    >>> brain_sm.getDepartmentID
    <bound method Department.getDepartmentID of <Department at /plone/setup/departments/department-1>>

    >>> brain_sm.getDepartmentID()
    'DX'

    >>> brain_sm.DepartmentID
    'DX'
