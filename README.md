# Finance Tracker 
 > Web project made with Bootstrap, Jinja, Flask and SQLAlchemy

## Live demo: ~~https://expense-tracker-1133.herokuapp.com/~~ - no longer available due to Heroku changes in policy
### ~~Please note that this app is deployed with Heroku so the first time when you open it you have to wait until the server initialize in order to view it.~~
To test the app clone the repo and run it locally
- You can use Finance_Examle.xls file in repository to test the Statement page
 
 
 ## Features: 
  - Logging/Sign-up
  - Expenses adding
  - Statement reader
  
 ### Demo view logged in account
![image](https://user-images.githubusercontent.com/38993490/184943304-5a867691-77f4-48a1-b39c-3e938b948634.png)

### Demo of a readed statement 
![image](https://user-images.githubusercontent.com/38993490/184945422-0c4ef2a5-c556-4cd7-a409-c60381807b09.png)

# How it works
When a anonymous user opens the page - there are 2 options: Login or Sign-up \
After logging each user has its own panel for registering expenses while there are summed and displayed \
Statement page is to read an xls file and sort in categories: Food,Gas,Others and displayed each and then summed
> Statement page reads properly only finance statements as the example xls file!

### Purpose of the project 
> Simple web MVC for learning how to work with Flask, creating database models, relationships between tables, get and post request to the DataBase, working with HTML template engine

