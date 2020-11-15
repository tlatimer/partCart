displayNames = {
    'desc': 'Description',
    'vendor': 'Vendor',
    'partnum': 'Part Num',
    'location': 'Location',
    'barcode': 'Barcode',
    'sellprice': 'Sell Price',
    'cost': 'Cost',
    'notes': 'Notes',
    'name': 'Cross Ref',
    'timestamp': 'Last Sold',
}

partCols = list(displayNames.keys())

searchCols = [
    'desc',
    'vendor',
    'partnum',
    'location',
    'name',
    'timestamp',
]

showPartsHeader = ['[#]'] + [displayNames[i] for i in searchCols]