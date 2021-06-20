from rest_framework.response import Response
from rest_framework.views import APIView
from re import sub
import pandas as pd


def convertToCamelCase(string):
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return string[0].lower() + string[1:]

def getJSONForStrategy(xls, sheet, sheet_type):
    result = {}
    data = pd.read_excel(xls, sheet)

    if sheet_type == "Current":
        data['List Revenue']= '$'+data['List Revenue'].map('{:,.0f}'.format)
        data['Expenditure']= '$'+data['Expenditure'].map('{:,.0f}'.format)
        data['Discount']= (data.Discount*100).map('{:,.1f}'.format)+'%'
    else:
        data['Suggested Revenue'] = '$' + data['Suggested Revenue'].map('{:,.0f}'.format)
        data['Discount'] = (data.Discount * 100).map('{:,.0f}'.format) + '%'
        data['Industry Share (%)'] = (data['Industry Share (%)'] * 100).map('{:,.1f}'.format) + '%'
        data['Impact'] = '$' + data['Impact'].map('{:,.0f}'.format)

    header = list(data.columns)
    header = [convertToCamelCase(i) for i in header]
    header.pop(0)
    result.update({
        'columns': header
    })

    data = data.to_dict('records')
    for record in data:
        obj = {}
        listHeader = ''
        for k,v in record.items():
            if (k != 'Strategies'):
                obj.update({
                    convertToCamelCase(k) : v
                })
            else:
                listHeader = convertToCamelCase(v)

        result.update({
            listHeader: obj
        })
    return [result]

def getJSONForProduct(xls, sheet, sheet_type):
    result = {}
    data = pd.read_excel(xls, sheet)

    header = list(data.columns)
    header = [convertToCamelCase(i) for i in header]
    header.pop(0)
    result.update({
        'columns': header
    })

    num = data._get_numeric_data()
    num[num < 0] = 0
    productData = data[data['Product Segment'].str.contains("Product")]

    if sheet_type == "Current":
        productData['totalMarketValue'] = '$' + productData['totalMarketValue'].map('{:,.0f}'.format)
        productData['List Revenue'] = '$' + productData['List Revenue'].map('{:,.0f}'.format)
        productData['Expenditure'] = '$' + productData['Expenditure'].map('{:,.0f}'.format)
        productData['Discount'] = (productData.Discount * 100).fillna(0).map('{:,.1f}'.format) + '%'
    else:
        productData['Suggested Revenue'] = '$' + productData['Suggested Revenue'].map('{:,.0f}'.format)
        productData['Discount'] = (productData.Discount * 100).map('{:,.1f}'.format) + '%'
        productData['Industry Share (%)'] = (productData['Industry Share (%)'].fillna(0) * 100).map('{:,.1f}'.format) + '%'
        productData['Impact'] = '$' + productData['Impact'].map('{:,.0f}'.format)

    productData = productData.to_dict('records')

    summary = data[~data['Product Segment'].str.contains("Product")]
    summary = summary.to_dict('records')

    result.update({
        'productData': [{}],
        'summary': [{}]
    })

    for product in productData:
        obj = {}
        listHeader = ''
        for k, v in product.items():
            if (k != 'Product Segment'):
                obj.update({
                    convertToCamelCase(k): v
                })
            else:
                listHeader = convertToCamelCase(v)
        result['productData'][0].update({
            listHeader: obj
        })

    for s in summary:
        obj = {}
        listHeader = ''
        for k, v in s.items():
            if (k != 'Product Segment'):
                obj.update({
                    convertToCamelCase(k): v
                })
            else:
                listHeader = convertToCamelCase(v)

        if 'summaryfield' in listHeader or listHeader == 'savings':
            result['summary'][0].update({
                listHeader: obj.get('impact') if obj.get('impact') else obj.get('discount')
            })
        else:
            result['summary'][0].update({
                listHeader: obj
            })

    return [result]


class IndexView(APIView):
    def get(self, request):
        xls = pd.ExcelFile('core/resources/Technical_assessment_source_data.xlsx', engine='openpyxl')

        sheet_list = xls.sheet_names
        result = {
            'strategies': [{}],
            'productSegment': [{}]
        }
        for sheet in sheet_list:
            s = sheet.split(',')
            if s[0] == 'Table3':
                result["strategies"][0].update({
                    convertToCamelCase(s[1]): getJSONForStrategy(xls, sheet, s[1])
                })
            else:
                result["productSegment"][0].update({
                    convertToCamelCase(s[1]): getJSONForProduct(xls, sheet, s[1])
                })
        return Response(result)
