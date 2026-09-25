# NESO ChatGPT Conversation

## Purpose

This file captures the NESO news-processing discussion from the start of the current chat, including the stakeholder/sector taxonomy, NESO purpose and responsibilities, AI prompt recommendations, Data & AI requirements, JSON structures, and recommended processing flow.

---

## 1. NESO Stakeholders and Sectors

Initial stakeholder groups discussed:

| Stakeholder group | Examples / sectors |
|---|---|
| Government & public bodies | DESNZ, UK Government, devolved governments, local authorities |
| Regulators | Ofgem and other relevant regulatory bodies |
| Electricity generation | Offshore wind, onshore wind, solar, nuclear, biomass, gas |
| Electricity networks | Transmission Owners, DNOs, DSOs |
| Gas | Gas transmission, distribution, suppliers, storage, infrastructure |
| Energy suppliers & retailers | Electricity/gas suppliers and energy retailers |
| Flexibility providers | Battery storage, demand-side response, aggregators |
| Hydrogen | Hydrogen producers, networks, storage and users |
| Heat | Heat networks, heat-pump and low-carbon heating organisations |
| Industrial energy users | Manufacturing, chemicals, steel, cement and major users |
| Transport | EV charging, EVs, rail, aviation and maritime |
| Consumers | Households, businesses and consumer organisations |
| Communities | Community energy and local organisations |
| Environment | Environmental NGOs and conservation organisations |
| Land & marine | Landowners, agriculture, fisheries and offshore interests |
| Technology & digital | Technology, data, AI, cybersecurity and telecoms |
| Academia & research | Universities and energy research organisations |
| Finance & investment | Banks, investors and infrastructure funds |
| Infrastructure developers | Renewable, network and storage developers |
| Media | Energy and specialist media |
| International organisations | International energy organisations and system operators |

The key classification distinction is:

- **Stakeholder** = who is involved?
- **Sector** = which part of the energy system?
- **Topic** = what is happening?

---

## 2. Suggested Stakeholder Taxonomy

| Code | Stakeholder | Sector |
|---|---|---|
| GOV | Government | Public sector |
| REG | Regulators | Regulation |
| GEN | Electricity generation | Electricity |
| NET | Electricity networks | Electricity |
| GAS | Gas | Gas |
| SUP | Energy suppliers | Energy retail |
| STO | Energy storage | Electricity |
| FLX | Flexibility | Electricity |
| HYD | Hydrogen | Hydrogen |
| HEA | Heat | Heat |
| IND | Industry | Industrial energy |
| TRA | Transport | Transport |
| CON | Consumers | Consumer |
| COM | Communities | Community |
| ENV | Environment | Environment |
| LAN | Land & marine | Land/marine |
| DIG | Digital & technology | Technology |
| RES | Research | Academia |
| FIN | Finance | Financial |
| DEV | Infrastructure developers | Infrastructure |
| INT | International | International energy |
| MED | Media | Media |

### Example classification

```json
{
  "article_id": "12345",
  "primary_sector": "GEN",
  "secondary_sectors": ["NET", "FIN"],
  "stakeholders": [
    {
      "name": "Offshore wind developers",
      "category": "GEN",
      "role": "generator"
    },
    {
      "name": "Transmission network operators",
      "category": "NET",
      "role": "network_operator"
    }
  ],
  "topics": [
    "offshore wind",
    "grid connection",
    "investment"
  ],
  "neso_relevance": "high"
}
```

---

## 3. Database Model

The taxonomy should preferably be stored as reference data rather than embedded throughout application code.

```text
stakeholder_sector
------------------
id
code
name
description
parent_id
active

article_stakeholder
-------------------
article_id
stakeholder_id
role
confidence

article_sector
--------------
article_id
sector_id
primary
confidence
```

---

# 4. NESO Purpose

NESO was created as a result of the UK's 2023 Energy Act and builds on the previous Electricity System Operator (ESO).

The supplied NESO purpose is:

> NESO is responsible for planning and delivering the energy of today and the future. It looks at all sources of energy, such as gas and electricity, and works with customers, other organisations and government to deliver what is needed to reach a zero-carbon future.

