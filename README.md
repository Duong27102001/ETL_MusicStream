<div align="center">
  <h1>MUSIC STREAMING DATA PIPELINE</h1>
</div>

## Mô tả dự án
Hệ thống ETL pipeline để xử lý dữ liệu streaming từ nền tảng nghe nhạc, lưu trữ vào postgre data warehouse và quản lý bằng apache airflow.
## NỘI DUNG THỰC HIỆN
- [Mô tả dự án](#Mô-tả-dự-án)
- [Kiến trúc dự án](#Kiến-trúc-dự-án)
- [Tổng quan về bộ dữ liệu](#tổng-quan-về-bộ-dữ-liệu)
- [Thiết kế data warehouse](#Thiết-kế-data-warehouse)
- [Xây dựng data pipeline](#Xây-dựng-data-pipeline)
- [video]
## Kiến trúc dự án
(#../data/image/pipe.PNG)
## Tổng quan về bộ dữ liệu
Bộ dữ liệu gồm 2 thư mục là log_data và song_data lưu trữ các file json. [Dữ liệu được tham khảo từ nguồn Udacity.](https://github.com/san089/Udacity-Data-Engineering-Projects)</br>
### Song data
- Bộ dữ liệu song_data chứa thông tin về các bài hát và nghệ sĩ. </br>
- Record mẫu:
```bash
{"num_songs": 1,"artist_id": "ARD7TVE1187B99BFB1", "artist_latitude": null,"artist_longitude": null,"artist_location": "California - LA","artist_name": "Casual","song_id": "SOMZWCG12A8C13C480", "title": "I Didn't Mean To", "duration": 218.93179, "year": 0}
```
- Thông tin thuộc tính

| Trường             | Kiểu dữ liệu  | Mô tả |
|--------------------|--------------|------------------------------------------------|
| `num_songs`       | Integer      | Số lượng bài hát của nghệ sĩ (thường là 1). |
| `artist_id`       | String       | ID duy nhất của nghệ sĩ trong hệ thống. |
| `artist_latitude` | Float/Null   | Vĩ độ địa lý của nghệ sĩ (nếu có). |
| `artist_longitude`| Float/Null   | Kinh độ địa lý của nghệ sĩ (nếu có). |
| `artist_location` | String       | Địa điểm của nghệ sĩ (có thể không chuẩn hóa). |
| `artist_name`     | String       | Tên nghệ sĩ. |
| `song_id`         | String       | ID duy nhất của bài hát. |
| `title`           | String       | Tiêu đề bài hát. |
| `duration`        | Float        | Thời lượng bài hát (giây). |
| `year`            | Integer      | Năm phát hành (nếu không có thì giá trị là 0). |

### Log data
- Bộ dữ liệu log_data chứa thông tin chi tiết về hành vi của người dùng trên nền tảng phát nhạc trực tuyến. Mỗi bảng ghi trong log phản ánh một hành động cụ thể của người dùng, chẳng hạn như phát bài hát, đăng nhập hoặc chuyển trang.
- Record mẫu:
  ``` bash
  {"artist":"The White Stripes","auth":"Logged In","firstName":"Kate","gender":"F","itemInSession":89,"lastName":"Harrell","length":241.8673,"level":"paid","location":"Lansing-East Lansing, MI","method":"PUT","page":"NextSong","registration":1540472624796.0,"sessionId":293,"song":"My Doorbell (Album Version)","status":200,"ts":1541549126796,"userAgent":"\"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/37.0.2062.94 Safari\/537.36\"","userId":"97"}
  ```
- Thông tin thuộc tính

| Trường          | Kiểu dữ liệu  | Mô tả |
|----------------|--------------|------------------------------------------------|
| `artist`       | String       | Tên nghệ sĩ của bài hát đang phát (có thể null). |
| `auth`         | String       | Trạng thái xác thực của người dùng (`Logged In`, `Logged Out`). |
| `firstName`    | String       | Tên của người dùng. |
| `gender`       | String       | Giới tính của người dùng (`M` hoặc `F`). |
| `itemInSession`| Integer      | Mục số trong phiên phát nhạc hiện tại. |
| `lastName`     | String       | Họ của người dùng. |
| `length`       | Float        | Độ dài bài hát (giây). |
| `level`        | String       | Loại tài khoản (`free` hoặc `paid`). |
| `location`     | String       | Vị trí địa lý của người dùng. |
| `method`       | String       | Phương thức HTTP (`GET`, `POST`, `PUT`). |
| `page`         | String       | Loại hành động người dùng thực hiện (`NextSong`, `Home`, `Logout`, ...). |
| `registration` | Float        | Thời gian đăng ký của người dùng (dạng timestamp). |
| `sessionId`    | Integer      | ID phiên làm việc của người dùng. |
| `song`         | String       | Tên bài hát đang phát (có thể null). |
| `status`       | Integer      | Mã trạng thái HTTP (`200`, `404`, ...). |
| `ts`           | Integer      | Timestamp của hành động. |
| `userAgent`    | String       | Thông tin trình duyệt của người dùng. |
| `userId`       | String       | ID của người dùng (có thể là chuỗi rỗng nếu chưa đăng nhập). |

## Thiết kế data warehouse

## Xây dựng data pipeline


