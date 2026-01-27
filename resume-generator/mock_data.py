"""Mock data for Resume Generator.

This module provides stubbed API responses for testing the resume generator
without making actual API calls to web search or LinkedIn.
"""

# Mock web search results for different people
MOCK_SEARCH_RESULTS: dict[str, dict] = {
    "John Smith": {
        "results": [
            {
                "title": "John Smith - Senior Software Engineer at TechCorp | LinkedIn",
                "url": "https://linkedin.com/in/johnsmith",
                "snippet": "Senior Software Engineer with 8+ years of experience in building scalable distributed systems. Previously at StartupXYZ and Google. Stanford CS graduate."
            },
            {
                "title": "johnsmith (John Smith) · GitHub",
                "url": "https://github.com/johnsmith",
                "snippet": "Open source contributor with 500+ contributions. Maintainer of popular-lib (5k stars). Active in Python and Go communities."
            },
            {
                "title": "TechCorp Engineering Blog - Meet John Smith",
                "url": "https://techcorp.io/blog/meet-john-smith",
                "snippet": "John leads our platform infrastructure team, focusing on microservices architecture and cloud-native development."
            },
            {
                "title": "John Smith - Speaker at PyCon 2023",
                "url": "https://pycon.org/speakers/john-smith",
                "snippet": "Talk: 'Scaling Python Applications to 1M Users' - Best practices for building high-performance Python backends."
            }
        ]
    },
    "Jane Doe": {
        "results": [
            {
                "title": "Jane Doe - VP of Product at InnovateCo | LinkedIn",
                "url": "https://linkedin.com/in/janedoe",
                "snippet": "VP of Product with 12+ years in product management. Led products reaching 50M+ users. MBA from Harvard Business School."
            },
            {
                "title": "Jane Doe on Product Leadership - Forbes",
                "url": "https://forbes.com/jane-doe-product-leadership",
                "snippet": "Interview with Jane Doe on building customer-centric products and leading high-performing product teams."
            },
            {
                "title": "InnovateCo Announces New VP of Product",
                "url": "https://innovateco.com/news/new-vp-product",
                "snippet": "Jane Doe joins InnovateCo from MegaTech where she led the consumer products division."
            }
        ]
    },
    "Alex Johnson": {
        "results": [
            {
                "title": "Alex Johnson - Data Scientist at AI Labs | LinkedIn",
                "url": "https://linkedin.com/in/alexjohnson",
                "snippet": "Data Scientist specializing in NLP and machine learning. PhD from MIT. Published 15+ papers in top ML conferences."
            },
            {
                "title": "Alex Johnson - Google Scholar",
                "url": "https://scholar.google.com/alexjohnson",
                "snippet": "Citations: 2,500+. Research areas: Natural Language Processing, Deep Learning, Transformers."
            },
            {
                "title": "AI Labs Research Team",
                "url": "https://ailabs.com/team",
                "snippet": "Alex Johnson leads the NLP research team, working on next-generation language models."
            }
        ]
    }
}

