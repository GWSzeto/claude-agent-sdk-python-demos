"""Mock data for Content Pipeline Agent - Sample content for pipeline processing."""

# =============================================================================
# Sample Articles (HTML and Text formats)
# =============================================================================

SAMPLE_ARTICLES = [
    {
        "id": "article-001",
        "title": "Introduction to Machine Learning",
        "format": "html",
        "source_language": "en",
        "content": """<!DOCTYPE html>
<html>
<head>
    <title>Introduction to Machine Learning</title>
    <script src="analytics.js"></script>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/articles">Articles</a>
        <a href="/about">About</a>
    </nav>

    <main>
        <article>
            <h1>Introduction to Machine Learning</h1>
            <p class="author">By Dr. Sarah Chen | January 15, 2024</p>

            <p>Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. This technology has revolutionized numerous industries, from healthcare to finance.</p>

            <h2>Key Concepts</h2>
            <p>At its core, machine learning relies on algorithms that can identify patterns in data. These patterns are then used to make predictions or decisions. The three main types of machine learning are:</p>

            <ul>
                <li><strong>Supervised Learning</strong>: The algorithm learns from labeled training data, making predictions based on that data.</li>
                <li><strong>Unsupervised Learning</strong>: The algorithm finds hidden patterns in data without pre-existing labels.</li>
                <li><strong>Reinforcement Learning</strong>: The algorithm learns by interacting with an environment and receiving rewards or penalties.</li>
            </ul>

            <h2>Real-World Applications</h2>
            <p>Machine learning powers many technologies we use daily. Recommendation systems on Netflix and Spotify analyze your preferences to suggest content. Email spam filters learn to identify unwanted messages. Self-driving cars use ML to navigate roads safely.</p>

            <p>In healthcare, machine learning assists in diagnosing diseases from medical images, predicting patient outcomes, and discovering new drugs. Financial institutions use it for fraud detection, risk assessment, and algorithmic trading.</p>

            <h2>Getting Started</h2>
            <p>To begin your machine learning journey, start with Python and libraries like scikit-learn, TensorFlow, or PyTorch. Understanding statistics and linear algebra will provide a strong foundation. Practice with datasets from Kaggle to build real-world experience.</p>
        </article>
    </main>

    <footer>
        <p>&copy; 2024 Tech Learning Hub. All rights reserved.</p>
        <a href="/privacy">Privacy Policy</a>
        <a href="/terms">Terms of Service</a>
    </footer>

    <script>trackPageView('article-001');</script>
</body>
</html>""",
        "metadata": {
            "author": "Dr. Sarah Chen",
            "date": "2024-01-15",
            "word_count": 320,
            "category": "Technology"
        }
    },
    {
        "id": "article-002",
        "title": "Climate Change: A Global Challenge",
        "format": "html",
        "source_language": "en",
        "content": """<!DOCTYPE html>
<html>
<head>
    <title>Climate Change: A Global Challenge</title>
</head>
<body>
    <div class="sidebar">
        <h3>Related Articles</h3>
        <ul>
            <li><a href="/renewable-energy">Renewable Energy Solutions</a></li>
            <li><a href="/carbon-footprint">Reducing Your Carbon Footprint</a></li>
        </ul>
        <div class="advertisement">
            <img src="ad-banner.jpg" alt="Advertisement">
        </div>
    </div>

    <article class="main-content">
        <h1>Climate Change: A Global Challenge</h1>
        <p class="meta">Environmental Report | March 2024</p>

        <p>Climate change represents one of the most pressing challenges facing humanity today. Global temperatures have risen approximately 1.1°C above pre-industrial levels, causing widespread environmental disruption.</p>

        <h2>The Science Behind Climate Change</h2>
        <p>The greenhouse effect, while natural and necessary for life on Earth, has been amplified by human activities. Burning fossil fuels releases carbon dioxide and other greenhouse gases into the atmosphere, trapping heat and warming the planet.</p>

        <p>Scientists have observed accelerating ice sheet melting in Greenland and Antarctica, rising sea levels threatening coastal communities, more frequent and intense extreme weather events, and shifting ecosystems affecting biodiversity worldwide.</p>

        <h2>Economic Implications</h2>
        <p>The World Bank estimates that climate change could push 132 million people into poverty by 2030. Agricultural productivity is declining in many regions, while infrastructure damage from extreme weather costs billions annually.</p>

        <h2>Solutions and Hope</h2>
        <p>Despite the challenges, solutions exist. Renewable energy costs have dropped dramatically, making solar and wind competitive with fossil fuels. Electric vehicles are becoming mainstream. Many countries have committed to net-zero emissions by 2050.</p>

        <p>Individual actions matter too: reducing energy consumption, choosing sustainable transportation, eating less meat, and supporting climate-conscious policies all contribute to the solution.</p>
    </article>

    <footer>
        <p>Subscribe to our newsletter for weekly environmental updates.</p>
    </footer>
</body>
</html>""",
        "metadata": {
            "author": "Environmental Research Team",
            "date": "2024-03-10",
            "word_count": 280,
            "category": "Environment"
        }
    },
    {
        "id": "article-003",
        "title": "La Revolución de la Inteligencia Artificial",
        "format": "text",
        "source_language": "es",
        "content": """La Revolución de la Inteligencia Artificial

Por María García López | Febrero 2024

La inteligencia artificial está transformando fundamentalmente la manera en que vivimos y trabajamos. Desde asistentes virtuales hasta diagnósticos médicos, la IA se ha convertido en una parte integral de nuestra vida cotidiana.

Los Fundamentos de la IA

La inteligencia artificial se refiere a sistemas informáticos diseñados para realizar tareas que normalmente requieren inteligencia humana. Esto incluye el reconocimiento de voz, la toma de decisiones, la traducción de idiomas y el reconocimiento visual.

El aprendizaje profundo, una rama del aprendizaje automático, utiliza redes neuronales artificiales inspiradas en el cerebro humano. Estas redes pueden procesar grandes cantidades de datos y aprender patrones complejos.

Aplicaciones Actuales

En el sector salud, la IA ayuda a detectar enfermedades en etapas tempranas mediante el análisis de imágenes médicas. Los algoritmos pueden identificar tumores, anomalías cardíacas y otras condiciones con precisión comparable a la de los especialistas.

El sector financiero utiliza IA para detectar fraudes, evaluar riesgos crediticios y automatizar operaciones de trading. Los chatbots impulsados por IA proporcionan servicio al cliente las 24 horas.

El Futuro de la IA

Los expertos predicen que la IA continuará evolucionando rápidamente. La IA generativa, capaz de crear texto, imágenes y música, está abriendo nuevas posibilidades creativas. Sin embargo, también surgen importantes cuestiones éticas sobre privacidad, empleo y sesgo algorítmico que la sociedad debe abordar.""",
        "metadata": {
            "author": "María García López",
            "date": "2024-02-20",
            "word_count": 250,
            "category": "Tecnología"
        }
    },
    {
        "id": "article-004",
        "title": "The Future of Remote Work",
        "format": "markdown",
        "source_language": "en",
        "content": """# The Future of Remote Work

*By James Thompson | April 2024*

The COVID-19 pandemic permanently altered the landscape of work. What began as an emergency measure has evolved into a fundamental shift in how organizations operate.

## The Hybrid Model Emerges

Most companies have adopted hybrid work arrangements, combining remote and in-office days. Studies show that **73% of employees** prefer flexible work options, and companies offering flexibility see higher retention rates.

### Benefits of Remote Work

- **Increased productivity**: Many workers report fewer distractions at home
- **Better work-life balance**: Elimination of commute time
- **Cost savings**: Reduced office space and commuting expenses
- **Wider talent pool**: Companies can hire from anywhere

### Challenges to Address

1. Maintaining company culture across distributed teams
2. Ensuring equitable treatment of remote vs. in-office employees
3. Preventing burnout from always-on culture
4. Securing sensitive data outside office networks

## Technology Enablers

Cloud computing, video conferencing, and collaboration tools have made remote work seamless. AI-powered tools now help with:

- Automated meeting transcription and summaries
- Asynchronous video communication
- Virtual whiteboarding and brainstorming
- Performance tracking and feedback

## Looking Ahead

The future workplace will likely be more flexible, more digital, and more focused on outcomes rather than hours. Organizations that adapt will thrive; those that don't risk losing top talent to more progressive competitors.

> "The office is no longer a place you go; it's a thing you do." — Future of Work Institute""",
        "metadata": {
            "author": "James Thompson",
            "date": "2024-04-05",
            "word_count": 270,
            "category": "Business"
        }
    },
]

