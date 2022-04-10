# encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from bs4 import BeautifulSoup as bs
import urllib.request
from transformers import pipeline as pipe

from github_issue import make_github_issue
from config import NEW_SUB_URL, KEYWORD_LIST


class Model:
#     def __init__(self, model_path):
    def __init__(self):
        self.summarizer = pipe("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text: str):
        return self.summarizer(text, max_length=200)


def main():
    model = Model()
    
    page = urllib.request.urlopen(NEW_SUB_URL)
    soup = bs(page)
    content = soup.body.find("div", {'id': 'content'})

    issue_title = content.find("h3").text
    dt_list = content.dl.find_all("dt")
    dd_list = content.dl.find_all("dd")
    arxiv_base = "https://arxiv.org/abs/"

    assert len(dt_list) == len(dd_list)

    keyword_list = sorted(KEYWORD_LIST)
    keyword_dict = {key: [] for key in keyword_list}

    for i in range(len(dt_list)):
        paper = {}
        paper_number = dt_list[i].text.strip().split(" ")[2].split(":")[-1]
        paper['main_page'] = arxiv_base + paper_number
        paper['pdf'] = arxiv_base.replace('abs', 'pdf') + paper_number

        paper['title'] = dd_list[i].find("div", {"class": "list-title mathjax"}).text.replace("Title: ", "").strip()
        paper['authors'] = dd_list[i].find("div", {"class": "list-authors"}).text.replace("Authors:\n", "").replace(
            "\n", "").strip()
        paper['subjects'] = dd_list[i].find("div", {"class": "list-subjects"}).text.replace("Subjects: ", "").strip()
        paper['abstract'] = dd_list[i].find("p", {"class": "mathjax"}).text.replace("\n", " ").strip()
        paper['tldr'] = model.summarize(paper['abstract'])

        for keyword in keyword_list:
            if keyword.lower() in paper['abstract'].lower():
                keyword_dict[keyword].append(paper)

    full_report = ''
    for keyword in keyword_list:
        # full_report = full_report + '## Keyword: ' + keyword + '\n'
        full_report = full_report + '<h2>Keyword: ' + keyword + '</h2>'

        if len(keyword_dict[keyword]) == 0:
            full_report = full_report + 'There is no result <br>'
        else:
            full_report = full_report + "<details>"
            for paper in keyword_dict[keyword]:
                # report = '### {}\n - **Authors:** {}\n - **Subjects:** {}\n - **Arxiv link:** {}\n - **Pdf link:** {}\n - **Abstract**\n {}' \
                #     .format(paper['title'], paper['authors'], paper['subjects'], paper['main_page'], paper['pdf'],
                #             paper['abstract'])
                report = f"<h3>{paper['title']}</h3>\
                    <strong>Authors:</strong> {paper['authors']}<br>\
                    <strong>Subjects:</strong> {paper['subjects']}<br>\
                    <strong>Arxiv:</strong> <a href='{paper['main_page']}'>{paper['main_page']}</a><br>\
                    <strong>PDF:</strong> <a href='{paper['pdf']}'>{paper['pdf']}</a><br>\
                    <strong>Abstract:</strong> {paper['abstract']}<br>\
                    <strong>TLDR:</strong> {paper['tldr']}"
                full_report = full_report + report + '<br>'
            full_report = full_report + "</details>"

    # Authentication for user filing issue (must have read/write access to repository to add issue to)
    if 'GITHUB' in os.environ:
        USERNAME, TOKEN = os.environ['GITHUB'].split(',')
    make_github_issue(title=issue_title, body=full_report, assignee=USERNAME, TOKEN=TOKEN, labels=keyword_list)


if __name__ == '__main__':
    main()
