from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum

class DebateCreate(BaseModel):
    date: str
    position: Literal['OG', 'OO', 'CG', 'CO']
    points: int = Field(ge=0, le=3)
    speaks: int = Field(ge=0, le=100)
    reply: int = Field(default=0, ge=0, le=50)
    motion: str
    infoslide: str
    tournament: int | None = None 
    categories: CategoryList | None = None
    order: int = Field(default=0, ge=0, le=2)
    has_reply: bool = False
    
    

class Category(str, Enum):
    africa = "Africa"
    animal_rights = "Animal Rights"
    art = "Art"
    ai = "Artificial Intelligence"
    asia = "Asia"
    australia = "Australia"
    charity = "Charity"
    children = "Children"
    cities = "Cities"
    climate_change = "Climate Change"
    colonialism = "Colonialism"
    criminal_justice = "Criminal Justice"
    culture = "Culture"
    cybersecurity = "Cybersecurity"
    democracy = "Democracy"
    development = "Development"
    disability_rights = "Disability Rights"
    drugs = "Drugs"
    econ = "Economics"
    education_academia = "Education/Academia"
    elderly_aging = "Elderly/Aging"
    energy = "Energy"
    environment = "Environment"
    ethics = "Ethics"
    europe = "Europe"
    feminism = "Feminism"
    healthcare = "Healthcare"
    historical_memory = "Historical Memory"
    housing = "Housing"
    human_rights = "Human Rights"
    immigration = "Immigration"
    indigenous_people = "Indigenous People"
    ir = "International Relations"
    labor = "Labor"
    latam = "Latin America"
    law = "Law"
    lgbtq = "LGBTQ+"
    media = "Media"
    medical = "Medical"
    mental_health = "Mental Health"
    middle_east = "Middle East"
    military = "Military"
    minorities = "Minority Communities"
    nationalism = "Nationalism"
    philosophy = "Philosophy"
    police = "Police"
    policy = "Policy"
    politics = "Politics"
    privacy = "Privacy"
    private_property = "Private Property"
    refugees_asylum = "Refugees/Asylum"
    religion = "Religion"
    romance_sex = "Romance/Sex"
    romance = "Romance/Sexuality"
    science = "Science/Technology"
    social_justice = "Social Justice"
    social_policy = "Social Policy"
    sports = "Sports"
    terrorism = "Terrorism"
    trade = "Trade"
        
    
class CategoryList(BaseModel):
    categories: list[Category]