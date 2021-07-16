# Research Helper
This application helps you to host design and run your own researches.

Currently this project is in early alpha. 
Available functionalities:
- create user
- login / logout
- create experiment
  - set factors and levels
  - upload an excel file with the given structure(context, stimulus, lexicalization)
- run experiment
- list experiments of the user with number of fills
- list the items of the experiment
- delete experiments


# How to install
requrements: python 3.8+
clone the repository
in root folder: `>python manage.py migrate`

 `>python manage.py runserver`
 the app is good to go on localhost!
 
 There is currently no deployable / production build
 
 creating an experiment:
 ![image](https://user-images.githubusercontent.com/22302671/125205144-22f3e580-e281-11eb-992f-56b3174b0052.png)
 
 running an experiment:
 ![image](https://user-images.githubusercontent.com/22302671/125205201-69e1db00-e281-11eb-821a-fcec8fc4ac46.png)
