import os
from brownie import Contract, accounts, web3, chain
import schedule
import time

dev = accounts.add(os.getenv("OWNER_KEY"))
bb_usdc = "0x3B998BA87b11a1c5BC1770dE9793B17A0dA61561"
bb_dai = "0x2Ff1552Dd09f87d6774229Ee5eca60CF570AE291"
herbs = Contract.from_explorer('0x261e122e2c6aa341B9f132D37C621457d797Bb47')
dai = Contract.from_explorer("0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E")
usdc = Contract.from_explorer("0x04068DA6C83AFCFA0e13ba15A6696662335D5B75")

def job():
    while herbs.sample(bb_usdc, {"from": dev})[0] > 3000 * 1e6 or herbs.sample(bb_dai, {"from": dev})[0] > 3000 * 1e18:
        print(f"collecting herbs...{chain.height}")
        dai_before = dai.balanceOf(herbs)
        usdc_before = usdc.balanceOf(herbs)
        gas_price = web3.eth.gas_price / 1e9
        if gas_price < 1500:
            herbs.collect({"from": dev, "gas_limit": "7500000"})
            dai_after = dai.balanceOf(herbs)
            usdc_after = usdc.balanceOf(herbs)

            if dai_after > dai_before:
                print(f'DAI gain: {(dai_after - dai_before) / 1e18}')
            if usdc_after > usdc_before:
                print(f'USDC gain: {(usdc_after - usdc_before) / 1e6}')
        else:
            print(f"gas price {gas_price} gwei too expensive")
            break
    print("done collecting herbs")

schedule.every().minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(30)
