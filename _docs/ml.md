https://docs.locust.io/en/stable/

[Tutorial]: Performance Test ML Serving APIs using Locust and FastAPI
Ashmi Banerjee
Ashmi Banerjee
6 min read
·
Jul 10, 2022

A step-by-step tutorial to use Locust to load test a (pre-trained) image classifier model served using FastAPI.
Our tech stack for the tutorial

In my previous tutorial, we journeyed through building end-points to serve a machine learning (ML) model for an image classifier through an image classifier app, in 4 steps using Python and FastAPI.

In this follow-up tutorial, we will focus on load/performance testing our end points using Locust.

    If you have followed my last tutorial on serving a pre-trained image classifier model from TensorFlow Hub using FastAPI, then you can directly jump to Step 2 ⬇️ of this tutorial.😉

Step 0. Prerequisites

    Make sure you’re using Python 3.6+
    Create a virtual environment and activate it
    virtualenv venv
    source venv/bin/activate
    Install dependencies
    — Create the requirements.txt file as following
    — Now install the requirements as pip3 install -r requirements.txt

fastapi~=0.75.0
uvicorn==0.17.6
pydantic==1.9.1
tensorflow
tensorflow_hub
locust

4. Create the project structure as follows

fastapi-backend
├── src
│ ├── app
│ │ ├── app.py
│ └── pred
│ │ ├── models
│ │ │ ├── tf_pred.py
│ │ └── image_classifier.py
│ └── utils
│ │ ├── utilities.py
│ └── main.py
├── tests
│ ├── performance_tests
│ │ ├── locust_test.py
└── requirements.txt

Step 1. Implement our Endpoint(s)

In the app.py file, implement the /predict/tf/ end-point using FastAPI. This is the end-point that we will later test using locust.

    You can skip the details in this section and directly jump to Step 2 ⬇️ if you have already read my previous tutorial.😉

First, after importing the required packages, in line 5, we initialise the FastAPI app with the name of our API (here referred to as the Image Classifier API, but you can address it by any name) as its title.

But before we implement this end-point, in line 7, we need to define the data model as a class that inherits from theBaseModel we imported from Pydantic in line 3.
Our data model just has one attribute: img_url which is a str storing the URL of the image used for classification.

Since we are sending data to the backend, we implement the end-point as a POST request in line 10.

The function predict_tftakes in input a request (of datatype Img, the data model created above) and returns a JSON containing the status code (HTTP code 200 in case of a valid prediction), the predicted label, and the prediction probability.

It then calls the run_classifier function where all the image classification happens.

In case of a null prediction, it raises an HTTPException with the status code 404, hinting that there is some problem with the image.

Since prediction model implementation is not the focus of the topic, I have skipped it here for simplicity purposes.
However, if you are interested you can find more details either in the code repository or in my other tutorial focusing on FastAPI.

You can use any pre-trained/self-trained model for experimentation purposes. In this case, I have used a pre-trained TensorFlow MobileNet_V2 model from the TensorFlow hub.
Step 2. Write performance tests using Locust for the end-point(s)

To load test our end-points, we use Locust, which is an open-source load testing tool that allows us to write our tests in Python and renders the load testing UI directly on our browsers.

In the class, PerformanceTests we define the different load tests as each task (line 8). The class PerformanceTests inherits HttpUser from the locust module. This way we are able to interact with the API that we implemented.

Here, since we are using a single test to test our end-point, so we use @task(1) for this purpose.

We define our test case inside the function test_tf_predict in the following steps:

    Line 10 : We prepare the sample Image of the data type Imgclass (same as the data model initialised before) with a hard-coded image URL. (You can use any image URL of your choice). This is the same image URL that we use to get our classification.
    Line 11 : We define our headers for the request.
    Line 13 : We send a post request using the client.

    It should be noted that in Line 13 we just define the endpoint, i.e. “/predict/tf”, and not the complete API URL.

Step 3. Running Locust tests and accessing them through the Locust UI

Once you have implemented the different tests (e.g. @task(1) , @task(2) , … @task(n) ), the next step would be to run them.

We use the following command to run our locust tests:

locust -f tests/performance-tests/locust_test.py

The test UI can be monitored/accessed from http://127.0.0.1:8089/

    However, before you start your locust server, do not forget to run your FastAPI server (as described here) in parallel as well.

Interpreting the Locus UI

http://127.0.0.1:8089/ should display the following UI. We enter the number of concurrent users to be 100 in this case and the host to be the FastAPI server URL (in this case http://127.0.0.1:8000)

Once we hit the Start swarming button, it takes us to multiple screens showing progress on the performance of our API under load.

The different tabs can be interpreted as follows:
Statistics

The first screen Statistics gives us a high-level overview of our test. Here, it can be seen the speed at which our API responded during the progress of the test, the number of requests per second (RPS) and the number of failures encountered.
Charts

The Charts tab creates visualisation of the results. It shows how the number of requests changes with the number of processes (users), and how these values impact the API speed.
Failures/Exceptions

As the name suggests, the failures encountered during the tests are depicted here.
Since our API worked as expected, we do not have any failure/exception documented here.
Download Data

This tab lets you download the respective data in CSV format.
Conclusion

Load testing your software is one of the best practices of software development, which comes with the following benefits:

    Minimised cost of failure for organisations
    Improved software scalability
    Reduced risk for system downtime.
    Helps identify inefficient codes and hidden bugs in the system.
    Simulates simultaneous web app usage by multiple users.

The biggest advantage of using Locust for this purpose is that it lets you write load tests in plain Python and automatically renders the load testing UI in your browser.

Moreover, it has very thorough yet simple documentation which is helpful for its implementation.

Hence, if you are deploying your ML model in production, you should thoroughly load test your end-point(s) to make sure that they do not break under stress (simultaneous requests).
This will not only significantly improve the scalability of your system but also enhance its efficiency by reducing the risk of system failures.
