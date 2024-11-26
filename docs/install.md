## Installation Guide

## Prerequisites
Before you begin, ensure you have met the following requirements:

- **Operating System:** Windows, macOS, Linux
- **Web Browser:** A modern web browser (e.g., Google Chrome, Mozilla Firefox, Safari)

***Install Python***:
1. **Download Python:**
   Download the Windows installer for the Python version you desire from [Python Downloads](https://www.python.org/downloads/). Based on your operating system, you can download and install Python's latest or older versions. Make sure to download the python version  - 3.10

2. **Install Python:**
   Double-click on the downloaded file and follow the instructions provided.

3. **Add Python to Environment Variables:**
   Once completed, add Python to the environment variables of your system settings to enable Python compiling from your command line.

4. **Verify Installation:**
   You can verify if the Python installation was successful either through the command line or the IDLE app that gets installed along with Python. Search for the command prompt and type:
   ```bash
   python --version

## Follow these steps to install the project:

### Installing (for Windows)

*1. Clone the Repository* - Start by cloning the repository to your local machine. 
  
``` bash
    git clone https://github.com/Fall-2024-SE-Group/FilmFolio.git
```
    
  (OR) Download the .zip file on your local machine from the following link
  
    https://github.com/Fall-2024-SE-Group/FilmFolio/


*2. Navigate into the project directory*

``` bash
cd FilmFolio/
```

*3. Setting up the virtual python environment*
```bash
python -m venv venv
```
```
.\venv\Scripts\activate
```

*4. Get a TMDB API Key*
To get an API Key from TMDB:

- Go to the TMDB Website and sign up.
- Under your account icon, click Settings.
- Go to the API section, and under the Request an API Key section, click on the link.
- Register for an API key, agree to the terms of use, and fill in the required information.

*5: Create a .env File with Your TMDB API Key*

Create a .env file in the src folder with the following content:

    # .env
    TMDB_API_KEY=YOUR_TMDB_API_KEY
    Replace YOUR_TMDB_API_KEY with the actual API key you obtained from TMDB.

*6. Install dependencies*

``` bash
pip install --upgrade pip
```
```
pip install -r requirements.txt
```

*7. Navigate to entry folder*

``` bash
cd app/
```

*8. Set up the database*
``` bash
python init_db.py

*9. Run the application*
``` bash
python run.py
```
*10 Open the Application in Your Browser*

After starting the server, open the following URL in your browser:

      http://127.0.0.1:8000/
    
   


### Mac OS

MacOS comes with Python pre-installed. But it's Python Version 2.7, which is now deprecated (abandoned by the Python developer community).

1)**Install Homebrew:**

To install the latest version of python in your mac, first you need to install [Homebrew](https://brew.sh/), a powerful package manager for Mac.*

-Open your terminal and run this command to install Homebrew in your system:
```bash
"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
-Your terminal will ask for admin.user access of your system. You will need to type your password to run this command. This is the same password you type when you log into your Mac. Type it and hit enter.


2)**Install Python:**

Once you are done with installing the Homebrew package, you can run this command in your terminal to install python with the desired version you want.
```bash
python version 3.11.0
```

3)**Verify Installation:**

Once done, you can run this command to check if you have successfully installed python in your system or its version:
```bash
python3 --version
```


## Maintaining Database file

To create/add new tables, run the following commands before starting the server:
```bash
flask shell
from app import db
db.create_all()
````

To delete all the tables, run following commands before starting the server:
```bash
flask shell
from app import db
db.drop_all()
```