import pandas as pd

def interpolate_sofr_rate(sofr_rate_before:float, days_before:int, sofr_rate_after:float, days_after:int):
    '''
    Fucntion to interpolate SOFR rate between maturities

    Args:
    sofr rate before
    bays before
    sofr rate after
    days after
    '''

    return (days_before/(days_before+days_after)*sofr_rate_after + 
            days_after/(days_before+days_after)*sofr_rate_before)

class DiscountFactor:
    '''
    Encapsulates all the parameters that go into creating a discount factor 
    series.
    '''
    def __init__(self, sofr_series:pd.DataFrame, cashflow_dates:pd.DataFrame):
        '''
        
        sofr series dataframe:
            columns - "settlement_date", "sofr_rate"
        
        cashflow_dates:
            columns - "date" (dates of the cashflow)
        '''

        self.sofr_series = sofr_series
        self.final_table = cashflow_dates


    def get_days_between(self)->None:
        # converting dates to datetime
        self.final_table['date'] = pd.to_datetime(self.final_table['date'])
        self.final_table['days_between'] = self.final_table['date'].diff().dt.days

        print(self.final_table.head())
    
    def days_before_after_loader(self)->None:
        self.sofr_series['cashflow_date'] = self.final_table['date'].copy()
        self.sofr_series['days_after'] = self.sofr_series['settlement_date'] - self.sofr_series['cashflow_date']
        self.sofr_series['days_before'] = self.sofr_series['cashflow_date'] - self.sofr_series['settlement_date'].shift(1)
        self.sofr_series['sofr_before'] = self.sofr_series['sofr_rate'].shift(1)
        print(self.sofr_series)

    def interporlate_sofrs(self):
        interpolated_sofr = self.sofr_series.iloc[1:].apply(
            lambda row: interpolate_sofr_rate(row['sofr_before'], row['days_before'], row['sofr_rate'], row['days_after']),
            axis=1
        )

        return interpolated_sofr

    def get_discount_factors(self)->list:
        pass

if __name__ == "__main__":
    dates = pd.read_excel("swap_cashflow_dates.xlsx")
    soft_series = pd.read_excel("sofr_series.xlsx")

    disc_factor = DiscountFactor(soft_series, dates)

    disc_factor.get_days_between()
    disc_factor.days_before_after_loader()
    res = disc_factor.interporlate_sofrs()
    print(res)