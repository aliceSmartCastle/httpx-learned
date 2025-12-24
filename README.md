# QuickStart HTTPX module
  ## Step 1 : install httpx module
### In the Ubuntu bash install

``` bash
 pip install httpx[http2] 
---additional http2 support---
```
#### in windows11 PowerShell
``` powershell
pip install httpx[http2]
```
***step one finish*** 
***
##  Step 2 : Passing Parameters in URLS
 import need moules
``` python
#impor need moudles
from httpx import Response, URL,get,post,put,head,delete,options
from enum import Enum, auto
from typing import Literal
```
__create__ the http response Enum class
``` python
class requestMethod(Enum):
    get = auto()
    post = auto()
    put = auto()
    delete = auto()
    head = auto()
    options = auto()
 ```
__enter__ the main function
``` python
def ResponseUrlState(url_link: str = '', method: str = 'get', wayData: dict = None, getParam: dict = None,
                     getterWay: Literal['params', 'params_url', 'normal_url'] = '', headers: dict = None,
                     postFile: Any = None, postJson: Any = None) -> URL | Response:
   ```     

__check__ the method is valid httpx request  
__default__ use the url_link address or customer url_link
``` python
  responseMethodList = [request.name for request in requestMethod]

    if method not in responseMethodList:
        raise ValueError(f"method {method} is not in {responseMethodList}")

    if url_link == '':
        url_link = 'https://httpbin.org/'
     
``` 
__create__ the http response dictionary  
__match__ different httpx passing  parameters  of functions
``` python
    # all test call this function   
    # print(ResponseUrlState(method=requestMethod.requestEnum.name,getterWay='params')
    response_param = {requestMethod.get.name: get(url_link + 'get', params=getParam, headers=headers), #200 OK
                      requestMethod.post.name: post(url_link + 'post', data=wayData, files=postFile, json=postJson), #200 OK
                      requestMethod.put.name: put(url_link + 'put', data=wayData), # 200 OK
                      requestMethod.delete.name: delete(url_link + 'delete'), # 200 OK
                      requestMethod.head.name: head(url_link + 'get'),       # 200 OK
                      requestMethod.options.name: options(url_link + 'get') #200 OK
                      }

``` 
__build__ the not parameters  of http response dictionary
``` python
    # all test call this function   
    # print(ResponseUrlState(method=requestMethod.requestEnum.name)
    request_normal = {requestMethod.get.name: get(url_link),  # 200 OK
                      requestMethod.post.name: post(url_link), #405 Method Not Allowed
                      requestMethod.put.name: put(url_link),    #405 Method Not Allowed
                      requestMethod.delete.name: delete(url_link), # 405 Method Not Allowed
                      requestMethod.head.name: head(url_link),     #  200 OK
                      requestMethod.options.name: options(url_link) #  200 OK
                      }
                      

``` 
__Getter__ two method Response
``` python
    urlHttp = response_param.get(method)
    normalHttp = request_normal.get(method)
```
__passing__ the getterWay to return different response
``` python
    match getterWay:
        case 'params':
            return urlHttp
        case 'params_url':
            param_url = urlHttp.url
            return param_url
        case 'normal_url':
            normal_get = normalHttp.url
            return normal_get
        case '' | _:
            return request_normal.get(method)
``` 
__tell__ you how to use this function
``` python
   print(ResponseUrlState(method=requestMethod.get.name, getParam={'key1': 'value1', 'key2': ['subvalue', 'sub1value']}
                           , getterWay='params_url'))
```
__on__ the bash input result  
__sure__ you have the QuickStart.py file in the directory  
__test__ the first function input
``` bash
echo "https://httpbin.org/get?key1=value1&key2=subvalue&key2=sub1value"
``` 
__call__ this function again,but argument is not same of first
``` python
 print(ResponseUrlState(method=requestMethod.post.name
                           , getterWay='normal_url'))
```
__bash__ input result
``` bash
echo "https://httpbin.org/"
``` 
__finish__ function test
``` python
    print(ResponseUrlState(method=requestMethod.get.name,getterWay='params'
                           ))
```
__bash__ input result

