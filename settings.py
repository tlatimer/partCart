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
}

allPartCols = list(displayNames.keys())

updateCols = {
    'desc': 'Description',
    'vendor': 'Vendor',
    'partnum': 'Part Num',
    'location': 'Location',
    'barcode': 'Barcode',
    'sellprice': 'Sell Price',
    'cost': 'Cost',
    'notes': 'Notes',
}

searchCols = [
    'desc',
    'vendor',
    'partnum',
    'name',
    'location',
    'qty',
    'timestamp',
]

colsToSearch = [
    'desc',
    'loc',
    'partnum',
    'barcode',
]

# findPartsHeader = ['[#]'] + [displayNames[i] for i in searchCols]