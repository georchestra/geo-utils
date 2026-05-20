import lxml.etree as ET
from datetime import date


class ThesaurusKeyword:
    def __init__(
        self,
        concept=None,
        keyword=None,
        thesaurus_shortlink=None,
        thesaurus_url=None,
        thesaurus_title=None,
        thesaurus_key=None,
    ):
        self.concept = concept
        self.keyword = keyword
        self.thesaurus_url = thesaurus_url
        self.thesaurus_shortlink = thesaurus_shortlink
        self.thesaurus_title = thesaurus_title
        self.thesaurus_key = thesaurus_key

    def tostring(self):
        return f"{self.concept},{self.keyword},{self.thesaurus_url},{self.thesaurus_shortlink},{self.thesaurus_title},{self.thesaurus_key}"

    # load from result from GN_API get_thesaurus_dict function
    def load_from_json_get_thesaurus_dict(self, json):
        self.thesaurus_key = json["key"]
        self.thesaurus_title = json["title"]
        self.thesaurus_url = json["url"]
        self.thesaurus_shortlink = json["url"].rpartition("/")[0] + "/"

    def load_from_json_search_thesaurus_dict(self, json):
        self.concept = json["uri"]
        self.keyword = json["value"]
        self.thesaurus_key = json["thesaurusKey"]

    def to_xml(self):
        return f"""<mri:descriptiveKeywords
                    xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0"
                    xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/2.0"
                    xmlns:mrs="http://standards.iso.org/iso/19115/-3/mrs/1.0"
                    xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0"
                    xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0"
                    xmlns:gcx="http://standards.iso.org/iso/19115/-3/gcx/1.0"
                    xmlns:xlink="http://www.w3.org/1999/xlink">
                    <mri:MD_Keywords>
                        <mri:keyword>
                            <gcx:Anchor xlink:href="{self.concept}">{self.keyword}</gcx:Anchor>
                        </mri:keyword>
                        <mri:type>
                            <mri:MD_KeywordTypeCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_KeywordTypeCode" codeListValue="theme"/>
                        </mri:type>
                        <mri:thesaurusName>
                            <cit:CI_Citation
                                xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/2.0">
                                <cit:title>
                                    <gcx:Anchor xlink:href="{self.thesaurus_shortlink}">{self.thesaurus_title}</gcx:Anchor>
                                </cit:title>
                                <cit:date>
                                    <cit:CI_Date>
                                        <cit:date>
                                            <gco:Date>{date.today()}</gco:Date>
                                        </cit:date>
                                        <cit:dateType>
                                            <cit:CI_DateTypeCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode" codeListValue="publication"/>
                                        </cit:dateType>
                                    </cit:CI_Date>
                                </cit:date>
                                <cit:identifier>
                                    <mcc:MD_Identifier>
                                        <mcc:code>
                                            <gcx:Anchor xlink:href="{self.thesaurus_url}">{self.thesaurus_key}</gcx:Anchor>
                                        </mcc:code>
                                    </mcc:MD_Identifier>
                                </cit:identifier>
                            </cit:CI_Citation>
                        </mri:thesaurusName>
                    </mri:MD_Keywords>
                </mri:descriptiveKeywords>
            """


class Metadata:
    def __init__(self, xml_string: str = ""):
        try:
            self.meta = ET.fromstring(xml_string.encode("utf-8"))
            # reading ns from xml and create ns = { "gco": "http://standards.iso.org/iso/19115/-3/gco/1.0",...etc}
            self.ns = self._get_dynamic_namespaces()
        except Exception as e:
            self.meta = None

    def _get_dynamic_namespaces(self) -> dict:
        """
        Explore XML to get all namespace
        """
        namespaces = {}
        for prefix, uri in self.meta.xpath("//namespace::*"):
            if prefix is None:
                namespaces["default"] = uri
            else:
                namespaces[prefix] = uri
        return namespaces

    def to_string(self):
        if self.meta is not None:
            return ET.tostring(self.meta, pretty_print=True, encoding="unicode")
        else:
            return ""

    def save_into_file(self, filename_path):
        with open(filename_path, "w") as f:
            f.write(self.to_string())

    def load_from_file(self, filename_path):
        with open(filename_path, "r", encoding="utf-8") as f:
            meta_xml = f.read()
        self.meta = ET.fromstring(meta_xml.encode("utf-8"))
        self.ns = self._get_dynamic_namespaces()

    def add_thesaurus_to_metadata(self, thesaurus: ThesaurusKeyword):
        if self.meta is not None:
            xpath = "/mdb:MD_Metadata/mdb:identificationInfo/mri:MD_DataIdentification"
            # "/mdb:MD_Metadata/mdb:identificationInfo/mri:MD_DataIdentification/mri:descriptiveKeywords[4]"
            elements = self.meta.xpath(xpath, namespaces=self.ns)
            if not elements:
                print("XPath Not found")
            else:
                fragment_to_add = ET.fromstring(thesaurus.to_xml())
                if fragment_to_add is not None:
                    target_element = elements[0]
                    target_element.append(fragment_to_add)
                else:
                    print("Unable to load thesaurus")
        else:
            print("Error meta object not loaded")

    def apply_xslt_tranformation(self, xsl_path):
        pass

    def search_and_replace(self, search, replace):
        pass

    def append_value_xpath(self, xpath, value):
        pass

    def update_value_xpath(self, xpath: str, value: str = ""):
        if self.meta is not None:
            elements = self.meta.xpath(xpath, namespaces=self.ns)
            if not elements:
                print(f"XPath Not found: {xpath}")
                return
            target_element = elements[0]
            try:
                fragment_to_add = ET.fromstring(value)
                parent = target_element.getparent()
                if parent is not None:
                    target_element.addnext(fragment_to_add)
                    parent.remove(target_element)
                    print("Okay good")
                else:
                    print("Can't replace parent, because it is the root")

            except Exception as e:
                # mean not xml content of value
                target_element.text = value
                # clearing childrens
                for child in target_element.getchildren():
                    target_element.remove(child)
                print("Okay good")


if __name__ == "__main__":
    from gn_api import GN_API

    gn = GN_API(
        server="http://localhost:8080", username="testadmin", password="testadmin"
    )
    geo = gn.get_thesaurus_dict("local.theme.geographie-ofb")
    mayotte = gn.searchin_thesaurus_dict(keyword="Mayotte")[0]

    meta = Metadata()
    meta.load_from_file("./sample_meta2.xml")
    t = ThesaurusKeyword()
    t.load_from_json_get_thesaurus_dict(geo)
    t.load_from_json_search_thesaurus_dict(mayotte)

    meta.add_thesaurus_to_metadata(t)
    # meta.update_value_xpath(xpath="/mdb:MD_Metadata/mdb:identificationInfo/mri:MD_DataIdentification/mri:citation/cit:CI_Citation/cit:identifier/mcc:MD_Identifier/mcc:code",
    #                         value='<gco:CharacterString xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0" >mdlkfsdmflkdsftest</gco:CharacterString>')
    meta.update_value_xpath(
        xpath="/mdb:MD_Metadata/mdb:identificationInfo/mri:MD_DataIdentification/mri:citation/cit:CI_Citation/cit:identifier/mcc:MD_Identifier/mcc:code/gco:CharacterString",
        value="testnewidentifier",
    )
    meta.save_into_file("./sample_meta3.xml")
