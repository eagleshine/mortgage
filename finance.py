#! /usr/bin/python

import sys
from decimal import Decimal, ROUND_HALF_UP

def _monthly_payment(APR, months, total_amount):
    r = APR/12
    x = 1 + r
    return Decimal(total_amount * r / (1 - (1/x)**months))

def _round_money(x):
    return x.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

class Loan(object):

    def __init__(self, APR, months, amount):
        self.apr = Decimal(APR)
        self.rate = Decimal(APR/12)
        self.months = Decimal(months)
        self.amount = Decimal(amount)
        self.payment = _round_money(_monthly_payment(APR, months, amount))

    def monthly_payment(self):
        return self.payment

    def composition(self):
        """generate (principle, interests, remaining) for each month"""
        total = self.amount
        for x in xrange(0, self.months):
            interest = _round_money(total * self.rate)
            principle = self.payment - interest
            total = total - principle
            yield principle, interest, total

    def composition_accumulation(self):
        res = list()
        principle,interests = 0,0
        for p, i, t in self.composition():
            principle += p
            interests += i
            res.append((principle, interests, t))
        return res

def main():
    apr = float(sys.argv[1])
    months = int(sys.argv[2]) * 12
    total_amount = float(sys.argv[3])
    loan = Loan(apr, months, total_amount)
    print "Monthly payment = ", loan.monthly_payment()

    n = 0
    print "month    Printciple   Interest      remaining"
    for x in loan.composition():
        n +=1
        print n, x
    n = 0
    print "month    Printciple(acc)   Interest(acc)      remaining"
    for x in loan.composition_accumulation():
        n +=1
        print n, x

if __name__ == '__main__':
    main()
