import logging

logging.basicConfig(
    filename='arena_tickets.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def display_tickets(tickets):
    print("\n--- DANH SÁCH VÉ ---")
    print("Mã Vé | Tên Khách Hàng | Giá Vé | Chỗ Ngồi | Trạng Thái")
    print("-" * 50)
    if not tickets:
        print("Hiện chưa có vé nào trong hệ thống.")
        return

    for t in tickets:
        try:
            status_text = f"{t['status']} [ĐÃ HỦY]" if t['status'] == "Cancelled" else t['status']
            print(f"{t['ticket_id']} | {t['buyer_name']} | {t['price']} | {t['seat']} | {status_text}")
        except KeyError as e:
            print("Lỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.")
            logging.error(f"Missing key while displaying ticket: {e}")
    
    logging.info("User viewed ticket list.")

def book_ticket(tickets):
    ticket_id = input("Nhập mã vé: ")
    for t in tickets:
        if t['ticket_id'] == ticket_id:
            print(f"Lỗi: Mã vé {ticket_id} đã tồn tại.")
            logging.warning(f"Duplicate ticket ID entered: {ticket_id}")
            return

    name = input("Nhập tên khách hàng: ")
    while True:
        try:
            price = float(input("Nhập giá vé: "))
            if price <= 0:
                print("Giá vé phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Giá vé phải là số. Vui lòng nhập lại.")
            logging.warning("Invalid price input while booking ticket")
    
    area = input("Nhập khu vực ghế: ")
    while True:
        try:
            seat_num = int(input("Nhập số ghế: "))
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")
    
    new_ticket = {
        "ticket_id": ticket_id,
        "buyer_name": name,
        "price": price,
        "status": "Booked",
        "seat": (area, seat_num)
    }
    tickets.append(new_ticket)
    print(f"Thành công: Đã đặt vé {ticket_id} cho khách hàng {name}.")
    logging.info(f"Booked new ticket [{ticket_id}] for [{name}]")

def change_seat(tickets):
    t_id = input("Nhập mã vé cần đổi chỗ: ")
    for t in tickets:
        if t['ticket_id'] == t_id:
            new_area = input("Nhập khu vực ghế mới: ")
            while True:
                try:
                    new_num = int(input("Nhập số ghế mới: "))
                    break
                except ValueError:
                    print("Số ghế phải là số nguyên. Vui lòng nhập lại.")
            t['seat'] = (new_area, new_num)
            print(f"Thành công: Đã đổi chỗ vé {t_id} sang {new_area}-{new_num}.")
            logging.info(f"Seat changed for ticket [{t_id}] to [{new_area}-{new_num}]")
            return
    print(f"Không tìm thấy vé mang mã {t_id}.")
    logging.warning(f"Change seat failed - Ticket {t_id} not found")

def cancel_ticket(tickets):
    t_id = input("Nhập mã vé cần hủy: ")
    for t in tickets:
        if t['ticket_id'] == t_id:
            if t['status'] == "Cancelled":
                print(f"Vé {t_id} đã ở trạng thái cancelled trước đó.")
            else:
                t['status'] = "Cancelled"
                print(f"Thành công: Vé {t_id} đã được hủy.")
                logging.warning(f"Ticket [{t_id}] has been cancelled.")
            return
    print(f"Không tìm thấy vé mang mã {t_id}.")
    logging.warning(f"Cancel ticket failed - Ticket {t_id} not found")

def calculate_revenue(tickets):
    total = 0.0
    for t in tickets:
        try:
            if t['status'] == "Booked":
                total += t['price']
        except KeyError:
            print("Lỗi: Một vé đang bị thiếu dữ liệu doanh thu.")
            logging.error("Missing key while calculating revenue: 'price'")
            return 0.0
    return total

def show_report(tickets):
    booked = [t for t in tickets if t['status'] == "Booked"]
    cancelled = [t for t in tickets if t['status'] == "Cancelled"]
    print(f"Tổng số vé đã đặt: {len(booked)}")
    print(f"Tổng số vé đã hủy: {len(cancelled)}")
    print(f"Tổng doanh thu hợp lệ: {calculate_revenue(tickets)}")
    logging.info(f"Revenue report generated. Total: {calculate_revenue(tickets)}")

if __name__ == "__main__":
    ticket_db = [
        {"ticket_id": "T01", "buyer_name": "Nguyen Van A", "price": 500.0, "status": "Booked", "seat": ("A", 1)},
        {"ticket_id": "T02", "buyer_name": "Tran Thi B", "price": 300.0, "status": "Cancelled", "seat": ("B", 5)},
        {"ticket_id": "T03", "buyer_name": "Le Van C", "price": 500.0, "status": "Booked", "seat": ("A", 2)}
    ]
    
    while True:
        choice = input("""
--- HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ---
1. Xem danh sách vé đã bán
2. Đặt vé mới
3. Đổi chỗ ngồi (Cập nhật vé)
4. Hủy vé
5. Báo cáo doanh thu
6. Thoát chương trình
========================================
Chọn chức năng (1-6): """)
        
        if choice == '1': display_tickets(ticket_db)
        elif choice == '2': book_ticket(ticket_db)
        elif choice == '3': change_seat(ticket_db)
        elif choice == '4': cancel_ticket(ticket_db)
        elif choice == '5': show_report(ticket_db)
        elif choice == '6':
            print("Cảm ơn bạn đã sử dụng hệ thống quản lý vé Rikkei Esports.")
            logging.info("Ticket management system closed.")
            break
        else:
            print("Lựa chọn không hợp lệ!")