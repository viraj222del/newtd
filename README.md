# Technical Debt Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Team: BlackBox

##  Live Demo

🔗 [Live Demo](https://technicaldebtanalyzer.streamlit.app)  
🎥 [Video Demo](https://youtu.be/j8wcMvob1IQ?si=2lwcagYU73zMSOt6)

##  Introduction
Technical Debt Analyzer is a developer-friendly tool that helps teams maintain high code quality by providing comprehensive analysis and actionable insights. It combines static code analysis with AI-powered recommendations to help you write better, more secure code.

##  Table of Contents

- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Key Features](#-key-features)
- [AI-Powered Analysis](#-ai-powered-analysis)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Contributors](#-contributors)
- [License](#-license)

##  Problem: Hidden cost of VibeCoding
- **Technical Debt**: Hasty code makes the software fragile and expensive to fix, slowing down all future work.
- **Security Risks:** Rushed coding creates serious flaws that leave the software vulnerable to attacks.
- **Unable to Scale:** The weak foundation collapses under heavy user load, preventing real growth.
- **Low Developer Productivity:** Messy code increases debugging time and reduces team efficiency.

##  Our Solution - AI Powered Technical Debt Analyzer
- **AI-Powered Code Analysis:** Uses AI to scan the entire repository and understand real code risks.
- **Clear Risk Scores:** Provides simple technical debt and security risk scores for quick decisions.
- **Actionable Insights:** Highlights the main risk factor per file to guide focused improvements.
- **Scalability Readiness Check:** Identifies architectural and performance risks that can block future growth.
##  Key Features

### Code Metrics
- **Lines of Code (LOC)**: Total lines of executable logic in the repository, excluding comments and blank lines.
- **Cyclomatic Complexity**: Measures logic density based on the number of independent control flow paths (ifs, loops).
- **Churn Analysis**: Tracks the volume and frequency of code changes over time to identify unstable or volatile files.
- **Risk Score**: A quantitative 0–100 grade indicating potential technical debt based on complexity, history, and stability.
- **Ownership Entropy**: Measures how code knowledge is distributed among contributors to identify knowledge silos.
- **Bug Fix Frequency**: Tracks how often a file is modified specifically to resolve software defects or issues.
- **Main Risk Factor**: Identifies the specific primary driver (e.g., high complexity or age) behind a module's debt.
- **Fan-in**: Measures system coupling by counting how many other internal files depend on or import a specific module.
- **Dependencies**: Tracks the total number of external libraries or internal modules a file requires to function.
- **Test Status**: An estimated risk factor indicating the likelihood of missing test coverage based on file naming and path.
- **Systemic Score**: Measures the "blast radius" of a failure by multiplying internal risk by system-wide coupling (Fan-in).
- **Comment to Code Ratio**: Calculates the balance of documentation relative to raw logic to ensure long-term readability.
- **Code Duplication**: Identifies duplicated code blocks
- **File Size Analysis**: Flags unusually large files
- **Comment Density**: Measures code documentation levels
- **Function Length**: Identifies overly complex functions
- **Maintainability Index**: A combined health score indicating how easily a file can be supported, modified, and evolved.
- **Code Quality Index**: A composite 0–100 grade balancing structural integrity, documentation density, and historical stability.

### Security Analysis
- **API Key Detection**: Scans for exposed API keys and credentials across the entire codebase.
- **Security Vulnerabilities**: Identifies common security anti-patterns and risky code structures.
- **Dependency Risk**: Analyzes third-party packages for known vulnerabilities and outdated versions.
- **Hardcoded Secret Detection**: Scans for passwords, private keys, and sensitive tokens embedded in source code or configuration files.
- **Insecure Function Mapping**: Identifies the usage of dangerous functions or libraries prone to exploitation (e.g., `eval`, `exec`).
- **Config Misconfiguration**: Detects insecure settings in environment files, Dockerfiles, or infrastructure-as-code scripts.

### Contributor Analysis
- **Efficiency Score**: Measures the average impact per developer by calculating lines of code added relative to their total commits.
- **Total Commits Distribution**: Tracks the volume of activity and frequency of saves for each individual contributor.
- **Lines Added Distribution**: Quantifies the raw coding output per developer to identify major code authors.
- **Risk Contribution**: Evaluates the amount of technical debt or complexity introduced by each specific contributor's changes.
- **Bus Factor Analysis**: Identifies critical project files that rely on too few developers, posing a risk if key members leave.
- **Contributor Diversity**: Visualizes the number of unique developers working on each file to ensure balanced code ownership.
- **Commits & Lines (%)**: Provides a percentage-based breakdown of total repository work distributed across the team.
- **Knowledge Concentration Risk**: Pinpoints files where expertise is siloed within a single person, creating maintenance bottlenecks.
- **Top Risk Files**: Highlights the specific files with the highest concentration of risk and the lowest contributor diversity.

### AI-Powered Insights
- **Automated Code Review**: AI-generated suggestions for code improvements
- **Technical Debt Assessment**: Estimates effort required for maintenance
- **Refactoring Recommendations**: Specific suggestions for code improvement

##  AI-Powered Analysis
Our tool leverages Google's Gemini AI to provide:
- Contextual code analysis
- Smart recommendations for improvements
- Natural language explanations of complex issues
- Automated code review comments
- Predictive maintenance insights

##  Tech Stack
- **Frontend**: Streamlit, HTML, CSS, JavaScript
- **Backend**: Python, JavaScript
- **AI/ML**: Google Gemini API (Gemini 2.5 Flash, Gemini 3 Flash)
- **Authentication**: Firebase
- **Version Control**: Git
- **Deployment**: Streamlit Cloud

##  Getting Started

### Prerequisites

- Python 3.8+
- Git
- Google Cloud Account (for Gemini API)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/viraj22del/TechDebtAnalyzer
   cd code-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys 
   ```

4. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

##  Contributors

- [Visha Yadav](https://github.com/vishayadav) 
- [Viraj Ravani](https://github.com/v3ravani)


##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.











