
![Logo](/app_images/logo.png)


# Team Up

This is a Discussion Forum App whereby users can login, create a Topic for discussion and the topic can have multiple rooms associated with it.


## Cloning the repository

Clone the project

```bash
  git clone https://github.com/alexkasema/team_up
```

 Move into the directory where we have the project files :

```bash
  cd team_up
```

Create a virtual environment :

```bash
# Let's install virtualenv first
pip install virtualenv

# Then we create our virtual environment
virtualenv envname

```

Activate the virtual environment :

```bash
  envname\Scripts\activate
```

Install the requirements :

```bash
  pip install -r requirements.txt
```

## Running the App

To run the App, we use :

```bash
  python manage.py runserver
  ⚠ Then, the development server will be started at http://127.0.0.1:8000/
```


## Screenshots

![App Image](/app_images/index1.png)

![App Image](/app_images/profile1.png)

![App Image](/app_images/create1.png)

![App Image](/app_images/room1.png)
