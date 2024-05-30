Title : Cross Age Person Identification for Forensics

Group Members:
Aditya Kombde ( Team Lead )
Parimal Thakre
Umair Khan
Pranav Mukund

Guided by: Prof S. S. Bhandare

Instructions to Run Applicaiton:

1. Unzip the file CAPID.zip
2. Ensure that System have cl.exe compiler and other C/C++ libraries. If not then install through Visual Studio community edition
3. Edit path variable in user variable 
    C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.16.27023\bin\Hostx86\x86
    C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\IDE

    Note: Change the path as in your current System 
4. From Anaconda Navigator open cmd prompt.
5. Navigate to the folder where you have unzipped the file CAPID.zip
6. Create conda environment using "environment.yml" file
7. Activate the environment
8. Navigate to Notebook Folder
9. Download Pretrained Model from Google Drive : "https://drive.google.com/file/d/1OmfAjP3BAqVxaQ2pwyJuOYUHy_incMNd/view?usp=share_link"
10. Move the Pretrained model file " mtlface checkpoints.tar" to Notebook folder.
10. Execute the app.py file using command " python app.py" or " python3 app.py"
11. Open the browser and navigate to "http://127.0.0.1:5000" or the given local host on command line.
12. Upload the image of the person and click on "Detect" button to get the result.

