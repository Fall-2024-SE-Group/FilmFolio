
# Installation Guide

## Prerequisites
Before you begin, ensure you have met the following requirements:

- **Operating System:** Windows, macOS, Linux
- **Web Browser:** A modern web browser (e.g., Google Chrome, Mozilla Firefox, Safari)

## Install Python:
### Windows
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


## Follow these steps to install the project:

### 1. Clone the Repository* - Start by cloning the repository to your local machine. 
  
``` bash
    git clone https://github.com/Fall-2024-SE-Group/FilmFolio.git
```
    
  (OR) Download the .zip file on your local machine from the following link
  
    https://github.com/Fall-2024-SE-Group/FilmFolio/


### 2. Navigate into the project directory*

``` bash
cd FilmFolio/
```

### 3. Setting up the virtual python environment*
```bash
python -m venv venv
```
```
.\venv\Scripts\activate
```

### 4. Get a TMDB API Key*
To get an API Key from TMDB:

- Go to the TMDB Website and sign up.
- Under your account icon, click Settings.
- Go to the API section, and under the Request an API Key section, click on the link.
- Register for an API key, agree to the terms of use, and fill in the required information.

### 5: Create a .env File with Your TMDB API Key*

Create a .env file in the src folder with the following content:

    # .env
    TMDB_API_KEY=YOUR_TMDB_API_KEY
    Replace YOUR_TMDB_API_KEY with the actual API key you obtained from TMDB.

### 6. Install dependencies*

``` bash
pip install --upgrade pip
```
```
pip install -r requirements.txt
```

### 7. Navigate to entry folder*

``` bash
cd app/
```

### 8. Set up the database*
``` bash
python init_db.py

### 9. Run the application*
``` bash
python run.py
```
### 10 Open the Application in Your Browser*

After starting the server, open the following URL in your browser:

      http://127.0.0.1:8000/
    
   
## Docker Installation Guide

Follow these steps to install Docker on your system and run the project.

---

**Installing Docker**

### **For Windows**

1. **Download Docker Desktop**:
   - Visit the [Docker Desktop for Windows download page](https://www.docker.com/products/docker-desktop/).
   - Download the installer for your Windows version (Windows 10/11 or higher).

2. **Install Docker Desktop**:
   - Run the downloaded installer.
   - Follow the installation wizard steps and ensure that **"Install required Windows components for WSL 2"** is checked.

3. **Enable WSL 2 Backend**:
   - Open PowerShell as Administrator and run:
     ```powershell
     wsl --install
     ```
   - Set WSL 2 as the default version:
     ```powershell
     wsl --set-default-version 2
     ```

4. **Start Docker Desktop**:
   - Launch Docker Desktop and complete the setup.

5. **Verify Installation**:
   - Open a terminal (Command Prompt or PowerShell) and run:
     ```bash
     docker --version
     docker run hello-world
     ```

---

### **For macOS**

1. **Download Docker Desktop**:
   - Visit the [Docker Desktop for Mac download page](https://www.docker.com/products/docker-desktop/).
   - Download the installer for macOS.

2. **Install Docker Desktop**:
   - Open the downloaded `.dmg` file.
   - Drag the Docker icon to your **Applications** folder.

3. **Start Docker Desktop**:
   - Launch Docker Desktop from the Applications folder and follow the setup instructions.

4. **Verify Installation**:
   - Open a terminal and run:
     ```bash
     docker --version
     docker run hello-world
     ```

---

### **For Linux**

1. **Update Package Index**:
   ```bash
   sudo apt update
   sudo apt upgrade -y

2.  **Install Prerequisites**:


      ```bash
       sudo apt install -y\
           ca-certificates\
           curl\
           gnupg\
           lsb-release`
    
3.  **Add Docker's Official GPG Key**:
   
      ```bash
       sudo mkdir -p /etc/apt/keyrings
       curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg`


3.  **Set Up Docker Repository**:

       ```bash
       echo\
         "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu\
         $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`


4.  **Install Docker Engine**:

       ```bash
       sudo apt update
       sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`


5.  **Verify Installation**:

    -   Run the following commands:

        ```bash
        docker --version
        docker run hello-world`


6.  **(Optional) Add Your User to Docker Group**:

    -   To run Docker commands without `sudo`:

        ```bash
        sudo usermod -aG docker $USER`

    -   Log out and back in for the changes to take effect.

* * * * *

**Running the Project Using Docker**
------------------------------------

Once Docker is installed, follow these steps to run the project:

1.  **Clone the Repository**:

   ``` bash
       git clone https://github.com/Fall-2024-SE-Group/FilmFolio.git
   ```
    
  (OR) Download the .zip file on your local machine from the following link
  
    https://github.com/Fall-2024-SE-Group/FilmFolio/

2.  **Build the Docker Image**: Run the following command to build the Docker image:
   
          docker build -t filmfolio:latest .


4.  **Run the Docker Container**: Use the following command to start the project:

         docker run -d -p 8000:8000 filmfolio:latest

       -   This will map port 8000 on your machine to port 8000 in the container.

5.  **Access the Application**: Open your browser and go to:

             http://localhost:8000

6.  **Stopping the Container**:
    -   To get the container ID
         ```bash
        docker ps
        docker stop <container_id_or_name>
    -   To stop the running container:
         docker stop <container_id_or_name>


7.  **Rebuilding After Code Changes**: If you make changes to the code, rebuild the Docker image:

   
          docker build -t filmfolio:latest .

    
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
