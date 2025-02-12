import numpy as np
from scipy.stats import linregress
from pylatex import Document, Tabular, NoEscape
from pdf2image import convert_from_path

def correct(x):
    if x.is_integer():
        return int(x)
    return x
def generate_latex_document(x_values, y_values):
    doc = Document()
    
    doc.packages.append(NoEscape(r'\usepackage{graphicx}'))  # Required for resizebox
    doc.packages.append(NoEscape(r'\usepackage{amsmath}'))
    
    doc.append(NoEscape(r'\renewcommand{\arraystretch}{2}'))
    
    x_mean = round(np.mean(x_values),4)
    y_mean = round(np.mean(y_values),4)
    x_var = round(np.var(x_values),4)
    y_var = round(np.var(y_values),4)
    corr_coef = round(np.corrcoef(x_values, y_values)[0, 1],4)
    reg_coef = round(round((np.sum((x_values-x_mean)*(y_values-y_mean)))/len(y_values),4)/x_var,4)
    doc.append(NoEscape(r'\resizebox{1.2\textwidth}{!}{%'))  # Resize to 75% of text width
    with doc.create(Tabular('c|' + 'c|' * 7 )) as table:
        # Column labels
        table.add_hline()
        table.add_row([NoEscape(r'i'),NoEscape(r'$x_i$'),NoEscape(r'$y_i$'),
                       NoEscape(r'$x_i-\overline{x}$'),NoEscape(r'$y_i-\overline{y}$'),
                       NoEscape(r'$(x_i-\overline{x})(y_i-\overline{y})$'),
                       NoEscape(r'$(x_i-\overline{x})^2$'),NoEscape(r'$(y_i-\overline{y})^2$')])
        table.add_hline()

        # Table data with row sums
        for idx, (x, y) in enumerate(zip(x_values,y_values)):
            table.add_row([idx+1,x,y,round(x-x_mean,4),round(y-y_mean,4),round((x-x_mean)*(y-y_mean),4),round((x-x_mean)**2,4),round((y-y_mean)**2,4)])
        table.add_hline()

        # Column sums and Sigma symbol
        table.add_row([NoEscape(r'$\Sigma$')] + [round(np.sum(x_values),4),round(np.sum(y_values),4),
                                                 round(np.sum(x_values-x_mean),4),
                                                 round(np.sum(y_values-y_mean),4),
                                                 round(np.sum((x_values-x_mean)*(y_values-y_mean)),4),
                                                 round(np.sum((x_values-x_mean)**2),4),
                                                 round(np.sum((y_values-y_mean)**2),4)])
        table.add_hline()
    doc.append(NoEscape(r'}\\'))  # Close resizebox
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'\Large $\overline{x}=\frac{%s}{%s}=%s$' % (round(np.sum(x_values),4),len(x_values),x_mean)))
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'\Large $\overline{y}=\frac{%s}{%s}=%s$' % (round(np.sum(y_values),4),len(y_values),y_mean)))
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'\Large $Cov(x,y)=\frac{1}{n}\Sigma(x_i-\overline{x})(y_i-\overline{y})=\frac{%s}{%s}=%s$' % (round(np.sum((x_values-x_mean)*(y_values-y_mean)),4),len(y_values),round((np.sum((x_values-x_mean)*(y_values-y_mean)))/len(y_values),4))))
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'\Large $Var(x)=\frac{1}{n}\Sigma{(x_i-\overline{x})}^2=\frac{%s}{%s}=%s$' % (round(np.sum((x_values-x_mean)**2),4),len(y_values),x_var)))
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'\Large $Var(y)=\frac{1}{n}\Sigma{(y_i-\overline{y})}^2=\frac{%s}{%s}=%s$' % (round(np.sum((y_values-y_mean)**2),4),len(y_values),y_var)))
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'\Large $Kor(x,y)=\frac{Cov(x,y)}{\sqrt{Var(x)Var(y)}}=\frac{%s}{\sqrt{%s \cdot %s}}=%s$' % (round((np.sum((x_values-x_mean)*(y_values-y_mean)))/len(y_values),4),x_var,y_var,corr_coef)))
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'\Large $koef. regresije=\frac{Cov(x,y)}{Var(x)}=\frac{%s}{%s}=%s$' % (round((np.sum((x_values-x_mean)*(y_values-y_mean)))/len(y_values),4),x_var,reg_coef)))
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'\Large \text{jednadžba pravca:}\\'))
    doc.append(NoEscape(r'$y-\overline{y}=\frac{Cov(x,y)}{Var(x)}(x-\overline{x})$\\'))
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'$y-%s=%s(x-%s)$\\' % (y_mean,reg_coef,x_mean)))
    doc.append(NoEscape(r'\\[1em]'))
    if (y_mean-reg_coef*x_mean) > 0:
        doc.append(NoEscape(r'$y=%sx+%s$' %(reg_coef,round(y_mean-reg_coef*x_mean,4))))
    else:
        doc.append(NoEscape(r'$y=%sx%s$' %(reg_coef,round(y_mean-reg_coef*x_mean,4))))
    doc.generate_pdf('linear_regression', clean_tex=False)
    image = convert_from_path('linear_regression.pdf')
    image[0].save('linear_regression.png','PNG')

# Example usage
if __name__ == "__main__":
    x_values = []
    y_values = []

    print("Enter the x values (space-separated numbers):")
    row = input().strip()
    x_values.append([float(x.strip()) for x in row.split()])
    x_values = np.round(np.array(x_values).flatten(),2)
    print("Enter the y values (space-separated numbers):")
    row = input().strip()
    y_values.append([float(x.strip()) for x in row.split()])
    y_values = np.round(np.array(y_values).flatten(),2)

    generate_latex_document(x_values,y_values)



