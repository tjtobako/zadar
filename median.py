import numpy as np
from scipy.stats import chi2_contingency, chisquare, chi2
from pylatex import Document, Tabular, NoEscape
from pdf2image import convert_from_path
import math
def generate_latex_document(values, frequencies):
    doc = Document()
    for value in values:
        if value.is_integer():
            value = int(value)
    doc.packages.append(NoEscape(r'\usepackage{graphicx}'))  # Required for resizebox
    doc.packages.append(NoEscape(r'\usepackage{amsmath}'))
    
    doc.append(NoEscape(r'\renewcommand{\arraystretch}{1.5}'))

    col_labels = ["x", "frekvencije"]
    full_array = np.repeat(values,frequencies)
    mean = round(np.mean(full_array),2)
    var = round(np.var(full_array),2)
    std_dev = math.sqrt(var)
    # Observed Frequencies Table
    doc.append(NoEscape(r'\textbf{\huge Tablica\\}'))
    doc.append(NoEscape(r'\resizebox{0.4\textwidth}{!}{%'))  # Resize to 75% of text width
    with doc.create(Tabular('|c|c|' )) as table:
        # Column labels
        table.add_hline()
        table.add_row(col_labels)
        table.add_hline()

        # Table data with row sums
        for value, freq in zip(values.astype(int),frequencies.astype(int)):
            table.add_row([value,freq])
            table.add_hline()

    doc.append(NoEscape(r'}'))  # Close resizebox
    numerator_terms = ' + '.join(f'{x} \\times {f}' for x, f in zip(values, frequencies))
    doc.append(NoEscape(r'\Large \[ \text{x} = \frac{'))
    doc.append(NoEscape(numerator_terms))
    doc.append(NoEscape(r'}{'))
    denominator = ' + '.join(map(str, frequencies))
    doc.append(NoEscape(denominator))
    doc.append(NoEscape(r'} = %s\]'% (mean)))
    #for value,freq in zip()
    doc.generate_pdf('median', clean_tex=False)
    image = convert_from_path('median.pdf')
    image[0].save('median.png','PNG')

# Example usage
if __name__ == "__main__":
    values = []
    freqs = []

    print("Enter the values (space-separated numbers):")
    row = input().strip()
    values.append([float(x.strip()) for x in row.split()])
    values = np.array(values).flatten()
    print("Enter the frequencies of the values (space-separated numbers):")
    row = input().strip()
    freqs.append([int(x.strip()) for x in row.split()])
    freqs = np.array(freqs).flatten()
    print("values:",values)
    print("frequencies:",freqs)
    generate_latex_document(values,freqs)

    print("LaTeX document with tables generated as 'chi_square_test_report.pdf'")

