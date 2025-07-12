# Resite

This project helps to form random pairs from a list of participants 
so that people get new partners every time. 
It is especially useful in educational institutions: 
it allows students to interact with different classmates 
rather than sitting with the same people.

# Main features
- Saving participant lists - can be reused.
- Generating pairs - new pairs each time.
- API for pair generation and list management.

# Getting Started
First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/Azizka21/Resite.git
    $ cd Resite
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver