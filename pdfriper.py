import re
from pdfminer.high_level import extract_text

def extract_cv_data(pdf_file_path):
    """
    Extracts core details from a CV PDF file.

    Args:
      pdf_file_path: Path to the PDF file.

    Returns:
      A dictionary containing extracted details.
    """

    with open(pdf_file_path, 'rb') as pdf_file:
        # Extract text for all pages
        text = extract_text(pdf_file_path, page_numbers=None)

        # Create a dictionary to store extracted data
        cv_data = {
            'name': None,
            'email': None,
            'phone': None,
            'linkedin': None,
            'github': None,
            'skills': [],
            'experience': [],
            'education': [],
        }

        # Extract name
        name_match = re.search(r'^\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s*$', text, re.MULTILINE)
        if name_match:
            cv_data['name'] = name_match.group(1)

        # Extract email
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        if email_match:
            cv_data['email'] = email_match.group(0)

        # Extract phone number
        phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        if phone_match:
            cv_data['phone'] = phone_match.group(0)

        # Extract LinkedIn profile URL
        linkedin_match = re.search(r'linkedin\.com/in/[a-zA-Z0-9-]+', text)
        if linkedin_match:
            cv_data['linkedin'] = linkedin_match.group(0)

        # Extract Github profile URL
        github_match = re.search(r'github\.com/[a-zA-Z0-9-]+', text)
        if github_match:
            cv_data['github'] = github_match.group(0)

        # Extract skills
        skills_match = re.findall(r'(?i)\b(Skill|Expertise|Proficiency|Knowledge)s?\s*:\s*([\w\s,]+)', text)
        for _, skills_list in skills_match:
            cv_data['skills'].extend(skills_list.split(', '))

        # Extract experience
        experience_match = re.findall(r'(?i)\b(Experience|Work\s+History)\s*:\s*(.*)', text, re.DOTALL)
        for _, experience_text in experience_match:
            # Process and clean experience details
            experience_details = re.findall(r'(.*?)\s*(\d{1,2}\/\d{1,2}\/\d{4}|\d{4})', experience_text, re.DOTALL)
            for detail in experience_details:
                role = detail[0].strip()
                dates = detail[1].strip()
                cv_data['experience'].append({'role': role, 'dates': dates})

        # Extract education
        education_match = re.findall(r'(?i)\b(Education|Academic\s+Background)\s*:\s*(.*)', text, re.DOTALL)
        for _, education_text in education_match:
            # Process and clean education details
            education_details = re.findall(r'(.*?)\s*(\d{1,2}\/\d{1,2}\/\d{4}|\d{4})', education_text, re.DOTALL)
            for detail in education_details:
                degree = detail[0].strip()
                year = detail[1].strip()
                cv_data['education'].append({'degree': degree, 'year': year})

        return cv_data


if __name__ == '__main__':
    pdf_file_path = 'C:\\Users\\ASUS\\Downloads\\Obi_William-FullStack_dev.pdf'  # Replace with the actual path to your CV file
    cv_data = extract_cv_data(pdf_file_path)
    print(cv_data)

