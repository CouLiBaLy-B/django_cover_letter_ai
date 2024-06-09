# ResumeAI: Cover Letter Generator

## Overview

ResumeAI is a Django-based web application that harnesses the power of AI to generate high-quality cover letters tailored to specific job descriptions. By combining the user's professional profile with the details of a job posting, ResumeAI crafts personalized cover letters that increase the chances of landing an interview.

## Features

1. **User Authentication**: Secure user registration and login system.
2. **Cover Letter Generation**: AI-powered creation of cover letters based on:
   - User's profile (uploaded as a PDF)
   - Job description (pasted into the application)
3. **Job Title Extraction**: Automatically extracts the job title from the provided job description.
4. **Cover Letter History**: Users can view and manage their previously generated cover letters.
5. **PDF Download**: Generated cover letters can be downloaded as PDFs for easy sharing and application.

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **AI Model**: HuggingFace's `mistralai/MixTraL-8x7B-Instruct-v0.1`
- **PDF Handling**: 
  - `PyPDF2` for extracting text from user profiles
  - `xhtml2pdf` for generating cover letter PDFs
- **Other Libraries**:
  - `langchain` for interacting with the HuggingFace model
  - `decouple` for managing environment variables

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/CouLiBaLy-B/django_cover_letter_ai.git
   cd resumeai
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root.
   - Add your HuggingFace API key:
     ```
     huggingface_api_key=your_api_key_here
     ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

7. Visit `http://localhost:8000` in your browser.

## Usage

1. Register or log in to your account.
2. Upload your professional profile as a PDF.
3. Paste the job description into the provided textarea.
4. Click "Generate" to create your personalized cover letter.
5. Preview, edit (if needed), and download your cover letter as a PDF.
6. Access your cover letter history anytime from the "Saved Blog Posts" link.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here, e.g., MIT License]

## Contact

Developed by [Ibrahim](https://www.linkedin.com/in/bourahima-coulibaly-6bb335218/). Feel free to connect for any queries or collaborations.

---

Note: This README assumes certain project structures and dependencies. Adjust accordingly based on your actual project setup.