import aiohttp
import asyncio
import json


async def get_ebisus_data(wallet):
    url = f'https://api.ebisusbay.com/walletoverview?pageSize=1000&wallet={wallet}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_floor_price(session, col_url, address, sztuk):
    async with session.get(col_url) as col_response:
        col_data = await col_response.json()
        fp = None
        for col in col_data['collections']:
            nazwa = col['address']
            if nazwa == address:
                fp = str(col['stats']['total']['floorPrice'])
                break
        return fp
async def get_nfts_ebisus(wallet):
    data = await get_ebisus_data(wallet)
    nfts_ebisus = []
    suma = 0
    async with aiohttp.ClientSession() as session:
        tasks = []
        for erc721 in data['data']['erc721']:
            address = erc721['address'].strip()
            sztuk = int(erc721['balance'])
            col_url = f"https://api.ebisusbay.com/collectioninfo?pageSize=750&direction=desc&sortBy=totalvolume&search=&page=all"
            tasks.append(asyncio.ensure_future(get_floor_price(session, col_url, address, sztuk)))
        results = await asyncio.gather(*tasks)
        for i, erc721 in enumerate(data['data']['erc721']):
            name = erc721['name']
            address = erc721['address'].strip()
            balance = int(erc721['balance'])
            fp = results[i]
            result = balance * float(fp) if fp is not None else None
            suma += result if result is not None else 0
            nft_ebisus = {
                'name': name,
                'address': address,
                'balance': balance,
                'floor_price': fp,
                'result': result
            }
            nfts_ebisus.append(nft_ebisus)
    with open('nft_ebisus.json', 'w') as f:
        json.dump(nfts_ebisus, f)
    return nfts_ebisus, suma