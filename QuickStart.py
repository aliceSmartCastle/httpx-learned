import json.decoder
import os
from json import JSONDecodeError
from typing import Literal, Any
from enum import Enum, auto
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from PIL.ImageFile import ImageFile
from httpx import Response, URL, get, post, put, head, delete, options, HTTPStatusError, codes
from UserAgentGet import User_Agent


class requestMethod(Enum):
    get = auto()
    post = auto()
    put = auto()
    delete = auto()
    head = auto()
    options = auto()
    status = auto


def open_file(file_path: str = os.getcwd(), file_name: str = '', file_key: str = '') -> dict[str, bytes]:
    if file_name == '' or file_key == '':
        raise ValueError('file_name not allowed empty')
    with open(os.path.join(file_path, file_name), 'rb+') as f:
        return {file_key: f.read()}


def open_json(file_name: str, file_path: str = os.getcwd(), pretty: bool = True) -> str | dict:
    with open(os.path.join(file_path, file_name), 'rb+') as js:
        json_file = json.load(js)
        if pretty:
            return json.dumps(json_file, indent=4, ensure_ascii=False)
        else:
            return json_file


def ResponseUrlState(url_link: str = '', method: str = 'get', wayData: dict = None, getParam: dict = None,
                     getterWay: Literal['params', 'params_url', 'normal_url'] = '', headers: dict = None,
                     postFile: Any = None, postJson: Any = None, post_content: bytes = '',
                     extra_address: str = '') -> URL | Response:
    """
     :param post_content: the content argument of response post
     :param extra_address: additional the address to the request get
     :param postJson:  the JSON argument of response post
     :param postFile: the file argument of response post
     :param headers: the header argument of response get
     :param method: the different http response type
     :param getParam: given the http 'get' argument of response
     :param url_link: if it's empty
                      it will use httpbin.org,else it will use the url_link
     :param wayData:  wayData  given the http 'post' and 'put' argument of response
     :param getterWay: given the different way to get the response type


     """

    responseMethodList = [request.name for request in requestMethod]

    if method not in responseMethodList:
        raise ValueError(f"method {method} is not in {responseMethodList}")

    if url_link == '':
        url_link = 'https://httpbin.org/'

    # all test call this function
    # print(ResponseUrlState(method=requestMethod.requestEnum.name,getterWay='params')
    response_param = {requestMethod.get.name: get(url_link + 'get', params=getParam, headers=headers),  #200 OK

                      requestMethod.post.name: post(url_link + 'post', data=wayData, files=postFile, json=postJson,
                                                    content=post_content),
                      # 200 OK
                      requestMethod.put.name: put(url_link + 'put', data=wayData),  # 200 OK
                      requestMethod.delete.name: delete(url_link + 'delete'),  # 200 OK
                      requestMethod.head.name: head(url_link + 'get'),  # 200 OK
                      requestMethod.options.name: options(url_link + 'get')  #200 OK
                      }
    # all test call this function
    # print(ResponseUrlState(method=requestMethod.requestEnum.name)
    request_normal = {requestMethod.get.name: get(url_link + extra_address),  # 200 OK
                      requestMethod.post.name: post(url_link),  #405 Method Not Allowed
                      requestMethod.put.name: put(url_link),  #405 Method Not Allowed
                      requestMethod.delete.name: delete(url_link),  # 405 Method Not Allowed
                      requestMethod.head.name: head(url_link),  #  200 OK
                      requestMethod.options.name: options(url_link)  #  200 OK
                      }

    urlHttp = response_param.get(method)
    normalHttp = request_normal.get(method)

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
            return normalHttp


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
            native_encodings = ResponseUrlState(url_link=url_link).encoding

            if native_encodings is not None:
                native_encodings = new_encoding
                return native_encodings
            else:
                return 'encoding  changed failed'
        case '' | _:  #default return the response encoding
            return ResponseUrlState(url_link=url_link).encoding


def binary_data(url_link: str = '') -> ImageFile | UnidentifiedImageError:
    try:
        return Image.open(BytesIO(url_Content(url_link=url_link, needContent='content')))
    except UnidentifiedImageError as e:
        return e


def fetch_json(url_link: str = '') -> JSONDecodeError | Any:
    try:
        return ResponseUrlState(url_link=url_link).json()
    except json.decoder.JSONDecodeError as e:
        return e


def status_code(url_link: str = '', extra_address: str = '') -> None | HTTPStatusError | int:
    response_apply = ResponseUrlState(url_link=url_link, method=requestMethod.get.name, extra_address=extra_address)
    response_status = response_apply.status_code
    if response_status > 300:
        try:
            response_apply.raise_for_status()
        except HTTPStatusError as err:
            return err

    else:
        assert (response_status == codes.OK)
        return response_status


if __name__ == '__main__':
    my_UA = User_Agent()
    # print(ResponseUrlState(method=requestMethod.get.name,headers={"cookie":"best food"},url_link='https://www.python.org/'))
    files_here = open_file(file_name='pyproject.toml', file_key='upload-files')
    json_test = open_json(file_name="hello.json", pretty=False)
    #print(status_code(url_link='https://www.python.org/', extra_address='jobs/helps'))

    print(url_Content(needContent='post',postContent=b'welcome to python'))
#print(binary_data(url_link='https://www.python.org/static/community_logos/python-logo.png'))
#print(fetch_json(url_link='https://dummyjson.com/test'))
