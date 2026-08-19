from advisor import get_business_advice

prompt = """
Product: Rice
Current Stock: 500
Sales Last Month: 1000
Sales This Month: 750

Give recommendations.
"""

print(get_business_advice(prompt))