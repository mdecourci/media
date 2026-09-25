# NESO News Processing Pipeline — AI Prompts and Taxonomy

## 1. Purpose

This document captures the design work from this chat for an Azure-based NESO news-processing pipeline. The focus is on the stakeholder/sector taxonomy, AI prompts, NESO-purpose-aware classification, Data & AI analysis, and the final AI processing flow.

---

## 2. NESO Stakeholders and Sectors

A practical taxonomy separates **sector** from **stakeholder type**.

### Stakeholder / sector categories

| ID | Category | Typical organisations / examples |
|---|---|---|
| GOV | Government & public bodies | UK Government departments, devolved administrations, local authorities |
| REG | Regulators | Ofgem and other relevant regulators |
| GEN | Electricity generation | Renewable, nuclear, thermal and other generators |
| NET | Electricity networks | Transmission and distribution network operators |
| GAS | Gas | Gas producers, networks, storage and market participants |
| SUP | Energy suppliers & retailers | Energy suppliers and retail businesses |
| STO | Energy storage | Batteries, pumped hydro and other storage providers |
| FLX | Flexibility | Demand response, aggregators and flexibility service providers |
| HYD | Hydrogen | Hydrogen producers, networks, users and technology providers |
| HEA | Heat | Heat networks, heat-pump providers and other heat-sector organisations |
| IND | Industrial energy users | Energy-intensive industry and major commercial users |
| TRA | Transport | EVs, charging infrastructure and transport-energy organisations |
| CON | Consumers | Domestic and commercial energy consumers |
| COM | Communities & local interests | Community energy and local organisations |
| ENV | Environment | Environmental organisations and sustainability bodies |
| LAN | Land & marine | Landowners, offshore interests and marine stakeholders |
| DIG | Technology & digital | Data, AI, software, cloud and digital infrastructure organisations |
| RES | Academia & research | Universities, research institutes and think tanks |
| FIN | Finance & investment | Banks, investors, insurers and infrastructure funds |
| DEV | Energy infrastructure developers | Developers of generation, networks, storage and other infrastructure |
| INT | International organisations | International energy organisations and cross-border institutions |
| MED | Media | Energy and business news organisations |

### Suggested database representation

Keep the sector and stakeholder classification separate.

Possible tables:

```text
stakeholder_sector
------------------
id
code
name
description

article_stakeholder
-------------------
article_id
stakeholder_id
confidence

article_sector
--------------
article_id
sector_id
is_primary
confidence
```

---

## 3. Suggested Article Classification JSON

```json
{
  "article_id": "12345",
  "primary_sector": "NET",
  "secondary_sectors": ["GEN", "GOV"],
  "stakeholders": [
    {
      "code": "NET",
      "name": "Electricity networks",
      "confidence": 0.94
    }
  ],
  "topics": [
    "connections",
    "network_planning"
  ],
  "neso_relevance": "high"
}
```

---

# 4. NESO Purpose and Responsibilities

The AI prompts should evaluate articles against the actual purpose and responsibilities of NESO rather than simply producing a generic news summary.

NESO was created as a result of the UK's 2023 Energy Act and builds on the previous Electricity System Operator (ESO).

The supplied NESO purpose/context for this project is:

- Planning and delivering the energy of today and the future.
- Looking across energy sources including gas and electricity.
- Working with customers, organisations and government to support a zero-carbon future.
- NESO's customers include the groups and organisations it works with across the energy system.
- Providing independent, whole-energy-system insight and recommendations.
- Supporting security of supply.
- Operating the energy system using engineering, data science and intelligent systems.
- Improving connections and reducing connection delays.
- Assessing whole-energy-system resilience.
- Providing energy insights and recommendations to government and Ofgem.
- Developing a coherent whole-energy-system market strategy.
- Using data and AI to improve evidence-based decisions and consumer outcomes.

---

# 5. NESO Responsibility Taxonomy

Use these responsibility codes when classifying an article.

