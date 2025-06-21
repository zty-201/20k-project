import requests
import time
import urllib.parse
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class IndeedJobScraper:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('HASDATA_API_KEY')
        if not self.api_key:
            raise ValueError("API key not provided and HASDATA_API_KEY not found in environment")
            
        self.base_url = "https://api.hasdata.com/scrape/indeed"
        self.headers = {
            'x-api-key': self.api_key,
            'Content-Type': "application/json"
        }
    
    def search_jobs(self, keywords: str, location: str = "New York, NY", limit: int = 20, start: int = 0) -> List[Dict]:
        """
        Search for jobs on Indeed using the HasData listing API
        
        Args:
            keywords: Search query (e.g., "software engineer", "python developer")
            location: Location to search (e.g., "New York, NY", "Remote")
            limit: Maximum number of jobs to retrieve
            start: Starting index for pagination
            
        Returns:
            List of job dictionaries
        """
        print(f"Searching for '{keywords}' jobs in '{location}'...")
        
        # Use the correct HasData Indeed listing endpoint
        endpoint = f"{self.base_url}/listing"
        
        # Build query parameters
        params = {
            'keyword': keywords,
            'location': location,
            'domain': 'www.indeed.com'
        }
        
        if start > 0:
            params['start'] = start
        
        try:
            # Make API request
            print(f"Making request to: {endpoint}")
            print(f"Parameters: {params}")
            
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=30)
            
            print(f"API Response Status: {response.status_code}")
            
            if response.status_code == 401:
                raise Exception("Invalid API key. Check your HasData API key.")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please wait before making more requests.")
            elif response.status_code != 200:
                print(f"Error response: {response.text}")
                raise Exception(f"API returned status {response.status_code}")
            
            # Parse response
            data = response.json()
            
            # Debug: show response structure
            print("Response structure:")
            if isinstance(data, dict):
                print(f"Response keys: {list(data.keys())}")
            else:
                print(f"Response type: {type(data)}")
            
            # Extract jobs from response
            jobs = self._extract_jobs_from_response(data, limit)
            
            print(f"Successfully extracted {len(jobs)} jobs")
            return jobs
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return []
        except Exception as e:
            print(f"Error searching jobs: {e}")
            return []
    
    def _extract_jobs_from_response(self, data: Dict, limit: int) -> List[Dict]:
        """Extract job data from HasData API response"""
        jobs = []
        
        try:
            # Try different possible response structures
            jobs_data = None
            
            if isinstance(data, dict):
                # Common response structures
                possible_keys = ['jobs', 'results', 'data', 'listings', 'items']
                
                for key in possible_keys:
                    if key in data:
                        jobs_data = data[key]
                        print(f"Found jobs data under key: '{key}'")
                        break
                
                # If no specific key found, maybe the data itself is the jobs list
                if jobs_data is None and isinstance(data, list):
                    jobs_data = data
            
            if not jobs_data:
                print("Could not find jobs data in response")
                print("Full response:", data)
                return []
            
            # Process each job
            for i, job_item in enumerate(jobs_data):
                if i >= limit:
                    break
                    
                if isinstance(job_item, dict):
                    job = self._normalize_job_data(job_item)
                    if job:
                        jobs.append(job)
            
        except Exception as e:
            print(f"Error extracting jobs from response: {e}")
        
        return jobs
    
    def _normalize_job_data(self, job_data: Dict) -> Optional[Dict]:
        """Normalize job data from HasData response to standard format"""
        try:
            # Map common field names to our standard format
            field_mappings = {
                'title': ['title', 'job_title', 'position', 'name'],
                'company': ['company', 'company_name', 'employer'],
                'location': ['location', 'job_location', 'city', 'place'],
                'description': ['description', 'job_description', 'summary', 'snippet'],
                'salary': ['salary', 'pay', 'compensation', 'wage'],
                'job_type': ['job_type', 'type', 'employment_type'],
                'posted_date': ['posted_date', 'date_posted', 'published', 'date'],
                'url': ['url', 'link', 'job_url', 'href']
            }
            
            normalized_job = {}
            
            for standard_field, possible_fields in field_mappings.items():
                value = None
                for field in possible_fields:
                    if field in job_data and job_data[field]:
                        value = job_data[field]
                        break
                
                normalized_job[standard_field] = value if value else "N/A"
            
            # Add source
            normalized_job['source'] = 'Indeed'
            
            # Ensure we have at least a title
            if normalized_job.get('title') == "N/A":
                return None
            
            return normalized_job
            
        except Exception as e:
            print(f"Error normalizing job data: {e}")
            return None
    
    def filter_jobs(self, jobs: List[Dict], keywords: List[str] = None, 
                   min_salary: int = None, remote_only: bool = False) -> List[Dict]:
        """Filter jobs based on additional criteria"""
        filtered_jobs = []
        
        for job in jobs:
            # Check remote requirement
            if remote_only:
                location_text = job.get("location", "").lower()
                description_text = job.get("description", "").lower()
                title_text = job.get("title", "").lower()
                
                remote_terms = ["remote", "work from home", "telecommute", "wfh", "work-from-home"]
                if not any(term in location_text or term in description_text or term in title_text 
                          for term in remote_terms):
                    continue
            
            # Check additional keywords
            if keywords:
                searchable_text = (
                    job.get("title", "") + " " + 
                    job.get("description", "") + " " + 
                    job.get("company", "")
                ).lower()
                
                if not any(keyword.lower() in searchable_text for keyword in keywords):
                    continue
            
            filtered_jobs.append(job)
        
        return filtered_jobs
    
    

