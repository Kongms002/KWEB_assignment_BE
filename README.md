# KWEB_assignment_FE
Stack: Flask (Python Framework)

## Settings
1. <strong>Clone the Repository:</strong> Begin by cloning the project repository from GitHub:
```
git clone https://github.com/your-username/your-project.git
```

2-1. <strong>Install Virtualenv</strong>: First, install virtualenv on your system using the following command:
```
pip install virtualenv
virtualenv venv
```
2-2. <strong>Activate the Virtual Environment:</strong> Activate the newly created virtual environment:
- For Windows:
```
venv\Scripts\activate
```
- For macOs and Linux:
```
source venv/bin/activate
```

3. <strong>Install Dependencies:</strong> While the virtual environment is active, install the required packages. Use Poetry to install project dependencies. This command will read the pyproject.toml file and install all required packages:
```
pip install poetry
poetry install
```

4. <strong>Run the Project:</strong> Once the dependencies are installed, you can run the project using the appropriate command. For example:
```
python main.py
```

5. <strong>Access the Project:</strong> After starting the project, you should be able to access it in your web browser. Open your preferred browser and navigate to the appropriate URL as specified in the project documentation.

6. <strong>(Sensitive).env File Setting:</strong> This is settings of .env file.
```
JWT_SECRET_KEY = kongms002
DB_URL = mongodb+srv://admin:20020221@kweb.tuduaqz.mongodb.net/
```
