<h1>BLOG WEBSITE</h1>
<h3>Using:</h3>
<ul>
<li>FLASK</li>
<li>BOOTSTRAP</li>
<li>WTFORMS</li>
<li>SQLALCHEMY</li>
<li>SMTLIB</li>
<li>GRAVATAR</li>
<li>CKEDITOR</li>
</ul>
<h3>Features:</h3>
<ul>
<li>Responsive</li>
<li>Admin privileges to add and delete posts</li>
<li>User's can be signed</li>
<li>Users can comment</li>
<li>Users have avatars</li>
<li>Posts with images</li>
<li>Working contact form</li>
</ul>
<h4>TO-DOs Before Running or Deploying</h4>
<ul>
<li>First registered user will be admin</li>
<li>After registration, admin and users need to
login to post or comment</li>
<li>Change the 'Your Blog' text in the html files</li>
<li>To be able to send emails from contact form; 
</li>
<ul>
<li>Assign an email address to 'gmail' variable</li>
<li>Assign an email address to 'to_addrs' argument</li>
<li>Either create an environment variable called 
'GMAIL_PASSWORD' or enter the password directly to the
'password_gmail' variable.</li>
</ul>
</ul>
<h4>Guidance For Deploying on Render.com</h4>
<ol>
<li>Register for free account.</li>
<li>From New+ button create a new Web Service</li>
<li>Give access to your GitHub repos for Render</li>
<li>Choose the repo you are trying to deploy</li>
<li>Name the app</li>
<li>Choose the free plan and 'Create Web Service'</li>
<li>From New+ button create a new PostgresSQL</li>
<li>Name the database</li>
<li>Copy 'Internal Connection String' (ICS)</li>
<li>Choose the free plan and 'Create Database'</li>
<li>Go back to the Web Service</li>
<li>Choose 'Environment'</li>
<li>Add a new variable called DATABASE_URL</li>
<li>Paste ICS as the value</li>
<li>If ICS starts with 'postgres', change it to 'postgresql'</li>
</ol>