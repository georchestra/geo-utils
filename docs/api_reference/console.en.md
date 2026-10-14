

## [Console: `Console_api`](https://github.com/georchestra/geo-utils/blob/main/geOrchestra/console/console.py)

The top-level client's `console` attribute is an instance of `Console_api`. It sends requests to `/console/private/...` using HTTP Basic authentication.

### Users

| Method | Purpose | Result notes |
| --- | --- | --- |
| `getusers(uid="", filter=None)` | Read a user by UID or request the users endpoint | Response text on HTTP 200; otherwise `None`. The `filter` parameter is currently unused. |
| `createnewuser(org, sn, givenname, mail, description)` | Create a user | Response text on HTTP 200; otherwise an error string. |
| `updateuserdetails(uid, json)` | Update a user; `json` is a JSON-encoded request body | Response text on HTTP 200; otherwise `None`. |
| `deluser(id)` | Delete a user | Response text on HTTP 200; otherwise an error string. |

### Organizations

| Method | Purpose | Result notes |
| --- | --- | --- |
| `getorgs(uid="", filter=None)` | Read an organization by UID or request the organizations endpoint | Response text on HTTP 200; otherwise `None`. The `filter` parameter is currently unused. |
| `createneworgs(name, shortName, orgType, address="", description="", note="", mail="", url="", b64logo="")` | Create an organization | `orgType` should be a Console-supported type such as `Association`, `Company`, `NGO`, `Individual`, or `Other`. Returns response text on HTTP 200; otherwise an error string. |
| `delorgs(id)` | Delete an organization | Response text on HTTP 200; otherwise an error string. |

### Roles

| Method | Purpose | Result notes |
| --- | --- | --- |
| `getroles(uid="")` | Read roles, optionally scoped by `uid` | Response text on HTTP 200; otherwise `None`. |
| `createnewroles(cn="NEWROLE", description="Default description")` | Create a role | Response text on HTTP 200; otherwise an error string. |
| `updaterolesuser(uuid="testadmin", cn="ROLE")` | Assign a role to a user | Response text on HTTP 200; otherwise an error string. |

These operations may require administrator privileges. Return values are response text, `None`, or an error string rather than a common response type. Check each result before continuing.
