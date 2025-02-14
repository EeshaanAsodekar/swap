from scipy.optimize import minimize_scalar
### swap rate calculator
def calculate_swap_rate(nominal:float, floating_rates:list, discount_factors:list):
    
    # discounting any cashflow
    def pv_flow(cash_flow, discount_factor):
        pv = 0
        for cf, df in zip(cash_flow, discount_factor):
            pv += cf * df
        
        return pv
    
    # number of payments
    no_of_cashflows = len(floating_rates)

    # list of floating leg payments
    float_leg_cashflow = [nominal*rate for rate in floating_rates]
    
    # list of fixed leg payments
    fix_leg = lambda rate: [nominal*rate]*no_of_cashflows

    def objective(swap_rate):
        fixed_leg_cashflow = fix_leg(swap_rate)
        pv_fix_leg = pv_flow(fixed_leg_cashflow, discount_factors)
        pv_float_leg = pv_flow(float_leg_cashflow, discount_factors)

        return abs(pv_fix_leg - pv_float_leg)

    result = minimize_scalar(objective, bounds=(0,1), method="bounded")

    return result.x



### swap valuer
class Leg:
    '''
    Leg of a swap
    
    attributes:
    1. cashflows (list)
    2. discout_factor (list)
    3. description (str)
    '''
    def __init__(self, cashlows:list, discount_factors:list, description:str):
        self.cashflows = cashlows
        self.discount_factors = discount_factors
        self.no_of_quarters = len(cashlows)
        self.description = description
    
    def present_val_of_leg(self)->float:
        present_val = 0
        for i in range(len(self.cashflows)):
            present_val += self.cashflows[i] * self.discount_factors[i]
        
        return present_val


class Swap:
    '''
    class to price any vanilla swap.

    Attributes
    leg1 (Leg)
    leg2 (Leg)
    '''
    def __init__(self, leg1:Leg, leg2:Leg, discount_factors:list):
        if leg1.no_of_quarters != leg2.no_of_quarters:
            raise ValueError("Need both swap legs to be of same period")
        self.leg1 = leg1
        self.leg2 = leg2
        self.discout_factors = discount_factors
    
    def swap_value(self, perspective_of:str, facing_against:str):
        if perspective_of == self.leg1.description and facing_against== self.leg2.description:
            return self.leg2.present_val_of_leg() - self.leg1.present_val_of_leg()
        elif perspective_of == self.leg2.description and facing_against== self.leg1.description:
            return self.leg1.present_val_of_leg() - self.leg2.present_val_of_leg()
        else:
            raise ValueError("incorrect arguments for swap valuation")

if __name__ == "__main__":
    ### swap valuation calculator
    cashflows_fix = [1.5, 1.5, 1.5]
    cashflows_float = [1.258, 1.694, 1.857]
    discount_factors = [0.9944, 0.9778, 0.9600]

    float_leg = Leg(cashflows_float, discount_factors, "float")
    fix_leg = Leg(cashflows_fix, discount_factors, "fix")

    fix_float_swap = Swap(fix_leg, float_leg)

    print(fix_float_swap.swap_value("fix", "float"))
    print(fix_float_swap.swap_value("float", "fix"))

    ### swap rate calculator
    nominal =  100_000_000
    floating_rates = [
            4.3715,
            3.8388,
            3.4911,
            3.2938,
            3.1785,
            3.1099,
            3.0788,
            3.0792
        ]

    discount_factors = [
        0.9763,
        0.9669,
        0.9583,
        0.9504,
        0.9429,
        0.9355,
        0.9282,
        0.9210
    ]
    decimal = [rate/100 for rate in floating_rates]
    print(calculate_swap_rate(nominal, decimal, discount_factors))