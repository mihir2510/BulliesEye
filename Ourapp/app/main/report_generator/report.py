from docxtpl import DocxTemplate
import os

def find_context():

    return {
        'name': 'Kaustubh Damania',
        'sign': 'K.D.',
        'date': '13-02-2019',
        'list_criminals': 'Kunal Sonawane, Anay Kulkarni, etc.',
        'desc': 'Just a Twitter URL here!!!!',
        'witnesses': 'Mihir Gada, Fatema Motiwala',
        'reported_to': 'admin',
        'reporting_date': '13-02-2019',
        'actions': 'null'
    }

def fill_jinja(input_file, output_file, context):
    doc = DocxTemplate(input_file)
    # context = find_context()
    doc.render(context)
    doc.save(output_file)

if __name__ == '__main__':
    fill_jinja('report_template.docx', 'newreport.docx', find_context())
