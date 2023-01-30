README
This code is a collection of tests that test the functionality of a patient identifier endpoint.

Technologies Used
Python 3
requests: Used to make HTTP requests to the endpoint
json: Used to parse the JSON response
jsonpath: Used to extract specific values from the JSON response
pytest: Used as the test framework
Selenium: Webdriver to run automated tests
Chrome browser

How to Run the Tests
1. Create a python virtual environment using the following command on commandline/terminal
python3 -m venv  venv
2. Ensure that you have the necessary dependencies installed (see the requirements.txt)

3. Run the following command to launch the test server
cd api-server 
flask run

4. Run the follwing command
pytest
in the directory where the test files are located.

Assumptions
Following were the assumptions made

1. Patient name could be a combination of any number of words example John Doe, Jane Robert Doe , Steven John Joe Doe all are valid names.
2. VIKO1988M and JO1997M patient identifer are already present in the database and hence we get an 409 status code back when trying to do POST request to /identity api with these Ids as body.
3. All the API and web pages have the same base url.

Further improvements to be made
1. We can execute the scenario 3 tests in multiple browsers.
2. All tests need to be executed in parallel.
3. Include confirguration files for saving the base url and api path values.
