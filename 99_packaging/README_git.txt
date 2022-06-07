Version control with Git

The steps below are for GitHub, but should work similarly for other providers. 


1) Login to the Git-Provider homepage (for instance GitHub)

2) Use the navigation to go to "Your repositories"

3) Select 'New', give  the repository a name (e.g. 'cmp22') and description and
  optionally select "Add a README File" and "add a .gitignore" file
  (select python in the drop-down menu)

Version control with Git

The steps below are for GitHub, but should work similarly for other providers. 


1) Login to the Git-Provider homepage (for instance GitHub)

2) Use the navigation to go to "Your repositories"

3) Select 'New', give  the repository a name (e.g. 'cmp22') and description and
  optionally select "Add a README File" and "add a .gitignore" file
  (select python in the drop-down menu)

  click "Create repository"


Next you have an empty repository with a README.md file and a .gitignore file.
The README.md is a markdown file similar to the markdown cells in the jupyter notebooks. 
You can use it to describe your code here. 
The .gitignore files contains a list of file- and directory names that git should ignore.


To access your GitHub repository from the git client you need to setup a secure way to authenticate.
There are several ways to do this, the simplest is to set up a token.
The  token will be the password to access the repository. 


4) Navigate to "Settings" --> "Developer Settings" --> "Personal access tokens" and create a token.
  The token is sopposed to be secret - save it in a secure place. It is shown to you only once. 

5) You can setup credential caching (saves password for some time, default 900 seconds)

   git config --global credential.helper cache

   or

   git config --global credential.helper cache

   to save permanently (clear text, not secure).


6) Change to the directory where you want the working copy of your repository be located,
   for instance the package directory created for PIP

7) Git requires to check out a repository to an empty directory.
   You can either do this and copy the source you want to work on
   into  this directory. Alternatively you can check out to a
   temporary directory and move the .git directory and  other files
   into your source directory
   
   Here: checking out the reposotory into a temporary directory:

   git clone https://github.com/<USERNAME>/cmp22.git temp
   cd temp
   mv .git .gitignore README.md ..
   cd ..
   rm -rf temp


8) Check the status:

   git status

9) Add the existing files to git ("staging")

   git add cmp22 setup.py
   git status

10) Commit the changes

    git commit

11) Upload files to the reporitory. This will ask for username and password. Use the token as password. 

    git push

12) Check the GitHub page of your repository. 






