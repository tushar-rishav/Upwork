import lxml.html as PARSER
import openpyxl
from requests import Session

wb = openpyxl.load_workbook('data.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')
req = Session()
for i in xrange(2,12):
    r = req.get(sheet['A{}'.format(i)].value.encode('utf-8'))
    raw = r.text.encode('utf-8')
    root = PARSER.fromstring(raw)
    s =root.xpath("p/text()")
    with open('output{}.txt'.format(i), 'w') as fp:
        for t in s:
            fp.write(t.encode('utf-8').strip())
