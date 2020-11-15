displayNames = {
    'desc': 'Description',
    'vendor': 'Vendor',
    'partnum': 'Part Num',
    'location': 'Location',
    'barcode': 'Barcode',
    'sellprice': 'Sell Price',
    'cost': 'Cost',
    'notes': 'Notes',
    'group': 'Group',
}

searchCols = [
    'desc',
    'vendor',
    'partnum',
    'location',
    'group',
]

partCols = list(displayNames.keys())
partCols.remove('group')

showPartsHeader = ['[#]'] + [displayNames[i] for i in searchCols]