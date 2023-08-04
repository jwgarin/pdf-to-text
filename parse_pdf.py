import requests
import PyPDF2
import os
import re
import typing
import time


class ParsePDF:
    """Parse PDF contents"""
    def __init__(self, link=None, filename=None, cookies=None, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'}, name='', driver=None):
        self.link = link
        self.filename = filename
        self.cookies = cookies
        self.headers = headers
        self.name = name
        self.driver = driver
    
    def _request(self):
        if self.cookies:
            return requests.get(self.link, cookies=self.cookies, headers=self.headers, stream=True)
        elif self.headers:
            return requests.get(self.link, headers=self.headers, stream=True)
        else:
            return requests.get(self.link, stream=True)

    def get_text(self):
        if self.link:
            try:
                r = self._request()
            except Exception as exc:
                raise Exception('pdf download failed: {} - {}'.format(self.link, str(exc)))
            self.filename = 'tmp.pdf'
            with open(self.filename, 'wb') as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
        else:
            pass
        if os.path.getsize(self.filename) == 0:
            return ''
        with open(self.filename, 'rb') as f:
            f_content = f.read()
            try:
                pdf_idx = f_content[:1000].index(b'%PDF')
            except:
                raise Exception('PDF index not found: {}\n\n{}'.format(self.link, ascii(f_content)))
        with open(self.filename, 'wb') as f:
            f.write(f_content[pdf_idx:])
        pdf_text = ''
        page = 0
        while True:
            with open(self.filename, 'rb') as f:
                pdf_reader = PyPDF2.PdfFileReader(f)
                try:
                    page_obj = pdf_reader.getPage(page)
                except:
                    break
                page_text = page_obj.extractText()
                pdf_text += page_text
            page += 1
        if self.link:
            os.remove(self.filename)
        return pdf_text
