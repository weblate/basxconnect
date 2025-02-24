basxconnect
===========

A core implementation of a CRM system for non-profit organizations.

(It feels like the README is the wrong document to place the whole vision/mission/core values stuff but it will be okay for now I think)

Vision
------
Providing non-profit organizations with a code framework that helps to build tools for managing their data.

Mission
-------
Create and maintain a django-based framework which implements:
- A standardized UI concept based on IBM's carbon design system
- CRM-like core data models which are open to extension
- Code building blocks and shortcuts which allow easy customization and extension

Core values
-----------
- Open source development (this, however does *not* include free support)
- Use of existing and proven technology where possible while minimizing external dependencies
- Focus on workflows and tasks for Non-Profit organizations (User experience)
- Writing code and APIs for developers, not for website administrators (Developer experience)
- Development does not center around a final *product* but around the tools to create a *product* (because every *product* is different)


What we have so far
-------------------

- Integration of the core parts of carbon design in django (*"like bootstrap for django"*)
- CRUD-framework (*"Quick generation of create/read/update/delete views"*)
- HTML-layout framework which allows a more flexible hooking-in than the standard HTML-rendering mechanisms (*"DOM on the server side"*)
- Core model to manage people, communication and relationships
- Demo project which implements a bare-bone version of a *product*

What we still need to do
------------------------

- Finishing the implementation of the carbon design components
- Adding a workflow engine which allows code-based configuration of manual and automated workflows (e.g. uploading a file, waiting for approval from a certain role, sending out an email automatically, etc.)
- Implementing an extension which provides donation models and workflows
- Improving the existing code base to have better support for extendability
- Write documentation where necessary and add code-examples and how-to's
- Implement revisions completely to allow going to a certain date and maybe display diffs
- Maybe: Add a developer option to easily find out which part of the interface are generated where in the code (making customization a lot easier)

Other TODOs:
- Replace initial data in migrations files with fixture files or scripts
- Explain more why basxConnect is necessary and the difference to alternative solutions

We would like to thank the following projects for their work, they provide a valuable base for basxConnect:

- Translation: https://weblate.org/
- Design System: https://www.carbondesignsystem.com/
