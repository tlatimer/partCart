db_fname = 'partCart2.db'

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

all_bin_cols = ['desc', 'loc', 'sellprice']
all_crossref_cols = ['vendor', 'partnum', 'barcode', 'cost']

colsToSearch = ['desc', 'loc', 'partnum', 'barcode']

crossRefDispCols = ['vendor', 'partnum']
binDispCols = ['desc', 'loc', 'qty', 'lastsold']

searchDisplayCols = crossRefDispCols + ['||'] + binDispCols

findPartsHeader = ['[#]'] + [displayNames[i] for i in searchDisplayCols]
