from enum import Enum


class Industry(str, Enum):
    FINANCE = "Finance"
    INFORMATION_TECHNOLOGY = "Information Technology"
    HEALTHCARE = "Healthcare"
    CONSUMER_DISCRETIONARY = "Consumer Discretionary"
    COMMUNICATION_SERVICES = "Communication Services"
    INDUSTRIALS = "Industrials"
    CONSUMER_STAPLES = "Consumer Staples"
    ENERGY = "Energy"
    UTILITIES = "Utilities"
    REAL_ESTATE = "Real Estate"


class Role(str, Enum):
    MEMBER = "Member"
    ADMIN = "Admin"