| Code | Responsibility | Purpose |
|---|---|---|
| SP | Strategic Planning | Whole-energy-system insight, scenarios and recommendations |
| SOS | Security of Supply | Future supply/demand, adequacy and security |
| SO | Systems Operations | Operating the energy system safely, securely and efficiently |
| CON | Connections | Improving connection processes, dates and network coordination |
| RES | Whole Energy System Resilience | Identifying risks, vulnerabilities and emergency resilience |
| EI | Energy Insights | Monitoring trends and providing evidence-based recommendations |
| EM | Energy Markets | Whole-energy-system market strategy, balancing and flexibility |
| DAI | Data & AI | Data quality, access, interoperability, governance and AI-enabled insight |

---

# 6. NESO Strategic Planning

Strategic Planning provides comprehensive, independent insight across the whole energy system.

The AI should consider:

- Whole-energy-system planning
- Future energy scenarios
- Long-term energy-system change
- Recommendations to policymakers
- Recommendations to industry decision makers
- Recommendations to NESO leadership
- Accelerating the energy transition
- Interactions between different energy vectors

---

# 7. Security of Supply

Security of Supply covers whole-energy-system scenarios and future supply/demand.

The AI should consider:

- Supply adequacy
- Demand forecasts
- Capacity
- Resource adequacy
- Energy security
- Whole-energy-system scenarios
- Emerging scenarios
- Flexible supply and demand
- Objective and impartial analysis
- Robust and transparent methods/data
- Seasonal Outlook Reports
- Capacity Market
- Resource Adequacy
- Electricity System Restoration Standard (ESRS)

---

# 8. Systems Operations

Systems Operations combines human expertise, engineering, data science and intelligent systems.

The AI should consider:

- Operational flexibility
- Real-time or near-real-time energy-system operation
- Engineering expertise
- Data science
- Intelligent systems
- Operational automation
- Faster analysis and decision making
- Secure energy operation
- Sustainable energy operation
- Affordable energy
- Customer relationships

---

# 9. Connections

The Connections responsibility aims to make energy connections easier and more timely.

The AI should consider:

- Connection delays
- Connection queues
- Connection dates
- Grid connections
- Generation connections
- Storage connections
- Demand connections
- Coordinated network planning
- Infrastructure management
- Offshore grids
- Energy storage
- Reducing costs caused by connection delays
- Local jobs and economic growth
- Homes generating or storing energy
- Energy-system expansion
- Clean energy deployment

---

# 10. Whole Energy System Resilience

This responsibility focuses on risks and vulnerabilities across the whole energy system.

The AI should consider:

- Energy-system risks
- Vulnerabilities
- Whole-energy-system resilience
- Interactions between energy vectors
- Emergency response
- Emergency investigations
- Industry preparedness
- Compliance
- Electricity System Restoration Standard
- Seasonal Outlook Reports
- Capacity Market
- Resource Adequacy
- Recommendations following incidents

---

# 11. Energy Insights

Energy Insights focuses on stakeholder engagement, long-term trends and recommendations.

The AI should consider:

- Stakeholder perspectives
- Energy-system trends
- Long-term trends
- Evidence-based recommendations
- Recommendations to UK Government
- Recommendations to Ofgem
- Industry perspectives
- Different stakeholder viewpoints

---

# 12. Energy Markets

NESO's energy-market role considers the whole energy system rather than electricity in isolation.

The AI should consider:

- Electricity markets
- Gas markets
- Hydrogen markets
- Carbon markets
- Market integration
- Whole-energy-system market strategy
- Government interaction
- Regulator interaction
- Industry interaction
- Efficient investment
- Secure net-zero electricity
- Value for businesses
- Value for industry
- Value for households
- Electricity balancing
- Ancillary services
- Low-carbon flexibility
- Transmission/distribution interaction

---

# 13. Data & AI

Data & AI is a major NESO responsibility in this taxonomy.

### Purpose

The full picture of the energy system requires data held by many organisations.

The supplied context identifies several challenges:

- Data quality varies.
- Data may be shared slowly.
- Data may not be shared at all.
- Data may not be compatible between organisations.

NESO's Data & AI role is therefore concerned with enabling:

- Trustworthy data
- Easily accessible data
- Fortified data as a building block of the energy transition
- Effortless data exchange
- Collaboration on AI-driven decisions
- Standardised frameworks
- Strong data governance
- Interoperability
- AI-driven insights
- Evidence-based decisions
- Tangible consumer benefits

