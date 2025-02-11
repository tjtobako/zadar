from scipy.stats import norm
from pylatex import Document, Tabular, NoEscape
from pdf2image import convert_from_path
def calculate_normal_probabilities(mean, std_dev, filename):
    doc = Document()
    doc.packages.append(NoEscape(r'\usepackage{graphicx}'))  # Required for resizebox
    doc.packages.append(NoEscape(r'\usepackage{amsmath}'))
    doc.packages.append(NoEscape(r'\usepackage{enumerate}'))
    #doc.append(NoEscape(r'\begin{flushleft}'))
    doc.append(NoEscape(r'\Large $ X \sim N(' + str(mean) + r', ' + str(std_dev) + r'^2) $'))
    #doc.append(NoEscape(r'\end{flushleft}'))
    """
    Calculate probabilities based on a normal distribution.

    Parameters:
    - mean (float): Mean of the normal distribution
    - std_dev (float): Standard deviation of the normal distribution
    """
    doc.append(NoEscape(r'\begin{enumerate}[a)]'))
    print("Enter probability condition (<>, <, >) or blank to exit:")

    while True:
        condition = input("Condition (<> for range, < for less than, > for greater than): ").strip()
        
        if not condition:
            print("Exiting program.")
            break

        if condition == "<>":
            try:
                lower_bound = float(input("Enter lower bound: ").strip())
                if lower_bound.is_integer():
                    lower_bound = int(lower_bound)
                upper_bound = float(input("Enter upper bound: ").strip())
                if upper_bound.is_integer():
                    upper_bound = int(upper_bound)
                z_lower = round((lower_bound-mean)/std_dev,2)
                z_upper = round((upper_bound-mean)/std_dev,2)
                prob_lower = round(norm.cdf(z_lower, 0, 1),4)
                prob_upper = round(norm.cdf(z_upper, 0, 1),4)
                probability = round(prob_upper-prob_lower,4)
                doc.append(NoEscape(r'\Large \item $P(%s < X < %s)$' % (lower_bound, upper_bound)))
                doc.append(NoEscape(r'$=P\left(\frac{%s-%s}{%s} < \frac{X-%s}{%s} < \frac{%s-%s}{%s}\right)$' % (lower_bound,mean,std_dev,mean,std_dev,upper_bound,mean,std_dev)))
                doc.append(NoEscape(r'$=P\left(%s < Z < %s \right)$' % (z_lower,z_upper)))
                doc.append(NoEscape(r'$=\Phi\left( %s \right) - \Phi\left( %s \right)$' % (z_upper, z_lower)))
                doc.append(NoEscape(r'$=%s - %s = %s $' % (prob_upper, prob_lower, probability)))
                if lower_bound >= upper_bound:
                    print("Error: Lower bound should be less than upper bound. Try again.")
                    continue
                print(f"Probability that the variable is between {lower_bound} and {upper_bound}: {probability:.4f}")
            except ValueError:
                print("Invalid input. Please enter numeric values.")

        elif condition == "<":
            try:
                value = float(input("Enter a value: ").strip())
                if value.is_integer():
                    value = int(value)
                z = round((value-mean)/std_dev,2)
                probability = round(norm.cdf(z, 0, 1),4)
                doc.append(NoEscape(r'\item $P(X < %s)$' % (value)))
                doc.append(NoEscape(r'$=P\left(\frac{X-%s}{%s} < \frac{%s-%s}{%s}\right)$' % (mean,std_dev,value,mean,std_dev)))
                doc.append(NoEscape(r'$=P\left(Z < %s \right)=\Phi\left( %s \right)$' % (z,z)))
                doc.append(NoEscape(r'$= %s $' % (probability)))
                print(f"Probability that the variable is less than {value}: {probability:.4f}")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        elif condition == ">":
            try:
                value = float(input("Enter a value: ").strip())
                if value.is_integer():
                    value = int(value)
                z = round((value-mean)/std_dev,2)
                probability = round(1-round(norm.cdf(z, 0, 1),4),4)
                doc.append(NoEscape(r'\item $P(X > %s) = 1 - P(X < %s)$' % (value, value)))
                doc.append(NoEscape(r'$=1-P\left(\frac{X-%s}{%s} < \frac{%s-%s}{%s}\right)$' % (mean,std_dev,value,mean,std_dev)))
                doc.append(NoEscape(r'$=1-P\left(Z < %s \right)$' % (z)))
                doc.append(NoEscape(r'$=1 - \Phi\left( %s \right) =  %s $' % (z,probability)))
                print(f"Probability that the variable is greater than {value}: {probability:.4f}")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
                
        else:
            print("Invalid condition. Please enter one of: <>, <, or >.")
    doc.append(NoEscape(r'\end{enumerate}'))
    doc.generate_pdf(filename, clean_tex=False)
    image = convert_from_path(f'{filename}.pdf')
    image[0].save(f"{filename}.png",'PNG')
if __name__ == "__main__":
    # Get mean and standard deviation
    try:
        mean = float(input("Enter the mean of the normal distribution: ").strip())
        std_dev = float(input("Enter the standard deviation of the normal distribution: ").strip())
        if std_dev <= 0:
            print("Standard deviation must be positive. Exiting.")
        else:
            calculate_normal_probabilities(mean, std_dev, "normal_distribution")
    except ValueError:
        print("Invalid input. Please enter numeric values for mean and standard deviation.")
