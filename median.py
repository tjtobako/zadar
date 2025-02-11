import numpy as np
from scipy.stats import chi2_contingency, chisquare, chi2
from pylatex import Document, Tabular, NoEscape
from pdf2image import convert_from_path
import math
def correct(x):
    if x.is_integer():
        return int(x)
    return x
def generate_latex_document(values, frequencies):
    doc = Document()
    
    doc.packages.append(NoEscape(r'\usepackage{graphicx}'))  # Required for resizebox
    doc.packages.append(NoEscape(r'\usepackage{amsmath}'))
    
    doc.append(NoEscape(r'\renewcommand{\arraystretch}{1.5}'))

    col_labels = ["x", "frekvencije"]
    full_array = np.repeat(values,frequencies)
    mean = round(np.mean(full_array),2)
    var = round(np.var(full_array),2)
    std_dev = round(math.sqrt(var),2)
    # Observed Frequencies Table
    doc.append(NoEscape(r'\textbf{\huge Tablica\\}'))
    doc.append(NoEscape(r'\resizebox{0.4\textwidth}{!}{%'))  # Resize to 75% of text width
    with doc.create(Tabular('|c|c|' )) as table:
        # Column labels
        table.add_hline()
        table.add_row(col_labels)
        table.add_hline()

        # Table data with row sums
        for value, freq in zip(values.astype(float),frequencies.astype(int)):
            table.add_row([correct(value),freq])
            table.add_hline()

    doc.append(NoEscape(r'}'))  # Close resizebox
    numerator_terms = ' + '.join(f'{f} \\times {correct(x)}' for f, x in zip(frequencies, values))
    doc.append(NoEscape(r'\Large \[ \overline{x} = \frac{'))
    doc.append(NoEscape(numerator_terms))
    doc.append(NoEscape(r'}{'))
    denominator = ' + '.join(map(str, frequencies))
    doc.append(NoEscape(denominator))
    doc.append(NoEscape(r'} = %s\] \\'% (correct(mean))))
    if len(full_array)%2==0:
        doc.append(NoEscape(r'Medijan je $\frac{1}{2} \cdot x_{(%s)}+\frac{1}{2} \cdot x_{(%s)}=%s$ \\' % (int(len(full_array)/2),int(len(full_array)/2+1),int(np.median(full_array)))))
    else:
        doc.append(NoEscape(r'Medijan je $x_{(%s)}=%s$ \\' % (int((len(full_array)+1)/2),int(np.median(full_array)))))
    
    doc.append(NoEscape(r'\begin{align*}'))
    doc.append(NoEscape(r'\hspace*{-\leftmargin} '))
    numerator_terms = ' + '.join(f'{f}\\! \\cdot \\!({correct(x)}\\!-\\!{correct(mean)})^2' for f, x in zip(frequencies, values))
    doc.append(NoEscape(r'\text{var} &= \frac{'))
    doc.append(NoEscape(numerator_terms))
    doc.append(NoEscape(r'}{'))
    denominator = ' + '.join(map(str, frequencies))
    doc.append(NoEscape(denominator))
    doc.append(NoEscape(r'}'))
    doc.append(NoEscape(r'\\'))
    doc.append(NoEscape(r'&= %s'% (correct(var))))
    doc.append(NoEscape(r'\end{align*}'))
    doc.append(NoEscape(r'\text{std. devijacija} $= \sqrt{%s} = %s$ \\' % (correct(var), std_dev)))
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



