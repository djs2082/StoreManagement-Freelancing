# Shield. Store Management

Shield. Store Management is a software solution for effective management of shop for your
business. It provides lot of features as mentioned below.

# Features

1)Automatic Generation of total bill for customers with respect to purchased items.  
2)Auto calculation of total discounts based on previously inserted items  
3)Generate bills for customers online in the format of pdf  
4)You can view details of your all the customers anytime on this portal  
5)shows total sale of the day, sorted with different payment options  
6)shows all your stock remaining and their selling price and cost price in dashboard  
7)shows statistics of sales for last 30 days  
8)provides interactive admin portal for adding and deleting stock of your shop  

## Technologies

1)Python3  
2)Djang Rest Framework  
3)Node js(to run react js)  



## Installation

This application is containerized using Docker.
if you have docker-compose installed on your machine. below command will start project on your machine by hadling all the dependencies. Run this command in root directory of project.

```bash
docker-compose up
```
if you don't have docker-compose installed on your machine. then you can start project with below process

install react dependences(run below command in frontend folder)

```bash
npm install
```

install python3 dependencies(run below command in backend/Himalaya/ folder)

```bash
pip3 install -r requirements.txt
```

start backend server (run below commands in backend/Himalaya/ folder)

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

start frontend server (run below command in frontend folder)

```bash
npm start
```
create user for your demonstration by running below command and follow steps(in backend/Himalaya/)

```bash
python3 manage.py createsuperuser
```
## Usage

This application is available for commercial purposess. For getting paid version of this, contact below:

Email: dilipjoshis98@gmail.com 
Mobile: 8975427620  

## License
[MIT](https://choosealicense.com/licenses/mit/)