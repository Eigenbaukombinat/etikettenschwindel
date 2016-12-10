import odf.userfield
import os.path
import tempfile
import shutil
import json
import subprocess

from flask import Flask, render_template, request

app = Flask(__name__)


with open('config.json') as configfile:
    CONFIG = json.loads(configfile.read())

_TEMPLATES_MAP = {}
for template in CONFIG['templates']:
    _TEMPLATES_MAP[template['id']] = template


def clean_newlines(value):
    return value.replace('\r', '')


FILTERS = [clean_newlines]


def apply_filters(data):
    for key, value in data.items():
        for filter_func in FILTERS:
            data[key] = filter_func(value)


def fill_template(template_filename, tempdir, data):
    apply_filters(data)
    output_path = os.path.join(tempdir, 'output.odt')
    with open(template_filename, 'rb') as template_file:
        with open(output_path, 'wb') as output_file:
            converter = odf.userfield.UserFields(template_file, output_file)
            converter.update(data)
    return output_path


def map_types(type_):
    if type_ == 'string':
        return 'text'
    raise ValueError("Unsupported Field Type: %s" % type_)


def get_fields(template_id):
    fields = []
    template_filename = _TEMPLATES_MAP[template_id]['template']
    with open(template_filename, 'rb') as template_file:
        converter = odf.userfield.UserFields(template_file, None)
        for fieldname, type_, value in converter.list_fields_and_values():
            fields.append(dict(id=fieldname, inputtype=map_types(type_),
                value=value))
    return fields


def preview_doc(template_filename, data):
    tempdir = tempfile.mkdtemp()
    output_path = fill_template(template_filename, tempdir, data)
    subprocess.call([
        CONFIG['soffice'], '--invisible', '--norestore', '--headless',
        '--convert-to', 'jpg',
        '--outdir',  tempdir, output_path])
    imgfile = os.path.join(tempdir, 'output.jpg')    
    if not os.path.isfile(imgfile):
        raise ValueError('Output from soffice not found. Make sure soffice '
            'is not already running.')
    with open(imgfile, 'rb') as img:
        preview_contents = img.read()
    shutil.rmtree(tempdir)
    return preview_contents


def print_doc(template_id, data, printer_name):
    tempdir = tempfile.mkdtemp()
    template_filename = _TEMPLATES_MAP[template_id]['template']
    pagesize = _TEMPLATES_MAP[template_id]['pagesize']
    output_path = fill_template(template_filename, tempdir, data)
    subprocess.call([
        CONFIG['soffice'], '--invisible', '--norestore', '--headless',
        '--print-to-file', '-printer-name', printer_name,
        '--outdir',  tempdir, output_path])

    ps_file = os.path.join(tempdir, 'output.ps')
    if not os.path.isfile(ps_file):
        raise ValueError('Output from soffice not found. Make sure soffice '
            'is not already running.')
    subprocess.call([
        CONFIG['lpr'], '-P', printer_name, '-o', 'PageSize=%s' % pagesize, ps_file])
    shutil.rmtree(tempdir)



@app.route('/')
def index():
    return render_template('index.html', templates=CONFIG['templates'])

@app.route('/template/<template_id>')
def use_template(template_id):
    if 'print' in request.args:
        print_doc(template_id, to_dict(request.args), CONFIG['printer'])
    return render_template('use_template.html', template_id=template_id,
        fields=get_fields(template_id), data=request.args,
        query_string=request.query_string)


def to_dict(args):
    outdict = {}
    for key, val in args.items():
        outdict[key] = val
    return outdict

@app.route('/preview/<template_id>/preview.jpg')
def preview_label(template_id):
    preview_contents = preview_doc(_TEMPLATES_MAP[template_id]['template'],
        to_dict(request.args))
    return preview_contents
