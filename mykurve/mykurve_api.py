"""Parses data from the mykurve API"""
import requests
import logging
from datetime import datetime

from .const import TOKEN, MY_INFORMATION, DASHBOARD, CUSTOMER_ACCOUNTS, mykurve_headers, CONSUMPTION_GRAPH
from .data_classes import AccountInfo, Accounts, Account, Token, Dashboard, TimeRange, PagedMeterReading, \
    ConsumptionMeter, Tariff, ConsumptionAverages, TariffHistory, ConsumptionGraph
from .exceptions import  NotAuthenticated, AuthenticationFailed

_LOGGER = logging.getLogger(__name__)

class MyKurveApi:
    """mykurve API"""

    def __init__(self):
        _LOGGER.debug("MyKurveApi initialised")

    def get_token(self, username: str, password: str) -> Token:
        """ Make a POST requesting the access token and return it """

        headers = mykurve_headers.copy()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = {
            "username": username,
            "password": password,
            "grant_type": "password",
            "scope": "api-name",
            "client_id": "ApiClient",
        }

        try:
            response = requests.post(TOKEN, headers=headers, data=data, timeout=5)

            if response.status_code == 200:
                token_data_without_mfa = response.json()
                return Token(**token_data_without_mfa)

            if response.status_code == 400:
                raise NotAuthenticated("Unexpected status code: " + str(response.status_code))

            if response.status_code == 401:
                raise AuthenticationFailed("Unexpected status code: " + str(response.status_code))

        except requests.exceptions.RequestException:
            raise RuntimeError(f"Failed to retrieve token: {response.status_code}")

    def get_accounts(self, token: str) -> Accounts:
        headers = mykurve_headers.copy()
        headers["Authorization"] = f"Bearer {token}"

        response = requests.get(CUSTOMER_ACCOUNTS, headers=headers, timeout=3)

        if response.status_code == 200:
            accounts_data = response.json()
            accounts_list = [Account(**account) for account in accounts_data.get("accounts", [])]
            return Accounts(accounts=accounts_list)
        raise RuntimeError(f"Failed to retrieve account number: {response.status_code}")

    def get_account_info(self, token: str, account_number: str) -> AccountInfo:
        headers = mykurve_headers.copy()
        headers["Authorization"] = f"Bearer {token}"

        response = requests.get(f"{MY_INFORMATION}{account_number}", headers=headers, timeout=3)

        if response.status_code == 200:
            account_info = response.json()
            return AccountInfo(**account_info)
        raise RuntimeError(f"Failed to retrieve account info: {response.status_code}")

    def get_dashboard(self, token: str, account_number: str) -> Dashboard:
        headers = mykurve_headers.copy()
        headers["Authorization"] = f"Bearer {token}"

        response = requests.get(f"{DASHBOARD}{account_number}", headers=headers, timeout=3)

        if response.status_code == 200:
            dashboard = response.json()
            return Dashboard(**dashboard)
        raise RuntimeError(f"Failed to retrieve account info: {response.status_code}")

    def get_consumption_graph(self, token: str, account_number: str, timeRange: TimeRange, page: int) -> ConsumptionGraph:
        headers = mykurve_headers.copy()
        headers["Authorization"] = f"Bearer {token}"

        response = requests.get(f"{CONSUMPTION_GRAPH}{account_number}&timeRange={timeRange.value}&page={page}", headers=headers, timeout=3)

        if response.status_code == 200:
            consumption_graph = response.json()
            return self.parse_dashboard_data(consumption_graph)
        raise RuntimeError(f"Failed to retrieve account info: {response.status_code}")

    def parse_dashboard_data(self, consumption_graph):
        # For the consumptionMeter
        paged_meter_readings = [
            PagedMeterReading(
                periodStartUtc=datetime.fromisoformat(item['periodStartUtc']),
                readTimeUtc=datetime.fromisoformat(item['readTimeUtc']),
                actualValue=item['actualValue'],
                consumptionValue=item['consumptionValue'],
                consumptionCost=item['consumptionCost'],
                standingCharge=item['standingCharge']
            )
            for item in consumption_graph['consumptionMeter']['pagedMeterReadings']
        ]

        consumption_meter = ConsumptionMeter(
            meterSerial=consumption_graph['consumptionMeter']['meterSerial'],
            totalPagedConsumptionValue=consumption_graph['consumptionMeter']['totalPagedConsumptionValue'],
            totalPagedConsumptionCost=consumption_graph['consumptionMeter']['totalPagedConsumptionCost'],
            meterUnit=consumption_graph['consumptionMeter']['meterUnit'],
            rateCharge=consumption_graph['consumptionMeter']['rateCharge'],
            standingCharge=consumption_graph['consumptionMeter']['standingCharge'],
            pagedMeterReadings=paged_meter_readings
        )

        # For the tariffHistory
        tariffs = [
            Tariff(
                tariffId=item['tariffId'],
                consumerNumber=item['consumerNumber'],
                pricingPlanCode=item['pricingPlanCode'],
                pricingPlanDescription=item['pricingPlanDescription'],
                rate=item['rate'],
                standingCharge=item['standingCharge'],
                tariffChangeDate=datetime.fromisoformat(item['tariffChangeDate'])
            )
            for item in consumption_graph['tariffHistory']['tariffs']
        ]

        tariff_in_force_now = consumption_graph['tariffHistory']['tariffInForceNow']
        tariff_in_force_now = Tariff(
            tariffId=tariff_in_force_now['tariffId'],
            consumerNumber=tariff_in_force_now['consumerNumber'],
            pricingPlanCode=tariff_in_force_now['pricingPlanCode'],
            pricingPlanDescription=tariff_in_force_now['pricingPlanDescription'],
            rate=tariff_in_force_now['rate'],
            standingCharge=tariff_in_force_now['standingCharge'],
            tariffChangeDate=datetime.fromisoformat(tariff_in_force_now['tariffChangeDate'])
        )

        tariff_history = TariffHistory(tariffs=tariffs, tariffInForceNow=tariff_in_force_now)

        # For consumption averages
        consumption_averages_data = consumption_graph['consumptionAverages']
        consumption_averages = ConsumptionAverages(
            dailyCost=consumption_averages_data['dailyCost'],
            dailyUsage=consumption_averages_data['dailyUsage'],
            weeklyCost=consumption_averages_data['weeklyCost'],
            weeklyUsage=consumption_averages_data['weeklyUsage'],
            monthlyCost=consumption_averages_data.get('monthlyCost'),
            monthlyUsage=consumption_averages_data.get('monthlyUsage')
        )

        # Instantiate the Dashboard
        consumptionGraph = ConsumptionGraph(
            consumptionMeter=consumption_meter,
            tariffHistory=tariff_history,
            consumptionAverages=consumption_averages
        )

        return consumptionGraph