# =============================================================================
# Sample Documents (Business and Technical)
# =============================================================================

SAMPLE_DOCUMENTS = [
    {
        "id": "doc-001",
        "title": "Quarterly Financial Report Q4 2024",
        "format": "text",
        "source_language": "en",
        "content": """QUARTERLY FINANCIAL REPORT
Q4 2024 | Acme Corporation

EXECUTIVE SUMMARY

Acme Corporation delivered strong results in Q4 2024, exceeding analyst expectations across key metrics. Revenue grew 15% year-over-year to $2.4 billion, driven by robust performance in our cloud services division.

KEY FINANCIAL HIGHLIGHTS

Revenue: $2.4 billion (up 15% YoY)
Operating Income: $480 million (up 22% YoY)
Net Income: $360 million (up 18% YoY)
Earnings Per Share: $3.42 (up from $2.90)
Free Cash Flow: $520 million

SEGMENT PERFORMANCE

Cloud Services Division
Revenue increased 28% to $1.2 billion, representing 50% of total revenue. Customer acquisition remained strong with 2,400 new enterprise clients. Annual recurring revenue (ARR) reached $4.8 billion.

Enterprise Software Division
Revenue grew 8% to $800 million. The division completed successful launches of three major product updates. Customer retention rate improved to 94%.

Professional Services Division
Revenue of $400 million, up 5% from prior year. Margins expanded 200 basis points due to operational efficiencies.

OUTLOOK FOR 2025

Management expects continued momentum into 2025:
- Full-year revenue guidance: $10.2-10.5 billion
- Operating margin target: 22-24%
- Planned R&D investment: $800 million
- New product launches: 5 major releases planned

RISKS AND CONSIDERATIONS

Key risks include macroeconomic uncertainty, increasing competition in cloud services, and potential regulatory changes in key markets. The company maintains a strong balance sheet with $3.2 billion in cash to navigate challenges.""",
        "metadata": {
            "author": "Finance Department",
            "date": "2024-12-15",
            "word_count": 260,
            "document_type": "financial_report"
        }
    },
    {
        "id": "doc-002",
        "title": "API Integration Technical Specification",
        "format": "text",
        "source_language": "en",
        "content": """API INTEGRATION TECHNICAL SPECIFICATION
Version 2.1 | Last Updated: January 2024

1. OVERVIEW

This document specifies the technical requirements for integrating with the Acme Platform API. The API follows RESTful conventions and uses JSON for request and response payloads.

2. AUTHENTICATION

All API requests require authentication via OAuth 2.0 bearer tokens. Tokens are obtained through the authorization endpoint and expire after 3600 seconds.

Endpoint: POST /oauth/token
Required Parameters:
  - client_id: Your application's client ID
  - client_secret: Your application's secret key
  - grant_type: "client_credentials"

3. BASE URL AND VERSIONING

Production: https://api.acme.com/v2
Staging: https://api-staging.acme.com/v2

All endpoints are versioned. The current stable version is v2. Version v1 is deprecated and will be sunset on March 31, 2025.

4. RATE LIMITING

Rate limits are enforced per API key:
  - Standard tier: 1,000 requests per minute
  - Premium tier: 10,000 requests per minute
  - Enterprise tier: Custom limits

Rate limit headers are included in all responses:
  - X-RateLimit-Limit: Maximum requests allowed
  - X-RateLimit-Remaining: Requests remaining in window
  - X-RateLimit-Reset: Unix timestamp when limit resets

5. ERROR HANDLING

The API returns standard HTTP status codes:
  - 200: Success
  - 400: Bad Request (invalid parameters)
  - 401: Unauthorized (invalid or expired token)
  - 403: Forbidden (insufficient permissions)
  - 429: Too Many Requests (rate limit exceeded)
  - 500: Internal Server Error

Error responses include a JSON body with error code and message.

6. ENDPOINTS

6.1 Users
  GET /users - List all users
  GET /users/{id} - Get user by ID
  POST /users - Create new user
  PUT /users/{id} - Update user
  DELETE /users/{id} - Delete user

6.2 Resources
  GET /resources - List resources with pagination
  GET /resources/{id} - Get resource details
  POST /resources - Create resource
  PATCH /resources/{id} - Partial update

7. WEBHOOKS

Configure webhooks to receive real-time notifications for events. Webhook payloads are signed using HMAC-SHA256 for verification.""",
        "metadata": {
            "author": "Engineering Team",
            "date": "2024-01-20",
            "word_count": 340,
            "document_type": "technical_specification"
        }
    },
    {
        "id": "doc-003",
        "title": "Product Launch Strategy Brief",
        "format": "text",
        "source_language": "en",
        "content": """PRODUCT LAUNCH STRATEGY BRIEF
Project Phoenix | Confidential

PRODUCT OVERVIEW

Project Phoenix is our next-generation analytics platform designed for mid-market enterprises. The platform combines real-time data processing with AI-powered insights, enabling businesses to make faster, data-driven decisions.

TARGET MARKET

Primary: Mid-market companies (500-5,000 employees) in technology, retail, and financial services sectors.

Secondary: Enterprise companies seeking departmental solutions before company-wide adoption.

Market Size: Total addressable market estimated at $8.5 billion, with our serviceable market at $2.1 billion.

COMPETITIVE POSITIONING

Key Differentiators:
1. 10x faster query performance than legacy solutions
2. No-code dashboard builder for business users
3. Native AI assistant for natural language queries
4. Competitive pricing at 40% below enterprise alternatives

LAUNCH TIMELINE

Phase 1 (Months 1-2): Private beta with 50 select customers
Phase 2 (Month 3): Public beta launch at industry conference
Phase 3 (Month 4): General availability with full marketing push

MARKETING STRATEGY

Pre-Launch:
- Analyst briefings and early reviews
- Customer advisory board formation
- Content marketing: 10 thought leadership pieces

Launch Week:
- Press release and media outreach
- Product demo webinar (target: 5,000 registrations)
- Social media campaign across LinkedIn and Twitter

Post-Launch:
- Customer case study development
- Partner channel enablement
- Paid advertising campaign ($500K budget)

SUCCESS METRICS

90-day targets:
- 500 trial signups
- 50 paid conversions
- $2M in pipeline
- 4.5+ star rating on G2""",
        "metadata": {
            "author": "Product Marketing",
            "date": "2024-02-01",
            "word_count": 280,
            "document_type": "strategy_brief"
        }
    },
]


