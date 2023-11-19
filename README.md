# Vulnerable bank

This course project for Cyber Security course in University of Helsinki. This
project contains five vulnerabilities and their fixes.

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
setting variable in `project/settings.py`.

Security flaws are from OWASP Top 10 for 2021 list.

### Insecure design
[bank/views.py](https://github.com/elehtine/vulnerable-bank/tree/main/bank/views.py#L14)

There is no validation for sending money in bank. That could easily be taken
advantage of by sending negative amount of money. In that way sender gets money
from the receiver.

It will be fixed by validating input. It should be done in the backend but it
is often also done in the frontend so error is easier to avoid by users. This
kind of flaws in business domain are not always easy to spot by programmers.
These flaws can be less trivial. In this bank case it is easy to spot and fix.
Also unit tests are often added to ensure that validation will be working in
the future.


### Crosse-site request forgery
[project.settings.py](https://github.com/elehtine/vulnerable-bank/tree/main/project/settings.py#L55)
[bank/templates/bank/account.html](https://github.com/elehtine/vulnerable-bank/tree/main/bank/templates/bank/account.html#L8)

Vulnerable bank doesn't prevent cross-site request forgery. This way malicious
user could make own form which will create post request to vulnerable bank. If
careless user submits form then malicious user could get money transform from
careless user.

This is form that Bob could use to get money from Alice:
```
<form action="localhost:8080/bank/alice" method="POST">
    <input type="hidden" name="receiver" value="bob" />
    <input type="hidden" name="amount" value="1000000" />
    <input type="submit" value="View pictures" />
</form>
```

This can be tried running server with
```
python3 -m http.server 9000
```
and trying to click button in [malicious_link.html](http://localhost:9000/malicious_link.html).

This can be fixed by using CSRF middleware token. It will generate new request
for every request of the page. Without up to date token requests are not
processed and malicious form would do nothing.


### Identification and Authentication
[initial.json](https://github.com/elehtine/vulnerable-bank/tree/main/initial.json#9)

OWASP top 10 has Identification and Authentication Failures. It includes
permits default, weak, or well-known passwords, such as "Password1" or
"admin/admin".

Project admin user indeed is "admin/admin" which should not be allowed. This
can be avoided by not loading `initial.json` data and creating admin user with 
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
pages and send money for themselves by replacing their username in the url with
other user.

This can be fixed by checking which user made the transfer request instead of
allowing users to inform in the url which user is sending money. In my fix I
compared these two to each other. Often access control mechanism is implemented
once and used through the application.


### Injection
[blog/views.py](https://github.com/elehtine/vulnerable-bank/tree/main/blog/views.py#L13)
description of flaw 5...
how to fix it...

Blog message could contain SQL injection. Malicious user could for example post
a message which shows other user's balance.

Following input creates message which contains balance of admin:
```
message', 3), ((SELECT balance FROM bank_account WHERE owner_id = 1), 3); --
```

This can be avoided by escaping all text given to queries. Every database
management system have implemented protection against SQL injection.
