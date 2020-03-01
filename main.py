from apriori import Apriori

items = ['bread', 'milk', 'cheese', 'beer', 'umbrella', 'diaper', 'water', 'detergent']
trans = []
trans.append('milk,beer,umbrella,diaper'.split(','))
trans.append('umbrella,diaper,beer,detergent,bread'.split(','))
trans.append('beer,water,diaper,detergent'.split(','))
trans.append('beer,cheese,diaper,detergent,bread'.split(','))
trans.append('beer,umbrella,diaper,water'.split(','))

ap = Apriori()
ap.calculate(items, trans, 0.4, 0.7)
ap.info()