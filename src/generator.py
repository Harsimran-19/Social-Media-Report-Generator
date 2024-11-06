import datetime
import json

from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq

from models.settings import settings
from crawlers.linkiden import LinkedInCrawler
from src.db import database
from src.llm import get_chain
from models.schemas import ReportProfiles
from models.templates import PROFILES_REPORT_TEMPLATE, PROFILES_TEMPLATE_REFINE


class LinkedInReportGenerator:
    def __init__(self):
        self.crawler = LinkedInCrawler()
        self.database = database
        self.llm = ChatGroq(
            model="mixtral-8x7b-32768",
            api_key='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'
        )

    def crawl_and_store_data(self, profile_url: str) -> int:
        """Crawls LinkedIn profile for data and stores it in the database."""
        profile_data = self.crawler.extract(profile_url)
        profiles_collection = self.database['linkedin_profiles']
    
        # Store or update the profile and posts data in one document
        profiles_collection.update_one(
            {'Name': profile_data['Name']},  # Use 'Name' as the unique identifier
            {'$set': profile_data},
            upsert=True
        )
    
        return len(profile_data["Posts"])


    def get_profile_from_db(self) -> List[Dict[str, Any]]:
        """Retrieves LinkedIn profile data from the database."""
        profiles_collection = self.database['linkedin_profiles']
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=7)
        
        # Assuming 'Name' is the unique identifier for profiles, adjust if needed
        return list(profiles_collection.find({
            'date': {'$gte': start_date, '$lte': end_date}
        }))



    @staticmethod
    def get_profile_text(profiles: List[Dict[str, Any]]) -> List[str]:
        """Extracts text content from the entire LinkedIn profile data."""
        unique_profiles = set()
        
        for profile in profiles:
            name = profile.get("Name", "N/A")
            about = profile.get("About", "N/A")
            experience = profile.get("Experience", "N/A")
            education = profile.get("Education", "N/A")
            posts = profile.get("Posts", [])
    
            profile_text = f"Name: {name}\nAbout: {about}\nExperience: {experience}\nEducation: {education}\n"
    
            # Add posts if available
            if posts:
                posts_text = "\n".join([post.get("content", "") for post in posts])
                profile_text += f"Posts:\n{posts_text}\n"
    
            unique_profiles.add(profile_text)
    
        return list(unique_profiles)

    def create_report(self, profile_data: List[str]) -> str:
        """Generates a report using the LLM for the entire LinkedIn profile data."""
        chain_1 = get_chain(
            self.llm,
            PROFILES_REPORT_TEMPLATE,  # Update this template to include sections like About, Experience, etc.
            input_variables=["input_var"],
            output_key="report",
        )
    
        result_1 = chain_1.invoke({"input_var": profile_data})
        report = result_1["report"]
    
        output_parser = PydanticOutputParser(pydantic_object=ReportProfiles)
        format_output = {"format_instructions": output_parser.get_format_instructions()}
    
        chain_2 = get_chain(
            self.llm,
            PROFILES_TEMPLATE_REFINE,  # Ensure this template is designed to refine the entire profile
            input_variables=["raport", "format_instructions"],
            output_key="formatted_report",
        )
    
        result_2 = chain_2.invoke({"raport": report, "format_instructions": format_output})
    
        return result_2["formatted_report"]
    
    def generate_report(self, profile_url: str):
        """Main function to generate a LinkedIn profile report for the entire scraped data."""
        # Step 1: Crawl and store LinkedIn profile data (not just posts)
        profile_count = self.crawl_and_store_data(profile_url)
        print(f"Crawled and stored {profile_count} profiles.")
    
        # Step 2: Retrieve the profile from the database
        db_profiles = self.get_profile_from_db()
        print(f"Retrieved {len(db_profiles)} profiles from the database.")
    
        # Step 3: Process profile data and create report
        profile_text = self.get_profile_text(db_profiles)
        report_data_str = self.create_report(profile_text)
        print(f"Generated report for profile: {report_data_str}")
    
        return report_data_str