NESO's customers include groups and organisations across the energy system that it works with.

The move from the previous ESO role expands responsibility from supplying electricity to taking a broader whole-energy-system role.

The AI should therefore assess news against NESO's actual purpose and responsibilities rather than simply checking whether NESO is mentioned.

---

# 5. NESO Responsibilities

The agreed responsibility taxonomy is:

| Code | Responsibility | AI focus |
|---|---|---|
| SP | Strategic Planning | Whole-energy-system planning, scenarios, energy transition and recommendations |
| SOS | Security of Supply | Supply/demand, resource adequacy, capacity and energy security |
| SO | Systems Operations | System operation, flexibility, balancing and operational capability |
| CON | Connections | Connections, queues, dates, capacity, offshore grids and storage |
| RES | Whole Energy System Resilience | Risks, vulnerabilities, emergency response and restoration |
| EI | Energy Insights | Trends, analysis, evidence, stakeholder perspectives and advice |
| EM | Energy Markets | Electricity/gas/hydrogen/carbon markets, balancing and flexibility |
| DAI | Data & AI | Data quality, access, interoperability, governance, AI and analytics |

---

# 6. Strategic Planning

NESO develops comprehensive and independent insights across the entire energy system.

Relevant areas include:

- Whole-energy-system planning
- Future energy scenarios
- Energy-transition planning
- Long-term system development
- Recommendations to policymakers
- Recommendations to industry
- Recommendations to NESO leadership
- Interactions between energy vectors

---

# 7. Security of Supply

Relevant areas include:

- Whole-energy-system scenarios
- Future supply and demand
- Resource adequacy
- Energy security
- Capacity Market
- Seasonal Outlook Reports
- Generation availability
- Fuel availability
- Interconnection
- Storage
- Network constraints
- Extreme events
- Trusted, robust and transparent data and methods

---

# 8. Systems Operations

Relevant areas include:

- Operating and improving energy systems
- Engineering expertise
- Data science
- Intelligent systems
- Operational flexibility
- Balancing
- Demand response
- Faster analysis and decision making
- Secure and sustainable energy operation
- Customer relationships and operable flexibility

---

# 9. Connections

Relevant areas include:

- Easier and timely connections
- Connection queues
- Connection dates
- Generation connections
- Demand connections
- Storage connections
- Connection infrastructure
- Increasing electrification
- Strategic network planning
- Offshore grids
- Innovative connection solutions
- Reducing delays and associated costs

---

# 10. Whole Energy System Resilience

Relevant areas include:

- Identifying risks and vulnerabilities
- Whole-energy-system risk assessments
- Resilience assessments
- Interactions between energy vectors
- Emergency preparation and response
- Investigations of incidents
- Unbiased recommendations following events
- Seasonal Outlooks
- Capacity Market
- Resource Adequacy
- Electricity System Restoration Standard (ESRS)

---

# 11. Energy Insights

Relevant areas include:

- Stakeholder engagement
- Long-term energy trends
- Independent analysis
- Transparent analysis
- Recommendations to UK Government
- Recommendations to Ofgem
- Policy decisions
- Industry strategy
- Emerging developments

---

# 12. Energy Markets

Relevant areas include:

- Electricity markets
- Gas markets
- Hydrogen markets
- Carbon markets
- Cross-market solutions
- Market strategy
- Efficient investment
- Secure net-zero electricity
- Balancing markets
- Ancillary services
- Low-carbon flexibility
- Transmission and distribution markets

---

# 13. Data & AI

Data & AI was added as a full NESO responsibility.

The supplied purpose is that understanding the full picture of the energy system is necessary both for live operations and future planning. Energy-system data is held in many different places by many organisations, which can lead to:

- varying data quality
- slow data sharing
- unavailable data
- incompatible data
- fragmented information

NESO's Data & AI objectives include:

- Enabling trustworthy data
- Making data easily accessible
- Providing fortified data as a building block of the energy transition
- Enabling effective data exchange
- Supporting collaboration on AI-driven decisions
- Implementing standardised frameworks
- Providing strong data governance
- Championing interoperability
- Using AI to unlock valuable insights
- Supporting critical evidence-based decisions
- Delivering tangible benefits for consumers

