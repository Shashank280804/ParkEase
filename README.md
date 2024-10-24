
# Overview

ParkEase is an advanced video analytics solution that automates vehicle plate recognition and vacant parking slot detection using cutting-edge AI techniques. The system integrates YOLOv8 for real-time object detection and OpenCV for video processing. Flask is used to create a web interface that allows users to view the live feed of detected plates and parking slots, and it provides a detailed dashboard to track vehicle statuses.

# Tech Stack

**YOLOv8:** For object detection of vehicle plates and parking slots.
**OpenCV:** For video capture and frame processing.   
**Flask:** Backend web framework for serving video streams and managing user interactions.  
**EasyOCR:** For optical character recognition (OCR) to extract text from vehicle plates.  
**HTML,CSS,Bootstrap:** For creating a responsive and user-friendly interface.

# Features
## Plate Recognition System
- Vehicle Plate Recognition: Detects and recognizes vehicle plates using YOLOv8 and OpenCV.
- Vehicle Status Tracking: Tracks the state of vehicles (in/out) and displays it in a user-friendly table.
- User Authentication: Allows users to log in or sign up to access vehicle status information.
- Responsive Dashboard: Displays vehicle data in a table format, including date, time, state (in/out), and plate number.

## Slot Detection System
- Vacant Slot Detection: Detects vacant parking slots in real-time using YOLOv8.
- Live Feed: Shows a live video stream of detected vacant slots in the parking area.
- Real-Time Processing: Processes frames from a connected camera - in real-time to continuously detect changes in slot occupancy.


## API Reference

#### Get Parking Status Dashboard
```http
    GET /dashboard
```

| Parameter | Type     | Description                  |
| :-------- | :------- | :-------------------------   |
| `user_id` | `string` | **Required**. Id of the user |

#### Get Profile

```http
    GET /profile
```
| Parameter | Type     | Description                  |
| :-------- | :------- | :-------------------------   |
| `user_id` | `string` | **Required**. Id of the user |

#### Edit Profile

```http
   PUT /edit-profile
```
| Parameter           | Type     | Description                                   |
| :--------           | :------- | :--------------------------------             |
| `user_id`           | `string` | **Required**. Id of the user                  |
| `profile_data`      | `object` | **Required**. Data to update the profile      |

#### Register Vehicle
```http
    POST /vehicle-registration
```
| Parameter      | Type     | Description                                |
| :--------      | :------- | :-------------------------                 |
| `vehicle_data` | `object` | **Required**. Vehicle registration details |


#### Slot Detection
```http
    GET /video_feed
```
| Parameter | Type     | Description                  |
| :-------- | :------- | :-------------------------   |
| `user_id` | `string` | **Required**. real-time video of parking slot detection. |


## Documentation

[Documentation](https://linktodocumentation)


## Installation

- Clone the repository
```
git clone https://github.com/Shashank280804/ParkEase.git
```
- Navigate to the project directory
```
cd my-project
```  
- Install the necessary Python dependencies    
```
pip install Flask OpenCV-python easyocr ultralytics
```
- Run the Flask application:
```
python main.py
```

## Screenshots

![App Screenshot](https://drive.google.com/file/d/12LkYXWce5H97-k9gIOnrnHOLMOM4ID15/view?usp=sharing, https://drive.google.com/file/d/12xtO-Iu0KtIpgC38TIStJAuvpIrIWcW7/view?usp=sharing, https://drive.google.com/file/d/14Mitj60VWQ-JP5uY6j2i1qX0fqd90s4X/view?usp=sharing, https://drive.google.com/file/d/1HBdypAapkNIahnR1JsXd0PjDvmFNXXKr/view?usp=sharing, https://drive.google.com/file/d/1OUqBuc3vKg248NLG1yvb71uhpd7Ousku/view?usp=sharing, https://drive.google.com/file/d/1QNvQGCwkkw65SaxdeuwSOEDgYd0knJfT/view?usp=sharing, https://drive.google.com/file/d/1ZXC9zkIsjoG7Ub_vfBSZThQK5PghRiLT/view?usp=sharing, https://drive.google.com/file/d/1ZvXuqGqOwuXvkmlj9YADAZnZWTDIpHI8/view?usp=sharing, https://drive.google.com/file/d/1eHqPHlTLYqp-89g_I2i9xlg8w1LEpilC/view?usp=sharing, https://drive.google.com/file/d/1nQL3bCmGXrt0Ov5c6lipU-L1sSET6LsW/view?usp=sharing, https://drive.google.com/file/d/1ws4asZyObS8ecfqVfvmQ2RBIwLZFgNxY/view?usp=sharing)



# Usage
#### Vehicle Registration:
Users can register their vehicles through the provided registration interface. The system will store vehicle information, including the plate number, for future recognition.  
#### Plate Recognition:
The system captures video frames using OpenCV, and YOLOv8 is used to detect vehicle plates. EasyOCR then extracts the text from the detected plate for further processing.
#### Slot Detection:
YOLOv8 is also utilized to detect vacant parking slots in real-time by analyzing the video feed of the parking area.
#### Dashboard:
Users can log in to the system and view the status of their vehicles on the dashboard. The dashboard provides:

