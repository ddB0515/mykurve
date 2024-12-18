"""Constants for mykurve API"""

BASE_API_URL = "https://api.mykurve.com"

TOKEN = f"{BASE_API_URL}/connect/token"
CUSTOMER_ACCOUNTS = f"{BASE_API_URL}/api/Pages/CustomerAccounts"
MY_INFORMATION = f"{BASE_API_URL}/api/Pages/MyInformation?accountNumber="
DASHBOARD = f"{BASE_API_URL}/api/Pages/Dashboard?accountNumber="
CONSUMPTION_GRAPH = f"{BASE_API_URL}/api/Pages/ConsumptionGraphV2?accountNumber="

mykurve_headers = {
	"Accept": "application/json",
	"Accept-Encoding": "gzip, deflate, br, zstd",
	"Accept-Language": "en-GB,en;q=0.5",
	"Connection": "keep-alive",
	"Host": "api.mykurve.com",
	"Origin": "https://www.mykurve.com",
	"Referer": "https://www.mykurve.com/",
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}