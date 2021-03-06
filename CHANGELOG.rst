Changelog
#########

0.2.6
-----

* Add an external_pdf_url field to the Article model
* Update the ``import_journals_from_fedora`` command to be able to import UNB journals, issues and articles

0.2.5
-----

* Add a website URL field to the Journal model

0.2.4
-----

* Add OAI datestamp fields to the Journal, Issue and Article models
* Increase localidentifiers' max length
* Increase Person's firstname/lastname max lengths
* Remove unused ``Journal.formely`` field (its equivalent is the ``Journal.previous_journal`` field)
* Add managers to retrieve Journal/Issue/Article instances without external URLs
* Update the ``import_journals_from_oai`` command in order to import issues and articles

0.2.3
-----

* Fix: increase the maximum length of the Affiliation model's name field

0.2.2
-----

* Add a ``copyrights`` ManyToManyField on the Article model
* Update the ``import_journals_from_fedora`` management command to import article copyrights

0.2.1
-----

* Add an Affiliation model and associates it to the Person abstract model through a ManyToManyField
* Update the ``import_journals_from_fedora`` management command to import affiliations
* Add new model admin classes

0.2.0
-----

* Add new fields to the Journal, Issue and Article models in order to limit interactions with Fedora
* Fix an error that occured when importing cultural journals without codes
* Improve error handling of the ``import_journals_from_fedora`` command
* Fix importation of journals without OAISET_INFO datastream

0.1.19
------

* Add a ``othername`` field on on the ``Person`` model
* Add a ``letter_prefix`` property on the ``Person`` model
* Add a ``full_name`` property on the ``Person`` model
* Fix article authors importation

0.1.18
------

* Improve Journal code uniqueness logic in import_journals_from_fedora command

0.1.17
------

* Ensure that the Journal code is unique when importing journals from Fedora

0.1.16
------

* Add a way to know the year coverage of journals for open access issues
* Simplifies open access definition on ``Journal`` and ``Issue`` models
* Add a way to import the ISSN print / ISSN web when using the ``import_journals_from_fedora`` command
* The ``Issue.year`` is now required
* Remove unused ``last_oa_issue`` property
* Fix the use issues' publication year when computing movable limitations

0.1.15
------

* Replace ``previous_code`` / ``next_code`` Journal fields by foreign keys

0.1.14
------

* Add ``volume_slug`` property on the ``Issue`` model that can be used in URL patterns

0.1.13
------

* Add a way to detect inexistant datastream on Fedora objects when accessing file contents using the ``FedoraFileDatastreamView``

0.1.12
------

* Add a way to store previous/next journals in Journal instances

0.1.11
------

* Ensure that issues without number or volume can always have a title
* Add a way to get issue titles including first page and last page

0.1.10
------

* Fix an ``AttributeError`` that occured when fetching image information associated with Fedora articles

0.1.9
-----

* Add polymorphism to the ``EruditDocument`` model

0.1.8
-----

* Fix ``setup`` module

0.1.7
-----

* Simplify the journal providers settings and replace them by a single ``JOURNAL_PROVIDERS`` setting
* Add the ``Thesis`` model
* Add the ``import_theses_from_oai`` command
* Add a ``logo`` field to the ``Collection`` model
* Fix the ``has_coverpage`` property on the ``Issue`` model

0.1.6
-----

* Adds a ``publication_allowed_by_authors`` field on the ``Article`` model
* Fixed an error occuring when searching for Journal instances through the Django admin

0.1.5
-----

* Improve the ``has_coverpage`` property when the Fedora repository is not available

0.1.4
-----

* Adds a ``thematic_issue`` field to the ``Issue`` model and update the ``import_journals_from_fedora`` command
* Adds a ``has_coverpage`` property on the ``Issue`` model

0.1.3
-----

* Adds a ``type`` field to the ``Article`` model and update the ``import_journals_from_fedora`` command
* Remove old ``get_absolute_url`` methods

0.1.2
-----

* Adds a DisciplineFatory to test disciplines

0.1.1
-----

* Adds a SizeConstrainedImageField model field to define ImageField fields with size and dimensions constraints
* Forces Organisation.badge images to be redimensioned to 140x140 pixels
* Add a missing migration related to the deletion of the Event model
