# mykurve library

Unofficial async library to retrieve details of https://api.mykurve.com/ or https://www.mykurve.com/ account
This was done for personal project but feel free to use on your own risk 

Hope will be useful to someone and if there is any issues (what I think there is...) please open PR or issue will 
try to help/fix in mean time

## Note
- If your account has 2FA enabled, pass either `mfa_code` (a code you already
  generated) or `mfa_secret` (the base32 secret from the QR code shown during 2FA
  setup) to `get_token()`. With `mfa_secret`, the code is generated for you via TOTP.
  If 2FA is required and neither is passed, `get_token()` raises `MfaCodeRequired`.

### How to use 

```python
import asyncio

from mykurve import MyKurveApi
from mykurve.data_classes import TimeRange

userName = "<your_account>"
password = "your_password"
mfaSecret = "<your_2fa_secret>"  # only needed if 2FA is enabled

async def main():
    api = MyKurveApi()

    token = await api.get_token(userName, password, mfa_secret=mfaSecret)
    print(token)

    account = await api.get_accounts(token.access_token)
    print(account)

    account_info = await api.get_account_info(token.access_token, account.accounts[0].accountNumber)
    print(account_info)

    dashboard = await api.get_dashboard(token.access_token, account.accounts[0].accountNumber)
    print(dashboard)

    dashboard = await api.get_consumption_graph(token.access_token, account.accounts[0].accountNumber, TimeRange.DAY, 0)
    print(dashboard)


if __name__ == "__main__":
    asyncio.run(main())
```

If you like what I'm doing please support me <br/>
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/ddb0515)