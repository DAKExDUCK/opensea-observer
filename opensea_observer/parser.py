from .functions import req


def get_info(name):
    status, response = req(name)
    if status == 200:
        name = response['collection']['name']
        stats = response['collection']['stats']

        payment_token = response['collection']['payment_tokens'][0]['symbol']
        usd_price_of_payment_token = response['collection']['payment_tokens'][0]['usd_price']

        floor_price = stats['floor_price']
        floor_price_usd = usd_price_of_payment_token * floor_price if floor_price else None
        
        return name, payment_token, floor_price, floor_price_usd
    else:
        return None