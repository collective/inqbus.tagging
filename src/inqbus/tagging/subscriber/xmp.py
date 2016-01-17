import lxml.etree as ET
import re


def searchXMLContent(image_data) :
    """
    Extract the XMP content from the byte stream, using a regular expression search
    @param image_data: byte stream of the image content
    @return: RDF data as a string
    @rtype: string
    """
    rdfpat = r"(?sm)^.*(<rdf:RDF.*</rdf:RDF>)"
    r_rdf = re.compile(rdfpat)
    q = r_rdf.search(image_data)
    if q:
        return q.group(1)
    return ""



def parse(image_data):

#    image_data = open("/home/volker/Downloads/view").read()
#    image_data = open("/picture_store/bilder/2015/2015_01_10_intronisationsfeier_FCH/very_best/small/small_IMG_5097.jpg").read()

    xml = searchXMLContent(image_data)
    if not xml:
        return {}

    # parse the XMP portion of the image data
    root = ET.fromstring(xml)

    result = {}
    # find all top level elements
    for tag in root[0].findall("./*"):
        # check if the tag contains a tuple
        sub_tags = tag.findall(".//rdf:Bag/rdf:li", namespaces=tag.nsmap)
        # if we have subtags put them into a list
        if sub_tags:
            sub_tags_result = [sub_tag.text for sub_tag in sub_tags]
            result[tag.tag] = sub_tags_result
        else:
            result[tag.tag] = tag.text

    return result