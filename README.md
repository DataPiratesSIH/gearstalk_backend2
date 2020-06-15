## gearStalk- backend-2

### Metadata format
```js
// For a video of 1 second
{
    "_id": "ObjectId",
    "video_id": "video_id",
    "metadata": [
        {
            "timestamp": 0, // 0 seconds
            "persons": [
                {
                    "box": [x,y,w,h],
                    "labels": [], // Length of labels and colors should be same
                    "colors": [_,_] // top 2 colors in the image,
                },
                {
                    "box": [x,y,w,h],
                    "labels": [],
                    "colors": [_,_] // top 2 colors in the image,
                }
            ]
        },
            {
            "timestamp": 0.5, // 0.5 seconds
            "persons": [
                {
                    "box": [x,y,w,h],
                    "labels": [], // Length of labels and colors should be same
                    "colors": [_,_] // top 2 colors in the image,
                },
                {
                    "box": [x,y,w,h],
                    "labels": [],
                    "colors": [_,_] // top 2 colors in the image,
                }
            ]
        },
            {
            "timestamp": 1, // 1 second
            "persons": [
                {
                    "box": [x,y,w,h],
                    "labels": [], // Length of labels and colors should be same
                    "colors": [_,_] // top 2 colors in the image,
                },
                {
                    "box": [x,y,w,h],
                    "labels": [],
                    "colors": [_,_] // top 2 colors in the image,
                }
            ]
        }
    ]
}
```