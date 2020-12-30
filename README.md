# Django PyGrader
This Django webpage will let you create assignments with multiple test cases and have
students submit .py files which will be run against all the cases. Students can see
their results instantly and instructors can look at a student's results, or the results
of an assignment.


This program is designed to be compatible with Brigham Young University's Learning Suite,
but the goal is for it be generally useable.

## URLs

#### /admin
Default Django admin page.

#### /
The index page, which has links to basic site functions. 

#### /submit
Shows a dropdown menu asking which assignment you want to submit, then redirects to the
submit page for that assignment.

#### /submit/\<str:assignment_name>
A page where a student can enter their NetID and upload a .py file and submit an
assignment.

#### /view_submission_result
A page which asks for a submission ID and redirects you to that submission result. To
protect student privacy without a student login system, submission results are not
identifiable. To get to a submission result page, you have to know the submission result
ID, which is its ID in the Django database.

#### /view_submission_result/\<int:submission_id>
A page that shows the result of a submission. Shows the grade the submission recieved
and the I/O for each test case with excpected and actual output.

#### /create_assignment
A page the allows an instructor to create a new assignment. The assignment needs a name,
an open and close date/time, a number of allowed submissions, a whitespace seperated list
of allowed Python packages, and a grading method.

#### /add_test_case/\<str:assignment_name>
A page the allows an instructor to add a test case to an assignement. A test case has
a string representation of the command line arguments for the test case, and a list of
files that the code should have access to. This allows for the student to hard code a
filename like 'data.txt' and have that data change between cases if desired.

#### /manage_net_ids
A menu for instructor NetID functions.

#### /add_net_id
A page that allows an instructor to add a NetID. A NetID is just a unique identifier for
a student that allows them to submit assignments. A NetID can optionally be associated
with a name.

#### /remove_net_id
A page that allows an instructor to remove a NetID from the database.

#### /upload_net_id_csv
A page that allows an upload of a csv file and will add all NetIDs found in it. Made to
be compatible with the BYU Learning Suite student list download, but also generally
compatible with any CSV that has a NetID column. Will also try to find data from "Name"
and "First Name", "Last Name" columns. This function will add or update NetIDs.

#### /clear_net_id
A page that allows and instructor to clear all NetIDs from the database.

#### /grader_login
A page the allows someone to login and access the instructor pages.

#### /success
A page that shows a success message on successful operations.

#### /failure
A page the shows a failure message on successful operations.

## TODO:
* Finish create test case functionality
* Test basic functionality
* Honestly all the testing after that
* A nice way for someone to deploy this
* Change site to use https
* Make test submit selection page