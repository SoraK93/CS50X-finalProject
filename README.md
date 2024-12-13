# CS50 Diary
## Video Demo:  <URL HERE>
## Description:
The idea for this diary came from my need for a central/ common space for all the course mates to interact with each other whether they are pursuing online or on-site course, whether they are new or old to computer science in general. Yes, we have ways to form study groups (whatsapp, discord), but they do not meet my needs. What I wanted was something akin to how we can interact with anyone in the classroom chat and have an in-depth discussion on topics that interest us and at the same time it can also be a place where we can express ourselves on whatever topic we fill comfortable with.

**Main purpose of this diary is _sharing and interacting_** (Obviously not sharing answers to P-Set which will defeat the purpose of the course).  

To fulfil this goal, I decided to create a web-app which can be used to share our thoughts and troubles with others. 

<ins>This application is based on flask and will support User defined permissions</ins>:
+ A registered user 
    + Can view any posts
    + Can create, edit and delete their own posts
    + Can update username and email
    + Can change password (Require a valid email, because a temporary link will be sent to the user for verification)
    + Can read/ write comments on any post
+ A guest user
    + Can view any posts
    + Can register and become a registered user
    + Do not have access to do anything else
    + Can read comments on any posts
+ If clicked on username on the post, app will filter out all the posts related to that user


## Project Structure and each file
We are using Flask-blueprint structure for this project. Since, this structure makes upgrading, adding or removing files/ features much easier and modular
#### <ins>**Tree model of the Project</ins>:**
+ **Project**
    + **blog**
        + **main**
            + **\_\_init__.py** - turns main folder into package
            + **routes.py** – contain functions which will be executed when related features are triggered
        + **posts**
            + **\_\_init__.py** - turns posts folder into package
            + **forms.py** - contains the structure of forms used for create posts, update posts
            + **routes.py** – contain functions which will be executed when related features are triggered
        + **static**
            + **profile_pics** - all files are used for users profile image
            + **image files** - Represent all the background images used in this web app
            + **style.css** - Represents the custom css used
        + **templates**
            + **about.html** - Contains our mindset and thought process for this web app
            + **comment.html** - registered users can comment on each post
            + **contact.html** - contains a way to contact us
            + **create_post.html** - this page is used to create new posts by registered users
            + **delete_modal.html** - this is a bootstrap modal which is used like pop-up confirmation when user wants to delete there post
            + **home.html** - this is the homepage of the site
            + **layout.html** - this contains the basic layout for the site. It includes all the essential html tags, css linking, javascript linking
            + **login.html** - this page where users login from when using this web app
            + **post.html** - this is where user can check any post is greater detail
            + **profile.html** - this page contains options to change username, email and user profile image.
            + **register.html** - this page is where new users will go for creating new account
            + **reset_password.html** - this page will only show up when the user clicks on the url sent to their registered email
            + **reset_request.html** - this page is used to initiate the process of password reset
            + **user.html** - this page contains the layout of users profile page, this can later be expanded upon
        + **users**
            + **\_\_init__.py** - turns users folder into package
            + **forms.py** - contains the structure of all the forms used for login, registration, update profile, password reset
            + **routes.py** – contain functions which will be executed when related features are triggered
            + **utilities.py** - contains functions related to sending mail, storing profile picture in static folder
        + **\_\_init__.py** - initialize flask and more application and registers blueprint
        + **models.py** - this contains models of all the tables we are using/ creating in sqlite.db
        + **config.py** - to keep my web app setting organized. We can switch from development to production by changing settings in config, or run both at the same time
        + **.env**
    + **instance**
        + **sqlite.db** - this is the central database of our web app
    + **.gitignore** - this file defines all the filetypes git commands will ignore. It’s a type of precautionary measure we use so that we do not upload any confidential files to the web
    + **run.py** - this file will act like the start button for the program. Upon running this file our web app will be live and ready to take on users

## Initial project goals and changes
Initially my target was to make a portfolio for the project, but as my research towards what and how to start my project. I decided to make a blog style diary for my final project. My biggest drive for this project came from the fact that this will require me to create a proper file structure, maintain at least a basic level of version control and implement many different languages together to create this project.

## Challenges

## Sources & Documentation used during this project
[Flask Tutorial](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH) - Used this to learn basic of Flask using python.

[Flask]()

[Flask-SQLAlchemy]()

[Flask-login]()

[Flask-WTForms]()

[Bcrypt]()

[CKEditor]()
