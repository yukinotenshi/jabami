# Jabami

HLS Video Transcoder Microservice

### Specification
1. This project is using Python 3
2. Built on top of Flask with Peewee ORM
3. Currently uses sqlite for simplicity


### Installation

1. Move to this project directory and do the usual
    
    ```pip install -r requirements.txt```

2. Run ```setup.py```

    ```python3 setup.py```

    If you receive an input like
    
    ```FFMPEG not installed! Please install ffmpeg and add it to PATH```
    
    Then please install FFMPEG from it's official site
    
    https://ffmpeg.org


### Run

1. Simply run ```python app.py```

### Endpoints

1. Upload video

    ```[POST] http://host/video```
   
   ```files = ['video_file']```
   
   POST with ```multipart/form-data```
   
2. Get video status

    ```[GET] http://host/video/<video_id>```
3. Add video to transcoder queue

    ```[POST] http://host/queue```

    ```json = {"video_id" : <int>, "qualities" : ["360p", "480p", "720p", "1080p"]}```

4. Get HLS stream manifest

    ```[GET] http://host/static/<video_filename_without_ext>/master.m3u8```

### Endpoints return [1-3]

Success :

```{"filename":<filename>, "id":<int>, "in_queue":<bool>, "is_processed":<bool>, "video_qualities":<List[int]>, "created_at":<DATE>, "updated_at":<DATE>}```

Fail :

```{"code" : <int>, "error" : <str>}```


### Deployment

To be defined