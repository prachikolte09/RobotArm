# Robotic arms Package Sorter

Package Sorter is a web application built using FastAPI and Javascript for sorting packages based on their dimensions and mass. This webapp is deployed on Free-tier of third party service Vercel. 
Inputs can be tested at 

[https://robot-nrtyg3kd0-prachis-projects-18131715.vercel.app/](https://robot-nrtyg3kd0-prachis-projects-18131715.vercel.app/)

### Objective

Imagine you work in Thoughtful’s robotic automation factory, and your objective is to write a function for one of its robotic arms that will dispatch the packages to the correct stack according to their volume and mass.

### Rules

Sort the packages using the following criteria:

- A package is **bulky** if its volume (Width x Height x Length) is greater than or equal to 1,000,000 cm³ or when one of its dimensions is greater or equal to 150 cm.
- A package is **heavy** when its mass is greater or equal to 20 kg.

Must dispatch the packages in the following stacks:

- **STANDARD**: standard packages (those that are not bulky or heavy) can be handled normally.
- **SPECIAL**: packages that are either heavy or bulky can't be handled automatically.
- **REJECTED**: packages that are **both** heavy and bulky are rejected.

### Implementation

Implement the function **`sort(width, height, length, mass)`** (units are centimeters for the dimensions and kilogram for the mass). This function must return a string: the name of the stack where the package should go.

## Features

- Accepts package dimensions (width, height, length) and mass as input.
- Sorts packages into different categories: STANDARD, SPECIAL, or REJECTED.
- Provides a user-friendly interface for submitting package details and viewing sorting results.

## Requirements

- Python 3.8 or higher
- FastAPI
- Pydantic
- Jinja2 (for templating)
- [Optional] JavaScript for client-side form validation and interaction

## Installation

1. Clone this repository to your local machine
  `  git clone https://github.com/prachikolte09/RobotArm.git`
2. Navigate to the project directory
3. Install the required dependencies using pip:
   ` pip install -r requirements.txt`

## Usage

1. Start the FastAPI server:

   ` uvicorn main:app --reload`
2. Open your web browser and go to http://localhost:8000 to access the web application.

3. Enter the dimensions and mass of the package in the provided form and submit it.

4. View the sorting result displayed on the webpage.


# Assumptions
1. Most of the validation are given in JS file as per the objective of the assignment 
2. No characters are allowed. Regex are used.
3. API validations are temporary shown in pop alerts can be changed better

# Improvement
1. Limit values are kept static as per assignment can be accepted from frontend 
2. Units can be changed and hence the limits can be changed to match values