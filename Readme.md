__________________________ config __________________________

## type crawl:
+ 1: request
+ 2: selenium

## type response:
+ 1: html
+ 2: json

## type find result:
+ 1: list elements
+ 2: list string
+ 3: list int
+ 4: string
+ 5: int
+ 6: datetime
+ 7: timestamp
<!-- + 3: list string -->


## type find:
+ 1: find by xpath
+ 2: find by xpath + regex


## type output:
+ 1: list elements
+ 2: list string
+ 3: list int
+ 4: string
+ 5: int
+ 6: datetime: 
+ 7: true/false


## type action:
+ 1: click
+ 2: get attributes
+ 3: scroll down
+ 4: send keys
+ 5: crawl detail
+ 6: enter

## type result:
+ 1: string
+ 2: list string
+ 3: list element

## auto add key:
+ 0: False
+ 1: True


## 2 kiểu tổ chức file config: config dùng cho crawl bằng requests(config.json) và config dùng cho crawl bằng selenium(config_detail.json; có các step để định hình quá trình crawl)
key "data" để đánh dấu bắt đầu đệ quy đọc phần config bên trong, tên các key con trong key "data" được tái sử dụng làm key cho object output luôn.

__________________________ database __________________________
## type:
+ 2: lịch thi đấu
+ 5: bảng xếp hạng



# INFO
## thuật toán chính:
+ 1: bắt đầu
+ 2: chạy main_crawl.py
+ 3: quét lịch tiếp theo, thêm vào job store
+ 4: chạy job trong jobs store, mỗi job gồm 2 việc thành phần: cập nhật trận đấu hiện tại và cập nhật lịch mới, bảng xếp hạng mới
+ 5: quay về bước 3

## thuật toán crawl detail:
+ 1: bắt đầu
+ 2: chạy hàm crawl2
+ 3: hàm crawl2 lặp lại crawl chi tiết một trận đấu, thời gian giữa các lần crawl là 1 phút, lặp tối đa 200 lần.

## thuật toán crawl lịch, bảng xếp hạng:
+ 1: bắt đầu
+ 2: lặp qua các config
+ 3: tại mỗi config sẽ check key "end_league"
+ 4: send request 
+ 5: bóc tách
+ 6: lưu

## api:
curl --location --request POST 'http://192.168.19.187:8000/info' \
--header 'Content-Type: application/json' \
--data-raw '{
    "topic":"affcup",
    "type":2,
    "team_0":"việt nam",
    "team_1":"lào",
    "id":"",
    "time(chính xác: yyyy-mm-dd)":"",
    "time(trước ngày: yyyy-mm-dd)":"",
    "time(sau ngày: yyyy-mm-dd)":""
}'


