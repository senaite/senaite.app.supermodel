2.6.0 (2025-04-04)
------------------

- #25 Compatibility with core#2584 (SampleType to DX)
- #24 Do not take IARAnalysesField as a uidreference-like field
- #23 Rely on getRaw for the retrieval of UIDs from reference-like fields
- #21 Fix error when using Title() or Description() on DX-based types
- #20 Special handling of title and description attributes
- #19 Prioritize getters instead of fieldnames on value retrieval from instance


2.5.0 (2024-01-03)
------------------

- #18 Avoid brain lookup for temporary objects
- #17 Do not fail when no catalog brain was found


2.4.0 (2023-03-10)
------------------

- Version 2.3.0 -> 2.4.0


2.3.0 (2022-10-03)
------------------

- #14 Ignore fields from extensible metadata schema
- #13 Remove dependency to Products.TextIndexNG3 (test layer)


2.2.0 (2022-06-10)
------------------

- #12 Fix infinite recursion for catalog values containing `Missing.Value`


2.1.0 (2022-01-05)
------------------

- #11 Do not consider Auditlog catalog as primary catalog


2.0.0 (2021-07-26)
------------------

- Version bump


2.0.0rc3 (2021-01-04)
---------------------

- Version bump


2.0.0rc2 (2020-10-13)
---------------------

- Version bump


2.0.0rc1 (2020-08-05)
---------------------

- Compatibility with `senaite.core` 2.x


1.2.4 (2020-08-04)
------------------

- version bump


1.2.3 (2020-03-02)
------------------

- #10 Fix API import


1.2.2 (2020-03-01)
------------------

- #9 Support Dexterity Fields


1.2.1 (2019-07-01)
------------------

- #8 Do not process "0" values to Portal-SuperModels
- #7 Fix traceback when initializing a supermodel with a catalog brain
- #6 Added Destructor and further improvements
- #5 Fix UID->SuperModel conversion of UIDReferenceFields
- #4 Skip private fields starting with `_`


1.2.0 (2019-03-30)
------------------

- Compatibility release for SENAITE CORE 1.3.0


1.1.0 (2018-10-04)
------------------

- #2 Allow to pass in a catalog brain or instance to initialize a SuperModel


1.0.0 (2018-07-19)
------------------

- Initial Release