# Mock LinkedIn profile data
MOCK_LINKEDIN_PROFILES: dict[str, dict] = {
    "John Smith": {
        "name": "John Smith",
        "headline": "Senior Software Engineer at TechCorp",
        "location": "San Francisco, CA",
        "email": "john.smith@email.com",
        "phone": "(555) 123-4567",
        "linkedin_url": "linkedin.com/in/johnsmith",
        "summary": "Passionate software engineer with 8+ years of experience building scalable distributed systems. Strong background in Python, Go, and cloud-native technologies. Open source contributor and conference speaker.",
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "TechCorp",
                "location": "San Francisco, CA",
                "duration": "Jan 2020 - Present",
                "description": [
                    "Led development of microservices architecture serving 10M+ daily requests",
                    "Reduced system latency by 40% through performance optimization",
                    "Mentored team of 5 junior engineers on best practices"
                ]
            },
            {
                "title": "Software Engineer",
                "company": "StartupXYZ",
                "location": "Palo Alto, CA",
                "duration": "Jun 2016 - Dec 2019",
                "description": [
                    "Built full-stack features using React and Node.js for B2B SaaS platform",
                    "Implemented CI/CD pipelines reducing deployment time by 60%",
                    "Contributed to open-source projects with 1000+ GitHub stars"
                ]
            },
            {
                "title": "Software Engineering Intern",
                "company": "Google",
                "location": "Mountain View, CA",
                "duration": "Summer 2015",
                "description": [
                    "Developed internal tools for the Cloud Platform team",
                    "Received return offer for full-time position"
                ]
            }
        ],
        "education": [
            {
                "degree": "B.S. Computer Science",
                "school": "Stanford University",
                "location": "Stanford, CA",
                "year": "2016",
                "details": "GPA: 3.8/4.0, Dean's List"
            }
        ],
        "skills": [
            "Python", "Go", "JavaScript", "TypeScript", "React", "Node.js",
            "AWS", "GCP", "Docker", "Kubernetes", "PostgreSQL", "Redis",
            "Microservices", "System Design", "CI/CD"
        ],
        "certifications": [
            "AWS Solutions Architect - Professional",
            "Google Cloud Professional Cloud Architect"
        ]
    },
    "Jane Doe": {
        "name": "Jane Doe",
        "headline": "VP of Product at InnovateCo",
        "location": "New York, NY",
        "email": "jane.doe@email.com",
        "phone": "(555) 987-6543",
        "linkedin_url": "linkedin.com/in/janedoe",
        "summary": "Strategic product leader with 12+ years driving product vision and execution at scale. Proven track record of launching products reaching 50M+ users. Expertise in B2C and B2B product development, data-driven decision making, and building high-performing teams.",
        "experience": [
            {
                "title": "VP of Product",
                "company": "InnovateCo",
                "location": "New York, NY",
                "duration": "Mar 2021 - Present",
                "description": [
                    "Lead product strategy for suite of enterprise collaboration tools",
                    "Grew monthly active users from 5M to 20M in 2 years",
                    "Manage team of 15 product managers across 4 product lines"
                ]
            },
            {
                "title": "Director of Product",
                "company": "MegaTech",
                "location": "Seattle, WA",
                "duration": "Jan 2017 - Feb 2021",
                "description": [
                    "Led consumer products division with $100M+ annual revenue",
                    "Launched mobile app reaching #1 in App Store productivity category",
                    "Established product-led growth strategy increasing conversion by 35%"
                ]
            },
            {
                "title": "Senior Product Manager",
                "company": "TechStartup",
                "location": "San Francisco, CA",
                "duration": "Aug 2012 - Dec 2016",
                "description": [
                    "Managed end-to-end product lifecycle for core platform features",
                    "Conducted user research informing product roadmap decisions",
                    "Collaborated with engineering to deliver features on schedule"
                ]
            }
        ],
        "education": [
            {
                "degree": "MBA",
                "school": "Harvard Business School",
                "location": "Boston, MA",
                "year": "2012",
                "details": "Baker Scholar (Top 5%)"
            },
            {
                "degree": "B.A. Economics",
                "school": "Yale University",
                "location": "New Haven, CT",
                "year": "2008",
                "details": "Magna Cum Laude"
            }
        ],
        "skills": [
            "Product Strategy", "Product-Led Growth", "User Research", "A/B Testing",
            "Agile/Scrum", "Roadmap Planning", "Stakeholder Management",
            "Data Analytics", "SQL", "Figma", "JIRA"
        ],
        "certifications": [
            "Pragmatic Marketing Certified - PMC Level III",
            "Certified Scrum Product Owner (CSPO)"
        ]
    },
    "Alex Johnson": {
        "name": "Alex Johnson",
        "headline": "Senior Data Scientist at AI Labs",
        "location": "Boston, MA",
        "email": "alex.johnson@email.com",
        "phone": "(555) 456-7890",
        "linkedin_url": "linkedin.com/in/alexjohnson",
        "summary": "Data scientist and ML researcher specializing in NLP and deep learning. PhD from MIT with 15+ publications in top-tier conferences (NeurIPS, ACL, EMNLP). Passionate about applying cutting-edge ML to solve real-world problems.",
        "experience": [
            {
                "title": "Senior Data Scientist",
                "company": "AI Labs",
                "location": "Boston, MA",
                "duration": "Sep 2021 - Present",
                "description": [
                    "Lead NLP research team developing next-generation language models",
                    "Published 5 papers at NeurIPS and ACL with 500+ citations",
                    "Built production ML pipeline processing 1B+ tokens daily"
                ]
            },
            {
                "title": "Machine Learning Engineer",
                "company": "DataCorp",
                "location": "Cambridge, MA",
                "duration": "Jun 2019 - Aug 2021",
                "description": [
                    "Developed sentiment analysis models with 95% accuracy",
                    "Deployed ML models serving 100K+ predictions per second",
                    "Reduced model training time by 3x using distributed computing"
                ]
            }
        ],
        "education": [
            {
                "degree": "Ph.D. Computer Science",
                "school": "Massachusetts Institute of Technology",
                "location": "Cambridge, MA",
                "year": "2019",
                "details": "Dissertation: 'Neural Approaches to Language Understanding'"
            },
            {
                "degree": "B.S. Computer Science & Mathematics",
                "school": "UC Berkeley",
                "location": "Berkeley, CA",
                "year": "2014",
                "details": "Summa Cum Laude, Phi Beta Kappa"
            }
        ],
        "skills": [
            "Python", "PyTorch", "TensorFlow", "Transformers", "NLP",
            "Deep Learning", "Machine Learning", "Data Analysis",
            "SQL", "Spark", "AWS SageMaker", "MLOps"
        ],
        "certifications": [
            "AWS Machine Learning Specialty",
            "Google Cloud Professional ML Engineer"
        ]
    }
}

