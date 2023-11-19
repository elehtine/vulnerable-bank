# Vulnerable bank

This course project for Cyber Security course in University of Helsinki. This
project contains five vulnerabilities and their fixes.

Project contains banking system. Initial users have accounts in the bank. They
can send money to each other. If new accounts are created with Django's admin
page their bank accounts needs to be added manually.

There is additional blog application where users can send messages.

## Fixing flaws

Vulnerability flaws are toggled off by changing `FIX_FLAWS = True` in
project/settings.py.


## Installing instructions

Run following commands to set up and run project on your machine:

```
python3 manage.py migrate
python3 manage.py loaddata initial.json
python3 manage.py runserver
```

There is following three users:
| username | password    |
|----------|-------------|
| admin    | admin       |
| alice    | redqueen    |
| bob      | squarepants |

## Report

Project [vulnerable-bank](https://github.com/elehtine/vulnerable-bank) contains
source code and installing instructions. All security flaws are fixed by
setting variable in `project/settings.py`. There is
[initial.json](https://github.com/elehtine/vulnerable-bank) file which contains
initial data for the application.

Security flaws are from OWASP Top 10 for 2021 list.

### Insecure design
[bank/views.py](https://github.com/elehtine/vulnerable-bank/tree/main/bank/views.py#L14)

There is no validation for sending money in bank. That could easily be taken
advantage of by sending negative amount of money. In that way sender gets money
from the receiver. Also it is possible to have negative balance because of lack of any
checks.

It will be fixed by validating input. It should be done in the backend but it
is often also done in the frontend so error is easier to avoid by users. This
kind of flaws in business domain are not always easy to spot by programmers.
These flaws can be less trivial. In this bank case it is easy to spot and fix.
Also unit tests are often added to ensure that validation will be working in
the future.

My fix is checking that transfer amount is at least zero and at most the balance user have.
That is what bank wants it to be.


### Crosse-site request forgery
[project.settings.py](https://github.com/elehtine/vulnerable-bank/tree/main/project/settings.py#L55)
[bank/templates/bank/account.html](https://github.com/elehtine/vulnerable-bank/tree/main/bank/templates/bank/account.html#L8)

Vulnerable bank doesn't prevent cross-site request forgery. This way malicious
user could make own form which will create post request to vulnerable bank. If
careless user submits form then malicious user could get money transform from
careless user.

To successfully use cross-site request forgery malicious user needs to send user
a link or a form that malicious user couldn't use by himself because a lack of
authorisation. When careless user is authenticated and then uses form provided by
a malicious user then authorisation is not a problem because careless user is
authorisated.

This is form that malicious Bob could use to get money from careless Alice:
```
<form action="localhost:8080/bank/alice" method="POST">
    <input type="hidden" name="receiver" value="bob" />
    <input type="hidden" name="amount" value="1000000" />
    <input type="submit" value="View pictures" />
</form>
```

This can be tried in your machine by running server with
```
python3 -m http.server 9000
```
and trying to click button in [malicious_link.html](http://localhost:9000/malicious_link.html).

This can be fixed by using CSRF middleware token. It will generate new request
for every request of the page. Without up to date token requests are not
processed and malicious form would do nothing.

I fixed this vulnerability by using `CsrfViewMiddleware` of Django. This generates CSRF
middleware token and forms cannot be evaluated in the views without the token.


### Identification and Authentication
[initial.json](https://github.com/elehtine/vulnerable-bank/tree/main/initial.json#9)

OWASP top 10 contains Identification and Authentication Failures. It includes
permits default, weak, or well-known passwords, such as "Password1" or
"admin/admin".

Poor passwords are one of the most common user mistakes. Users are always warned
about this but still many people use same password in most of their applications.
When they leak their password all of their accounts are compromised.

Project admin user indeed is "admin/admin" which should not be allowed. This
can be avoided in Vulnerable bank by not loading `initial.json` data and
creating admin user with 
```
python3 manage.py createsuperuser
```
This command prevents creating users with weak passwords.

Strategies against this kind of threats include implementing multi-factor
authentication, implementing weak password checks when testing new or changed
passwords, and limiting failed login attempts.


### Broken Access Control
[bank/views.py](https://github.com/elehtine/vulnerable-bank/tree/main/bank/views.py#L26)

Vulnerable bank doesn't authorise users. Users could even go each other's bank
pages by replacing their username in the url with other user. This allows users to see
each other's balance and even transfer money from the other users.

This can be fixed by checking which user made the transfer request instead of
allowing users to inform in the url which user is sending money. Often access
control mechanism is implemented once and used through the application. One often used
tactic is always deny access by default and whitelist all groups and users that can access
the resource.

In my application only authorisation problem is in bank transfer. I fixed this by checking
that authenticated user is the same user that they claims to be.

### Injection
[blog/views.py](https://github.com/elehtine/vulnerable-bank/tree/main/blog/views.py#L13)

Blog message could contain SQL injection. In SQL injection the data given to the
SQL query contains for example another query. In this way effects can be different
from what it would normally be. This is perhaps the most known threat. It can allow
malicious users to do any kind of database commands that are not intended to be
allowed.

Malicious user could for example post a message which shows other user's balance.

Following input creates message which contains balance of admin:
```
message', 3), ((SELECT balance FROM bank_account WHERE owner_id = 1), 3); --
```

This can be avoided by escaping all text given to queries. Every database
management system have implemented protection against SQL injection. It is well
known that these implementation should be used.

In the blog messages I didn't escape these texts which makes these SQL injections
possible. It doesn't only add vulnerabilities to blog but also in the bank. My fix
is to use those Django SQL parameter escaping functionalities. It is easy way to avoid
all known SQL injections.
