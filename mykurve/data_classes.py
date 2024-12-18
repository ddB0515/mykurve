from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class TimeRange(Enum):
    DAY = 'Day'
    WEEK = 'Week'
    MONTH = 'Month'
    YEAR = 'Year'

@dataclass
class Token:
    access_token: str
    expires_in: int
    token_type: str
    scope: str
    CRC32: bool
    mfaEnabled: bool
    mfaRequiredInDays: None

@dataclass
class Account:
    accountNumber: str
    isActive: bool
    hasDebt: bool
    hasInactiveDebt: bool
    propertyAddress: str
    consumptionType: str
    utility: str
    utilityType: str

@dataclass
class Accounts:
    accounts: List[Account]

@dataclass
class AccountInfo:
    firstName: str
    lastName: str
    initials: str
    emailAddress: str
    phoneNumbers: List[str]
    fullAddress: str
    suburb: None
    postcode: str
    moveInDate: datetime
    moveOutDate: None
    utility: str
    utilityType: str
    supplier: str
    accountNumber: int
    linkedAccounts: List[str]
    additionalInformation: str
    tariffStandingCharge: float
    tariffRate: float
    emergencyCreditAllowance: float

# Define the Tariff class
@dataclass
class Tariff:
    tariffId: int
    consumerNumber: str
    pricingPlanCode: str
    pricingPlanDescription: str
    rate: float
    standingCharge: float
    tariffChangeDate: datetime

# Define the TariffHistory class
@dataclass
class TariffHistory:
    tariffs: List[Tariff]
    tariffInForceNow: Tariff

@dataclass
class PagedMeterReading:
    periodStartUtc: datetime
    readTimeUtc: datetime
    actualValue: float
    consumptionValue: float
    consumptionCost: float
    standingCharge: float


@dataclass
class ConsumptionMeter:
    meterSerial: str
    totalPagedConsumptionValue: float
    totalPagedConsumptionCost: float
    pagedMeterReadings: List[PagedMeterReading]
    meterUnit: str
    rateCharge: float
    standingCharge: float


@dataclass
class ConsumptionAverages:
    dailyCost: Optional[float]
    dailyUsage: Optional[float]
    weeklyCost: Optional[float]
    weeklyUsage: Optional[float]
    monthlyCost: Optional[float]
    monthlyUsage: Optional[float]

# Define the Dashboard class
@dataclass
class Dashboard:
    customerNumber: str
    accountNumber: str
    primaryConsumerNumber: str
    firstName: str
    lastName: str
    initials: str
    email: str
    creditThreshold: float
    lastKnownVelocityBalance: float
    lastKnownVelocityBalanceDate: datetime
    lastPayAmount: float
    consumptionBalance: float
    combinedBalance: float
    emergencyCreditAllowance: float
    emergencyCreditIsActive: bool
    isEmergencyCreditAvailable: bool
    emergencyCreditActivationDate: Optional[datetime]
    emergencyCreditConsumptionBalanace: float
    emergencyCreditRemaining: float
    lastMeterReadingDate: datetime
    lastMeterReading: float
    todaysUsage: float
    todaysUsageCost: float
    valveStatus: str
    payPointNumber: str
    inHouseDisplaySerialNumber: Optional[str]
    agedDebtAmount: Optional[float]
    agedDebtAmountDateTime: datetime
    paymentPlan: str
    paymentPlanActivationDate: Optional[datetime]
    amountPaid: Optional[float]
    tariffHistory: TariffHistory
    utility: str
    utilityType: str

@dataclass
class ConsumptionGraph:
    consumptionMeter: ConsumptionMeter
    tariffHistory: TariffHistory
    consumptionAverages: ConsumptionAverages
