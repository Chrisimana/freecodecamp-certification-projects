import math
import tkinter as tk
from tkinter import ttk, messagebox
import re

class FinancialCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Financial Calculator")
        self.root.geometry("600x500")
        self.setup_ui()
    
    def setup_ui(self):
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        
        # Create tabs
        self.tab_annuity = ttk.Frame(self.notebook)
        self.tab_mortgage = ttk.Frame(self.notebook)
        self.tab_retirement = ttk.Frame(self.notebook)
        self.tab_doubling_time = ttk.Frame(self.notebook)
        self.tab_logarithm = ttk.Frame(self.notebook)
        self.tab_scientific_notation = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.tab_annuity, text="Annuity Calculator")
        self.notebook.add(self.tab_mortgage, text="Mortgage Calculator")
        self.notebook.add(self.tab_retirement, text="Retirement Calculator")
        self.notebook.add(self.tab_doubling_time, text="Doubling Time")
        self.notebook.add(self.tab_logarithm, text="Logarithm Equation")
        self.notebook.add(self.tab_scientific_notation, text="Scientific Notation")
        
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Setup each tab
        self.setup_tab_annuity()
        self.setup_tab_mortgage()
        self.setup_tab_retirement()
        self.setup_tab_doubling_time()
        self.setup_tab_logarithm()
        self.setup_tab_scientific_notation()
        
        # Output area
        self.frame_output = ttk.Frame(self.root)
        self.frame_output.pack(fill='x', padx=10, pady=5)
        
        self.text_output = tk.Text(self.frame_output, height=4, width=70)
        self.scroll_output = ttk.Scrollbar(self.frame_output, orient='vertical', command=self.text_output.yview)
        self.text_output.configure(yscrollcommand=self.scroll_output.set)
        
        self.text_output.pack(side='left', fill='both', expand=True)
        self.scroll_output.pack(side='right', fill='y')
    
    def setup_tab_annuity(self):
        # Annuity Calculator Widgets
        ttk.Label(self.tab_annuity, text="Annuity Calculator", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # PV Input
        frame_pv = ttk.Frame(self.tab_annuity)
        frame_pv.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_pv, text="Present Value (PV):").pack(side='left')
        self.var_pv = tk.StringVar(value="0")
        self.entry_pv = ttk.Entry(frame_pv, textvariable=self.var_pv, width=15)
        self.entry_pv.pack(side='right')
        
        # PMT Input
        frame_pmt = ttk.Frame(self.tab_annuity)
        frame_pmt.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_pmt, text="Periodic Payment (PMT):").pack(side='left')
        self.var_pmt = tk.StringVar(value="0")
        self.entry_pmt = ttk.Entry(frame_pmt, textvariable=self.var_pmt, width=15)
        self.entry_pmt.pack(side='right')
        
        # Interest Rate Input
        frame_rate = ttk.Frame(self.tab_annuity)
        frame_rate.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_rate, text="Interest Rate (%):").pack(side='left')
        self.var_rate = tk.StringVar(value="5")
        self.entry_rate = ttk.Entry(frame_rate, textvariable=self.var_rate, width=15)
        self.entry_rate.pack(side='right')
        
        # Period Input
        frame_period = ttk.Frame(self.tab_annuity)
        frame_period.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_period, text="Period (months):").pack(side='left')
        self.var_period = tk.StringVar(value="12")
        self.entry_period = ttk.Entry(frame_period, textvariable=self.var_period, width=15)
        self.entry_period.pack(side='right')
        
        # Compounding Dropdown
        frame_compounding = ttk.Frame(self.tab_annuity)
        frame_compounding.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_compounding, text="Compounding:").pack(side='left')
        self.var_compounding = tk.StringVar(value="monthly")
        self.combo_compounding = ttk.Combobox(frame_compounding, textvariable=self.var_compounding, 
                                            values=['monthly', 'continuous'], width=12, state='readonly')
        self.combo_compounding.pack(side='right')
        
        # Calculate button and result
        ttk.Button(self.tab_annuity, text="Calculate Future Value", command=self.calculate_future_value).pack(pady=10)
        
        self.var_result_fv = tk.StringVar(value="Future Value: Rp0.00")
        ttk.Label(self.tab_annuity, textvariable=self.var_result_fv, font=('Arial', 10)).pack(pady=5)
    
    def setup_tab_mortgage(self):
        ttk.Label(self.tab_mortgage, text="Mortgage Calculator", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Loan Principal Input
        frame_principal = ttk.Frame(self.tab_mortgage)
        frame_principal.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_principal, text="Loan Amount:").pack(side='left')
        self.var_principal = tk.StringVar(value="200000000")
        self.entry_principal = ttk.Entry(frame_principal, textvariable=self.var_principal, width=15)
        self.entry_principal.pack(side='right')
        
        # Interest Rate Input
        frame_rate_mortgage = ttk.Frame(self.tab_mortgage)
        frame_rate_mortgage.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_rate_mortgage, text="Interest Rate (%):").pack(side='left')
        self.var_rate_mortgage = tk.StringVar(value="4.5")
        self.entry_rate_mortgage = ttk.Entry(frame_rate_mortgage, textvariable=self.var_rate_mortgage, width=15)
        self.entry_rate_mortgage.pack(side='right')
        
        # Term Input
        frame_term = ttk.Frame(self.tab_mortgage)
        frame_term.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_term, text="Years:").pack(side='left')
        self.var_term = tk.StringVar(value="30")
        self.entry_term = ttk.Entry(frame_term, textvariable=self.var_term, width=15)
        self.entry_term.pack(side='right')
        
        # Calculate button and result
        ttk.Button(self.tab_mortgage, text="Calculate Monthly Payment", command=self.calculate_mortgage).pack(pady=10)
        
        self.var_result_installment = tk.StringVar(value="Monthly Payment: Rp0.00")
        ttk.Label(self.tab_mortgage, textvariable=self.var_result_installment, font=('Arial', 10)).pack(pady=5)
    
    def setup_tab_retirement(self):
        ttk.Label(self.tab_retirement, text="Retirement Calculator", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Initial Investment
        frame_initial_investment = ttk.Frame(self.tab_retirement)
        frame_initial_investment.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_initial_investment, text="Initial Investment:").pack(side='left')
        self.var_initial_investment = tk.StringVar(value="10000000")
        self.entry_initial_investment = ttk.Entry(frame_initial_investment, textvariable=self.var_initial_investment, width=15)
        self.entry_initial_investment.pack(side='right')
        
        # Monthly Contribution
        frame_contribution = ttk.Frame(self.tab_retirement)
        frame_contribution.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_contribution, text="Monthly Contribution:").pack(side='left')
        self.var_contribution = tk.StringVar(value="500000")
        self.entry_contribution = ttk.Entry(frame_contribution, textvariable=self.var_contribution, width=15)
        self.entry_contribution.pack(side='right')
        
        # Rate of Return Input
        frame_return_rate = ttk.Frame(self.tab_retirement)
        frame_return_rate.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_return_rate, text="Rate of Return (%):").pack(side='left')
        self.var_return_rate = tk.StringVar(value="7")
        self.entry_return_rate = ttk.Entry(frame_return_rate, textvariable=self.var_return_rate, width=15)
        self.entry_return_rate.pack(side='right')
        
        # Years Input
        frame_years_retirement = ttk.Frame(self.tab_retirement)
        frame_years_retirement.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_years_retirement, text="Years:").pack(side='left')
        self.var_years_retirement = tk.StringVar(value="30")
        self.entry_years_retirement = ttk.Entry(frame_years_retirement, textvariable=self.var_years_retirement, width=15)
        self.entry_years_retirement.pack(side='right')
        
        # Calculate button and result
        ttk.Button(self.tab_retirement, text="Calculate Balance", command=self.calculate_retirement).pack(pady=10)
        
        self.var_retirement_balance = tk.StringVar(value="Future Balance: Rp0.00")
        ttk.Label(self.tab_retirement, textvariable=self.var_retirement_balance, font=('Arial', 10)).pack(pady=5)
    
    def setup_tab_doubling_time(self):
        ttk.Label(self.tab_doubling_time, text="Doubling Time Calculator", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Interest Rate Input
        frame_rate_doubling = ttk.Frame(self.tab_doubling_time)
        frame_rate_doubling.pack(fill='x', padx=20, pady=20)
        ttk.Label(frame_rate_doubling, text="Interest Rate (%):").pack(side='left')
        self.var_rate_doubling = tk.StringVar(value="7")
        self.entry_rate_doubling = ttk.Entry(frame_rate_doubling, textvariable=self.var_rate_doubling, width=15)
        self.entry_rate_doubling.pack(side='right')
        
        # Calculate button and result
        ttk.Button(self.tab_doubling_time, text="Calculate", command=self.calculate_doubling_time).pack(pady=10)
        
        self.var_result_doubling_time = tk.StringVar(value="Time to Double: 0 years")
        ttk.Label(self.tab_doubling_time, textvariable=self.var_result_doubling_time, font=('Arial', 10)).pack(pady=5)
    
    def setup_tab_logarithm(self):
        ttk.Label(self.tab_logarithm, text="Logarithm Equation Solver", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Base Input
        frame_base = ttk.Frame(self.tab_logarithm)
        frame_base.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_base, text="Base:").pack(side='left')
        self.var_base_log = tk.StringVar(value="10")
        self.entry_base_log = ttk.Entry(frame_base, textvariable=self.var_base_log, width=15)
        self.entry_base_log.pack(side='right')
        
        # Argument Input
        frame_argument = ttk.Frame(self.tab_logarithm)
        frame_argument.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_argument, text="Argument:").pack(side='left')
        self.var_argument_log = tk.StringVar(value="100")
        self.entry_argument_log = ttk.Entry(frame_argument, textvariable=self.var_argument_log, width=15)
        self.entry_argument_log.pack(side='right')
        
        # Calculate button and result
        ttk.Button(self.tab_logarithm, text="Calculate", command=self.calculate_logarithm).pack(pady=10)
        
        self.var_result_log = tk.StringVar(value="Result: 0")
        ttk.Label(self.tab_logarithm, textvariable=self.var_result_log, font=('Arial', 10)).pack(pady=5)
    
    def setup_tab_scientific_notation(self):
        ttk.Label(self.tab_scientific_notation, text="Scientific Notation Converter", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Standard Number Input
        frame_standard = ttk.Frame(self.tab_scientific_notation)
        frame_standard.pack(fill='x', padx=20, pady=10)
        ttk.Label(frame_standard, text="Standard Number:").pack(side='left')
        self.var_standard_number = tk.StringVar(value="12345")
        self.entry_standard_number = ttk.Entry(frame_standard, textvariable=self.var_standard_number, width=20)
        self.entry_standard_number.pack(side='right')
        
        # Button frame
        frame_buttons = ttk.Frame(self.tab_scientific_notation)
        frame_buttons.pack(fill='x', padx=20, pady=10)
        ttk.Button(frame_buttons, text="→ Scientific Notation", command=self.to_scientific_notation).pack(side='left', padx=10)
        ttk.Button(frame_buttons, text="← Standard Number", command=self.from_scientific_notation).pack(side='right', padx=10)
        
        # Scientific Notation Input
        frame_scientific = ttk.Frame(self.tab_scientific_notation)
        frame_scientific.pack(fill='x', padx=20, pady=10)
        ttk.Label(frame_scientific, text="Scientific Notation:").pack(side='left')
        self.var_scientific_notation = tk.StringVar()
        self.entry_scientific_notation = ttk.Entry(frame_scientific, textvariable=self.var_scientific_notation, width=20)
        self.entry_scientific_notation.pack(side='right')
    
    def log_output(self, message):
        """Helper method to log messages to the output area"""
        self.text_output.insert('end', message + '\n')
        self.text_output.see('end')
    
    def clear_output(self):
        """Clear the output area"""
        self.text_output.delete('1.0', 'end')
    
    def calculate_future_value(self):
        try:
            pv = float(self.var_pv.get())
            pmt = float(self.var_pmt.get())
            rate = float(self.var_rate.get()) / 100
            n = int(self.var_period.get())
            compounding = self.var_compounding.get()

            if compounding == "monthly":
                r = rate / 12
                fv = pv * (1 + r)**n + pmt * ((1 + r)**n - 1) / r
            else:  # continuous
                fv = pv * math.exp(rate * n/12) + pmt * (math.exp(rate * n/12) - 1) / (math.exp(rate/12) - 1)

            self.var_result_fv.set(f'Future Value: Rp{fv:,.2f}')
            self.log_output(f"Annuity future value calculated: Rp{fv:,.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating future value: {str(e)}")
    
    def calculate_mortgage(self):
        try:
            P = float(self.var_principal.get())
            r = float(self.var_rate_mortgage.get()) / 100 / 12
            n = int(self.var_term.get()) * 12

            if r == 0:  # Handle zero interest rate case
                monthly_installment = P / n
            else:
                monthly_installment = P * (r * (1 + r)**n) / ((1 + r)**n - 1)

            self.var_result_installment.set(f'Monthly Payment: Rp{monthly_installment:,.2f}')
            self.log_output(f"Mortgage payment calculated: Rp{monthly_installment:,.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating mortgage: {str(e)}")
    
    def calculate_retirement(self):
        try:
            P = float(self.var_initial_investment.get())
            C = float(self.var_contribution.get())
            r = float(self.var_return_rate.get()) / 100 / 12
            n = int(self.var_years_retirement.get()) * 12

            if r == 0:  # Handle zero interest rate case
                FV = P + C * n
            else:
                FV = P * (1 + r)**n + C * ((1 + r)**n - 1) / r

            self.var_retirement_balance.set(f'Future Balance: Rp{FV:,.2f}')
            self.log_output(f"Retirement balance calculated: Rp{FV:,.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating retirement balance: {str(e)}")
    
    def calculate_doubling_time(self):
        try:
            rate = float(self.var_rate_doubling.get()) / 100
            if rate <= 0:
                messagebox.showwarning("Warning", "Interest rate must be positive")
                return

            # Rule of 72 as an approximation
            time = 72 / (rate * 100)
            self.var_result_doubling_time.set(f'Time to Double: {time:.2f} years')
            self.log_output(f"Doubling time calculated: {time:.2f} years with interest rate {rate*100}%")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating doubling time: {str(e)}")
    
    def calculate_logarithm(self):
        try:
            base = float(self.var_base_log.get())
            argument = float(self.var_argument_log.get())

            if base <= 0 or base == 1:
                messagebox.showwarning("Warning", "Base must be positive and not equal to 1")
                return
            if argument <= 0:
                messagebox.showwarning("Warning", "Argument must be positive")
                return

            result = math.log(argument, base)
            self.var_result_log.set(f'Result: {result:.4f}')
            self.log_output(f"Log base {base} of {argument} = {result:.4f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating logarithm: {str(e)}")
    
    def to_scientific_notation(self):
        try:
            number = float(self.var_standard_number.get())
            scientific_notation = f"{number:.4e}"
            self.var_scientific_notation.set(scientific_notation)
            self.log_output(f"Converted {number} to scientific notation: {scientific_notation}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def from_scientific_notation(self):
        try:
            # Handle scientific notation (e.g., 1.23e4 or 1.23E4)
            scientific_notation = self.var_scientific_notation.get().lower().replace('×10^', 'e').replace('·10^', 'e')
            number = float(scientific_notation)
            self.var_standard_number.set(f"{number:,}")
            self.log_output(f"Converted {scientific_notation} to standard notation: {number:,}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid scientific notation (e.g., 1.23e4)")
    
    def run(self):
        self.root.mainloop()

# Run the calculator
if __name__ == "__main__":
    print("💰 Financial Calculator")
    print("=========================================")
    print("Comprehensive financial calculator with various tools:")
    print("• Annuity Calculator")
    print("• Mortgage Calculator")
    print("• Retirement Calculator")
    print("• Doubling Time Calculator")
    print("• Logarithm Equation Solver")
    print("• Scientific Notation Converter")
    print()
    
    calculator = FinancialCalculator()
    calculator.run()