Wear Tool Measurement
===

---
# Introduction to the topic
The goal of the Wear Tool Measurement is to detect, classify, and predict wear in chipping tasks. These chipping tasks are Turning and Milling Processes. 
The Turning Process is already working [see instructions down below], while the Turning process is still a work in progress.

**BAUMER CAMERA**:
Runs on UNIX (Ubuntu ...); Own API;
The Camera has its own API through which it can be accessed. Examples for the API can be found under `/baumer_api`.
Drivers can be downloaded on the Baumer Website.


## Milling Process
For the Milling Process, the code is running on a *Baumer ...* Camera. 

The Milling Process bares its own parameters. These can be found in the sketch down below. These parameters are an important information when classifying the wear. 


![Alt text](docs/img_readme/milling_parameter_graphic.png)
***Insert sketch of Parameters and Images of wear with parameters***

---

# Navigating Through The Application

Run through the application (how and where to navigate)

## How To Start The App?

To start the app in its current status, a small serious of steps have to be done before.

1. **Starting the Camera**

2. **Activating The Environment**

3. **Executing the Program**

4. **Closing the Program**


---

## How To Prepare Data?

The data the program can process are images of each sizes. To have a segmentation result, *Masks* of these images are also needed. These masks are the *Ground Truth* of every image, displaying the area of the wear. This is the process of *Semantic Segmentation* (see: https://de.mathworks.com/solutions/image-video-processing/semantic-segmentation.html).
These masks have to be created by hand. Best practice is using the *MatLab Image Labler* (content of *Image Processing Toolbox*). 
**Documentation on how to do it**

The final images and masks should be stored in the filesystem under `/images/raw_images` or `/masks/raw_masks` within a *new folder*.


In the *Data Preparation* tab, the images can be resized to a more fitting size. Herefore, the directory of the initial images (*Image directory source*) and the directory where the resized images will be saved to (*Image directory goal*) need to be selected.


![Alt text](docs/img_readme/frontend_dataprep.png)

The desired image size can be set in the *Image height* and *Image width* input. The input of which is the number of pixels, so the resolution of the image. Additionally, the number of channels can be altered. 
*Channels* mean the depth of the image arrays. So, for `grayscaled` images, the depth of the array would be `0`, for `RGB` images `3`, and for `CMYK` images `4` (see: https://medium.com/featurepreneur/understanding-the-concept-of-channels-in-an-image-6d59d4dafaa9). 

![Alt text](docs/img_readme/frontend_label_data.png)

**----- MISSING ------**
**Changing of the mask environment**
**Understanding "Mask Correction"**

## How To Train A New Model?

To understand the training of a Neural Network this might help:
https://towardsdatascience.com/an-introduction-to-neural-networks-with-implementation-from-scratch-using-python-da4b6a45c05b
For a basic explaination of the Train Test Split philosophy see maybe:
https://machinelearningmastery.com/train-test-split-for-evaluating-machine-learning-algorithms/
Or the official documentation: 
https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html

![Alt text](docs/img_readme/frontend_train_test_split.png)

The *Train-Test-Split* tab takes a full set of images and masks. It then splits off a random portion in the size of the wished for *Test size* and saves it to a new testing directory.

It is important, that masks and images are *belonging together* and have the *same size*. 
For new testing data set it is advisable to create a new directory.

The training of a new model can be done in the *Train New Model* tab. Here, one can select between a *Normal Mode* and an *Expert Mode*.

The *Normal Mode* provides the user with the basic functionality needed to train a new model.
To train a new Neural Net, the input parameters set by the user are the *name of the new model*, the *number of classes*, the *validation size*, ***CONTINUE HERE***

![Alt text](docs/img_readme/frontend_train_model_normal_mode.png)

![Alt text](docs/img_readme/frontend_train_model_expert_mode.png)

## How To Segment An Image?

![Alt text](docs/img_readme/frontend_segmentation.png)

---

## Where Can I Find Help?

![Alt text](docs/img_readme/frontend_help.png)

---
---
# Explaination to the code

## Structure
The code is structured into a *HTML frontend* and a *Python backend*. These are connected through the *Eel* library.
The frontend is hosted on a local server and displayed in the Browser. Every interaction can be done over this interface.
The backend provides all the function and computations. This includes especially the model training and segmentation of the images.

## Python Libraries
For the installation of the necessary libraries it is best practice to create a virtual environment. Herefore, **Anaconda** provides all the necessary tools, whilst being easy to use. 
- A documentation on how to install Anaconda can be found here: https://docs.anaconda.com/free/anaconda/install/index.html (Installation Guide)

- An introduction to Anaconda can be found here: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment (Creating a new environment)

Anaconda itself provides a User Inferface which is kind of self explainatory.

The libraries needed for the program can be found in the table below. All of them should be installable through `python pip`. It is important, that some libraries are not downwards compatible, and therefore require a certain order in which they are installed.
Since the versions of these libraries may or may not change the dependecies towards other libraries, it is best practice to take an empty environment, run the code, and install the packages regarding to the errors that appear.

| Package | Command | Used for |
|---|---|---|
|OpenCV (Python) | `pip install opencv-python` | Image Processing Operations|
| Tensorflow |`pip install tensorflow` | Machine Learning Functions|
| Eel |`pip install Eel` | Interface Between Python And HTML|
|SciKit-learn |`pip install scikit-learn` | Machine Learning Functions |
| Pillow |`pip install Pillow`| Image Processing Operations |
| Pandas |`pip install pandas` | Data Processing Operations |
| matplotlib |`pip install matplotlib` | Data Displaying Operations|

## Folder Structure
The folder structure can be found below. The main code for execution is located in the code directory. Inside, it is divided into the backendcode, directly inside the `code` folder, and the forntend part inside its designated folder.
Important documents and explainations can be found in the `docs` folder. 

The pretrained models are stored inside the `models` directory. Like the `training_images` and the `training_masks`, it is split into a `Milling` and a `Turning` part. Models get saved as a folder on their own and can be called accordingly as a directory.

The images and masks for training are stored in the `training_images` and `training_masks` folders. For every image, a mask exists with the same name as the image. 

- code
    - frontend
        - img
    - img
- docs
- logs
    - fit
- models
    - Milling
    - Turning
- training_images
    - Milling
    - Turning
    - Working Images (milling)
- training_masks
    - Milling
    - Turning

---
---
# HTML Frontend
Same structure as the backend

---
---
# Python Backend
The Python Backend provides all the calculations and functions the frontend cannot do. This includes especially the machine learning algorithms, image manipulation, and system-code-communication, like saving and loading files.


## Execution of the backend [`main.py`]
The entire application is started by executing the `main.py`-file. The function it executes is the `start_app()` function, which fires up the HTML interface over the Eel interface. It gathers the path to the directory on the system, and executes the `index.html` file with the Eel extension after navigating into the `frontend` folder. The parameter `mode` can be altered regarding the Browser the applicant wants to use.

Besides the main execution of the application, the `main` file provides function to the following:

- **Camera Functions**
The Camer is implemented under the `cameraBaumer.py` or `cameraSystem.py` file, but still has to be called and initialized in the `main` function. The following functions make use of the interface to the camera.
    - **Creating Video Stream** `video_feed()`
    To create a live Video Stream of the tool the python backend provides an extension to the JavaScript code, acting as an interface between camera and frontend. Therefore, a `VideoCamera` object has to be created and a Video Stream must be generated with the `gen()` function. The images streaming from the camera then are encoded into `blob` format (***B**inary **L**arge **OB**ject*), so the data can be passed to the JavaScript code with the Eel extension.
    - **Generating Video Stream** `gen(camera = VideoCamera)`
    This function generates a Video Stream with the help of the `VideoCamera` object, created in either one of the camera APIs (see down below). The Camera is initialized based on the system the code is running on. If the Baumer API is installed, meaning the system is executed on the Baumer Camera, the `main` file is loading the camera program fit for the Baumer Camera. If this is not the case, the regular Windows or Linux extension is called. Here, the *Camera Channel* of the specific system the code is running on has to be defined (usually between 1 and 3).
    - **Taking A Picture** `take_foto()`
    To take a foto the `take_foto` function uses the globally defined varaiables `filename`, `relevantImage`, and `cameraConnection`. The `cameraConnection` variable has been set before in the camera implementation (see above). The other two variables are set by this function and provide the filename and image data the image is handled with. Furthermore, through the`eel` extension, the image, encoded into blob format, is passed to the HTML interface.


- **Loading and Saving Images and Models**
The segmented images are stored in the `saved_images` folder, while the trained models are stored in the `models` folder. 
    - **Loading An Image** `loadImage(path: str)`
    A general function, that can be used to load images from a directory is provided with the `loadImage` function. The input it takes in the *path to the file* in form of a string. It accesses the global variable `filename` as path, and assignes the global `relevantImage` variable the new image data. By encoding the image data to `blob` format, the image data is exposed to the HTML interface over the `updatePicture` function.
    - **Loading A Model** `loadModel(path: str)`
    Loading the model from the saved directory is done in the same manner as with the images. It takes in the *path to the  directory* the model is stored in. The function set the global `myModel` variable for the keras object of the model by initializing a new `segmentation.Model` object. 
    - **Selecting A Directory** `get_directory(elementId: str)`
    To load, for example the model, over the HTML interface, a path string to the directory needs to be acquired. This can be acvhieved through an extra directory interface with the `get_directory` function. This function creates a `Tkinter` window, displaying the file explorer, and exposing the directory string to the according HTML element (e.g. text input) via the designated `elementId`.
    - **Selcting A File** `get_file(elementId: str)`
    The same procedure as in the `get_directory` function, but with `Tkinter` waiting for a file selection instead of a directory.
    - **Saving A Picture** `save_picture(path: str)`
    **???** Saves global `mask` variable and an image of the segmentation result to the directory over path input. The picture is saved with year, month, date, hour, minute, and second as filename. 
- **Preprocessing**
    - **Initialize Reshaper** `init_reshape(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int,y4: int)`
    Gathers the desired input shape of the model over the `getInputShape` function and builds a `Perspective` object called `reshaper` by passing the coordinate values of four prior selected points in the HTML interface. It returns the `reshaper` variable as global variable.
    - **Reshape Image** `reshape_image()`
    Grabs the global `relevantImage` variable and applies the `change_perspective` function of the `reshaper` on it (see *Data Preparation*). It later passes the `blob` encoded image to the HTML interface. 
    - **Crop Image Automatically** `auto_crop()`
    Takes the global `relevantImage` variable and applies the `generalUtensils.resize_image` function to it according to the model specific height and width. It later updates the image on the HTML surface as done in the previous functions.
    - **Change Shape Of Image** `change_image_shape(parameters)`
    Takes in parameters and creates a dictionary out of them with the `generalUtensils.get_parameters` function, then applies it to the `datapreparation.resizeImage` function (see *Helpful Functions* and *Data Preparation*).
    - **Mask Correction** `change_mask_extension(parameters)`
    **???**
    
- **Model Training** Interface to HTML Trainig Site
    - **Split Data Into Training And Test Data** `trainTestSplit(parameters)`
    Takes in parameters from the inputs of the HTML surface and turns them into a dictionary. Then it accesses the image and mask names over the selcted directory and splits them into a training and test margine using the built in sci-kit function `train_test_split` (see therefore: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html). Next, the images and masks are moved to the new location assigned in the HTML interface (saved in parameter dictionary).
    - **Training New Model** `train_model(parameters)`
    Takes in the parameters from the parameter input in the HTML surface, turns them into a dictionary, and trains model with the `modelTraining.trainModel` with it (see *Training New Model*).
    - **Evaluate Training Of The Model** `evaluateModel(multiclass: int, parameters)`
    Grabs the parameters from the parameters from the parameter input in the HTML surface, turns them into a dictionary, and evaluates them either as with the `evaluateTraining.multiclass_evaluation` when the input paramter `multiclass` is passed as `1` (True), or with the `evaluateTraining.binary_evaluation` when `multiclass` is passed as `0` (False).
    The return values of these functions are the *metrics* of the model, that are passed onto the HTML interface over the `eel` extension to the `outputMetric` function.

- **Segmenting An Image**
    - **Image Segmentation** `segment_image()`
    The segmentation applies the global variable for the pre-loaded model `myModel` onto the selected image `relevantImage` (also global variable). 
    In the first step, the model height width is compared with the image dimensions. If this is not the case, the function aborts and throws an error, asking for the right image size input.
    Next, the channels of the image are adjusted to the model input with the help of the `generalUtensils.adapt_channels` function (see *Helpful Functions*).
    In the third step, the segmentation is done by applying the `segmentation.Model.segment` on the image. 
    In the last step, the segmentation is evaluated by creating a `resultSegmentation.WearCluster` object with the masks of the segmentation result and applying its `wearClustering` function. The final mask of the wear segmentation, that indicates the boundaries of the wear, is displayed using `resultSegmentation.WearCluster.visualizeCluster`.
    In the end, the mask is passed to the HTML surface for display and the segmentation is evaluated using `resultSegmentation.wearWidth`.
    - **Live Segmentation** `liveSegementation()`


- **Unused Interfaces**
These interfaces have been used for the calibration of the **CAMERA BEFORE BAUMER** camera, but have been removed from this version. The functions can be found on other branches GitHub.
    - `readCalibration Parameter()`
    - `calibrateDistances(distance)`
    - `getPos(x1: int,x2: int,y1: int,y2: int)`
    - `tryOut()`






## Accessing the different cameras [`cameraSystem.py`, `cameraBaumer.py`]
camera implementation (and Baumer API)
## Helpful functions [`generalUtensils.py`]
general utensils
## Data Preparation [`datapreparation.py`, `perspective.py`]
data preparetion (and how to create masks) [data preparation, perspective, ]
### Data Preparation
### Perspective

## Training new model 
### `modelTraining.py`
### `evaluate_training.py`
### `U_Net_Model.py` 
### `U_Net_Model_v2.py`

model training (and explaination of the model) [modelTraining, evaluateTraining, U_Net_Model, U_Net_Model_v2]
## Segmenting an image 
### `segmentation.py`
### `segmentation_v2.py`
### `segmentation_test.py`
### `resultSegmentation.py`

segmentation [segmentation, segmentation_v2, segmentation_test, resultSegmentation]
