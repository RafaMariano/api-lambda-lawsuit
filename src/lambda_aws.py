import boto3
from bs4 import BeautifulSoup
import base64
import magic
import uuid
import re

BUCKET_NAME = 'data-analysis-files'
DIR_PATH = 'html-files'


def save_html(file_content):
    if magic.from_buffer(file_content, mime=True) != 'text/html':
        raise Exception('File is not HTML type')

    try:
        s3 = boto3.client('s3')

        while True:
            file_name = str(uuid.uuid4()) + ".html"
            file_path = DIR_PATH + "/" + file_name
            response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=file_path)

            if response.get('KeyCount', 0) == 0:
                break

        s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=file_content)

    except Exception as e:
        raise Exception(e)

    return file_name


def get_process_data(html):
    process_data = html.body.find('table', attrs={'id': '', 'class': 'secaoFormBody'}).text

    regex_groups = re.search('\s+Processo:\s+(.+?)\s+.+?\s+Classe:\s+(.+?(\s.+?)*)\s+Área:\s+(.+?)'
                             '(\s+(?:(?!Juiz:).+?))*\s+Juiz:\s+(.*)(\s+(?:(?!Valor\sda\sação:).+?))*\s+'
                             'Valor\sda\sação:\s+(.+?)\s+([0-9]+(\.|,*[0-9])*)', process_data)

    return {'process_number': regex_groups.group(1),
            'class': {
                'type': regex_groups.group(2),
                'area': regex_groups.group(4)
            },
            'judge': regex_groups.group(6).title(),
            'value': regex_groups.group(8) + " " + regex_groups.group(9)
            }


def get_process_parts(html):
    process_parts = html.body.find('table', attrs={'id': 'tablePartesPrincipais'})
    attrs_process_parts = process_parts.findAll('tr', attrs={'class': 'fundoClaro'})

    json_process_parts = {}
    for tr in attrs_process_parts:
        regex_groups = re.findall('\s+(.+?):\s+(.*)', tr.text)
        json = {'name': regex_groups[0][1]}

        lawyer = []
        for attr in regex_groups[1:]:
            lawyer.append(attr[1].title().replace(u'\xa0', u''))

        json['Advogad(a/o)'] = lawyer
        json_process_parts[regex_groups[0][0]] = json

    return json_process_parts


def get_last_move(html):
    last_move = html.body.find('tbody', attrs={'id': 'tabelaUltimasMovimentacoes'})
    first_element_of_last_move = last_move.find('tr', attrs={'class': 'fundoClaro'})

    regex_groups = re.search('\s*([0-9]+/[0-9]+/[0-9]+)\s*(.*)\s*"*([^<]*[^\n\t\"])', first_element_of_last_move.text)

    return {'date': regex_groups.groups(1)[0],
            'movement': regex_groups.groups(1)[1],
            'info': regex_groups.groups(1)[2].replace('\n', ' ').replace('  ', ' ')
            }


def insert_data(html_data):
    try:
        dynamodb = boto3.resource('dynamodb')
        data_analysis_table = dynamodb.Table('data-analysis-html')
        data_analysis_table.put_item(Item=html_data)

    except Exception as e:
        raise Exception(e)


def lambda_handler(event, context):
    try:
        file_content = base64.b64decode(event['content'])
        id_html = save_html(file_content)

        parsed_html = BeautifulSoup(file_content, features="html.parser")

        json = {'html_file_name': id_html,
                'data': {
                    'process_data': get_process_data(parsed_html),
                    'process_parts': get_process_parts(parsed_html),
                    'last_movement': get_last_move(parsed_html)
                }}

        insert_data(json)
        return json

    except Exception as e:
        return {'statusCode': 500,
                'message': str(e)
                }

