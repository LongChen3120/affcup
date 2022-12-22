__________________________ config __________________________

## type sport:
+ 1: đối kháng: gồm 2 đội, 2 người, 2 team,...; data gồm lịch, bxh
+ 2: hỗn hợp: nhiều bên tham gia thi đấu; data gồm lịch, kết quả của các bên

## type crawl:
+ 0: không crawl, lấy luôn thông tin từ config
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
__________________________ database __________________________
## type:
+ 2: lịch thi đấu
+ 5: bảng xếp hạng
+ 7: môn thể thao
+ 8: giải đấu
+ 9: kết quả