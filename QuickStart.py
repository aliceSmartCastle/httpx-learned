import json.decoder
import os
from json import JSONDecodeError
from pprint import pprint
from typing import Literal, Any
from enum import Enum, auto
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from PIL.ImageFile import ImageFile
from httpx import Response, URL, get, post, put, head, delete, options, HTTPStatusError, codes, stream, Cookies
from UserAgentGet import User_Agent


class requestMethod(Enum):
    get = auto()
    post = auto()
    put = auto()
    delete = auto()
    head = auto()
    options = auto()
    cookies = auto()


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
                     extra_address: str = '', add_cookies: dict | Cookies = None, Redirection: bool = False,
                     set_timeout: float = 0.4,get_auth:Any=None) -> URL | Response:
    """
     :param get_auth:    the auth argument of response get
     :param set_timeout:   the timeout argument of response get
     :param Redirection:  the Redirection argument of response get
     :param add_cookies: the cookies argument of response get
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
    response_param = {
        requestMethod.get.name: get(url_link + 'get', params=getParam, headers=headers, timeout=set_timeout),  #200 OK
        requestMethod.cookies.name: get(url_link + 'cookies', cookies=add_cookies),
        requestMethod.post.name: post(url_link + 'post', data=wayData, files=postFile, json=postJson,
                                      content=post_content),
        requestMethod.put.name: put(url_link + 'put', data=wayData),  # 200 OK
        requestMethod.delete.name: delete(url_link + 'delete'),  # 200 OK
        requestMethod.head.name: head(url_link + 'get'),  # 200 OK
        requestMethod.options.name: options(url_link + 'get')  #200 OK
        }
    # all test call this function
    # print(ResponseUrlState(method=requestMethod.requestEnum.name)
    request_normal = {
        requestMethod.get.name: get(url_link + extra_address, follow_redirects=Redirection, timeout=set_timeout,auth=get_auth),
        # 200 OK
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
                postContent: bytes = None, originHidden: bool = True, urlHidden: bool = True,
                headersHidden: bool = True) -> None | str | JSONDecodeError | bytes | Any:
    match needContent:
        case 'text':  #get the text of the response
            return ResponseUrlState(url_link=url_link).text
        case 'post':  #get the post *form* of the response

            information_Accept = ResponseUrlState(url_link=url_link, method=requestMethod.post.name, wayData=post_dict,
                                                  getterWay="params", postFile=post_files, postJson=post_json,
                                                  post_content=postContent)

            post_type = information_Accept.headers.get('content-type')

            acceptType = ['application/json']

            if post_type in acceptType:

                json_format_post = information_Accept.json()

                parse_request = {'arg': json_format_post.get('arg'),
                                 'data': json_format_post.get('data'),
                                 'files': json_format_post.get('files'),
                                 'form': json_format_post.get('form'),
                                 'json': json_format_post.get('json'),
                                 'origin': json_format_post.get('origin'),
                                 'url': information_Accept.url,
                                 'headers': information_Accept.headers,

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
                            request_it.update({i: v})
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


def status_code(url_link: str = '', extra_address: str = '') -> None | HTTPStatusError | Literal[codes.OK]:
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


def http_headers(url_link: str = '', content_type: bool = False):
    headInfo = ResponseUrlState(url_link=url_link, method=requestMethod.get.name)
    contentType = headInfo.headers.get('content-type')
    if content_type:
        return contentType
    else:
        return headInfo.headers


def stream_loop(url_link: str = '', stream_type: Literal['bytes', 'text', 'lines', 'raw', 'content-length'] = 'text',
                setting_length: int = 1000) -> str | list[Any]:
    stream_list = []

    if url_link == '':
        url_link = 'https://httpbin.org/'
    upper_get = requestMethod.get.name.upper()
    with stream(method=upper_get, url=url_link) as st:
        match stream_type:
            case 'bytes':
                for data in st.iter_bytes():
                    stream_list.append(data)
                return stream_list
            case 'text':
                for text in st.iter_text():
                    stream_list.append(text)
                return stream_list
            case 'lines':
                for line in st.iter_lines():
                    stream_list.append(line)
                return stream_list
            case 'raw':
                for raw in st.iter_raw():
                    stream_list.append(raw)
                return stream_list
            case 'content-length':
                if int(st.headers.get('content-length')) < setting_length:
                    stream_list.append(st.read())
                    return stream_list
                else:
                    return "setting length is not enough"

            case '' | _:
                return "unknown stream type"


def http_cookie(url_link: str = '', add_cookie: dict = None) -> dict:
    if url_link == '':
        url_link = 'https://httpbin.org/'
    cookie_fail = None
    try:
        cookie_info = ResponseUrlState(url_link=url_link, method=requestMethod.cookies.name, add_cookies=add_cookie,
                                       getterWay='params')
        cookie_fail = cookie_info
        cookie_success = cookie_info.json()

    except (JSONDecodeError, UnicodeDecodeError):
        return {cookie_fail.status_code: cookie_fail.text}

    return cookie_success


def history_watch(url_link: str = '', redirects: bool = True) -> dict:
    url_history = ResponseUrlState(url_link=url_link, method=requestMethod.get.name, Redirection=redirects)
    first_status = url_history.status_code
    next_status = url_history.next_request
    url_history = url_history.history
    return {'status': first_status, 'next_status': next_status, 'history': url_history}
def authentication_http(url_link: str = '', auth: tuple[str, str] = None) -> str:
    if url_link == '':
        url_link ='https://practicetestautomation.com/practice-test-login/'
    login_information = ResponseUrlState(url_link=url_link, method=requestMethod.get.name, get_auth=auth,set_timeout=1)
    if login_information.status_code == codes.OK:
        return "login success"
    else:
        return "login fail"


if __name__ == '__main__':
    my_UA = User_Agent()
    this_cookies = Cookies()
    # print(ResponseUrlState(method=requestMethod.get.name,headers={"cookie":"best food"},
    # url_link='https://www.python.org/'))
    files_here = open_file(file_name='pyproject.toml', file_key='upload-files')
    json_test = open_json(file_name="hello.json", pretty=False)
    #print(http_cookie(url_link='https://http.cat/',add_cookie={"American": "The USA", "English": "UK"}))
    #print(history_watch(url_link='https://dummyjson.com/', redirects=True))
    pprint(authentication_http(auth=(' student','Password1238')))

    #print(http_headers(url_link='https://www.python.org/'))

    #print(url_Content(needContent='post', postContent=hello world!', headersHidden=False))
#print(binary_data(url_link='https://www.python.org/static/community_logos/python-logo.png'))
#print(fetch_json(url_link='https://dummyjson.com/test'))
