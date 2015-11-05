"""
    Unit tests for all fields in the parser, for multiple IATI versions.
"""

import copy
import datetime
from django.core import management

from django.test import TestCase as DjangoTestCase # Runs each test in a transaction and flushes database
from unittest import TestCase

from lxml import etree
from lxml.builder import E

from iati.iati_parser import ParseIATI

from iati_synchroniser.models import IatiXmlSource, Publisher
import iati.models as iati_models
import iati_codelists.models as codelist_models
import organisation.models as org_models
from geodata.models import Country

from iati.IATI_1_03 import Parse as Parser_103
from iati.IATI_1_05 import Parse as Parser_105
from iati.IATI_2_01 import Parse as Parser_201
from organisation.organisation_2_01 import Parse as OrgParse_201
from organisation.organisation_1_05 import Parse as OrgPArse_105


def build_xml(version, organisation_identifier):
    """
        Construct a base activity file to work with in the tests
    """

    activities_attrs = { "generated-datetime": datetime.datetime.now().isoformat(),
        "version": version,

    }

    activity = E("iati-organisations",
        **activities_attrs
    )

    return activity

# def create_dummy_source(url, title, name, current_publisher, cur_type):
#     source = IatiXmlSource(
#         ref=name,
#         title=title,
#         publisher=current_publisher,
#         source_url=url,
#         type=cur_type)

#     source.save(process=False, added_manually=False)
#     return source

def copy_xml_tree(tree):
    return copy.deepcopy(tree)

def print_xml(elem):
    print(etree.tostring(elem, pretty_print=True))


def setUpModule():
    fixtures = ['test_publisher.json', 'test_codelists.json', 'test_vocabulary', 'test_geodata.json']

    for fixture in fixtures:
        management.call_command("loaddata", fixture)

def tearDownModule():
    management.call_command('flush', interactive=False, verbosity=0)

class ParserSetupTestCase(DjangoTestCase):

    # fixtures = ['test_publisher.json', 'test_codelists.json', 'test_vocabulary', 'test_geodata.json']

    def _get_organisation(self, iati_identifier):
        return org_models.Organisation.objects.get(id=iati_identifier)

    @classmethod
    def setUpClass(self):
        # for fixture in self.fixtures:
        #     management.call_command("loaddata", fixture)

        self.iati_identifier = "NL-KVK-51018586-0666"
        self.alt_iati_identifier = "NL-KVK-51018586-0667"

        self.iati_103 = build_xml("1.03", self.iati_identifier)
        self.iati_104 = build_xml("1.04", self.iati_identifier)
        self.iati_105 = build_xml("1.05", self.iati_identifier)
        self.iati_201 = build_xml("2.01", self.iati_identifier)


        dummy_source = IatiXmlSource.objects.get(id=2)

        parseIati = ParseIATI()
        self.parser_103 = parseIati.prepare_parser(self.iati_103, dummy_source)
        self.parser_104 = parseIati.prepare_parser(self.iati_104, dummy_source)
        self.parser_105 = parseIati.prepare_parser(self.iati_105, dummy_source)
        self.parser_201 = parseIati.prepare_parser(self.iati_201, dummy_source)

        assert(isinstance(self.parser_103, OrgPArse_105))
        assert(isinstance(self.parser_104, OrgPArse_105))
        assert(isinstance(self.parser_105, OrgPArse_105))
        assert(isinstance(self.parser_201, OrgParse_201))

        # todo: self.assertTrue source was handled appropriately
        # self.self.assertTrueEqual(self.parser_103.iati_source, self.parser_104.iati_source, self.parser_105.iati_source, self.parser_201.iati_source)

    @classmethod
    def tearDownClass(self):
        pass


class OrganisationTestCase(ParserSetupTestCase):
    """
    iati_activities__iati_activity
    CHANGELOG
    2.01: The version attribute was removed.
    1.02: Introduced the linked-data-uri attribute on iati-activity element
    """
    def setUp(self):
        self.iati_201 = copy_xml_tree(self.iati_201)

        # sample attributes on iati-activity xml
        self.attrs = {
            # "xml:lang": "en",
            "default-currency": "USD",
            "last-updated-datetime": datetime.datetime.now().isoformat(' '),
        }

        # default activity model fields
        self.defaults = {
            "hierarchy": 1,
            "default_lang": "en",
        }

        self.test_parser = self.parser_105
        iati_organisation = E("iati-organisation", **self.attrs)
        iati_organisation.append(E("organisation-identifier", self.iati_identifier))
        self.iati_201.append(iati_organisation)
        self.iati_201.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = "en" # ISO 639-1:2002
        # print(etree.tostring(self.iati_201, pretty_print=True))

        organisation = org_models.Organisation(iati_version_id="2.01")
        self.parser_201.register_model('Organisation', organisation)



    '''attributes:
    		'default-currency':'EUR',
		'last-updated-datetime':'2014-09-10T07:15:37Z',
		'{http://www.w3.org/XML/1998/namespace}lang':'en',

    tag:iati-organisation
    '''
    def test_iati_organisations__iati_organisation(self):
        attribs = {
        		'default-currency':'EUR',
		'last-updated-datetime':'2014-09-10T07:15:37Z',
		'{http://www.w3.org/XML/1998/namespace}lang':'en',

        }
        element = E('iati-organisation',E('iati-identifier','AA-AAA-123456789',{}),attribs)

        self.test_parser.iati_organisations__iati_organisation(element)
        org = self.test_parser.get_model('Organisation')
        """:type : org_models.Organisation """
        self.assertEqual(org.code,'AA-AAA-123456789')
        currency = self.test_parser.get_or_none(codelist_models.Currency, code=element.attrib.get('default-currency'))
        language = self.test_parser.get_or_none(codelist_models.Language, code='en')
        self.assertEqual(org.default_currency , currency)
        self.assertEqual(org.default_lang,language)
        self.assertEqual(org.last_updated_datetime,self.test_parser.validate_date(element.attrib.get('last-updated-datetime')))
        self.assertEqual(org.code,"AA-AAA-123456789")


        #assert








    '''attributes:

    tag:name
    '''
    def test_iati_organisations__iati_organisation__name(self):
        attribs = {

        }
        element = E('name','test narrative name',attribs)
        self.test_parser.iati_organisations__iati_organisation__name(element)
        org = self.test_parser.get_model('Organisation')
        """:type : org_models.Organisation """
        attribs = {

        }
        model = self.test_parser.get_model('NameNarrative')
        """ :type : org_models.Narrative """
        self.assertEqual('test narrative name',model.content)
        #assert



        #assert



