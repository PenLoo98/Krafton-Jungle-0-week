This program need to private data for using Google API

Google Cloud 서비스 계정의 비공개 키의 형식은 JSON이다. 
이 비공개키

1. create "privateData.json" file
2. input 3 keys into the "privateData.json"

// privateData.json
{
    "json_file_path" : "Google Cloud 계정의 비밀키인 JSON의 저장 경로",
    "spreadsheet_url" : "구글 스프레드 시트의 공유가 허용하는 URL",
    "file_path" : "추출한 데이터인 JSON의 저장할 경로"
}