### Data & AI subcategories

| Subcategory | What the AI should identify |
|---|---|
| Data quality | Accuracy, reliability, completeness and quality |
| Data provenance | Source, lineage and traceability |
| Data access | Availability and accessibility |
| Data exchange | Sharing and collaboration between organisations |
| Standards | Common standards and frameworks |
| Interoperability | Compatibility and integration |
| Governance | Ownership, controls, security and responsible use |
| AI | AI, ML, predictive analytics and intelligent systems |
| Energy-system insight | Forecasting, modelling, scenario analysis and evidence |
| Consumer benefit | Affordability, security, sustainability and efficiency |

---

# 14. Recommended AI Prompt Architecture

Rather than using a large number of completely independent prompts, group the work into a small number of AI calls.

Recommended flow:

```text
ARTICLE
   |
   v
WHAT HAPPENED?
   |
   v
WHO IS INVOLVED?
WHICH SECTOR?
WHAT TOPIC?
   |
   v
NESO RELEVANCE
   |
   v
WHICH NESO RESPONSIBILITY?
   |
   +--> SP
   +--> SOS
   +--> SO
   +--> CON
   +--> RES
   +--> EI
   +--> EM
   +--> DAI
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

This structure keeps the processing understandable and makes model execution easier to trace.

---

# 15. Common System Prompt

Use a common system instruction for the NESO AI processing stages.

```text
You are an energy-system news analysis assistant supporting the National Energy System Operator (NESO).

Your task is to analyse news articles objectively and identify information that is relevant to NESO's role across the whole energy system.

NESO's responsibilities include:

- Strategic Planning
- Security of Supply
- Systems Operations
- Connections
- Whole Energy System Resilience
- Energy Insights
- Energy Markets
- Data & AI

NESO considers the whole energy system, including electricity, gas, hydrogen, flexibility, storage, heat, transport and related infrastructure.

Analyse only information supported by the article.

Do not invent facts, causes, impacts, stakeholders or relationships.

Clearly distinguish:
- Facts explicitly stated in the article
- Reasonable implications supported by the article
- Information that is not known

When assessing potential NESO relevance, explain why the article relates to one or more NESO responsibilities.

Use concise, structured JSON-compatible output where requested.
```

---

# 16. Article Understanding Prompt

```text
Analyse the following news article.

Identify:

1. The main event or development.
2. The organisations involved.
3. The people or stakeholder groups involved, where explicitly stated.
4. The energy sectors involved.
5. The technologies involved.
6. The geographic scope.
7. The key facts.
8. Any dates, quantities or numerical information.
9. Any direct statements or important quotations.
10. Any important uncertainty or missing information.

Do not infer facts that are not supported by the article.

ARTICLE:
{{article}}
```

---

# 17. NESO Responsibility Classification Prompt

```text
Determine which NESO responsibilities are relevant to the article.

Responsibilities:

SP = Strategic Planning
SOS = Security of Supply
SO = Systems Operations
CON = Connections
RES = Whole Energy System Resilience
EI = Energy Insights
EM = Energy Markets
DAI = Data & AI

For each relevant responsibility provide:

- responsibility_code
- responsibility_name
- relevance: high, medium or low
- evidence from the article
- explanation

Only classify a responsibility when the article provides evidence that it is relevant.

ARTICLE:
{{article}}
```

---

# 18. NESO Relevance Prompt

```text
Assess the relevance of this article to NESO.

Consider NESO's role across:

- Strategic Planning
- Security of Supply
- Systems Operations
- Connections
- Whole Energy System Resilience
- Energy Insights
- Energy Markets
- Data & AI

Return:

{
  "neso_relevance": "high|medium|low|none",
  "reasons": [],
  "responsibilities": [],
  "evidence": []
}

Do not treat the presence of an energy-related keyword as sufficient evidence of NESO relevance.

ARTICLE:
{{article}}
```

---

# 19. Executive Summary Prompt

```text
Write a concise executive summary of the article for a NESO professional.

The summary must:

- Explain what happened.
- Identify the main organisations involved.
- Identify the relevant energy sector(s).
- Explain the significance of the development.
- Mention important numbers, dates or commitments.
- Avoid speculation.
- Focus on information useful to NESO.

