from pydantic import BaseModel, Field


class InformationProfiles(BaseModel):
    name: str = Field(description='Name of the LinkedIn profile or company page from where the information was extracted.')
    information: str = Field(description='Information extracted from the LinkedIn post or profile section (e.g., experience, education, achievements).')
    link: str = Field(description='Link to the LinkedIn post or section from where the information was extracted.')
    location: str = Field(description='Location associated with the profile or job experience.')


class FieldProfiles(BaseModel):
    name: str = Field(description='Name of the key. Available options are: Experience, Education, Achievements, Posts, Skills.')
    keys: list[InformationProfiles] = Field(description='List of extracted information for the specified key.')


class ReportProfiles(BaseModel):
    name: str = Field(description='Name of the report: LINKEDIN PROFILE REPORT')
    fields: list[FieldProfiles] = Field(description='List of all relevant keys for this LinkedIn profile report.')
