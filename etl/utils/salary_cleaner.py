import re

def clean_salary(salary):
    """
    Cleans a salary string by removing non-numeric characters and averaging values if multiple salary 
    figures are provided. Returns a float representing the cleaned salary value.

    Args:
        salary (str): The salary value as a string, which may include non-numeric characters.

    Returns:
        float or None: The cleaned salary value as a float, or None if cleaning fails.
    """
    if not salary or salary.strip() == '' or salary.lower() == 'nan':
        return None  
    
    print(f"Limpiando salario: {salary}")
    
    salary = re.sub(r'[^\d\.,\- ]', '', salary)  
    
    salary_numbers = re.findall(r'\d+[\.,]?\d*', salary) 
    
    if len(salary_numbers) >= 2:
        try:
    
            salary = sum([float(num.replace(',', '').strip()) for num in salary_numbers]) / len(salary_numbers)
        except ValueError:
            return None  
    
    elif len(salary_numbers) == 1:
        try:
            salary = float(salary_numbers[0].replace(',', '').strip())
        except ValueError:
            return None  
    else:
        return None  
    
    return salary