### Data & AI subcategories

```text
Data quality
Data accuracy
Data reliability
Data provenance
Data access
Data availability
Data sharing
Data exchange
Data standards
Data interoperability
Data integration
Data governance
Data ownership
Data management
Data security
Artificial intelligence
Machine learning
Predictive analytics
Intelligent systems
Automation
AI-assisted decision making
Energy-system forecasting
Energy-system modelling
Scenario analysis
Evidence-based decision making
Consumer benefits
```

An article mentioning AI should **not automatically be classified as highly relevant to NESO Data & AI**. The AI must establish a meaningful connection to the energy system, energy transition, decision making, interoperability, data or consumer outcomes.

---

# 14. Common NESO System Prompt

```text
You are an energy-sector news analysis assistant specialising in
the National Energy System Operator (NESO) and the Great Britain
energy system.

NESO was created following the UK's 2023 Energy Act. NESO builds on
the previous Electricity System Operator (ESO) role and has a broader
responsibility covering the whole energy system.

NESO's purpose is to plan and deliver the energy system of today and
the future. It considers major sources and forms of energy, including
electricity and gas, and works with customers, government, industry
and other organisations to support the transition towards a
zero-carbon future.

NESO's principal responsibilities are:

1. STRATEGIC PLANNING
2. SECURITY OF SUPPLY
3. SYSTEMS OPERATIONS
4. CONNECTIONS
5. WHOLE ENERGY SYSTEM RESILIENCE
6. ENERGY INSIGHTS
7. ENERGY MARKETS
8. DATA AND AI

NESO operates independently and has no commercial interest in
favouring one source of energy over another.

When analysing an article, determine whether it has a meaningful
relationship to one or more of these NESO responsibilities.

Do not assume an article is relevant simply because it mentions
energy, electricity, government, a company, renewable technology,
technology or AI.

Analyse only information supported by the article.
Do not invent facts.
Clearly distinguish facts, claims, forecasts and analysis.
```

---

# 15. Article Understanding Prompt

```text
Analyse the following news article.

Identify:

- main_event
- organisations
- people
- technologies
- projects
- policies
- markets
- locations
- dates
- financial_values
- energy_sources
- energy_system_issues
- claims
- forecasts
- decisions
- announcements

For each important item, distinguish between:

FACT
CLAIM
FORECAST
OPINION

Use only information contained in the article.

ARTICLE:
{article_content}
```

---

# 16. NESO Responsibility Classification Prompt

```text
Determine which NESO responsibilities are relevant to this article.

Allowed responsibilities:

STRATEGIC_PLANNING
SECURITY_OF_SUPPLY
SYSTEMS_OPERATIONS
CONNECTIONS
WHOLE_ENERGY_SYSTEM_RESILIENCE
ENERGY_INSIGHTS
ENERGY_MARKETS
DATA_AND_AI

For each relevant responsibility provide:

- responsibility
- relevance: HIGH, MEDIUM or LOW
- explanation
- supporting evidence from the article

An article may relate to multiple responsibilities.

Do not classify an article as relevant merely because NESO, ESO or
another energy organisation is mentioned.

Consider the substance of the article and its relationship to
NESO's actual responsibilities.

ARTICLE:
{article_content}
```

---

# 17. NESO Relevance Prompt

```text
Assess the overall relevance of this article to NESO.

Use:

HIGH
MEDIUM
LOW
NONE

HIGH:
The article directly concerns an area within NESO's responsibilities
or a development that could materially affect NESO's activities.

MEDIUM:
The article concerns an energy-system development that is relevant
to one or more NESO responsibilities but is not directly about NESO.

LOW:
The article has an indirect or limited relationship with NESO's
responsibilities.

NONE:
There is no meaningful relationship with NESO's responsibilities.

Explain the classification using evidence from the article.

ARTICLE:
{article_content}
```

---

# 18. Executive Summary Prompt

