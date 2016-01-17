import re

def _searchXMLContent(b) :
        """
        Extract the XMP content from the byte stream, using a regular expression search
        @param b: byte stream of the image content
        @return: RDF data as a string
        @rtype: string
        """
        rdfpat = r"(?sm)^.*(<rdf:RDF.*</rdf:RDF>)"
        r_rdf = re.compile(rdfpat)
        q = r_rdf.search(b)
        assert q != None, "Could not find the XMP content in the file"
        return q.group(1)


import lxml.etree as ET

openfile = open("/picture_store/bilder/2015/2015_01_10_intronisationsfeier_FCH/very_best/small/small_IMG_5097.jpg")
xml = _searchXMLContent(openfile.read())
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

pass
