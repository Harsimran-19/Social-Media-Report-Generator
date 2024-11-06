from src.generator import LinkedInReportGenerator

def main():
    # Replace with the LinkedIn profile URL you want to scrape
    profile_url = "https://www.linkedin.com/in/dalianaliu/"

    # Initialize LinkedIn Report Generator
    report_generator = LinkedInReportGenerator()

    # Generate the report
    report = report_generator.generate_report(profile_url)
    print(f"Generated Report:\n{report}")

if __name__ == "__main__":
    main()
