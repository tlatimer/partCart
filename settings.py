displayNames = {
    'desc': 'Description',
    'vendor': 'Vendor',
    'partnum': 'Part Num',
    'location': 'Location',
    'barcode': 'Barcode',
    'sellprice': 'Sell Price',
    'cost': 'Cost',
    'notes': 'Notes',
    'qty': 'Qty',
    'name': 'CrossRef',
    'timestamp': 'Last Sold',
}

partCols = list(displayNames.keys())

searchCols = [
    'desc',
    'vendor',
    'partnum',
    'name',
    'location',
    'qty',
    'timestamp',
]

findPartsHeader = ['[#]'] + [displayNames[i] for i in searchCols]