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
    NAMESPACES = {
        "cat": "http://standards.iso.org/iso/19115/-3/cat/1.0",
        "cit": "http://standards.iso.org/iso/19115/-3/cit/2.0",
        "dqm": "http://standards.iso.org/iso/19157/-2/dqm/1.0",
        "gco": "http://standards.iso.org/iso/19115/-3/gco/1.0",
        "gcx": "http://standards.iso.org/iso/19115/-3/gcx/1.0",
        "gex": "http://standards.iso.org/iso/19115/-3/gex/1.0",
        "gfc": "http://standards.iso.org/iso/19110/gfc/1.1",
        "gmd": "http://www.isotc211.org/2005/gmd",
        "gmi": "http://www.isotc211.org/2005/gmi",
        "gml": "http://www.opengis.net/gml/3.2",
        "gmx": "http://www.isotc211.org/2005/gmx",
        "gsr": "http://www.isotc211.org/2005/gsr",
        "gts": "http://www.isotc211.org/2005/gts",
        "lan": "http://standards.iso.org/iso/19115/-3/lan/1.0",
        "mac": "http://standards.iso.org/iso/19115/-3/mac/2.0",
        "mas": "http://standards.iso.org/iso/19115/-3/mas/1.0",
        "mcc": "http://standards.iso.org/iso/19115/-3/mcc/1.0",
        "mco": "http://standards.iso.org/iso/19115/-3/mco/1.0",
        "mda": "http://standards.iso.org/iso/19115/-3/mda/1.0",
        "mdb": "http://standards.iso.org/iso/19115/-3/mdb/2.0",
        "mdq": "http://standards.iso.org/iso/19157/-2/mdq/1.0",
        "mds": "http://standards.iso.org/iso/19115/-3/mds/2.0",
        "mdt": "http://standards.iso.org/iso/19115/-3/mdt/2.0",
        "mex": "http://standards.iso.org/iso/19115/-3/mex/1.0",
        "mmi": "http://standards.iso.org/iso/19115/-3/mmi/1.0",
        "mpc": "http://standards.iso.org/iso/19115/-3/mpc/1.0",
        "mrc": "http://standards.iso.org/iso/19115/-3/mrc/2.0",
        "mrd": "http://standards.iso.org/iso/19115/-3/mrd/1.0",
        "mri": "http://standards.iso.org/iso/19115/-3/mri/1.0",
        "mrl": "http://standards.iso.org/iso/19115/-3/mrl/2.0",
        "mrs": "http://standards.iso.org/iso/19115/-3/mrs/1.0",
        "msr": "http://standards.iso.org/iso/19115/-3/msr/2.0",
        "srv": "http://standards.iso.org/iso/19115/-3/srv/2.0",
        "xlink": "http://www.w3.org/1999/xlink",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    def __init__(self, xml_string: str = ""):
        self.meta = None
        self.ns = {}
        self._has_wrapper = False
        try:
            self.meta = ET.fromstring(xml_string.encode("utf-8"))
            # reading ns from xml and create ns = { "gco": "http://standards.iso.org/iso/19115/-3/gco/1.0",...etc}
            self.ns = self._get_dynamic_namespaces()
        except ET.XMLSyntaxError:
            # Resolve missing namespaces here.
            parser = ET.XMLParser(recover=True)
            document = ET.fromstring(
                f"<root>{xml_string}</root>".encode("utf-8"), parser=parser
            )
            if document is None or not len(document) or any(
                error.type != ET.ErrorTypes.NS_ERR_UNDEFINED_NAMESPACE
                for error in parser.error_log
            ):
                return
            if (document.text or "").strip() or any(
                (element.tail or "").strip() for element in document
            ):
                return
            namespaces = dict(document.nsmap)
            for element in document.iter():
                if not isinstance(element.tag, str):
                    continue
                local_namespaces = dict(self.NAMESPACES)
                local_namespaces.update(element.nsmap)
                if not element.tag.startswith("{") and ":" in element.tag:
                    prefix, local_name = element.tag.split(":", 1)
                    if prefix not in local_namespaces:
                        return
                    namespaces.setdefault(prefix, local_namespaces[prefix])
                    element.tag = ET.QName(local_namespaces[prefix], local_name).text
                for name, value in list(element.attrib.items()):
                    if not name.startswith("{") and ":" in name:
                        prefix, local_name = name.split(":", 1)
                        if prefix not in local_namespaces:
                            return
                        namespaces.setdefault(prefix, local_namespaces[prefix])
                        del element.attrib[name]
                        element.set(
                            ET.QName(local_namespaces[prefix], local_name), value
                        )
                type_name = element.get(
                    "{http://www.w3.org/2001/XMLSchema-instance}type", ""
                )
                if ":" in type_name:
                    prefix = type_name.split(":", 1)[0]
                    if prefix in local_namespaces:
                        namespaces.setdefault(prefix, local_namespaces[prefix])
            root = ET.Element(document.tag, attrib=document.attrib, nsmap=namespaces)
            root.text = document.text
            root.tail = document.tail
            root.extend(document)
            if len(root) == 1:
                self.meta = ET.fromstring(ET.tostring(root[0], with_tail=False))
            else:
                self.meta = root
                self._has_wrapper = True
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
            document = ET.fromstring(
                ET.tostring(self.meta), parser=ET.XMLParser(remove_blank_text=True)
            )
            if self._has_wrapper:
                return "".join(
                    ET.tostring(element, pretty_print=True, encoding="unicode", with_tail=False)
                    for element in document
                )
            return ET.tostring(document, pretty_print=True, encoding="unicode")
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

    def get_value_xpath(self, xpath, custom_namespaces=None):
        if self.meta is not None:
            if custom_namespaces is None:
                elements = self.meta.xpath(xpath, namespaces=self.ns)
            else:
                elements = self.meta.xpath(xpath, namespaces=custom_namespaces)
            if not elements:
                print(f"XPath Not found: {xpath}")
                return
            return ET.tostring(elements[0], pretty_print=True, encoding="unicode")

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
