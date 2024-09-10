
## Giải thích code base
- `main.py`: File chính để chạy thử nghiệm. Người dùng sẽ run file này để thu được kết quả thử nghiệm.
- `Parameters.py`: File để lưu các tham số của system model, bao gồm:
    - Số access server
    - Số level-2 server
    - Số level-3 server
    - Thời gian chạy thử nghiệm
    - Độ dài time interval
    - Computing resourse
    - Bandwidth
    - ...
    - Và một số thông tin bổ trợ khác được dùng rải rác trong code base. VD: Địa chỉ folder lưu file kết quả.
- `Setting.py`: File dùng để lưu các bộ CT type sẽ được dùng trong từng thử nghiệm
- `AccessServer.py`: File lập trình thực thể access server
- `HighLevelServer.py`: File lập trình thực thể high-level server
- `Initializer.py`: File lập trình ra class Initializer có vai trò chạy các hàm khởi tạo tham số cho hệ thống để chạy thử nghiệm 
- `Dijkstra.py`: Lập trình thuật toán Dijkstra được dùng để chạy ODO offloading.
- Các file `perform...OffloadingScheme.py`: Chứa các hàm tính toán kịch bản offloading cho các CT task trong hệ thống thử nghiệm.
- `DelayEvaluator.py`: File chạy các đánh giá thử nghiệm, có nhiệm vụ: 
    - gọi đến các hàm offloading
    - lưu data
- `Utils`: Folder lưu các hàm công cụ giúp sinh data, biểu diễn trực quan data (bằng python)
- `exp1_system_load_visualization.m`: File biểu diễn trực quan data bằng (bằng matlab). Tương tự, có các file cho experiment 2,3,4,5


