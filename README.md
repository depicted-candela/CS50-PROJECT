# THE **VIdeo** WEB-BASED APP
#### Video Demo:  [YouTube Video](https://youtu.be/oNFgFzCkGOM)
#### Description:

This web-based app is able to add audio to a static image. You can use it by following the following steps
1. Clic on **Register** button to add your user to your database
2. When you have completed the first step the page redirects automatically you to the **Log In** page, log in with your credentials
3. When you have completed the first step the page redirects automatically you to the Home Page. Clic on **Clic to start uploading your media files**
4. Upload your valid files for images (.jpeg, .jpg, .png) or audio (whatever) and then click on **Upload** Button
5. Wait until the python process is completed so as to a file called *video.mp4* is automatically downloaded
6. If you want to use again the app when you are in, simply put as inputs two more files that you consider to process
7. To get out from the web-based page simply clic on **Log Out**

The python app uses the library *moviepy* to process the files and *flask* as a environment for the web-based application.

The functionality that enables the automatic download of the resulting video is *send_from_directory* from flask library for python. Specifically the get_video() function created for the app performs this actions by using the called library.

The funcion *secure_filename* of werkzeug.utils module enables the correct manage of names to files. The app settings app.config['UPLOAD_FOLDER'], app.config['RESULTS_FOLDER'] and app.config['MAX_CONTENT_PATH'] are resposible for: set the folder of the input files, set the folder of the output files and set the maximum size (in bytes) allowed by the app to the user; respectively.

The sql database responsible for storing the credentials for users. The structure of the database was created as follows:

*CREATE TABLE users (*
*id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,*
*username TEXT NOT NULL,*
*hash TEXT NOT NULL);*
*CREATE TABLE sqlite_sequence(name,seq);*

#### App routes
* */login*: performs a series of steps to detect if the user inputs for login are invalid or are not in the sql database, if the validations say that the inputs are correct and in the database then redirect the user to the root base route */*, otherwise, redirect to the route */login* showing the errors that the user needs to correct
* */register*: performs a series of steps to detect if the user inputs for login are invalid or are in the sql database, if the validations say that the inputs are correct and not in the database then store the data in the sql database with a encrypted password, and redirect the user to the route */login*, otherwise, redirect to the route */register* showing the errors that the user needs to correct
* */*: renders the template **intro.html** using the *reder_template* function from flask library, **intro.html** contains the **home.html** file in which the user can upload their media files.
* */home*: renders the template **home.html** that calls the *POST* action of the */uploader* route
* */uploader*: performs a series of steps to detect if the user inputs for files are invalid, if are invalid, renders the **home.html** showing the errors that the user needs to correct, otherwise, read, and write the files to the called above folders and creates the *video.mp4* file that contains the audio and static image that were processed. At the end calls the */get-video/<path:video_name>* route
* */get-video/<path:video_name>*: by using the *send_from_directory* function enables the automatic download of the final file (*video.p4*)