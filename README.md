# Speckle Automate Workshop Tutorial

## Introduction
Quality Assurance and Quality Control (QAQC) in Building Information Modeling (BIM) traditionally relies on exporting models to neutral formats like IFC for validation. However, this process can introduce data loss before checking even begins. By validating data directly from the host application (like Revit, Rhino, etc.), we can:
- Check data in its native format
- Catch issues before information is lost in translation
- Validate application-specific parameters and properties
- Create more precise and reliable checks
- Reduce the validation feedback loop
- Enable teams to fix issues while actively working in their design tools

![qaqc-workshop](https://github.com/user-attachments/assets/6caac9e1-4dff-4ba7-87d1-88d297bf8a9f)

This workshop teaches you how to create automated QAQC systems using Speckle Automate that work directly with native application data. You'll learn to build validations that can:
- Systematically verify model data against project standards
- Process native application properties and parameters
- Create targeted validation rules for specific platforms
- Generate clear feedback that references native elements
- Enable teams to maintain high-quality BIM deliverables at source

By automating these checks at the source, teams can:
- Validate data before any export-related loss occurs
- Work with complete property sets from the authoring tool
- Create platform-specific validation rules
- Maintain data fidelity throughout the checking process
- Fix issues directly in the native environment
- Reduce the complexity of the QAQC workflow

## Learning Journey

### Exercise 0: Automate Foundations 🚀
Starting from the basic template in `main.py`, learn fundamental Speckle Automate concepts:
- Access native application data
- Navigate object hierarchies
- Interact with model elements
- Handle basic error cases

### Exercise 1: Multi-Object Processing 🔄
Build the foundation for systematic QAQC:
- Filter native application objects
- Process multiple elements efficiently
- Provide visual feedback in the Speckle viewer
- Handle platform-specific properties
- Configure validation scope

### Exercise 2: Validation Framework 🔍
Create a robust checking system:
- Validate native parameters and properties
- Filter by application-specific categories
- Create reusable platform-aware rules
- Implement tiered issue reporting
- Organize results for easy review

### Exercise 3: External Configuration 📊
Transform into a flexible, maintainable QAQC solution:
- Define standards in accessible spreadsheets
- Support complex native property validation
- Enable non-technical standards management
- Generate detailed validation reports
- Handle variations in property names

## Getting Started

### Creating Your Function
1. Navigate to [latest.speckle.systems/functions](https://latest.speckle.systems/functions)
2. Click the "New Function" button in the top right
3. Follow the wizard steps:
   - Authorize GitHub (first time only)
   - Choose the Python template
   - Define your function:
     - Add an optional avatar/logo
     - Choose a descriptive name
     - Add a description (supports Markdown)
     - Identify supported source applications
     - Add relevant tags

The wizard will:
- Create a GitHub repository with template code
- Set up GitHub Actions for deployment
- Configure necessary secrets (`SPECKLE_FUNCTION_ID` and `SPECKLE_FUNCTION_TOKEN`)
- Provide immediate access to start coding

### Next Steps
Once your function is created, you can either:
- Start from the template code in `main.py`
- Replace it with code from this workshop's exercises
- Work through the exercises incrementally to build your validation system

### Prerequisites
- Basic Python knowledge
- Poetry installed (`curl -sSL https://install.python-poetry.org | python3 -`)
- A verified Speckle account

## Additional Resources
- [Speckle Documentation](https://speckle.guide/)
- [Automate Documentation](https://speckle.guide/automate/)

## Getting Help
- Join our [Community Forum](https://speckle.community)
- Check exercise READMEs for detailed guidance
- Open GitHub issues for specific problems

## License
Apache License 2.0 - See LICENSE file for details