def _clean_location(self, location_data) -> str:
    """Clean and format location data"""
    if not location_data or location_data == "N/A":
        return "N/A"
    
    try:
        location_str = str(location_data)
        
        # Remove extra whitespace
        location_str = " ".join(location_str.split())
        
        # Handle zip codes - extract city, state and format nicely
        import re
        
        # Pattern to match "City, ST 12345" format
        zip_pattern = r'^(.+?),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$'
        match = re.match(zip_pattern, location_str)
        
        if match:
            city, state, zipcode = match.groups()
            return f"{city}, {state}"
        
        # Pattern to match "City, State" format
        if re.match(r'^.+,\s*[A-Z]{2}$', location_str):
            return location_str
        
        # If it's just "Remote" or similar
        if location_str.lower() in ['remote', 'work from home', 'telecommute']:
            return "Remote"
        
        return location_str
    
    except Exception as e:
        print(f"Error cleaning location {location_data}: {e}")
        return str(location_data)

def _normalize_job_data(self, job_data: Dict) -> Optional[Dict]:
    """Normalize job data from HasData response to standard format"""
    try:
        # Map common field names to our standard format
        field_mappings = {
            'title': ['title', 'job_title', 'position', 'name'],
            'company': ['company', 'company_name', 'employer'],
            'location': ['location', 'job_location', 'city', 'place'],
            'description': ['description', 'job_description', 'summary', 'snippet'],
            'salary': ['salary', 'pay', 'compensation', 'wage'],
            'job_type': ['job_type', 'type', 'employment_type'],
            'posted_date': ['posted_date', 'date_posted', 'published', 'date'],
            'url': ['url', 'link', 'job_url', 'href']
        }
        
        normalized_job = {}
        
        for standard_field, possible_fields in field_mappings.items():
            value = None
            for field in possible_fields:
                if field in job_data and job_data[field]:
                    value = job_data[field]
                    break
            
            # Apply special formatting for salary field
            if standard_field == 'salary':
                normalized_job[standard_field] = self._format_salary(value)
            else:
                normalized_job[standard_field] = value if value else "N/A"
        
        # Add source
        normalized_job['source'] = 'Indeed'
        
        # Ensure we have at least a title
        if normalized_job.get('title') == "N/A":
            return None
        
        return normalized_job
        
    except Exception as e:
        print(f"Error normalizing job data: {e}")
        return None
    
# Mock data function for testing
def get_mock_job_data():
    """Generate mock job data for testing"""
    return [
        {
            "title": "Senior Python Developer",
            "company": "Tech Corp",
            "location": "Remote",
            "description": "We are looking for an experienced Python developer to join our team. You will work on exciting projects using Django, Flask, and machine learning technologies.",
            "salary": "$120,000 - $150,000",
            "job_type": "Full-time",
            "posted_date": "2 days ago",
            "url": "https://indeed.com/example1",
            "source": "Indeed"
        },
        {
            "title": "Data Scientist",
            "company": "AI Solutions Inc", 
            "location": "San Francisco, CA",
            "description": "Join our data science team to build predictive models and analyze large datasets. Experience with Python, pandas, and scikit-learn required.",
            "salary": "$130,000 - $160,000",
            "job_type": "Full-time",
            "posted_date": "1 day ago",
            "url": "https://indeed.com/example2", 
            "source": "Indeed"
        },
        {
            "title": "Machine Learning Engineer",
            "company": "Innovation Labs",
            "location": "New York, NY", 
            "description": "Seeking ML engineer to deploy models in production. Strong background in Python, TensorFlow, and cloud platforms required.",
            "salary": "$140,000 - $170,000",
            "job_type": "Full-time",
            "posted_date": "3 days ago",
            "url": "https://indeed.com/example3",
            "source": "Indeed"
        },
        {
            "title": "Software Engineer",
            "company": "StartupXYZ",
            "location": "Austin, TX",
            "description": "Full-stack developer needed for fast-growing startup. React, Node.js, and AWS experience preferred.",
            "salary": "$90,000 - $120,000",
            "job_type": "Full-time", 
            "posted_date": "1 week ago",
            "url": "https://indeed.com/example4",
            "source": "Indeed"
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudFirst Inc",
            "location": "Remote",
            "description": "Looking for DevOps engineer with Kubernetes, Docker, and CI/CD pipeline experience.",
            "salary": "$110,000 - $140,000",
            "job_type": "Full-time",
            "posted_date": "4 days ago", 
            "url": "https://indeed.com/example5",
            "source": "Indeed"
        }
    ]