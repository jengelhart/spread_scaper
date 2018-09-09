# main driver program

# import kucoin xchange lib
from kucoin.client import Client

# function to check spread
def calcSpread( bid, ask):
    return ((ask - bid) / bid) * 100

# "sign-in"
client = Client('key1', 'key2')

# set runtime vars manually
pair = "ETH-BTC"
minSpread = 0.3 # %age
disp = 0.000001 # amount to undercut or outbid
orderSize = 0.00001 # quoted in first currency in pair

# loop to keep bot running
while True:
    # get orderbook to check bid-ask
    orderBook = client.get_order_book(pair, limit=1)
    bid = orderBook["BUY"][0][0]
    ask = orderBook["SELL"][0][0]
    spread = calcSpread(bid, ask)
    print("SPREAD: " + str(spread) + "%")
    
    if spread > minSpread:
        # get our active orders to check quantity and price points
        orders = client.get_active_orders(pair)
        noBuys = len(orders["BUY"]) == 0
        noSells = len(orders["SELL"]) == 0
        
        if noBuys and noSells:
            # place orders
            print("Placing new set of orders...")
            client.create_buy_order(pair, bid + disp, orderSize)
            client.create_sell_order(pair, ask - disp, orderSize)
            print("Orders placed")
        
        #else:
            # if there is a buy order and it is less than the bid, replace it
            #if len(orders["BUY"]) > 0 and orders["BUY"][0][2] < bid:
            #    orderID = orders["BUY"][0][5]
            #    print("Cancelling buy order...")
            #    client.cancel_order(orderID, "BUY", pair)
            #    print("Buy order cancelled")
            #    print("Placing new buy order...")
            #    client.create_buy_order(pair, bid + disp, orderSize)
            #    print("Buy order placed")
                
            # if there is a sell order and it is more than the ask, replace it
            #if len(orders["SELL"]) > 0 and orders["SELL"][0][2] > ask:
            #    orderID = orders["SELL"][0][5]
            #    print("Cancelling sell order...")
            #    client.cancel_order(orderID, "SELL", pair)
            #    print("Sell order cancelled")
            #    print("Placing new sell order...")
            #    client.create_sell_order(pair, ask - disp, orderSize)
            #    print("Sell order placed")

    else:
        print("Cancelling all orders")
        client.cancel_all_orders(pair)
        print("All orders cancelled")
