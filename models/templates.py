PROFILES_REPORT_TEMPLATE = (
    "You're a LinkedIn profile analyst. Analyze the LinkedIn profile and posts to create a concise report extracting the following information:\n"
    "1. Experience (e.g., job titles, company names, job descriptions, durations)\n"
    "2. Education (e.g., degrees, institutions, graduation years)\n"
    "3. Achievements (e.g., certifications, awards, major accomplishments)\n"
    "4. Posts (e.g., professional posts, shared content, articles)\n"
    "5. Skills (e.g., highlighted skills on the profile)\n"
    "For each item, include:\n"
    "- LinkedIn profile name or company name\n"
    "- Post or section link\n"
    "- Location (e.g., job location, education institution location)\n"
    "Only include information from the provided LinkedIn profile and posts that fits these categories.\n"
    "Posts and profile to analyze: {input_var}"
)

PROFILES_TEMPLATE_REFINE = (
    "You're a LinkedIn profile specialist who has generated a report on various LinkedIn profile sections and posts.\n"
    "Previous report: {raport}\n"
    "This report needs to be more concise and follow a predefined structure:\n"
    "1. Analyze your previous report.\n"
    "2. Adapt the report to the following structure: {format_instructions}\n"
    "If there's no relevant information for a key, leave it as an empty list.\n"
    "Your response should only contain the specified structure, without ```json ``` tags."
)
