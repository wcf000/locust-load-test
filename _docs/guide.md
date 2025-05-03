The Definitive Guide to Locust Load Testing
Performance Testing

By Mohamed Echout

Using Locust for load testing is a great option for determining your application's main breaking point in terms of performance and security.

This blog will give a step-by-step guide to Locust load testing. Read along or feel free to skip to the section that interests you most.
Table of Contents

    What is Locust Load Testing?
    Benefits of Locust for Load Testing
    Locust Load Testing Documentation
    Writing a Locust Load Test: Example
    Using Locust as a Library

Back to top
What is Locust Load Testing?

    Locust is a Python-based testing tool used for load testing and user behavior simulation. Load testing is the practice of testing a software application with the primary purpose of stressing the application's capabilities.

Locust is a tool that creates a set of testing functions that simulate a heavy number of users. This will determine the main breaking point in terms of performance, security, and application load management.

For load testing, Locust uses Python. In addition, it presents test results in a dashboard. One of the significant features of Locust is its well-documented code source, which means that its library can easily be understood and implemented by the software engineering team in a matter of hours.

📕 Related Resource: Learn more about Locust Performance Testing Using Java and Kotlin.
Back to top
Benefits of Locust for Load Testing

The main benefits of Locust can be defined as:

    A user-friendly web-based UI.
    Brings a set of dashboards, visualizations, and test reports that summarize the load testing process.
    Provides the testing team with a complete picture of the test's current performance.
    Enables the testing team to run multiple test scripts to find out the main performance and load handling problems..
    Enables the testing team to quickly increase the number of test cases and compare the test results for every task, user, and request.

You can find below the Locust user-friendly web-based UI:
Locust UI

And, in the next image, you will find a test report that summarizes the load testing process:
Locust load testing report
Open-Source Accessibility

Since Locust is an Open Source Software tool, this makes it stand out among others as it offers a wide range of accessibility to developers. These accessibility features provide the following benefits:

    Cost: As an Open Source technology, Locust can freely be used by any software engineering team to conduct their load testing procedure. This enables the team to incur less cost and focus their financial resources on hiring more talented software engineers.
    Flexibility: Locust can easily be used by any software engineering team and tested in different applications and websites without having to abide by specific rules or restrictions that proprietary software requires. In other words, as an open-source technology, Locust can be customized, changed, and used in any shape or form by the testing team with no restrictions or boundaries.

Back to top
Locust Load Testing Documentation
Installation

While Locust l is entirely based on Python, the Locust library doesn't come preinstalled in the Python environment, which means we will have to add it to our Python integrated development environment (IDE).

Python comes with a prebuilt installation tool known as the package installer for Python (pip). This tool enables Python developers to easily add new libraries and packages to the Python application code. To initialize the package installer for Python, we will be using the command pip:

!pip install locust

Getting Started

In this example, you will run a login registration script. The tested application can be a Python, Java, or any other programming-based application. To utilize the Locust library, follow the subsequent steps:

    Use the from keyword followed by the keyword import to add the HttpUser method and the task method in our program.
    Implement a testing class called TestUser using the keyword class followed by HttpUser as an argument for our class definition.
    Define your class's login and registration tasks using @tasks annotation that specifies user tasks.
    For every task, use the self keyword followed by the client command and finally call the action tested in our application using the keyword get.
    Last but not least, we will have to test a target page for every command. For our example, we will target our application's login and registration page.

The following Python code represents our load testing Python example:

from locust import HttpUser, task

class TestUser(HttpUser):
@task
def authenticate_task(self):
self.client.get("/login")
self.client.get("/register")

Back to top
Writing a Locust Load Test: Example

In this test script, you will run all the test cases you want to try on your application. To write this Locust script, follow the subsequent steps:

    Step 01: Start by importing the HttpUser, task, time, and between classes.
    Step 02: Create a class called AuthenticateUser that takes as an argument the HttpUser class imported at the beginning of our program.
    Step 03: Create a variable caller timer that will create 10 seconds between every executed task.
    Step 04: Define a function that will encapsulate the registration and login process called authenticate_task.
    Step 05: Implement a method called on_start that will be executed at the start of our test file.

The example described in this section can be found below:

import time
from locust import HttpUser, task, between

class AuthenticateUser(HttpUser):
timer = between(1, 10)

    @task
    def authenticate_task(self):
        self.client.get("/login")
        self.client.get("/register")

    def on_start(self):
        self.client.post("/register", json={"username":"testuser",
                                            "email":"test@test.com",
                                            "password":"password"})

Locust Load Testing Configuration

Configure Locust by running the locust command in your command line interpreter. It is important to understand the difference between the configuration and test files:

    Configuration file: used to customize Locust and the load testing settings.
    Test file: used to test your application by testing your methods and procedures.

The configuration file will contain some values that determine how your load testing process will be performed. These values can be the number of users used in the load testing process or the runtime of the load testing process. To conduct the proper configuration of Locust, the subsequent steps should be followed:

    Create a configuration file under the name locust.conf that will contain the configuration settings
    Write down the configuration options you wish you use in your program using the key-value pair format as shown below:

locustfile = locust_tests/my_locust_test.py
headless = true
master = false
expect-workers = 20
run-time = 20m

    Save your configuration file with the .conf extension.
    Finally, run the locust command in your command line with the name of your configuration file as an argument at the end of your command. An example of such a command can be as follows:

locust --config=master.conf

After running the configuration file in your command line, the following results will be displayed:
Locust load testing configuration result

For a full list of the configuration options, you can find the full documentation of Locust in the Configuration Command Line Options link.
Scalability in Distributed Systems

To scale up, Locust offers a set of processes called nodes that can be used to run a set of tasks. These nodes are known as workers as they perform specific functions in a given period. In addition, Locust offers the capability to link these nodes or workers to simulate a distributed load for large-scale load testing operations. The following instructions should be set:

    Initiate a starting point for our system by creating a master node:

locust -f test_webapp.py -master

    Distribute the load to a set of workers that will balance the processing power. The following command can be used as an example:

locust -f test_webapp.py --worker --master-host = IP1

locust -f test_webapp.py --worker --master-host = IP2

locust -f test_webapp.py --worker --master-host = IP3

locust -f test_webapp.py --worker --master-host = IP4

Make sure to assign the IP addresses of the respective servers used for the testing process for every worker.
Back to top
Using Locust as a Library

Locust can be used as a library encapsulating the testing environment using Python. This library contains prepacked methods to test your procedures, functions, or class methods. Follow these sequential steps to perform this task:

    Step 1: Create a testing environment by importing the environment class found in the locust.env package.
    Step 2: Create a testing object using the imported class environment followed by the name of your testing object.
    Step 3: Give the testing object the name of the user classes. The previously defined class [AuthenticateUser] will be used as the testing class in this example.

The example explained in this section can be found below:

from locust.env import Environment

test_env = Environment(user_classes=[AuthenticateUser])