```text
Create a concise executive summary of this article for a
professional NESO reader.

The summary should explain:

1. What happened?
2. Who is involved?
3. What part of the energy system is affected?
4. Why is this relevant to NESO, if relevant?
5. Which NESO responsibility or responsibilities are involved?
6. What important numbers, dates, targets or decisions are reported?

Use 3-5 sentences.

Use factual language.

Do not speculate.

Do not present claims or forecasts as established facts.

ARTICLE:
{article_content}

NESO ANALYSIS:
{neso_analysis}
```

---

# 19. Why This Matters to NESO Prompt

```text
Explain why this article may matter to NESO.

Consider:

- Strategic Planning
- Security of Supply
- Systems Operations
- Connections
- Whole Energy System Resilience
- Energy Insights
- Energy Markets
- Data & AI

Also consider NESO's role in:

- supporting the transition to a zero-carbon energy system
- whole-energy-system planning
- working with customers
- providing independent analysis
- advising government and Ofgem
- maintaining secure and resilient energy systems

Separate:

DIRECT_RELEVANCE
POTENTIAL_RELEVANCE
NO_CLEAR_RELEVANCE

Do not speculate beyond what can reasonably be supported by the article.

ARTICLE:
{article_content}
```

---

# 20. Stakeholder Classification Prompt

```text
Identify the significant stakeholders in the article.

Classify each stakeholder as one or more of:

Government
Regulator
Electricity generator
Network operator
Energy supplier
Storage provider
Flexibility provider
Energy developer
Hydrogen organisation
Gas organisation
Heat organisation
Industrial energy user
Transport organisation
Consumer
Community
Environmental organisation
Landowner
Marine organisation
Technology organisation
Data/AI organisation
Research organisation
Investor
International organisation
Other

For each stakeholder identify:

- name
- category
- role
- relationship to the article
- relationship to NESO, if stated or directly evident

Do not assume that an organisation is a NESO customer unless the
article or provided context supports this.

ARTICLE:
{article_content}
```

---

# 21. Sector Classification Prompt

```text
Identify the energy sectors affected by the article.

Possible sectors:

Electricity generation
Electricity transmission
Electricity distribution
Gas
Hydrogen
Heat
Energy storage
Flexibility
Energy markets
Transport
Industry
Buildings
Consumers
Technology
Data and AI
Environment
Land
Marine
Finance
Other

Return:

primary_sector
secondary_sectors
evidence

Only select sectors supported by the article.
```

---

# 22. Energy-System Topic Prompt

```text
Identify the main energy-system topics in the article.

Possible topics include:

Strategic planning
Whole-system planning
Energy transition
Net zero
Energy security
Security of supply
Resource adequacy
Demand forecasting
Generation forecasting
System operation
Grid balancing
Flexibility
Demand-side response
Ancillary services
Connections
Grid connections
Transmission
Distribution
Network planning
Network investment
Network constraints
Offshore grids
Interconnectors
Offshore wind
Onshore wind
Solar
Nuclear
Gas
Hydrogen
Energy storage
Battery storage
Heat
Electrification
Electric vehicles
Industrial decarbonisation
Energy markets
Electricity markets
Gas markets
Hydrogen markets
Carbon markets
Energy prices
Investment
Regulation
Policy
Resilience
Emergency preparedness
System restoration
ESRS
Climate
Environment
Biodiversity
Data
Artificial intelligence
Digitalisation
Cybersecurity
Innovation

Return the 1-7 most relevant topics.
```

---

# 23. Security of Supply Analysis Prompt

```text
Analyse whether this article contains information relevant to
security of energy supply in Great Britain.

Consider:

- supply
- demand
- generation capacity
- resource adequacy
- fuel availability
- network constraints
- interconnection
- storage
- weather
- extreme events
- infrastructure risks
- energy-system dependencies
- resilience

Return:

relevant: true/false

If true:

security_issue:
evidence:
affected_energy_source:
potential_system_effect:
uncertainty:

Do not create predictions that are not contained in the article.
```

---

# 24. Connections Analysis Prompt

```text
Determine whether this article concerns energy connections.

Look for:

- grid connections
- connection queues
- connection dates
- transmission connections
- distribution connections
- generation connections
- demand connections
- storage connections
- offshore wind connections
- offshore grids
- network capacity
- connection costs
- connection delays
- new connection infrastructure

If relevant, explain:

- what is being connected
- where
- who is involved
- the stated problem
- the stated solution
- relevant dates
- capacity
- cost
- implications for the energy system

ARTICLE:
{article_content}
```

