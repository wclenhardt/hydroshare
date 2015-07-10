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

