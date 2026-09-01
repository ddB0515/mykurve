import asyncio

from mykurve import MyKurveApi
from mykurve.data_classes import TimeRange

userName = "<your_username>"
password = "<your_password>"
mfaSecret = "<your_2fa_secret>"  # leave as-is / empty if account has no 2FA

async def main():
    api = MyKurveApi()

    token = await api.get_token(userName, password, mfa_secret=mfaSecret)
    print(token)

    account = await api.get_accounts(token.access_token)
    print(account)

    # account_info = await api.get_account_info(token.access_token, account.accounts[0].accountNumber)
    # print(account_info)

    dashboard = await api.get_dashboard(token.access_token, account.accounts[0].accountNumber)
    print(dashboard)
    # print(dashboard.accountNumber)

    consumption = await api.get_consumption_graph(token.access_token, account.accounts[0].accountNumber, TimeRange.DAY, 0)
    print(consumption)


if __name__ == "__main__":
    asyncio.run(main())