---

# 25. Energy Markets Analysis Prompt

```text
Determine whether this article concerns energy-market design,
operation or reform.

Consider:

- electricity markets
- gas markets
- hydrogen markets
- carbon markets
- market integration
- balancing markets
- ancillary services
- flexibility markets
- market reform
- investment signals
- cross-market solutions

Explain how the article relates to NESO's energy-market
responsibilities.

Separate reported facts from analysis and forecasts.

ARTICLE:
{article_content}
```

---

# 26. Data & AI Classification Prompt

```text
Analyse whether this article is relevant to NESO's Data & AI
responsibilities.

NESO's Data & AI responsibilities focus on:

1. TRUSTWORTHY DATA
   - data quality
   - data accuracy
   - data reliability
   - data provenance

2. DATA ACCESS AND EXCHANGE
   - data sharing
   - data availability
   - information exchange
   - collaboration between organisations

3. DATA STANDARDS AND INTEROPERABILITY
   - standardisation
   - common data models
   - interoperability
   - system integration
   - incompatible systems

4. DATA GOVERNANCE
   - data governance
   - data ownership
   - data management
   - data security
   - data controls
   - responsible data use

5. AI AND INTELLIGENT SYSTEMS
   - artificial intelligence
   - machine learning
   - predictive analytics
   - intelligent systems
   - automation
   - AI-assisted decisions

6. ENERGY-SYSTEM INSIGHT
   - using data or AI to understand the energy system
   - forecasting
   - modelling
   - scenario analysis
   - evidence-based decision making

7. CONSUMER BENEFITS
   - affordability
   - security
   - sustainability
   - energy-system efficiency
   - consumer outcomes

Return:

{
  "relevant": true/false,
  "relevance": "HIGH/MEDIUM/LOW",
  "areas": [],
  "reason": "",
  "evidence": []
}

Only identify an area when supported by the article.

ARTICLE:
{article_content}
```

---

# 27. Data & AI Impact Analysis Prompt

```text
Analyse the implications of this article for NESO's Data & AI
responsibilities.

Consider:

DATA QUALITY
DATA ACCESS
DATA SHARING
DATA STANDARDS
INTEROPERABILITY
DATA GOVERNANCE
DATA SECURITY
AI
INTELLIGENT SYSTEMS
ENERGY-SYSTEM INSIGHT
DECISION MAKING
CONSUMER BENEFITS

For each relevant area identify:

- what the article reports
- the organisations involved
- the potential relevance to NESO
- reported benefits
- potential benefits
- reported risks
- potential risks
- uncertainties

Clearly distinguish reported information from your analysis.

Do not speculate beyond the information provided.
```

---

# 28. General Impact Analysis Prompt

```text
Analyse the implications of this article for NESO and the
Great Britain energy system.

Consider impacts on:

- strategic planning
- security of supply
- system operations
- connections
- resilience
- energy insights
- energy markets
- data and AI
- energy transition
- NESO customers

Separate the results into:

REPORTED_IMPACTS
POTENTIAL_IMPACTS
RISKS
OPPORTUNITIES
UNCERTAINTIES

REPORTED_IMPACTS must be explicitly supported by the article.

POTENTIAL_IMPACTS, RISKS and OPPORTUNITIES must be clearly
identified as analysis rather than established facts.
```

---

# 29. Key Facts Prompt

```text
Extract the most important factual information from the article.

Return:

- organisations
- people
- dates
- locations
- quantities
- targets
- commitments
- projects
- technologies
- policy/regulatory references
- financial figures
- energy-system figures

Do not paraphrase facts in a way that changes their meaning.

ARTICLE:
{article_content}
```

---

# 30. Quote Extraction Prompt

```text
Extract important statements made by named people or organisations.

For each quote return:

- speaker
- organisation
- quote
- context

Only include quotations explicitly present in the source article.

Do not create or reconstruct quotations.

ARTICLE:
{article_content}
```

---

# 31. Final Human Review Prompt

