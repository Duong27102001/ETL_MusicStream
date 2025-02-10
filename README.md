<div align="center">
  <h1>MUSIC STREAMING ETL</h1>
</div>

## Overview
Dự án này cung cấp một giải pháp toàn diện về data pipeline để extract, transformation, load (ETTL) bộ dữ liệu về music stream sang data warehouse. Quá trình này tận dụng sự kết hợp của các công cụ bao gồm apache airflow, PostgreSQL và python.
## Table of content
- [overview](#overview)
- [Architecture]
- [Prerequisites]
- [System Setup]
- [video]
## Tổng quan về bộ dữ liệu
Bộ dữ liệu gồm 2 thư mục là log_data và song_data lưu trữ các file json.[Dữ liệu được tham khảo từ nguồn Udacity](https://github.com/san089/Udacity-Data-Engineering-Projects)</br>
### Song data
Bộ dữ liệu song_data chứa thông tin về các bài hát và nghệ sĩ. </br>
Record mẫu:
```bash
{"num_songs": 1,"artist_id": "ARD7TVE1187B99BFB1", "artist_latitude": null,"artist_longitude": null,"artist_location": "California - LA","artist_name": "Casual","song_id": "SOMZWCG12A8C13C480", "title": "I Didn't Mean To", "duration": 218.93179, "year": 0}
```
Thông tin thuộc tính

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

