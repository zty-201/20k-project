# job_dashboard.py
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from job_scraper import IndeedJobScraper, get_mock_job_data

# Load environment variables
load_dotenv()

def job_analysis_page():
    st.title("Job Market Analysis Dashboard")
    st.subheader("Indeed Job Scraping & Analysis")
    
    # Sidebar configuration
    st.sidebar.title("Job Search Settings")
    
    # Auto-load API key from environment, with manual override option
    auto_api_key = os.getenv('HASDATA_API_KEY')
    
    if auto_api_key:
        st.sidebar.success("✅ API Key loaded from environment")
        use_env_key = st.sidebar.checkbox("Use environment API key", value=True)
        
        if use_env_key:
            api_key = auto_api_key
            # Show partial key for confirmation
            masked_key = auto_api_key[:8] + "..." + auto_api_key[-4:]
            st.sidebar.text(f"Using key: {masked_key}")
        else:
            api_key = st.sidebar.text_input("Manual API Key Override", type="password")
    else:
        st.sidebar.warning("⚠️ No API key found in environment")
        api_key = st.sidebar.text_input("HasData API Key", type="password")
    
    # Mock data option
    use_mock_data = st.sidebar.checkbox("Use Mock Data (for testing)", value=False)
    
    # Show warning only if no API key available and not using mock data
    if not api_key and not use_mock_data:
        st.warning("Please enter your HasData API key in the sidebar or enable mock data for testing.")
        st.info("💡 **Tip**: Add `HASDATA_API_KEY=your_key_here` to your `.env` file to auto-load the key.")
        return
    
    # Search parameters
    keywords = st.sidebar.text_input("Job Keywords", value="python developer")
    location = st.sidebar.text_input("Location", value="Remote")
    limit = st.sidebar.slider("Max Jobs to Scrape", 5, 50, 20)
    
    # Additional filters
    st.sidebar.subheader("Filters")
    filter_keywords = st.sidebar.text_area("Additional Keywords (one per line)")
    remote_only = st.sidebar.checkbox("Remote Only")
    
    # Search button
    if st.sidebar.button("Search Jobs"):
        if use_mock_data:
            st.info("Using mock data for demonstration...")
            jobs = get_mock_job_data()
        else:
            try:
                # Create scraper with API key
                scraper = IndeedJobScraper(api_key)
                
                with st.spinner(f"Searching for '{keywords}' jobs in '{location}'..."):
                    jobs = scraper.search_jobs(keywords, location, limit)
            except Exception as e:
                st.error(f"Error creating scraper: {e}")
                return
        
        if not jobs:
            st.error("No jobs found or API error occurred.")
            if not use_mock_data:
                st.info("💡 Try using mock data to test the interface while debugging API issues.")
            return
        
        # Apply additional filters
        if filter_keywords.strip() or remote_only:
            additional_keywords = [k.strip() for k in filter_keywords.split('\n') if k.strip()]
            if not use_mock_data:
                jobs = scraper.filter_jobs(jobs, additional_keywords, remote_only=remote_only)
            else:
                # Apply filters to mock data too
                filtered_jobs = []
                for job in jobs:
                    # Check remote requirement
                    if remote_only:
                        location_text = job.get("location", "").lower()
                        if "remote" not in location_text:
                            continue
                    
                    # Check additional keywords
                    if additional_keywords:
                        job_text = (job.get("title", "") + " " + job.get("description", "")).lower()
                        if not any(keyword.lower() in job_text for keyword in additional_keywords):
                            continue
                    
                    filtered_jobs.append(job)
                jobs = filtered_jobs
        
        st.success(f"Found {len(jobs)} jobs!")
        
        # Convert to DataFrame
        df = pd.DataFrame(jobs)

         # Extract all URLs into an array
        job_urls = []
        for job in jobs:
            url = job.get('url')
            if url and url != 'N/A':
                job_urls.append(url)
        
        # Display the URLs array info
        st.info(f"📎 Found {len(job_urls)} job URLs out of {len(jobs)} total jobs")
        
        # Optional: Show the URLs in an expandable section
        with st.expander("🔗 View All Job URLs"):
            if job_urls:
                for i, url in enumerate(job_urls, 1):
                    st.write(f"{i}. {url}")
            else:
                st.write("No URLs found in the job data")
        
        # Store URLs in session state for later use
        st.session_state.job_urls = job_urls

                # Store URLs in session state for later use
        st.session_state.job_urls = job_urls
        
        # Print to console for debugging
        print(f"DEBUG: Found {len(job_urls)} URLs")
        print("DEBUG: URLs array:", job_urls)
        if job_urls:
            print("DEBUG: First URL:", job_urls[0])
        
        # Display basic stats
        st.subheader("Job Search Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Jobs", len(jobs))
        with col2:
            unique_companies = df['company'].nunique() if 'company' in df.columns else 0
            st.metric("Unique Companies", unique_companies)
        with col3:
            remote_count = sum(1 for job in jobs if 'remote' in job.get('location', '').lower())
            st.metric("Remote Jobs", remote_count)
        
        # Show jobs table
        st.subheader("Job Listings")
        
        if not df.empty:
            # Simple dataframe display
            display_columns = ['title', 'company', 'location', 'salary', 'posted_date']
            available_columns = [col for col in display_columns if col in df.columns]
            
            st.dataframe(
                df[available_columns] if available_columns else df,
                use_container_width=True,
                hide_index=True
            )
            
            # Expandable job details with links
            st.subheader("📋 Job Details & Links")
            
            for i, job in enumerate(jobs):
                with st.expander(f"🔍 {job.get('title', 'Unknown')} - {job.get('company', 'Unknown')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Company:** {job.get('company', 'N/A')}")
                        st.write(f"**Location:** {job.get('location', 'N/A')}")
                        st.write(f"**Salary:** {job.get('salary', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Job Type:** {job.get('job_type', 'N/A')}")
                        st.write(f"**Posted:** {job.get('posted_date', 'N/A')}")
                        
                        # Add clickable link
                        if job.get('url') and job.get('url') != 'N/A':
                            st.link_button("🔗 View Job Posting", job.get('url'))
                    
                    # Show description if available
                    if job.get('description') and job.get('description') != 'N/A':
                        st.write("**Description:**")
                        description = job.get('description', '')
                        if len(description) > 300:
                            description = description[:300] + "..."
                        st.write(description)
        else:
            st.write("No jobs to display.")

        # Basic job analytics
        if jobs:
            st.subheader("Job Analytics")
            
            # Company distribution
            if 'company' in df.columns and df['company'].notna().any():
                st.write("**Top Companies Hiring:**")
                company_counts = df['company'].value_counts().head(10)
                if not company_counts.empty:
                    st.bar_chart(company_counts)
            
            # Location distribution
            if 'location' in df.columns and df['location'].notna().any():
                st.write("**Jobs by Location:**")
                location_counts = df['location'].value_counts().head(10)
                if not location_counts.empty:
                    st.bar_chart(location_counts)
                
            # Additional insights
            st.subheader("📊 Additional Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Salary information
                salary_jobs = [job for job in jobs if job.get('salary') and job.get('salary') != 'N/A']
                if salary_jobs:
                    st.metric("Jobs with Salary Info", f"{len(salary_jobs)} / {len(jobs)}")
                
                # Recent postings
                recent_jobs = [job for job in jobs if 'day' in job.get('posted_date', '').lower()]
                if recent_jobs:
                    st.metric("Recent Postings (Last Week)", len(recent_jobs))
            
            with col2:
                # Average company posting
                if unique_companies > 0:
                    avg_jobs_per_company = len(jobs) / unique_companies
                    st.metric("Avg Jobs per Company", f"{avg_jobs_per_company:.1f}")
        
        # Export options
        st.subheader("📁 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save to CSV"):
                filename = f"job_search_{keywords.replace(' ', '_')}_{location.replace(' ', '_')}.csv"
                df.to_csv(filename, index=False)
                st.success(f"Results saved to {filename}")
        
        with col2:
            # Download button for CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"jobs_{keywords.replace(' ', '_')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    job_analysis_page()