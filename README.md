# Speckle Automate Workshop Tutorial

## Overview
This repository contains materials from the Speckle Automate workshop, adapted for self-guided learning. Learn to create automated validation rules for your Speckle models using Python and Google Sheets.

## Prerequisites
- A Speckle account (free at app.speckle.systems)
- Basic Python knowledge
- Python 3.8 or higher
- Required packages:
  - speckle-automate
  - pandas
  - python-Levenshtein

## Workshop Structure
The workshop is divided into several exercises, each building upon the previous:

1. **Exercise 1**: Basic Automate Function
   - Creating a simple automation that adds comments to random objects
   - Understanding the basic structure of an Automate function

2. **Exercise 2**: Multiple Object Selection
   - Working with multiple objects
   - Adding visualization features
   - Understanding object filtering

3. **Exercise 3**: Parameter Validation
   - Implementing property checks
   - Working with Revit parameters
   - Creating validation rules

4. **Exercise 4**: Rule-based Validation
   - Integrating with Google Sheets
   - Creating complex validation rules
   - Understanding the rule system

## Getting Started

### Setting Up Your Environment
1. Clone this repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

### Creating Your Rule Set
1. Make a copy of our [Google Sheets template](link-to-template)
2. Follow the template structure for defining rules:
   - Rule Number
   - Logic (WHERE/AND)
   - Property Name
   - Predicate
   - Value
   - Message
   - Report Severity

### Publishing Your Rules
1. In Google Sheets:
   - File → Share → Publish to Web
   - Choose "Tab-separated values (.tsv)" format
   - Copy the published URL

### Running the Automation
1. Configure your function inputs:
   - For basic tests: Comment phrase and number of elements
   - For validation: Category and property names
   - For rule-based validation: Your published TSV URL

2. Deploy to Speckle Automate:
   - Follow the deployment instructions in each exercise folder
   - Set up appropriate triggers for your automation

## Additional Resources
- [Workshop Slides](link-to-slides)
- [Speckle Automate Documentation](https://speckle.guide/automate.html)
- [Python SDK Documentation](https://speckle.xyz/docs/developers/python)

## Support
If you encounter any issues or have questions:
- Check our [Troubleshooting Guide](link)
- Join the [Speckle Community Forum](https://speckle.community)
- Open an issue in this repository

## License
This project is licensed under [appropriate license]
