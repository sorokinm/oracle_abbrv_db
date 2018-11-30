import requests
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import itertools
import codecs
import pickle


def get_html_from_sokr(additional_path):
    QUERY = 'http://www.sokr.ru'
    r = requests.get(QUERY + additional_path)
    return r.text.replace('<?xml version="1.0" encoding="utf-8"?>\n', '').replace('&nbsp', ' ')


def get_additional_paths_from_html(html):
    return list(set(get_info_by_xpath_form_html(html, '//li[@class="abbr  "]/a/@href')))


def get_info_by_xpath_form_html(html, xpath_query):
    QUERY = 'http://www.sokr.ru'
    response = HtmlResponse(url=QUERY, body=html, encoding='UTF-8')
    return Selector(response=response).xpath(xpath_query).extract()


def generate_abbrvs_of_length(length):
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    return [''.join(tuple) for tuple in itertools.product(list(alphabet), repeat=length)]


def generate_links_to_abbrv_data(abbrv_max_len):
    link_set = set()
    for abbrv_length in range(1, abbrv_max_len):
        for abbrv in generate_abbrvs_of_length(abbrv_length):
            links_l = get_additional_paths_from_html(get_html_from_sokr('/' + abbrv + '/'))
            link_set.update(links_l)
    return link_set


def get_abbrv_from_descr_html(html):
    return get_info_by_xpath_form_html(html, '//h1[@itemprop="term"]/text()')

def get_description(html):
    return get_info_by_xpath_form_html(html, '//dl[re:match(@class, "description *")]/dd/text()')[0]

def get_tag(html):
    l = get_info_by_xpath_form_html(html, '//dl[re:match(@class, "tags *")]/dd/text()')
    if len(l) != 0:
        return l[0]
    else:
        return ""


def get_csv_from_abbrv_info_page(additional_path):
    res_csv = ''
    html = get_html_from_sokr(additional_path)
    descr = get_description(html)
    tag = get_tag(html)
    for abbrv in get_abbrv_from_descr_html(html):
        res_csv += abbrv + "," + descr + "," + tag + ",\n"
    return res_csv


def save_str_to_file(csv, file_name):
    file = codecs.open(file_name, "a", "utf-8")
    file.write(csv)
    file.close()


if __name__ == '__main__':
#    additional_paths = generate_links_to_abbrv_data(3)
#    with open("additional_paths.dump", "wb") as fp:
#        pickle.dump(additional_paths, fp)
    additional_paths = ''
    with open("additional_paths.dump", "rb") as fp:
       additional_paths = pickle.load(fp)

    print("Here!")
    for additional_path in additional_paths:
        csv = get_csv_from_abbrv_info_page(additional_path)
        save_str_to_file(csv, '../../csvs/sokr.csv')