Maximum length: approximately 120 words.

ARTICLE:
{{article}}
```

---

# 20. Why This Matters to NESO Prompt

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

For each relevant responsibility explain:

1. What part of the article creates the relevance.
2. What NESO activity could be affected.
3. Whether the impact is current, emerging or longer term.

Do not speculate beyond the evidence.

ARTICLE:
{{article}}
```

---

# 21. Stakeholder Classification Prompt

```text
Identify the stakeholder groups represented or directly affected by the article.

Use these categories:

GOV, REG, GEN, NET, GAS, SUP, STO, FLX, HYD, HEA,
IND, TRA, CON, COM, ENV, LAN, DIG, RES, FIN, DEV, INT, MED

For each stakeholder return:

- code
- name
- role in the article
- confidence

Only include stakeholders supported by the article.

ARTICLE:
{{article}}
```

---

# 22. Sector Classification Prompt

```text
Identify the energy sectors relevant to this article.

Possible sectors include:

- Electricity generation
- Electricity networks
- Gas
- Energy supply
- Energy storage
- Flexibility
- Hydrogen
- Heat
- Industry
- Transport
- Consumers
- Energy infrastructure
- Digital/data/AI
- Other relevant energy sectors

Return:

- primary sector
- secondary sectors
- evidence
- confidence

ARTICLE:
{{article}}
```

---

# 23. Energy-System Topic Prompt

```text
Identify the main energy-system topics in this article.

Consider topics such as:

- Energy transition
- Net zero
- Generation
- Renewable energy
- Nuclear
- Grid infrastructure
- Transmission
- Distribution
- Connections
- Storage
- Flexibility
- Demand
- Energy security
- Resilience
- Energy markets
- Balancing
- Ancillary services
- Hydrogen
- Heat
- Transport
- Data
- AI
- Digitalisation
- Regulation
- Investment
- Planning

Return the relevant topics with evidence from the article.

ARTICLE:
{{article}}
```

---

# 24. Security of Supply Analysis Prompt

```text
Analyse the article from a NESO Security of Supply perspective.

Identify any evidence relating to:

- Supply adequacy
- Demand
- Capacity
- Generation availability
- Resource adequacy
- Energy security
- Supply disruption
- Flexibility
- Storage
- Interconnection
- Future scenarios
- Emerging risks

For each relevant issue explain:

- What the article says.
- Why it could matter to security of supply.
- Whether the issue is current or future.
- Any uncertainty.

ARTICLE:
{{article}}
```

---

# 25. Connections Analysis Prompt

```text
Analyse the article from a NESO Connections perspective.

Identify evidence relating to:

- Grid connections
- Connection queues
- Connection dates
- Generation connections
- Demand connections
- Storage connections
- Network planning
- Infrastructure management
- Offshore grids
- Coordinated network development
- Connection delays
- Connection costs

Return only issues supported by the article.

ARTICLE:
{{article}}
```

---

# 26. Energy Markets Analysis Prompt

```text
Analyse the article from a NESO Energy Markets perspective.

Consider:

- Electricity markets
- Gas markets
- Hydrogen markets
- Carbon markets
- Market integration
- Balancing
- Ancillary services
- Flexibility
- Transmission/distribution interaction
- Investment signals
- Market reform
- Consumer and industrial impacts

Explain which issues are directly relevant to NESO's whole-energy-system market role.

ARTICLE:
{{article}}
```

---

# 27. Data & AI Analysis Prompt

```text
Analyse the article from a NESO Data & AI perspective.

Identify whether the article contains evidence relating to:

1. Data quality
2. Data availability
3. Data sharing
4. Data exchange
5. Data interoperability
6. Data standards
7. Data governance
8. Data provenance
9. Artificial intelligence
10. Machine learning
11. Predictive analytics
12. Intelligent systems
13. Automation
14. Evidence-based decision making
15. Energy-system modelling or forecasting
16. Consumer benefits enabled by data or AI

For every relevant item return:

- category
- evidence
- relevance to NESO
- potential opportunity
- potential risk

Do not assume that mentioning AI automatically makes an article strategically important to NESO.

ARTICLE:
{{article}}
```

---

# 28. Impact Analysis Prompt

