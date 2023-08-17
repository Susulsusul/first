#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import json
from lib import CoinexPerpetualApi


# Replace it with your own API key.
access_id = '192BE1AD698D4604B9951F91FC1FD9EB'
secret_key = 'F4022AEB2BA98AD84EABED3B9C201A7CC3963862E1E2ED37'


if __name__ == "__main__":
    robot = CoinexPerpetualApi(access_id, secret_key)

    print(json.dumps(robot.ping(), indent=4))

    #print(json.dumps(robot.get_market_info(), indent=4))
    # print(robot.query_account())
   #result = robot.put_limit_order(
    #    'BTCUSDT',
    #    robot.ORDER_DIRECTION_BUY,
    #    0.0005,
    #    20000
    #    )
    #print(json.dumps(result, indent=4))

    s = robot.put_market_order( 'BTCUSDT', 2, 0.0005)
    print(json.dumps(s, indent=4))
    #print(s)
    
    
    sleep(5)
    q =robot.query_position_pending('BTCUSDT')
    print(json.dumps(q, indent=4))
    print(q['data'][0]["position_id"])
    
    c = robot.close_market('BTCUSDT', q['data'][0]["position_id"]  )
    print(json.dumps(c, indent=4))
    print(c)    

    #print( json.dumps( robot.cancel_order('BTCUSDT',102220926615)) )

