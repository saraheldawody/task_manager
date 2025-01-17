# Task Manager
## Description:
The Task Manager project is a web application built with Django and Django REST framework, designed to manage tasks efficiently. It provides endpoints for creating tasks, updating task status, linking tasks, and retrieving task details.

## Features:
- Task Creation: Users can create new tasks providing a title and description.
- Task Status Update: Tasks can be moved through different status levels: New, In Progress, and Done.
- Task Linking: Tasks can be linked together to represent dependencies or relationships.
- Task Retrieval: Users can retrieve task details including linked tasks if any.

## Installation and Setup:
1. Clone the repository from GitHub link.
2. Navigate to the project directory.
3. Install dependencies using 
'''
pip install -r requirements.txt
'''
4. Set up the database configurations in settings.py.
5. Run migrations using 
'''
python manage.py migrate.
'''
6. Start the development server with 
'''
python manage.py runserver.
'''

## Usage:
- Access the API endpoints using appropriate URLs for creating, updating, and retrieving tasks.
- Ensure proper authentication and authorization mechanisms are implemented for production deployment.