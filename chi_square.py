import numpy as np
from scipy.stats import chi2_contingency, chisquare, chi2
from pylatex import Document, Tabular, NoEscape
from pdf2image import convert_from_path

def chi_square_test(observed, expected=None, alpha=0.05):
    """
    Perform a chi-square test on the provided data.
    
    Parameters:
    observed: array-like
        For independence test: 2D contingency table
        For goodness of fit: 1D array of observed frequencies
    expected: array-like, optional
        Expected frequencies (only for goodness of fit test)
    alpha: float, optional
        Significance level (default 0.05)
        
    Returns:
    dict: Contains test statistics, p-value, and test conclusion
    """
    try:
        # Check if we're doing an independence test (2D array)
        if isinstance(observed, (list, np.ndarray)) and np.array(observed).ndim == 2:
            # Perform chi-square test of independence
            chi2_stat, p_value, dof, expected = chi2_contingency(observed)
            test_type = "independence"
        else:
            if expected is None:
                # If no expected frequencies provided, assume uniform distribution
                expected = np.ones_like(observed) * np.sum(observed) / len(observed)
            chi2_stat, p_value = chisquare(observed, expected)
            dof = len(observed) - 1
            test_type = "goodness of fit"
        
        # Prepare results
        result = {
            'test_type': test_type,
            'chi2_statistic': chi2_stat,
            'p_value': p_value,
            'degrees_of_freedom': dof,
            'significant': p_value < alpha,
            'alpha': alpha,
            'observed': np.array(observed),
            'expected': np.array(expected)
        }
        
        return result
    
    except Exception as e:
        raise ValueError(f"Error performing chi-square test: {str(e)}")

def generate_latex_document(observed, expected,chi_squared,dof,alpha, row_labels, col_labels):
    """
    Generate a LaTeX document containing tables for observed and expected frequencies.
    
    Parameters:
    observed: np.array
        Observed frequencies table
    expected: np.array
        Expected frequencies table
    row_labels: list of str
        Labels for the rows
    col_labels: list of str
        Labels for the columns
    """
    doc = Document()
    doc.packages.append(NoEscape(r'\usepackage{graphicx}'))  # Required for resizebox
    doc.packages.append(NoEscape(r'\usepackage{amsmath}'))
    
    doc.append(NoEscape(r'\title{Chi-Square Test Report}'))
    #doc.append(NoEscape(r'\maketitle'))

    # Increase table row height
    doc.append(NoEscape(r'\renewcommand{\arraystretch}{1.5}'))

    # Compute row sums, column sums, and grand total
    row_sums = np.sum(observed, axis=1)
    col_sums = np.sum(observed, axis=0)
    grand_total = np.sum(observed)

    # Observed Frequencies Table
    doc.append(NoEscape(r'\textbf{\huge Tablica pravih vrijednosti\\}'))
    doc.append(NoEscape(r'\resizebox{0.4\textwidth}{!}{%'))  # Resize to 75% of text width
    with doc.create(Tabular('|c|' + 'c' * observed.shape[1] + '|c|')) as table:
        # Column labels
        table.add_hline()
        table.add_row([''] + col_labels + [NoEscape(r'$\Sigma$')])
        table.add_hline()

        # Table data with row sums
        for label, row, row_sum in zip(row_labels, observed.astype(int), row_sums):
            table.add_row([label] + list(row) + [row_sum])
            table.add_hline()

        # Column sums and Sigma symbol
        table.add_row([NoEscape(r'$\Sigma$')] + list(col_sums) + [grand_total])
        table.add_hline()
    doc.append(NoEscape(r'}'))  # Close resizebox

    doc.append(NoEscape(r'\\\\\\'))  # Space between tables
    doc.append(NoEscape(r'\renewcommand{\arraystretch}{1.5}'))
    
    # Expected Frequencies Table
    doc.append(NoEscape(r'\textbf{\huge Tablica očekivanih vrijednosti}\\'))
    doc.append(NoEscape(r'\resizebox{0.4\textwidth}{!}{%'))  # Resize to 75% of text width
    table_data = expected.round(2).astype(str).tolist()
    with doc.create(Tabular('|c|' + 'c' * expected.shape[1] + '|')) as table:
        table.add_hline()
        table.add_row([''] + col_labels)
        table.add_hline()
        for label, row in zip(row_labels, table_data):
            table.add_row([label] + list(row))
            table.add_hline()
    doc.append(NoEscape(r'}'))  # Close resizebox
    doc.append(NoEscape(r'\vspace{10pt}'))
    doc.append(NoEscape(r'\\[1em]'))
    # Add the formula for chi-squared test statistic: 
    doc.append(NoEscape(r'\Large $\chi^2 = \sum \frac{(PRAVE - OČEKIVANE)^2}{OČEKIVANE}$'))
    
    # Add the calculation for each observed and expected frequency
    #doc.append(NoEscape(r'\vspace{10pt}'))
    doc.append(NoEscape(r'\\[1em]'))

    # For displaying the fraction for each pair of observed and expected values
    doc.append(NoEscape(r'\begin{equation*}'))
    doc.append(NoEscape(r'\begin{aligned}'))
    doc.append(NoEscape('&='))
    line_length = 0  # Keep track of terms per line

    for i, (o, e) in enumerate(zip(observed.flatten(), expected.flatten().round(2))):
        # Append the fraction
        fraction = r' \frac{(' + str(o) + ' - ' + str(e) + ')^2}{' + str(e) + '}'

        # Check if it's the last element to avoid trailing '+'
        if i != len(observed.flatten()) - 1:
            fraction += ' +'

        # Add a line break after 3 terms
        if line_length >= 2:
            doc.append(NoEscape(fraction + r' \\&'))
            line_length = 0
        else:
            doc.append(NoEscape(fraction))
            line_length += 1       
    doc.append(NoEscape(r'=' + str(chi_squared)))
    doc.append(NoEscape(r'\end{aligned}'))
    doc.append(NoEscape(r'\end{equation*}'))
    
    

    doc.append(NoEscape(r'\vspace{10pt}'))
    doc.append(NoEscape(r'\\[1em]'))
    
    doc.append(NoEscape(r'\Large Broj stupnjeva slobode jednak je $(%s - 1) \times (%s - 1)$ = %s.' % (observed.shape[1], observed.shape[0], dof)))
    
    doc.append(NoEscape(r'\\'))
    
    doc.append(NoEscape(r'\Large Razina značajnosti $\alpha$ = %s.' % (alpha)))
    doc.append(NoEscape(r'\\'))
