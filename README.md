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
source code and installing instructions.

FLAW 1:
exact source link pinpointing flaw 1...
description of flaw 1...
how to fix it...

Blog message could contain SQL injection. Malicious user could for example post
a message which contains SQL to delete all messages.


FLAW 2:
exact source link pinpointing flaw 2...
description of flaw 2...
how to fix it...

Bank doesn't prevent cross-site request forgery.


FLAW 3:
exact source link pinpointing flaw 3...
description of flaw 3...
how to fix it...

OWASP top 10 has Identification and Authentication Failures. It includes
permits default, weak, or well-known passwords, such as "Password1" or
"admin/admin".

Project admin user indeed is "admin/admin" which should not be allowed.


FLAW 4:
exact source link pinpointing flaw 4...
description of flaw 4...
how to fix it...

Broken Access Control bank doesn't authorise users.


FLAW 5:
exact source link pinpointing flaw 5...
description of flaw 5...
how to fix it...

Insecure design. Negative amount can be sent in bank.
