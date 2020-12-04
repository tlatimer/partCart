dbfname = 'partCart2.db'

displayNames = {
    # bins
    'desc': 'Description',
    'loc': 'Location',
    'sellprice': 'Sell Price',

    # crossrefs
    'vendor': 'Vendor',
    'partnum': 'Part Num',
    'barcode': 'Barcode',
    'cost': 'Cost',

    # qtychanges
    'qty': 'Qty',
    'lastsold': 'Last Sold',

    '||': '||',
}

# allPartCols = list(displayNames.keys())

colsToSearch = [
    'desc',
    'loc',
    'partnum',
    'barcode',
]

searchCols = [
    'vendor',
    'partnum',
    '||',
    'desc',
    'loc',
    'qty',
    'lastsold',
]

findPartsHeader = ['[#]'] + [displayNames[i] for i in searchCols]
