

# Introduction

Welcome to the Clipboard API! With it you can: get an API key, set and get clipboard contents.




# Authentication

>The Request returns JSON structured like this:

```Response 
{
    "access_token": "",
    "scope": "read write",
    "refresh_token": "",
    "token_type": "Bearer",
    "expires_in": 36000
}
```

Clipboard uses API keys to allow access to the API. Use the following API endpoint to create an account and get a API key.


### HTTP Request

`POST http://example.com/sign_up`

### Body Parameters
Parameter  | Description
---------  | -----------
username  | The username for a new account
password  | The password associated with username


Clipboard expects for the API key to be included in all API requests to the server in a header that looks like the following:

`Authorization: Bearer API_KEY_HERE`

<aside class="warning">
The user name must be unique 
</aside>
<aside class="notice">
You must replace <code>API_KEY_HERE</code> with your personal API key.
</aside>

***

# Clipboard
The Clipboard API is used to create clipboards and retrieve contents. It enables a way to quickily share text and files between multiple devices.
## Set Data
This endpoint creates a new clipboard and sets the contents.

> The setData command returns JSON structured like this:

```Response
{
  "id": "LxF4yGsq",

}
```



### HTTP Request

`POST http://example.com/api/clipboard`

### Body Parameters
#### Text Upload

Parameter   | Description
---------    | ---------
username        | The username 
password        |  The password
text            | The text to be uploaded 


#### File Upload

Parameter  | Description
---------  | -----------
username        | The username 
password        |  The password
file | The file to be uploaded 

<aside class="warning">
Files are limited to <code>1 MB</code> in size.
</aside>

<aside class="notice">
This id is required to retrive the data when executing the getData Request.
</aside>



## Get Data

This endpoint retrieves a specific clipboard's content.


### HTTP Request
> The response for text returns JSON structured like this:

```Response
{
    "data": "text"
}
```

`GET http://example.com/api/clipboard/getData/?session_id=[id]`


<aside class="notice">
The response for file downloands has the<code>Content-Disposition </code> header setup for automatic download.
</aside>
<aside class="warning">
Once a clipboard is retrieved, it is deleted.
</aside>


### URL Parameters

Parameter | Description
--------- | -----------
id | The ID of the clipboard data to retrieve

### Body Parameters

Parameter   | Description
---------    | ---------
username        | The username 
password        |  The password


## Get Metadata
This endpoint retrieves a specific clipboard media's metadata.

> The response for text returns JSON structured like this:

```Response
{
    "entry": {
        "session_id": "LfK6nnSq",
        "creation_time": "2018-04-15T22:26:29.227258Z"
    },
    "media_type": "Text"
}
```

> The response for a file returns JSON structured like this:

```Response

{
    "entry": {
        "session_id": "x2ORXMPE",
        "creation_time": "2018-04-15T23:08:51.932987Z"
    },
    "FileMetaData": {
        "file_name": "10677856_7r6NaRe.jpg",
        "file_length": 3,
        "file_type": "image/jpeg"
    },
    "media_type": "File"
}
```




### HTTP Request

`GET http://example.com/api/clipboard/getMetadata/?session_id=[id]`

#### URL Parameters

Parameter | Description
--------- | -----------
ID | The ID of the clipboard to retrieve

#### Body Parameters
Parameter   | Description
---------    | ---------
username        | The username 
password        |  The password



