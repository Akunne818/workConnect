from flask import redirect, url_for, session
from flask import request, jsonify
import os
import uuid
from flask import flash, abort, redirect, url_for, make_response
import subprocess
from models import storage
from models.jobSeeker import JobSeeker as User
from models.job import Job
from flask import Flask, render_template, request
from jinja2 import Environment, select_autoescape
from datetime import datetime, timedelta
from flask import jsonify
from builtins import set as built_in_set
from models.engine.auth import Auth
from sqlalchemy.orm.exc import NoResultFound
from email.message import EmailMessage
from email.mime.text import MIMEText
import ssl
import smtplib
import requests
from bs4 import BeautifulSoup
import re


AUTH = Auth()


app = Flask(__name__)
app.jinja_env.globals.update(datetime=datetime)

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Number of jobs per page
# Number of jobs per page
JOBS_PER_PAGE = 10

# Function to fetch and format jobs
def fetch_jobs():
    url = "https://remoteok.io/api"
    response = requests.get(url)
    jobs = response.json()[1:]  # Skip metadata (first element)

    # Sort jobs by position and date posted
    sorted_jobs = sorted(jobs, key=lambda job: (job.get('position'), job.get('date')))

    All_jobs = []
    for job in sorted_jobs:
        if not job.get('position'):
            continue
        description = re.sub(r'<[^>]*>', '', job.get('description', ''))
        All_jobs.append({
            'title': job.get('position'),
            'company': job.get('company'),
            'date': datetime.strptime(job.get('date'), '%Y-%m-%dT%H:%M:%S+00:00').strftime('%B %d, %Y'),
            'description': description,
            'categories': job.get('categories'),
            'tags': job.get('tags'),
            'type': job.get('type'),
            'location': job.get('location'),
            'company_logo': job.get('company_logo'),
            'company_url': job.get('company_url'),
            'source': job.get('source'),
            'source_url': job.get('source_url'),
            'apply_url': job.get('url'),
        })

    return All_jobs


# Main route to render the template
@app.route('/', methods=['GET'])
def index():
    # Load the first page initially
    All_jobs = fetch_jobs()[:JOBS_PER_PAGE]
    total_jobs = len(fetch_jobs())
    total_pages = (total_jobs // JOBS_PER_PAGE) + (1 if total_jobs % JOBS_PER_PAGE else 0)

    return render_template('index.html', All_jobs=All_jobs, total_pages=total_pages)

# API endpoint to return jobs for a specific page
@app.route('/jobs', methods=['GET'])
def jobs():
    page = request.args.get('page', 1, type=int)
    jobs = fetch_jobs()

    # Calculate start and end indices for jobs on the current page
    start = (page - 1) * JOBS_PER_PAGE
    end = start + JOBS_PER_PAGE
    paginated_jobs = jobs[start:end]

    return jsonify(paginated_jobs)



@app.route('/UserProfile/<session_id>', strict_slashes=False)
def UserProfile(session_id):
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(401)
    M_invoice = []
    invoices = storage.getInvoice(Invoice, user.id)
    for invoice in invoices:
        n_invoice = storage.get(Invoice, invoice)
        M_invoice.append(n_invoice)
    M_invoice = sorted(M_invoice, key=lambda x: x.created_at, reverse=True)
    return render_template('profile.html', user=user, M_invoice=M_invoice)


@app.route('/logout/<session_id>', strict_slashes=False)
def logout(session_id):
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for('index'))
    abort(403)

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Profile route"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    abort(403)

@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login route"""

    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            user = AUTH.get_user_from_session_id(session_id)

            # Set the session ID as a cookie in the response
            response = make_response(
                jsonify({"email": email, "user_id": user.id}))
            response.set_cookie("session_id", session_id)

            return jsonify({"session_id": session_id})

        # Incorrect login information
        return abort(401)

    except NoResultFound:
        # User not found
        return jsonify({"message": "User not found"}), 401

@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """get reset password token"""
    email = request.form.get('email')
    if email:
        try:
            reset_token = AUTH.get_reset_password_token(email)
            return (
                jsonify({"email": email, "reset_token": reset_token}), 200)
        except ValueError:
            abort(403)

@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """update password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    if email and reset_token and new_password:
        try:
            AUTH.update_password(reset_token, new_password)
            return (jsonify({"email": email,
                             "message": "Password updated"}), 200)
        except Exception:
            abort(403)

# Function to scrape full job description
def scrape_full_job_description(url):
    try:
        # Send a GET request to the job page
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content using the built-in HTML parser
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the section with class 'adp-body' (full job description)
            job_body_section = soup.find(class_='adp-body')

            if job_body_section:
                # Extract the text from the 'adp-body' section
                full_description = job_body_section.get_text(separator="\n").strip()
                return full_description
            else:
                return "Full description not available."
        else:
            return f"Failed to scrape the job page. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred while scraping the job page: {str(e)}"

# Function to fetch jobs from Adzuna API with pagination
def get_adzuna_jobs(page):
    base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": "60b518a4",  # Replace with your actual App ID
        "app_key": "6057c7ba906685ecc7ac88fd2e744047",  # Replace with your actual App Key
        "results_per_page": 10,  # Number of results to return per page
        "page": page,  # Page number for pagination
        "what": "python developer",  # Keyword for job search
        "where": "remote",  # Location for the job search (e.g., remote)
        "sort_by": "date"  # Sort jobs by the most recent
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)