# Default profile for unknown people
DEFAULT_PROFILE: dict = {
    "name": "Unknown Person",
    "headline": "Professional",
    "location": "United States",
    "email": "contact@email.com",
    "phone": "(555) 000-0000",
    "linkedin_url": "linkedin.com/in/unknown",
    "summary": "Experienced professional with diverse background.",
    "experience": [
        {
            "title": "Professional",
            "company": "Company",
            "location": "City, State",
            "duration": "2020 - Present",
            "description": ["Contributed to team projects and initiatives"]
        }
    ],
    "education": [
        {
            "degree": "Bachelor's Degree",
            "school": "University",
            "location": "City, State",
            "year": "2020",
            "details": ""
        }
    ],
    "skills": ["Communication", "Teamwork", "Problem Solving"],
    "certifications": []
}

DEFAULT_SEARCH_RESULTS: dict = {
    "results": [
        {
            "title": "No specific results found",
            "url": "https://example.com",
            "snippet": "Unable to find detailed information for this person."
        }
    ]
}


def get_search_results(name: str) -> dict:
    """Get mock search results for a person.

    Args:
        name: The person's name to search for

    Returns:
        Dict containing search results
    """
    # Try exact match first
    if name in MOCK_SEARCH_RESULTS:
        return MOCK_SEARCH_RESULTS[name]

    # Try case-insensitive match
    for key in MOCK_SEARCH_RESULTS:
        if key.lower() == name.lower():
            return MOCK_SEARCH_RESULTS[key]

    return DEFAULT_SEARCH_RESULTS


def get_linkedin_profile(name: str) -> dict:
    """Get mock LinkedIn profile for a person.

    Args:
        name: The person's name

    Returns:
        Dict containing LinkedIn profile data
    """
    # Try exact match first
    if name in MOCK_LINKEDIN_PROFILES:
        return MOCK_LINKEDIN_PROFILES[name]

    # Try case-insensitive match
    for key in MOCK_LINKEDIN_PROFILES:
        if key.lower() == name.lower():
            return MOCK_LINKEDIN_PROFILES[key]

    # Return default with the provided name
    default = DEFAULT_PROFILE.copy()
    default["name"] = name
    return default