``` bash
echo "<Response [200 OK]>"
``` 
**_step 2  two finish_**
*** 
## Step 3 :  Response Content
__require__ new function  
__write__ to your watch
``` python
def url_Content(url_link: str = '', needContent: Literal['text', 'change_encoding', 'content', 'post'] = '',
                new_encoding: str = '', post_dict: dict = None,
                post_files: Any = None, post_json: Any = None,
                postContent: bytes = None, originHidden: bool = True,urlHidden:bool =True,headersHidden:bool =True) -> None | str | JSONDecodeError | bytes | Any:
    match needContent:
        case 'text':  #get the text of the response
            return ResponseUrlState(url_link=url_link).text
        case 'post':  #get the post *form* of the response

            postResponse = ResponseUrlState(url_link=url_link, method=requestMethod.post.name, wayData=post_dict,
                                            getterWay="params", postFile=post_files, postJson=post_json,
                                            post_content=postContent).text

            if 'html' not in postResponse:

                parse_request = {'arg': json.loads(postResponse).get('arg'),
                                 'data': json.loads(postResponse).get('data'),
                                 'files': json.loads(postResponse).get('files'),
                                 'form': json.loads(postResponse).get('form'),
                                 'json': json.loads(postResponse).get('json'),
                                 'origin': json.loads(postResponse).get('origin'),
                                 'url': json.loads(postResponse).get('url'),
                                 'headers': json.loads(postResponse).get('headers'),
                                 }


                def valid_keyCheck(datas: dict = None):
                    if originHidden:
                        datas.pop('origin')
                    if urlHidden:
                        datas.pop('url')
                    if headersHidden:
                        datas.pop('headers')
                    request_it = {}
                    for i, v in datas.items():
                        if (v == {}) or (v is None) or (v == ''):
                            ...
                        else:
                         request_it.update({i:v})
                    return request_it

                pretty_dict = valid_keyCheck(parse_request)
                return pretty_dict

            else:
                return "post request file is not json"

       case 'content':  #get the content of the response
            return ResponseUrlState(url_link=url_link).content
       case 'change_encoding':  #change the encoding of the response
            ResponseUrlState(url_link=url_link).encoding = new_encoding
            if new_encoding is not None:
                return new_encoding
            else:
                return 'encoding  changed failed'
        case '' | _:  #default return the response encoding
            return ResponseUrlState(url_link=url_link).encoding


  ```  
__call__ this function
``` python
  print(url_Content(url_link='https://www.python.org/', needContent='change_encoding', new_encoding='utf-8'))
```
``` bash
echo "utf-8"
``` 
__call__ this function  again
``` python
  print(url_Content(url_link='https://www.python.org/', needContent='text'))
```
``` bash
# so many output,i can not waite in there
# this function remain usefully ways,you can find it
```
_**__step 3 finish__**_

***
## Step 4 : Binary Response Content
__construct__ new function  
__additional__ new import
``` python
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from PIL.ImageFile import ImageFile
def binary_data(url_link: str = '') -> ImageFile | UnidentifiedImageError:
    try:
     return Image.open(BytesIO(url_Content(url_link=url_link,needContent='content')))
    except UnidentifiedImageError as e:
        return e
```
__call__ this function
``` python
  print(binary_data())
```
``` bash
 echo 'cannot identify image file <_io.BytesIO object at 0x7c33942e7f60>'
 #getter the picture fail
```
``` python
 print(url_link='https://www.python.org/static/community_logos/python-logo.png')
```
``` bash
echo '<PIL.PngImagePlugin.PngImageFile image mode=RGB size=211x71 at 0x70285643ACF0>'
 #getter the picture success
```
_**__step 4 finish__**_
***
## Step 5 :  JSON Response Content
__construct__ the new JSON function
``` python
   print(fetch_json(url_link='https://dummyjson.com/test'))
```
__it__ will input the info of this bash
``` bash
 echo '{'status': 'ok', 'method': 'GET'}'
 #json api get method test seccess  
 #network connecting not any problem
```
_**__step 5 finish__**_
## Step 6 : Custom Headers
***
__just__ call ResponseUrlState function again           
``` python
      print(ResponseUrlState(method=requestMethod.get.name,headers={"cookie":"best food"}))
```
__it__ input the result

``` bash
 echo '<Response [200 OK]>'
 #if headers argument is valid
 #else raise some unknow error
```
_**__step 6 finish__**_
***
## Step 7 :  Sending Form Encoded Data
__calling__ url_Content
``` python
   print(url_Content(url_link='https://www.python.org/',needContent='post',post_dict={'python':['the python master','who is ?']}))
```
__if__ the url sever accept post form

``` bash
 echo '['the python master','who is ?']'
```
__else__ bash will input the error info

``` bash
 # this output the html info
```
_**__step 7 finish__**_
***
## Step 8 :  Sending Multipart File Uploads
__need__ to crate the open file function
``` python
  def open_file(file_path: str = os.getcwd(), file_name: str = '', file_key: str = '') -> dict[str, bytes]:
    if file_name == '' or file_key == '':
        raise ValueError('file_name not allowed empty')
    with open(os.path.join(file_path, file_name), 'rb+') as f:
        return {file_key: f.read()}

```
__after__ using url_Content function

``` python
     files_here = open_file(file_name='test.txt', file_key='test')
     print(url_Content(url_link='https://www.python.org/',needContent='post', post_files=files_here, post_dict={'name': 'John', 'age': 30}))
```
### note in there
__if__ bash output is JSON file,your send response 
__have__ been properly deal  
__else__ send response have been rejected  
__you__ receive the error file for the url_link  
_**__step 8 finish__**_
***
## Step 9 :  Sending JSON Encoded Data
__construct__ the read JSON function
``` python
def open_json(file_name: str, file_path: str = os.getcwd(), pretty: bool = True) -> str | dict:
    with open(os.path.join(file_path, file_name), 'rb+') as js:
        json_file = json.load(js)
        if pretty:
            return json.dumps(json_file, indent=4, ensure_ascii=False)
        else:
            return json_file
  
```
__following__ is the url_Content function
``` python
    json_send = open_json(file_name='test.json')
    print(url_Content(needContent='post', post_json=json_test))
```
__the__ note here is same to step note  
__detail__ information is seen to [step 8 note ! ](#note-in-there)
_**__step 9 finish__**_
***
## Step 10 : Sending Binary Request Data
  


















  

  


    
    
   
     