```text
Create a final NESO news-review item.

Return:

HEADLINE

EXECUTIVE_SUMMARY

NESO_RELEVANCE
- level
- reason

NESO_RESPONSIBILITIES
- relevant responsibilities

STAKEHOLDERS
- significant stakeholders
- category
- role

SECTORS
- primary
- secondary

TOPICS
- main topics

KEY_FACTS
- most important facts

SECURITY_OF_SUPPLY
- relevant/not relevant
- analysis if relevant

CONNECTIONS
- relevant/not relevant
- analysis if relevant

ENERGY_MARKETS
- relevant/not relevant
- analysis if relevant

DATA_AND_AI
- relevant/not relevant
- analysis if relevant

IMPACTS
- reported
- potential

RISKS
- reported
- potential

UNCERTAINTIES

IMPORTANT_QUOTES

SOURCE

Rules:

- Be factual and concise.
- Do not invent information.
- Do not speculate.
- Attribute claims to the organisation or person making them.
- Preserve important numbers, dates and targets.
- Do not assume that every energy-sector development is relevant to NESO.
- Do not assume that mentioning AI makes an article relevant to NESO's Data & AI responsibility.
```

---

# 32. Recommended Final JSON

```json
{
  "article_id": "12345",
  "headline": "...",
  "executive_summary": "...",

  "neso_relevance": {
    "level": "HIGH",
    "reason": "..."
  },

  "neso_responsibilities": [
    {
      "code": "DAI",
      "name": "Data & AI",
      "relevance": "HIGH",
      "reason": "..."
    },
    {
      "code": "SP",
      "name": "Strategic Planning",
      "relevance": "MEDIUM",
      "reason": "..."
    }
  ],

  "data_and_ai": {
    "relevant": true,
    "areas": [
      "Data interoperability",
      "AI decision support",
      "Energy-system insight"
    ],
    "summary": "...",
    "reported_benefits": [],
    "potential_benefits": [],
    "reported_risks": [],
    "potential_risks": [],
    "uncertainties": []
  },

  "stakeholders": [],
  "sectors": [],
  "topics": [],
  "key_facts": [],

  "security_of_supply": {},
  "connections": {},
  "energy_markets": {},

  "reported_impacts": [],
  "potential_impacts": [],
  "risks": [],
  "uncertainties": [],
  "important_quotes": []
}
```

---

# 33. Recommended AI Processing Flow

```text
                 NORMALISED ARTICLE
                         |
                         v
              +---------------------+
              |  Article Analysis    |
              +----------+----------+
                         |
             +-----------+------------+
             |           |            |
             v           v            v
        STAKEHOLDERS   SECTORS      TOPICS
             |           |            |
             +-----------+------------+
                         |
                         v
                NESO RELEVANCE
                         |
                         v
             NESO RESPONSIBILITY
                         |
        +----+----+----+----+----+----+----+----+
        |    |    |    |    |    |    |    |
        SP   SOS   SO  CON  RES   EI   EM   DAI
                                            |
                                            v
                                     DATA & AI ANALYSIS
                                            |
                                            v
                                      IMPACT / RISK
                                            |
                                            v
                                     FINAL SUMMARY
                                            |
                                            v
                                      HUMAN REVIEW
```

## Recommended grouping into AI calls

### Call 1 — SUMMARY

```text
article_understanding
key_facts
executive_summary
quotes
```

### Call 2 — CLASSIFICATION

```text
stakeholders
sectors
topics
neso_relevance
neso_responsibilities
```

### Call 3 — ANALYSIS

```text
security_of_supply
connections
energy_markets
data_and_ai
reported_impacts
potential_impacts
human_review
```

---

# 34. Final Design Principle

The central principle for this NESO news pipeline is:

> **The AI should assess each article against NESO's purpose and responsibilities, not merely summarise the article.**

The resulting review item should answer:

1. What happened?
2. Who is involved?
3. Which sector is affected?
4. Which NESO responsibility is relevant?
5. Why might it matter to NESO?
6. What are the reported facts, impacts and uncertainties?
7. Does Data & AI have a meaningful role?

This makes the system a NESO-focused energy intelligence and human-review pipeline rather than a generic news summarisation service.