#chi2.ppf(1 - alpha, df)
    critical_value = chi2.ppf(1 - alpha, dof).round(2)
    doc.append(NoEscape(r'\Large Iz tablice iščitamo kritičnu vrijednost $\chi^2_{(%s)}$ = %s.' % (1-alpha,critical_value)))
    doc.append(NoEscape(r'\\'))
    if chi_squared >= critical_value:
        doc.append(NoEscape(r'\Large Jer je $\chi^2=$%s > %s, odbacujemo nul hipotezu o jednakosti distribucija na razini značajnosti $\alpha$=%s.'%(chi_squared,critical_value,alpha)))
    else:
        doc.append(NoEscape(r'\Large Jer je $\chi^2=$%s < %s, ne možemo odbaciti nul hipotezu o jednakosti distribucija.'%(chi_squared,critical_value)))
    doc.generate_pdf('chi_square', clean_tex=False)
    image = convert_from_path('chi_square.pdf')
    image[0].save('chi_square.png','PNG')

# Example usage
if __name__ == "__main__":
    # Example for homogeneity test
    population_data = []
    print("Enter data for each population row (space-separated numbers):")
    print("Enter blank line when done")
    while True:
        row = input().strip()
        if not row:
            break
        population_data.append([int(x.strip()) for x in row.split()])
    
    population_data = np.array(population_data)

    # Perform the test and generate LaTeX document
    chi2_stat, p_value, dof, expected = chi2_contingency(population_data)
    result = chi_square_test(population_data)
    print("hi-kvadrat:",chi2_stat)
    print("\nObserved Frequencies:")
    print(np.array(population_data))
    print("\nExpected Frequencies:")
    print(expected.round(2))  # Rounded to 2 decimal places for readability

    print("\nEnter row labels (one per row, separated by spaces):")
    row_labels = input().split(" ")

    print("\nEnter column labels (one per column, separated by spaces):")
    col_labels = input().split(" ")
    print("\nEnter the significance level alpha (in the range [0,1]):")
    alpha = float(input())
    # Generate LaTeX document with tables
    generate_latex_document(result['observed'], result['expected'],chi2_stat.round(2),dof,alpha,row_labels, col_labels)

    print("LaTeX document with tables generated as 'chi_square_test_report.pdf'")

