import re

class TreeNode:
    def __init__(self, name, data=None):
        """
        Khởi tạo một nút trong cây.

        Tham số:
        - name: Tên của nút (string), ví dụ: "Lỗi chạy quá tốc độ".
        - data: Dữ liệu liên quan đến nút (dictionary). Mặc định là None.
        """
        self.name = name        # Tên nút
        self.data = data        # Dữ liệu ở tầng lá (mucPhat, phatBoSung, canCuPhapLy)
        self.children = {}      # Các nút con của nút hiện tại

class ViolationTree:
    def __init__(self):
        """
        Khởi tạo cây vi phạm với một nút gốc.
        """
        self.root = TreeNode("root")
    
    def add_violation(self, loiViPham, phuongTien, chiTietLoi, mucPhat, phatBoSung, canCuPhapLy):
        """
        Thêm một lỗi vi phạm vào cây.

        Tham số:
        - loiViPham: Tên lỗi vi phạm (string), ví dụ: "Lỗi chạy quá tốc độ".
        - phuongTien: Phương tiện vi phạm (string), ví dụ: "Ô tô", "Xe máy".
        - chiTietLoi: Chi tiết lỗi vi phạm (string), ví dụ: "Vượt quá 20km/h".
        - mucPhat: Mức phạt theo dạng a đồng – b đồng, ví dụ: 300.000 đồng – 400.000 đồng.
        - phatBoSung: Hình thức phạt bổ sung (string), ví dụ: "Tước GPLX 1 tháng".
        - canCuPhapLy: Căn cứ pháp lý (string), ví dụ: "Nghị định 100/2019/NĐ-CP".
        """
        # Tách loiViPham thành danh sách nếu có nhiều luật
        loiViPham_list = [x.strip() for x in loiViPham.split(",")]
        
        for loi in loiViPham_list:
            # Tầng 1: loiViPham
            if loi not in self.root.children:
                self.root.children[loi] = TreeNode(loi)
            
            # Tách phuongTien thành danh sách nếu có nhiều phương tiện
            phuongTien_list = [x.strip() for x in phuongTien.split(",")]
            for pt in phuongTien_list:
                # Tầng 2: phuongTien
                if pt not in self.root.children[loi].children:
                    self.root.children[loi].children[pt] = TreeNode(pt)
                
                # Tách chiTietLoi thành danh sách nếu có nhiều chi tiết
                chiTietLoi_list = [x.strip() for x in chiTietLoi.split(",")]
                for ct in chiTietLoi_list:
                    # Tầng 3: chiTietLoi
                    if ct not in self.root.children[loi].children[pt].children:
                        self.root.children[loi].children[pt].children[ct] = TreeNode(ct)
                    
                    # Tầng 4: Lá (dữ liệu vi phạm)
                    self.root.children[loi].children[pt].children[ct].data = {
                        "mucPhat": mucPhat,
                        "phatBoSung": phatBoSung,
                        "canCuPhapLy": canCuPhapLy
                    }

    def build_tree_from_json(self, json_data):
        """
        Xây dựng cây vi phạm từ dữ liệu JSON.

        Tham số:
        - json_data: Dữ liệu JSON chứa các lỗi vi phạm (dictionary).
        """
        for violation in json_data["trafficViolations"]:
            self.add_violation(
                violation["loiViPham"],
                violation["phuongTien"],
                violation["chiTietLoi"],
                violation["mucPhat"],
                violation["phatBoSung"],
                violation["canCuPhapLy"]
            )

    def print_tree(self, node=None, level=0):
        """
        In ra cây vi phạm dưới dạng văn bản.

        Tham số:
        - node: Nút bắt đầu để in cây (TreeNode). Mặc định là gốc.
        - level: Cấp độ của nút trong cây (int). Mặc định là 0.
        """
        if node is None:
            node = self.root
        print("  " * level + node.name)
        for child in node.children.values():
            self.print_tree(child, level + 1)

    def search_laws(self, loiViPham=None, phuongTien=None, chiTietLoi=None):
        # print(loiViPham, phuongTien, chiTietLoi)
        # print(type(loiViPham), type(phuongTien), type(chiTietLoi))
        """
        Tìm kiếm luật dựa trên các tham số: loiViPham, phuongTien, chiTietLoi.

        Tham số:
        - loiViPham: Tìm kiếm theo lỗi vi phạm.
        - phuongTien: Tìm kiếm theo lỗi vi phạm và phương tiện.
        - chiTietLoi: Tìm kiếm chi tiết theo lỗi vi phạm, phương tiện, và chi tiết lỗi.

        Kết quả:
        - Trả về danh sách các vi phạm dưới dạng dictionary, bao gồm:
          + "loiViPham": Tên lỗi vi phạm.
          + "phuongTien": Tên phương tiện vi phạm.
          + "chiTietLoi": Chi tiết lỗi vi phạm.
          + "mucPhat": Mức phạt.
          + "phatBoSung": Hình thức phạt bổ sung.
          + "canCuPhapLy": Căn cứ pháp lý.
        """
        results = []
        
        # Tìm trong tầng 1: loiViPham
        for loi_key, loi_node in self.root.children.items():
            if loiViPham is not None and loi_key != loiViPham:
                continue  # Bỏ qua nếu không khớp loiViPham
            
            # Tìm trong tầng 2: phuongTien
            for phuong_key, phuong_node in loi_node.children.items():
                if phuongTien is not None and phuong_key != phuongTien:
                    continue  # Bỏ qua nếu không khớp phuongTien
                
                # Tìm trong tầng 3: chiTietLoi
                for chi_key, chi_node in phuong_node.children.items():
                    if chiTietLoi is not None and chi_key != chiTietLoi:
                        continue  # Bỏ qua nếu không khớp chiTietLoi
                    
                    # Thêm luật vào kết quả
                    results.append({
                        "loiViPham": loi_key,
                        "phuongTien": phuong_key,
                        "chiTietLoi": chi_key,
                        **chi_node.data  # Gồm mucPhat, phatBoSung, canCuPhapLy
                    })
        
        return results
    def calculate_total_penalty_with_details(self, violations):
        """
        Tính tổng mức phạt, các căn cứ luật, và các phạt bổ sung từ danh sách các lỗi vi phạm.

        Tham số:
        - violations: Danh sách các lỗi vi phạm, mỗi phần tử là một dictionary chứa các thông tin
          về lỗi vi phạm, ví dụ: {"loiViPham": "Lỗi chạy quá tốc độ", "phuongTien": "Ô tô", "chiTietLoi": "Vượt quá 20km/h"}.

        Kết quả:
        - Trả về một dictionary chứa tổng mức phạt, các căn cứ luật, và các phạt bổ sung.
        """
        total_min_penalty = 0
        total_max_penalty = 0
        canCuLuat = set()  # Sử dụng set để tránh trùng lặp căn cứ luật
        phatBoSung = set()  # Sử dụng set để tránh trùng lặp phạt bổ sung

        # Danh sách chứa các mức phạt tối thiểu và tối đa
        min_penalties = []
        max_penalties = []

        # Hàm parse mức phạt đúng định dạng "a đồng – b đồng"
        def parse_penalty(mucPhat):
            # Dùng biểu thức chính quy để tách các số và loại bỏ phần "đồng"
            match = re.match(r"(\d{1,3}(?:\.\d{3})*) đồng\s*–\s*(\d{1,3}(?:\.\d{3})*) đồng", mucPhat)
            if match:
                # Chuyển các số thành int và loại bỏ dấu chấm (nếu có)
                min_penalty = int(match.group(1).replace(".", ""))
                max_penalty = int(match.group(2).replace(".", ""))
                return min_penalty, max_penalty
            else:
                return None, None

        # Duyệt qua từng lỗi vi phạm trong danh sách violations
        for violation in violations:
            loiViPham = violation.get("loiViPham")
            phuongTien = violation.get("phuongTien")
            chiTietLoi = violation.get("chiTietLoi")
            
            # Tìm các vi phạm tương ứng từ cây
            result = self.search_laws(loiViPham=loiViPham, phuongTien=phuongTien, chiTietLoi=chiTietLoi)
            
            # Nếu tìm thấy các vi phạm, cộng mức phạt vào tổng
            for res in result:
                # Lấy mức phạt (giả sử mức phạt luôn có định dạng "a đồng – b đồng")
                mucPhat = res["mucPhat"]
                phat_min, phat_max = parse_penalty(mucPhat)
                
                if phat_min is not None and phat_max is not None:
                    # Cộng trực tiếp giá trị min và max
                    min_penalties.append(phat_min)
                    max_penalties.append(phat_max)

                    # Thu thập các căn cứ luật và phạt bổ sung
                    canCuLuat.add(res["canCuPhapLy"])
                    if res["phatBoSung"]:
                        phatBoSung.add(res["phatBoSung"])

        # Tính tổng mức phạt min và max
        total_min_penalty = sum(min_penalties)
        total_max_penalty = sum(max_penalties)

        # Trả về kết quả
        return {
            "total_min_penalty": f"({total_min_penalty} đồng)",  # Trả về dưới dạng "(a đồng)"
            "total_max_penalty": f"({total_max_penalty} đồng)",  # Trả về dưới dạng "(b đồng)"
            "canCuLuat": list(canCuLuat),  # Chuyển set thành list
            "phatBoSung": list(phatBoSung)  # Chuyển set thành list
        }
