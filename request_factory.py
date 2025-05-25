import time

class RequestFactory:
    @staticmethod
    def request_headers_websocket(token):
        return {
            "Cookie": f"access_token={token}",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "es-419,es;q=0.9"
        }

    @staticmethod
    def request_candles(pair, duration):
        return [
            [{"t":2,"e":10,"uuid":"h1Jxv1","d":[{"pair": pair,"size": duration,"to": int(time.time()),"solid":True}]}],
            [{"t":2,"e":282,"uuid":"JYNMVY","d":[{"pair": pair,"size": duration,"to":int(time.time()),"solid":True}]}]
        ]

    @staticmethod
    def request_operation_market(account_id, amount, dir, duration, pair):
        return [
            {
                "d": [
                    {
                        "account_id": account_id,
                        "amount": amount,
                        "cat": "digital",
                        "dir": dir,
                        "duration": duration,
                        "group": "demo",                
                        "is_flex": False,
                        "pair": pair,
                        "pos": 0,
                        "risk_free_id": None,
                        "source": "platform",
                        "timestamp": int(time.time()),

                    }
                ],
                "e": 23,
                "t": 2,
                "uuid": "M7UK6IG5I2KOVYVEOFS"
            }
        ]
    
    @staticmethod
    def request_operation_limit(account_id, amount, dir, duration, price_order, pair):
        return [
            {
                "d": [
                    {
                        "account_id": account_id,
                        "amount": amount,
                        "course_target": price_order,
                        "dir": dir,
                        "duration": duration,
                        "group": "demo",                
                        "is_flex": False,
                        "pair": pair,
                        "winperc": 1
                    }
                ],
                "e": 40,
                "t": 2,
                "uuid": "MQan1v"
            }
        ]