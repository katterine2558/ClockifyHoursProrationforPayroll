⏱️ Clockify Hours Proration for Payroll

This application allows you to prorate Clockify time entries for each collaborator to facilitate payroll processing. The tool processes Clockify data, generating detailed reports for accurate payroll calculations.
📂 Project Structure

    Prorrateo.py
    Script for prorating the hours worked by each collaborator.

    f_generar_reporte.py
    Script for generating detailed payroll reports.

    run.py
    Main script to execute the proration and reporting process.

    Directories:
        _lib: Contains libraries or helper functions used in the scripts.
        _images: Stores images related to the project (e.g., documentation or examples).
        __pycache__: Compiled Python files.

    requirements.txt
    List of required Python dependencies.

    requirements.log
    Log file of installed dependencies.

🚀 Features

    Prorate Clockify Hours:
    Automatically divides work hours among collaborators for accurate payroll calculations.

    Generate Reports:
    Export detailed reports for payroll processing.

    Easy Integration:
    Scripts are customizable and easy to integrate with your current workflow.

🔧 Prerequisites

    Python 3.x

    Dependencies:
    Install required libraries:

    pip install -r requirements.txt

    Clockify API Key
    Obtain your API key from your Clockify account settings.

⚙️ How to Use

    Configuration:
        Update your API key and configuration parameters in Prorrateo.py and run.py.

    Run the Main Script:

python run.py

Generate Report:
Use f_generar_reporte.py to export the payroll report.

    python f_generar_reporte.py

📊 Output

    Prorated Data:
    CSV or Excel files with prorated hours per collaborator.

    Reports:
    Detailed payroll reports for easy processing.

🔒 Security

    API Key: Keep your Clockify API key secure.
    Data Privacy: Ensure only authorized users access the scripts and generated reports.

🤝 Contributing

Contributions are welcome! Submit an issue or pull request to suggest improvements.

📝 License

This project is licensed under the MIT License.