# =============================================================================
# Helper Functions
# =============================================================================

def get_article_by_id(article_id: str) -> dict | None:
    """
    Get a sample article by ID.

    Args:
        article_id: The article ID (e.g., "article-001")

    Returns:
        Article dict or None if not found
    """
    for article in SAMPLE_ARTICLES:
        if article["id"] == article_id:
            return article
    return None


def get_document_by_id(document_id: str) -> dict | None:
    """
    Get a sample document by ID.

    Args:
        document_id: The document ID (e.g., "doc-001")

    Returns:
        Document dict or None if not found
    """
    for doc in SAMPLE_DOCUMENTS:
        if doc["id"] == document_id:
            return doc
    return None


def get_content_by_id(content_id: str) -> dict | None:
    """
    Get any content (article or document) by ID.

    Args:
        content_id: The content ID

    Returns:
        Content dict or None if not found
    """
    return get_article_by_id(content_id) or get_document_by_id(content_id)


def get_articles_by_format(format: str) -> list[dict]:
    """
    Get articles filtered by format.

    Args:
        format: Content format ("html", "text", "markdown")

    Returns:
        List of articles matching the format
    """
    return [article for article in SAMPLE_ARTICLES if article["format"] == format]


def get_articles_by_language(language: str) -> list[dict]:
    """
    Get articles filtered by source language.

    Args:
        language: Language code ("en", "es", etc.)

    Returns:
        List of articles in that language
    """
    return [article for article in SAMPLE_ARTICLES if article["source_language"] == language]