```text
Analyse the potential implications of this article for NESO.

Separate the analysis into:

1. Direct impacts
2. Potential future impacts
3. Risks
4. Opportunities
5. Areas requiring monitoring

Map each item to one or more NESO responsibilities:

SP
SOS
SO
CON
RES
EI
EM
DAI

Clearly distinguish facts reported by the article from analytical implications.

ARTICLE:
{{article}}
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
{{article}}
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
{{article}}
```

---

# 31. Final Human Review Summary Prompt

```text
Create a final review item for a NESO human reviewer.

The output should contain:

1. Headline
2. Executive summary
3. Why it matters to NESO
4. NESO responsibilities affected
5. Stakeholders
6. Sectors
7. Topics
8. Key facts
9. Security of Supply implications
10. Connections implications
11. Energy Markets implications
12. Data & AI implications
13. Reported impacts
14. Potential impacts
15. Important quotations
16. Areas requiring human review

Clearly separate:

- What the article explicitly states
- What can reasonably be inferred
- What requires human assessment

ARTICLE:
{{article}}
```

---

# 32. Recommended Final JSON Structure

```json
{
  "article_id": "12345",
  "headline": "Example headline",

  "executive_summary": "...",

  "neso_relevance": {
    "level": "high",
    "reasons": []
  },

  "neso_responsibilities": [
    {
      "code": "SP",
      "name": "Strategic Planning",
      "relevance": "high",
      "evidence": []
    }
  ],

  "stakeholders": [
    {
      "code": "GEN",
      "name": "Electricity generation",
      "role": "...",
      "confidence": 0.95
    }
  ],

  "sectors": {
    "primary": "GEN",
    "secondary": ["NET", "STO"]
  },

  "topics": [],

  "key_facts": [],

  "security_of_supply": {
    "relevant": true,
    "issues": []
  },

  "connections": {
    "relevant": false,
    "issues": []
  },

  "energy_markets": {
    "relevant": true,
    "issues": []
  },

  "data_and_ai": {
    "relevant": false,
    "issues": []
  },

  "reported_impacts": [],

  "potential_impacts": [],

  "important_quotes": [],

  "human_review": {
    "questions": []
  }
}
```

---

# 33. Recommended AI Call Grouping

To reduce latency and token usage while keeping monitoring/tracing manageable, the prompts can be grouped into three main AI calls.

## Call 1 — SUMMARY

Purpose:

- Understand article
- Extract facts
- Produce executive summary
- Extract important quotations

Suggested outputs:

```text
article_understanding
key_facts
executive_summary
quotes
```

## Call 2 — CLASSIFICATION

Purpose:

- Stakeholders
- Sectors
- Topics
- NESO relevance
- NESO responsibilities

Suggested outputs:

```text
stakeholders
sectors
topics
neso_relevance
neso_responsibilities
```

## Call 3 — ANALYSIS

Purpose:

- Security of Supply
- Connections
- Energy Markets
- Data & AI
- Impacts
- Human-review questions

Suggested outputs:

```text
security_of_supply
connections
energy_markets
data_and_ai
reported_impacts
potential_impacts
human_review
```

This grouping provides a clear execution path for Azure monitoring and tracing.

---

# 34. Overall AI Processing Flow

```text
Raw Article
    |
    v
+-----------------------+
| Article Understanding |
+-----------------------+
    |
    v
+-----------------------+
| Classification        |
|                       |
| Stakeholders          |
| Sectors               |
| Topics                |
| NESO Relevance        |
| NESO Responsibilities |
+-----------------------+
    |
    v
+-----------------------+
| NESO Analysis         |
|                       |
| Security of Supply    |
| Connections           |
| Energy Markets        |
| Data & AI             |
| Impacts               |
+-----------------------+
    |
    v
+-----------------------+
| Final Review Item     |
+-----------------------+
    |
    v
Human Review
```

---

# 35. Design Principle

The central principle for this pipeline is:

> The AI should assess each article against NESO's purpose and responsibilities, not merely summarise the article.

This allows the resulting review item to answer both:

1. **What happened?**
2. **Why might this matter to NESO?**

The second question is the key differentiator between a generic news summarisation service and a NESO-focused intelligence pipeline.
