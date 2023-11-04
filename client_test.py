import unittest
from client3 import getDataPoint, getRatio

class ClientTest(unittest.TestCase):
    def test_getDataPoint_calculatePrice(self):
        quotes = [
            {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        # Iterate over quotes and make assertions for each one
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            self.assertEqual(stock, quote['stock'])
            self.assertEqual(bid_price, quote['top_bid']['price'])
            self.assertEqual(ask_price, quote['top_ask']['price'])
            self.assertEqual(price, (quote['top_bid']['price'] + quote['top_ask']['price']) / 2)

    def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
        quotes = [
            {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]

        result_1 = getDataPoint(quotes[0])
        self.assertEqual(result_1, ('ABC', 120.48, 119.2, 119.84))

        result_2 = getDataPoint(quotes[1])
        self.assertEqual(result_2, ('DEF', 117.87, 121.68, 119.775))

    def test_getDataPoint_calculatePriceZeroAsk(self):
        quotes = [
            {'top_ask': {'price': 0.0, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'XYZ'},
            {'top_ask': {'price': 0.0, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'PQR'}
        ]

        result_1 = getDataPoint(quotes[0])
        self.assertEqual(result_1, ('XYZ', 120.48, 0.0, 60.24))

        result_2 = getDataPoint(quotes[1])
        self.assertEqual(result_2, ('PQR', 117.87, 0.0, 58.935))

    def test_getDataPoint_calculatePriceZeroBid(self):
        quotes = [
            {'top_ask': {'price': 123.45, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 0.0, 'size': 109}, 'id': '0.109974697771', 'stock': 'LMN'},
            {'top_ask': {'price': 99.99, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 0.0, 'size': 81}, 'id': '0.109974697771', 'stock': 'STU'}
        ]
        result_1 = getDataPoint(quotes[0])
        self.assertEqual(result_1, ('LMN', 0.0, 123.45, 61.725))

        result_2 = getDataPoint(quotes[1])
        self.assertEqual(result_2, ('STU', 0.0, 99.99, 49.995))

    def test_getRatio_priceBZero(self):
        price_a = 119.2
        price_b = 0
        result = getRatio(price_a, price_b)
        self.assertEqual(result, None)

    def test_getRatio_priceAZero(self):
        price_a = 0
        price_b = 121.68
        result = getRatio(price_a, price_b)
        self.assertEqual(result, 0)

    def test_getRatio_priceAandBNotZero(self):
        price_a = 119.2
        price_b = 121.68
        result = getRatio(price_a, price_b)
        self.assertEqual(result, price_a / price_b)

    def test_getDataPoint_emptyQuotes(self):
        quotes = []

        # Check that getDataPoint handles an empty quotes list gracefully
        with self.assertRaises(IndexError):
            result = getDataPoint(quotes[0])
    
    def test_getDataPoint_emptyQuote(self):
       quote = {}
       # Check that getDataPoint handles an empty quote gracefully
       with self.assertRaises(KeyError):
           result = getDataPoint(quote)
            
    def test_getDataPoint_missingKey(self):
        quotes = [{'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771'}]
        with self.assertRaises(KeyError):
            getDataPoint(quotes[0])

    def test_getDataPoint_bidPriceGreaterThanAskPrice(self):
        quotes = [{'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}]
        result = getDataPoint(quotes[0])
        self.assertEqual(result, ('ABC', 120.48, 119.2, 119.84))

    def test_getDataPoint_bidPriceAndAskPriceZero(self):
        quotes = [{'top_ask': {'price': 0.0, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 0.0, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}]
        result = getDataPoint(quotes[0])
        self.assertEqual(result, ('ABC', 0.0, 0.0, 0.0))

if __name__ == '__main__':
    unittest.main()