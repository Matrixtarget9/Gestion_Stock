{

    'name': "stocks",
    'summary': '',
    'depends': ['base',
                'account', 'sale_management','stock'],
    'data': [
        'views/returnsview.xml',
        'report/report.xml',
        # 'report/report_detail_bon_sortie.xml',
        'data/sequence.xml',
    ],

}
