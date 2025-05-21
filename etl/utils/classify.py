def classify_category(title):
    """
    Classifies the job category based on the job title by matching it with predefined rules.
    - Categories include: Product, Management, Data, Engineering, UX, Design, Marketing, and Other.

    Args:
        title (str): The job title string.

    Returns:
        str: The job category, such as 'Product', 'Management', 'Data', etc.
    """

    category_rules = [
        ('Product', ['product manager', 'product owner', 'scrum master']),
        ('Management', ['vp', 'chief', 'head of', 'cto', 'ceo', 'director']),
        ('Data', ['data scientist', 'machine learning', 'ai', 'data engineer', 'big data']),
        ('Engineering', [
            'software engineer', 
            'backend', 
            'frontend',
            'fullstack',
            'python',
            'java'
        ]),
        ('UX', ['ux designer', 'user experience', 'interaction design']),
        ('Design', ['graphic designer', 'ui designer', 'visual designer']),
        ('Marketing', ['seo specialist', 'content creator', 'growth hacker']),
        ('Other', [])
    ]

    title_lower = title.lower().strip()
    
    for category, phrases in category_rules:
        for phrase in phrases:
            if phrase in title_lower:
                return category
    
    keyword_mapping = {
        'manager': 'Management',
        'director': 'Management',
        'engineer': 'Engineering',
        'developer': 'Engineering',
        'designer': 'Design',
        'data': 'Data',
        'analyst': 'Data',
        'ux': 'UX',
        'ui': 'Design',
        'marketing': 'Marketing',
        'product': 'Product',
        'scientist': 'Data'
    }
    
    for word in title_lower.split():
        if word in keyword_mapping:
            return keyword_mapping[word]
    
    return 'Other'


import re

seniority_keywords = {
    "Intern": ["intern"],
    "Trainee": ["trainee"],
    "Junior": ["jr", "junior", "entry level"],
    "Mid": ["mid", "intermediate", "associate"],
    "Senior": ["sr", "senior", "expert", "advanced"],
    "Lead": ["lead", "principal"],
}


def classify_seniority(raw_seniority: str) -> str:
    """
    Classify a job seniority level based on keywords found in the input string.

    Parameters:
    -----------
    raw_seniority : str
        The raw job seniority description (e.g., from a job title or metadata).

    Returns:
    --------
    str
        A standardized seniority level such as 'Junior', 'Mid', 'Senior', etc.,
        or 'Other' if no match is found or the input is invalid.

    Notes:
    ------
    The function uses a predefined dictionary `seniority_keywords` where each
    seniority level maps to a list of associated keywords. The input is matched
    against these keywords using case-insensitive regex with word boundaries.
    """
    if not isinstance(raw_seniority, str):
        return "Other"

    raw = raw_seniority.lower().strip()

    for level, keywords in seniority_keywords.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", raw):
                return level

    return "Other"
