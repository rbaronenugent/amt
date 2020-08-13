from math import inf

# personal variables
INCOME = int(input("What is your base salary? ").replace(",", "").replace(" ", ""))
MY_DEDUCTION = int(input("What deduction will you claim (12,400/24,800 is standard for single/joint filing)? ").replace(",", "").replace(" ", ""))
ISO_COUNT = int(input("How many ISOs are in your grant? ").replace(",", "").replace(" ", ""))
STRIKE_PRICE = float(input("What is your strike price? ").replace(",", "").replace(" ", ""))
FMV = float(input("What is the current FMV (409a price)? ").replace(",", "").replace(" ", ""))
MARRIED_OR_SINGLE = input("Will you file as single or married? S/M: ").replace(",", "").replace(" ", "").upper()
while MARRIED_OR_SINGLE not in ['M', 'S']:
    MARRIED_OR_SINGLE = input("OMG! PLEASE CHOOSE 'S' OR 'M'! ").replace(",", "").replace(" ", "").upper()

# IRS variables
# AMT
amt_tax_rates = [0.26, 0.28]
amt_brackets_low = [0, 197900]
amt_tax_exemption = 72900 if MARRIED_OR_SINGLE == 'S' else 113400
# federal rates
tax_rates = [0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]
brackets_low_dict = {
    'S': [0, 9875, 40125, 85525, 163300, 207350, 518400],
    'M': [0, 19750, 80250, 171050, 326600, 414700, 622050]
    }
brackets_low = brackets_low_dict[MARRIED_OR_SINGLE]


def regular_federal_tax_burden(income, deduction=12200):
    """
    calculates and returns your regular federal tax burden
    """

    brackets_high = brackets_low[1:] + [inf]
    income_in_each_bracket = [max(min(high, income - deduction) - low, 0) for low, high in zip(brackets_low, brackets_high)]
    tax_burden = sum([amount * tax_rate for amount, tax_rate in zip(tax_rates, income_in_each_bracket)])

    return tax_burden


def amt_tax_burden(shares_exercised, fmv, strike_price, income, deduction):
    """
    calculates and returns your amt tax burden
    """

    exercise_income = shares_exercised * (fmv - strike_price)
    amt_income = exercise_income + income - amt_tax_exemption - deduction

    amt_brackets_high = amt_brackets_low[1:] + [inf]
    amt_income_in_each_bracket = [max(min(high, amt_income - deduction) - low, 0) for low, high in zip(amt_brackets_low, amt_brackets_high)]
    amt_tax_burden = sum([amount * tax_rate for amount, tax_rate in zip(amt_tax_rates, amt_income_in_each_bracket)])

    return amt_tax_burden


# now find at how many shares AMT kicks in....
federal_tax = regular_federal_tax_burden(INCOME, deduction=MY_DEDUCTION)
for shares in range(0, ISO_COUNT):
    amt_tax = amt_tax_burden(shares, FMV, STRIKE_PRICE, INCOME, MY_DEDUCTION)
    if amt_tax > federal_tax:
        print("You can exercise %i ISOs at a total cost of $%i before paying AMT tax" % (shares - 1, (shares - 1) * STRIKE_PRICE))
        break

# full exercise
amt_tax = amt_tax_burden(ISO_COUNT, FMV, STRIKE_PRICE, INCOME, MY_DEDUCTION)
additional_tax = amt_tax - federal_tax
print("If you exercised all your ISOs you would pay $%i extra tax under AMT" % (max(additional_tax, 0)))

