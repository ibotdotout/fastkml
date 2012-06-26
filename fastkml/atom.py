# -*- coding: utf-8 -*-
"""
KML 2.2 supports new elements for including data about the author and
related website in your KML file. This information is displayed in geo
search results, both in Earth browsers such as Google Earth, and in other
applications such as Google Maps. The ascription elements used in KML
are as follows:

atom:author element - parent element for atom:name
atom:name element - the name of the author
atom:link element - contains the href attribute
href attribute - URL of the web page containing the KML/KMZ file

These elements are defined in the Atom Syndication Format. The complete
specification is found at http://atompub.org.

This library only  implements a subset of Atom that is useful with KML
"""
import logging
logger = logging.getLogger('fastkml.atom')


try:
    from lxml import etree
    LXML = True
except ImportError:
    import xml.etree.ElementTree as etree
    LXML = False


class Link(object):
    """
    Identifies a related Web page. The type of relation is defined by
    the rel attribute. A feed is limited to one alternate per type and
    hreflang.
    <link> is patterned after html's link element. It has one required
    attribute, href, and five optional attributes: rel, type, hreflang,
    title, and length.
    """
    __name__ = 'Link'
    ns = None

    href = None
    # href is the URI of the referenced resource

    rel = None
    # rel contains a single link relationship type.
    # It can be a full URI, or one of the following predefined values
    # (default=alternate):
    # alternate: an alternate representation
    # enclosure: a related resource which is potentially large in size
    # and might require special handling, for example an audio or video
    # recording.
    # related: an document related to the entry or feed.
    # self: the feed itself.
    # via: the source of the information provided in the entry.

    type = None
    # indicates the media type of the resource

    hreflang = None
    # indicates the language of the referenced resource

    title = None
    # human readable information about the link

    lenght = None
    # the length of the resource, in bytes


    def __init__(self, ns=None, href=None, rel=None, type=None,
                hreflang=None, title=None, lenght=None):
        if ns == None:
            self.ns = '{http://www.w3.org/2005/Atom}'
        else:
            self.ns = ns
        self.href = href
        self.rel = rel
        self.type = type
        self.hreflang = hreflang
        self.title = title
        self.lenght = lenght

    def from_string(self, xml_string):
        self.from_element(etree.XML(xml_string))


    def from_element(self, element):
        if self.ns + self.__name__.lower() != element.tag:
            raise TypeError
        else:
            if element.get('href'):
                self.href = element.get('href')
            else:
                logger.critical('required attribute href missing')
                raise TypeError
            if element.get('rel'):
                self.rel = element.get('rel')
            if element.get('type'):
                self.type = element.get('type')
            if element.get('hreflang'):
                self.hreflang = element.get('hreflang')
            if element.get('title'):
                self.title = element.get('title')
            if element.get('lenght'):
                self.rel = element.get('lenght')
            return element

    def etree_element(self):
        element = etree.Element(self.ns + self.__name__.lower())
        if self.href:
            element.set('href', self.href)
        else:
            logger.critical('required attribute href missing')
            raise TypeError
        element.set('rel', self.rel)
        element.set('type', self.type)
        element.set('hreflang', self.hreflang)
        element.set('title', self.title)
        element.set('lenght', self.lenght)

class _Person(object):
    """
    <author> and <contributor> describe a person, corporation, or similar
    entity. It has one required element, name, and two optional elements:
    uri, email.
    """
    ns = None

    name = None
    #conveys a human-readable name for the person.

    uri = None
    #contains a home page for the person.

    email = None
    #contains an email address for the person.

    def __init__(self, ns=None, name=None, uri=None, email=None):
        if ns == None:
            self.ns = '{http://www.w3.org/2005/Atom}'
        else:
            self.ns = ns
        self.name = name
        self.uri = uri
        self. email = email


    def etree_element(self):
        element = etree.Element(self.ns + self.__name__.lower())
        if self.name:
            name = etree.SubElement(element, "%sname" %self.ns)
            name.text = self.name
        else:
            logger.critical('No Name for person defined')
            raise TypeError
        if self.uri:
            #XXX validate uri
            uri = etree.SubElement(element, "%suri" %self.ns)
            uri.text = self.uri
        if self.email:
            #XXX validate email
            email = etree.SubElement(element, "%semail" %self.ns)
            email.text = self.email



    def from_string(self, xml_string):
        self.from_element(etree.XML(xml_string))

    def from_element(self, element):
        if self.ns + self.__name__.lower != element.tag:
            raise TypeError
        else:
            name = element.find('%sname' %self.ns)
            if name is not None:
                self.name = name.text
            uri = element.find('%suri' %self.ns)
            if uri is not None:
                self.uri = uri.text
            email = element.find('%semail' %self.ns)
            if email is not None:
                self.email = email.text


class Author(_Person):
    """ Names one author of the feed/entry. A feed/entry may have
    multiple authors."""
    __name__ = "Author"

class Contributor(_Person):
    """ Names one contributor to the feed/entry. A feed/entry may have
    multiple contributor elements."""
    __name__ = "Contributor"