def list_available_content() -> list[dict]:
    """
    List all available sample content with metadata.

    Returns:
        List of content summaries with id, title, format, language, word_count
    """
    content_list = []

    for article in SAMPLE_ARTICLES:
        content_list.append({
            "id": article["id"],
            "title": article["title"],
            "type": "article",
            "format": article["format"],
            "source_language": article["source_language"],
            "word_count": article["metadata"].get("word_count", 0),
        })

    for doc in SAMPLE_DOCUMENTS:
        content_list.append({
            "id": doc["id"],
            "title": doc["title"],
            "type": "document",
            "format": doc["format"],
            "source_language": doc["source_language"],
            "word_count": doc["metadata"].get("word_count", 0),
        })

    return content_list


def get_content_stats() -> dict:
    """
    Get statistics about available content.

    Returns:
        Dict with content statistics
    """
    all_content = SAMPLE_ARTICLES + SAMPLE_DOCUMENTS

    formats = {}
    languages = {}
    total_words = 0

    for item in all_content:
        # Count formats
        fmt = item["format"]
        formats[fmt] = formats.get(fmt, 0) + 1

        # Count languages
        lang = item["source_language"]
        languages[lang] = languages.get(lang, 0) + 1

        # Sum words
        total_words += item["metadata"].get("word_count", 0)

    return {
        "total_articles": len(SAMPLE_ARTICLES),
        "total_documents": len(SAMPLE_DOCUMENTS),
        "total_content": len(all_content),
        "total_words": total_words,
        "formats": formats,
        "languages": languages,
    }
