# Code Quality & Security Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful tool for analyzing code quality, identifying security vulnerabilities, and tracking technical debt in software repositories.

## 📌 Live Demo

🔗 [Live Demo](https://your-demo-link.vercel.app)  
🎥 [Video Demo](https://youtube.com/your-demo-video)

## 🚀 Introduction

Code Quality & Security Analyzer is a developer-friendly tool that helps teams maintain high code quality by providing comprehensive analysis and actionable insights. It combines static code analysis with AI-powered recommendations to help you write better, more secure code.

## 📑 Table of Contents

- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Key Features](#-key-features)
- [AI-Powered Analysis](#-ai-powered-analysis)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Contributors](#-contributors)
- [License](#-license)

## ❓ Problem Statement

- **Technical Debt Accumulation**: Difficulty in identifying and tracking technical debt across large codebases
- **Security Vulnerabilities**: Hard-to-spot security issues that could lead to breaches
- **Inconsistent Code Quality**: Lack of standardized metrics to measure and maintain code quality

## 💡 Our Solution

- **Comprehensive Analysis**: Combines multiple code quality metrics into a single, easy-to-understand report
- **AI-Powered Insights**: Uses Gemini AI to provide contextual analysis and recommendations
- **Developer-Friendly**: Simple setup and intuitive interface for quick adoption

## ✨ Key Features

### Code Metrics
- **Lines of Code (LOC)**: Total lines of code in the repository
- **Cyclomatic Complexity**: Measures code complexity based on control flow paths
- **Churn Analysis**: Tracks code changes over time to identify volatile files
- **Risk Score**: Quantifies potential technical debt and maintenance challenges
- **Ownership Entropy**: Measures code ownership distribution among contributors
- **Bug Fix Frequency**: Tracks frequency of bug fixes per file

### Security Analysis
- **API Key Detection**: Scans for exposed API keys and credentials
- **Security Vulnerabilities**: Identifies common security anti-patterns
- **Dependency Risk**: Analyzes third-party packages for known vulnerabilities

### Quality Metrics
- **Code Duplication**: Identifies duplicated code blocks
- **File Size Analysis**: Flags unusually large files
- **Comment Density**: Measures code documentation levels
- **Function Length**: Identifies overly complex functions

### AI-Powered Insights
- **Automated Code Review**: AI-generated suggestions for code improvements
- **Technical Debt Assessment**: Estimates effort required for maintenance
- **Refactoring Recommendations**: Specific suggestions for code improvement

### Reporting
- **Interactive Dashboards**: Visual representation of code quality metrics
- **Exportable Reports**: Share analysis results with team members
- **Historical Trends**: Track improvements over time
- **Priority Issues**: Highlights critical problems that need immediate attention

## 🤖 AI-Powered Analysis

Our tool leverages Google's Gemini AI to provide:
- Contextual code analysis
- Smart recommendations for improvements
- Natural language explanations of complex issues
- Automated code review comments
- Predictive maintenance insights

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: Google Gemini API
- **Authentication**: Firebase
- **Version Control**: Git
- **Deployment**: Vercel/Streamlit Cloud

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- Google Cloud Account (for Gemini API)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/code-analyzer.git
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

## 👥 Contributors

- [Viraj](https://github.com/yourusername)
- [Visha](https://github.com/co-contributor)

## 🙏 Acknowledgments

- Thanks to Google for the Gemini API
- Open source community for various libraries used
- Our mentors and peers for their valuable feedback

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.