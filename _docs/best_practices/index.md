.Locust Python

Scalability testing is an important part of getting web service production ready. There is a lot of tools for load testing, like Gatling, Apache JMeter, The Grinder, Tsung and others. There is also one (and my favorite) written in Python and built on the Requests library: Locust.

As it is noticed on Locust website:

    A fundamental feature of Locust is that you describe all your test in Python code. No need for clunky UIs or bloated XML, just plain code.

Locust installation

Performance testing python module Locust is available on PyPI and can be installed through pip or easy_install.

pip install locustio or: easy_install locust
Example locustfile.py

Then create locustfile.py following the example from docs. To test Django project I had to add some headers for csrftoken support and ajax requests. Final locustfile.py could be something like the following:

# locustfile.py
from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):

def on_start(self):
        self.login()

def login(self):
        # GET login page to get csrftoken from it
        response = self.client.get('/accounts/login/')
        csrftoken = response.cookies['csrftoken']
        # POST to login page with csrftoken
        self.client.post('/accounts/login/',
                         {'username': 'username', 'password': 'P455w0rd'},
                         headers={'X-CSRFToken': csrftoken})

@task(1)
    def index(self):
        self.client.get('/')

@task(2)
    def heavy_url(self):
        self.client.get('/heavy_url/')

@task(2)
    def another_heavy_ajax_url(self):
        # ajax GET
        self.client.get('/another_heavy_ajax_url/',
        headers={'X-Requested-With': 'XMLHttpRequest'})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior

Start Locust

To run Locust with the above python locust file, if it was named locustfile.py, we could run (in the same directory as locustfile.py):

locust --host=http://example.com

When python load testing app Locust is started you should visit http://127.0.0.1:8089/ and there you’ll find web-interface of our Locust instance. Then input Number of users to simulate (e.g. 300) and Hatch rate (users spawned/second) (e.g. 10) and press Start swarming. After that Locust will start “hatching” users and you will be able to see results in the table.
Python Data Visualization

So, the table is nice but we’d prefer to see results on a graph. There is an issue in which people ask to add graphical interface to Locust and there are several propositions how to display graphs for Locust data. I’ve decided to use Python interactive visualization library Bokeh.

It is easy to install python graphing library Bokeh from PyPI using pip:

pip install bokeh

Here is an example of running Bokeh server.

We can get Locust data in JSON format visiting http://localhost:8089/stats/requests. Data there should be something like this:

{
       "errors": [],
       "stats": [
           {
               "median_response_time": 350,
               "min_response_time": 311,
               "current_rps": 0.0,
               "name": "/",
               "num_failures": 0,
               "max_response_time": 806,
               "avg_content_length": 17611,
               "avg_response_time": 488.3333333333333,
               "method": "GET",
               "num_requests": 9
           },
           {
               "median_response_time": 350,
               "min_response_time": 311,
               "current_rps": 0.0,
               "name": "Total",
               "num_failures": 0,
               "max_response_time": 806,
               "avg_content_length": 17611,
               "avg_response_time": 488.3333333333333,
               "method": null,
               "num_requests": 9
           }
       ],
       "fail_ratio": 0.0,
       "slave_count": 2,
       "state": "stopped",
       "user_count": 0,
       "total_rps": 0.0
    }

To display this data on interactive plots we’ll create plotter.py file, built on usage of python visualization library Bokeh, and put it to the directory in which our locustfile.py is:
Running all together

So our Locust is running (if no, start it with locust --host=http://example.com) and now we should start Bokehserver with bokeh serve and then run our plotter.py with python plotter.py. As our script calls show, a browser tab is automatically opened up to the correct URL to view the document.

If Locust is already running the test you’ll see the results on graphs immediately. Else start a new test at http://localhost:8089/ and return to the Bokeh tab and watch the results of testing in real time.

That’s it. You can find the whole code at github.Feel free to clone it and run the example.

git clone https://github.com/steelkiwi/locust-bokeh-load-test.git
  cd locust-bokeh-load-test
  pip install -r requirements.txt
  locust --host=<place here link to your site>
  bokeh serve
  python plotter.py

You should have Bokeh tab opened in browser after running these commands. Now visit http://localhost:8089/ and start test there. Return to Bokeh tab and enjoy the graphs.