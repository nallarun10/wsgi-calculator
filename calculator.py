#! usr/bin/env python3
"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback

def body():
    """ Main body: text/html of the webpage """

    return """
    <h1>My Calculator<h1>
    <h2> Follow below instruction to perform basic calculation:</h2>
    
    <h3>To add, type /add/num1/num2/. to get sum of all nums.</h3>
    <h3>To subtract, type /subtract/num1/num2/. to get final difference between the nums.</h3>
    <h3>To multiply, type /multiply/num1/num2/. to get multiplication value of all nums.</h3>
    <h3>To divide, type /divide/num1/num2/. to get divsion of all nums, serially.</h3>
    """
def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum = 0
    for arg in args:
        sum += int(arg)
    return 'Sum of nums: {}'.format(str(sum))

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    diff = int(args[0])
    for arg in args[1:]:
        diff -= int(arg)
    return 'Subtration of the numbers: {}'.format(str(diff))

def multiply(*args):
    """ Returns a STRING with the multiplies the arguments """
    multiple = 1
    for arg in args:
        multiple *= int(arg)
    return 'Multiplied values: {}'.format(str(multiple))

def divide(*args):
    """ Returns a STRING with the divides the arguments """
    div = int(args[0])
    for arg in args[1:]:
        # if arg == 0:
        #     raise ZeroDivisionError ('No division by 0')
        # else:
        div /= int(arg)
    return 'Division of the all nums: {}'.format(str(div))


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    # func = add
    # args = ['25', '32']

    funcs = {
        '': body,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "500 Internal Server Error"
        body = "<h3> No divisions by zero</h3>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

    # sum = add(2,3,4,6)
    # print (str(sum))

    # sub = substract(23, 42)
    # print (sub)

    # mul = multiply(3,5, 2, 0, 2)
    # print (mul)

    # divs = (divide(22,11, 0))
    # print (divs)