# Goal
Incorporate the new HSAccess library, which provides the interface through which services can:
  1. Add resources
  2. Add users
  3. Add groups
  4. Add users to groups
  5. Change user's permissions wrt to groups
  6. Change user's permissions wrt to resources
  7. Change group's permissions wrt to resources

*This list is not exhaustive.*

Data about Users, Groups, Resources, and permissions is still stored in Django. Therefore, we duplicate such data, storing them twice: once in Django as before, and once in HSAccess.

# Why Is This Non-trivial?
The complexity (as it often does) comes from keeping the 2 data sources consistent with each other. To properly integrate HSAccess, therefore, we must find all of the places that mutate any piece of Django data that is also stored in HSAccess and mirror those changes in HSAccess.

The extent to which this is trivial is the extent to which our interfaces inside `hydroshare` confine and constrict the pieces of code which are allowed to mutate mirrored data. The complexity of integrating HSAccess therefore is in properly defining the interfaces that govern changes to the data.

# Process
We now explore the steps necessary to integrate HSAccess. We begin with a couple of refactors to strengthen internal interfaces, which will make it easier to identify the places where we need to mirror Django mutations.

## 1. `hs_core/hydroshare` As Truth
Refactor `resource.py`, `users.py` to expose top-level functions for *ALL* off the operations we perform on resources and users, respectively. Change uses throughout the code base to use only these functions for the operations they expose. The goal is to ensure that, for example, the only way to delete a resource is via the `resources.delete_resource(pk)` function, and the only way to create a user is via `users.create_account(...)`.

As a guage, treat `hs_core/hydroshare/utils.py` as a file private to `hs_core/hydroshare`. Those utility methods are mostly covered by top-level functionality exposed in `resource.py` and `users.py`. 

## 2. Treat ORM as an implementation of an interface
ORM is the way by which we mutate data in Django, and while it does save us from writing a lot of boilerplate code, it also does not provide a customizable/extendable interface. 

As an example, consider some ORM and non-ORM based code to provide a user with edit persmissions over a resource:

a. ORM-based:
```python
  if not res.edit_users.filter(pk=user.pk).exists():
    res.edit_users.add(user)
```
b. No ORM:
```python
  res.add_edit_user(user)
```
The second has many advantages over the first. First, we *cannot* forget to check if the user already has edit permissions because `add_edit_user` does it every time. But more importantly, the second helps us integrate HSAccess because it allows us to change what it means to add an editor.

Integrating HSAccess essentially involves redefining all of the operations that need to be mirrored, so it would help a lot to refactor the code that performs those operations to all invoke methods that hide the implementation. The most important place to start is to remove all uses of the permissions variables: `edit_users`, `edit_groups,` `view_users`, and `view_groups`. Replace all manipulations of those variables with methods on the `ResourcePermissionMixin` that provide the same functionality.

### An example:
####  Old Way
```python
  # definition
  class ResourcePermissionsMixin:
    ...
    edit_users = models.ManyToManyField(...)
    
  # usage
  res.edit_users.add(user)
```
#### New Way
```python
  # definition
  class ResourcePermissionsMixin:
    ...
    
    # edit_users is now PRIVATE
    __edit_users = models.ManyToManyField(...)
    
    def add_edit_user(user):
      if not self.__edit_users.filter(pk=user.pk).exists():
        self.__edit_users.add(user)
  
  # usage:
  res.add_edit_user(user)
```

## 3. `resource.py` and `users.py` 
Refactor the implementations of `resource.py` and `users.py` to now update Django, but also update HSAccess. Note that Django and HSAccess do not have identical interfaces, so the two pieces of code will not necessarily look identical, although they will achieve the same net effect (ex: share a resource with a user, or create a new account, etc).

### An example:

```python
  def create_user(....):
    
    # puts the user in HSAccess, throwing exceptions on fail
    def create_hsaccess_user(...):
      ...
  
    # puts the user in Django (same as how we do it now)
    def create_django_user(...):
    
    try:
      create_hsaccess_user(...)
      create_django_user(...)
      return new_user_id
    except Exception:
      # handle exception as necessary
```
