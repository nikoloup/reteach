import sys
import jinja2
import zipfile

def create_moodle_zip(course, out_name):
    xml_template = jinja2.Template(open('moodle.xml.template', 'r').read())

    moodle_xml_str = xml_template.render(course=course)

    moodle_zip = zipfile.ZipFile(out_name, 'w')

    moodle_zip.writestr('moodle.xml', moodle_xml_str)

    moodle_zip.close()