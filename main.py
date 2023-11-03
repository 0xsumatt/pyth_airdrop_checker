import csv 
import httpx
import asyncio

async def read_csv(filename):
    with open(filename,'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        tasks = []
        for row in csv_reader:
            wallet_address = row['address']
            tasks.append(fetch_status(wallet_address))
        await asyncio.gather(*tasks)

def write_csv(address, tokens):
    with open('eligible_addresses.csv', 'a', newline='') as eligible_file:
        csv_writer = csv.writer(eligible_file)
        csv_writer.writerow([address, tokens])

async def fetch_status(wallet_address):
    async with httpx.AsyncClient() as client:
        if "0x" in wallet_address:
            url = f"https://airdrop.pyth.network/api/grant/v1/amount_and_proof?ecosystem=evm&identity={wallet_address}"
        else:
            url = f"https://airdrop.pyth.network/api/grant/v1/amount_and_proof?ecosystem=solana&identity={wallet_address}"

        req = await client.get(url)
        json_resp = req.json()
        if 'error' in json_resp:
            print(f"address not eligible: {wallet_address}")
        else:
            tokens = int(json_resp['amount'])/1000000
            print(f"{wallet_address}: eligible for {tokens} tokens")
            write_csv(wallet_address, tokens)

if __name__ == "__main__":
    with open('eligible_addresses.csv', 'w', newline='') as eligible_file:
        csv_writer = csv.writer(eligible_file)
        csv_writer.writerow(['address', 'tokens'])
    asyncio.run(read_csv("wallets.csv"))
