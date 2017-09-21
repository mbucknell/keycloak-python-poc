# Proof of Concept - Authentication by verifying token generated by keycloak

### Running a local version of keycloak
Run a local version of keycloak. The following docker containers can be used to start a keycloak instance which is backed
up by a MySQL database.

```bash
% docker run --name mysql -e MYSQL_DATABASE=keycloak -e MYSQL_USER=keycloak -e MYSQL_PASSWORD=password -e MYSQL_ROOT_PASSWORD=root_password -p 3306:3306 -d mysql
% docker run --name keycloak -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -p 8080:8080 --link mysql:mysql jboss/keycloak-mysql
```
This creates a keycloak instance that you can access at localhost:8080/auth. It will create an 'admin' user with password, 'admin'.
You can create other users. The keycloak_example.py is set up to decode tokens for the security-admin-console audience. You will
need to go to this client and have dev tools on to grab the JWT token. This can be done be going to Realm Settings and clicking on the Keys
tab. The token will be in the request header, Authorization. Do not include the word "Bearer". You can create other users and add to
the admin role to test other users. To make things easier on you for testing, you may want to increase the token 
expiration time. That can be done on the Realm Settings page, in the Tokens tab.


### Running the keycloak_example.py script

To run the keycloak_example.py script, create a python3 virtual environment. This has been tested with 3.6. Then use pip to 
install the requirements. We are using PyJWT to decode the tokens. See https://pyjwt.readthedocs.io/en/latest/index.html
for more information about this package. We also will need to install the cryptography package which is 
needed because keycloak uses RSA to sign the tokens. 


```bash
% virtualenv --python=python3 env
% env/bin/pip install -r requirements.txt
```

Paste in your JWT token. Go to the Keys tab in Realm Settings and click on the Public Key for the RSA Type key. This will 
pop up a text box with the public key. Paste that into keycloak_example.py.

Run the script - ```env/bin/python keycloak_example.py```. This should print out the verified token.


### Using authorization in a Python microservice that uses Flask and Flask-Restplus.

The example app in this directory, uses the Flask extension, Flask JWT Simple (https://github.com/vimalloc/flask-jwt-simple).
It is a sister extension of flask-jwt-extended. It provides barebones support for working with JWT's which is what we need.
It appears to be in active development, along with it's sister extension. In fact, one of the issues I ran into had a very
recent issue opened about it, along with the workaround.

In the real application, we will grab the token from the request.headers['Authorization']. The public key should be specified
as an environment variable that gets put in the app.config object. 

This POC has a single endpoint, '/endpoint', which requires jwt authentication. In config.py we are setting, JWT_ALGORITHM, 
JWT_PUBLIC_KEY, and JWT_DECODE_AUDIENCE. If you try to run the application, you will need to provide your JWT_PUBLIC_KEY 
in .env file or in an environment variable. JWT_DECODE_AUDIENCE can also be modified to something other than 
'security-admin-role' in the same way.

See services.py for how to use the extension to require jwt authorization.

You can then test the endpoint using curl to specify (or not) the header including 'Authorization: Bearer ' with your
JWT token inserted.


Questions/issues that remain:
1. Do we want to be able configure which endpoints need authorization? Do we want the same level of configurablity as
the springboot microservices.
2. Implementation - how to make it easy to add this to all of our python applications. May want to consider some sort
of python module/package that can be imported into all applications. Alternatively, see what may be available as a Flask add-on
or plugin.
3. Can we use the above setup to easily test locally ... especially when testing microservices in isolation?