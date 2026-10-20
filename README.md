# Kiểm thử tự động website hỗ trợ học tiếng Trung

**Đề tài:** “Kiểm thử tự động website hỗ trợ học tiếng Trung và xây dựng công cụ tích hợp AI hỗ trợ phân tích kết quả.”

Dự án đánh giá website **HSK 3.0** bằng các bài kiểm thử tự động có sẵn và phát triển **HSK Test Lab** để chọn/chạy test, tổng hợp kết quả, lưu lịch sử và dùng Gemini giải thích lỗi. Đánh giá website là trọng tâm; công cụ AI hỗ trợ người kiểm thử đọc và điều tra kết quả.

[Báo cáo PDF](BAO_CAO.pdf) · [Hướng dẫn HSK Test Lab](ai-test-tool/README.md) · [Minh chứng thực nghiệm](ai-test-tool/experiments/README.md) · [Thiết lập Neon kiểm thử](ai-test-tool/docs/NEON-TEST-SETUP.md)

## Dự án gồm những gì?

| Thành phần | Vai trò |
| --- | --- |
| **Website HSK** — `hsk-app/` | Đối tượng đánh giá: xác thực, học từ vựng/flashcard, mở khóa bài, ôn tập SM-2, luyện viết, trò chơi, tiến độ/thống kê, tra từ và sổ tay |
| **Bộ Selenium** — `selenium-tests/` | Kiểm thử qua Chrome; một số ca đối chiếu thêm phản hồi API và trạng thái dữ liệu |
| **Bộ Vitest** — `hsk-app/frontend/tests/whitebox/` | Kiểm tra logic SM-2, mở khóa, ngưỡng điểm và bảo toàn kết quả |
| **HSK Test Lab** — `ai-test-tool/` | Công cụ local có giao diện tiếng Việt, điều phối Selenium/Vitest, đọc JUnit XML, lưu lịch sử và tích hợp Gemini |
| **Báo cáo và minh chứng** | `BAO_CAO.pdf`, XML, nhật ký, ảnh chụp và dữ liệu đối chiếu trong thư mục thực nghiệm |

## Kết quả đạt được

Số liệu dưới đây thuộc **đợt thực nghiệm ngày 19/10/2026**. Lần cập nhật README và bổ sung ảnh ngày **20/10/2026** sử dụng lại minh chứng đã lưu, không tạo thêm lượt chạy test.

| Hạng mục | Kết quả đã xác minh | Minh chứng gốc |
| --- | --- | --- |
| Selenium toàn bộ HSK | **85 ca: 75 PASS, 10 FAIL, 0 ERROR, 0 SKIP**; tỷ lệ đạt **88,24%** | [XML](ai-test-tool/experiments/2026-10-19/selenium-all-122951/report.xml), [tóm tắt](ai-test-tool/experiments/2026-10-19/selenium-all-122951/summary.json) |
| Vitest logic HSK | **22/22 PASS** khi chạy bằng lệnh và qua giao diện | [XML UI](ai-test-tool/experiments/2026-10-19/vitest-ui.xml), [đối chiếu CLI/UI](ai-test-tool/experiments/2026-10-19/cli-ui-comparison.json) |
| Tra từ/sổ tay chạy riêng | UI và CLI đều **10/10 PASS**, tên và trạng thái từng ca khớp nhau | [Đối chiếu nhóm nhỏ](ai-test-tool/experiments/2026-10-19/selenium-cli-ui-comparison.json) |
| Kiểm thử chính HSK Test Lab | **21/21 test đạt** | [Nhật ký kiểm thử công cụ](ai-test-tool/experiments/2026-10-19/tool-tests-after-selenium.log) |
| Kết quả hiển thị và lịch sử | **85/85 ca** trên giao diện khớp tên/trạng thái trong XML gốc | [Đối chiếu DOM/XML](ai-test-tool/experiments/2026-10-19/selenium-dom-verification.json) |
| Nhập báo cáo lịch sử | **70/70 XML** khớp parser đối chiếu độc lập, gồm 115 bản ghi testcase có thể trùng giữa các lượt | [Đối chiếu XML](ai-test-tool/experiments/2026-10-19/xml-compatibility.json) |
| Kết nối Gemini thực tế | **HTTP 200**, đã lưu phân tích lỗi của lượt Selenium đầy đủ | [Phản hồi Gemini](ai-test-tool/experiments/2026-10-19/selenium-gemini-analysis.json) |
| Đánh giá sơ bộ AI | 10 mẫu: **7 đúng, 3 đúng một phần**; chưa có người chấm độc lập | [Rubric và nhận xét sơ bộ](ai-test-tool/experiments/2026-10-19/ai-judgements.json) |

**Cách hiểu số liệu:** 21 test công cụ khác với 22 test logic HSK và 85 ca Selenium. Nhóm 10 ca là tập con được chạy ở lượt khác; không cộng lại thành ca mới. 70 XML là báo cáo lịch sử dùng kiểm tra khả năng nhập. Kết quả 7/10 của tập AI nhỏ không phải độ chính xác chung của Gemini.

### Minh chứng giao diện

**Lượt Selenium đầy đủ được mở lại từ lịch sử:** 85 ca, 75 đạt và 10 thất bại; thời gian runner khoảng **28 phút 48 giây**. Khối kết quả bên phải là lượt lịch sử đang xem; phần chọn nhóm bên trái dùng thiết lập lượt mới và độc lập với kết quả lịch sử.

![Lịch sử Selenium: 85 ca, 75 PASS và 10 FAIL](ai-test-tool/experiments/2026-10-19/selenium-history-result.png)

<details>
<summary>Xem ảnh Vitest 22/22 PASS và nhóm tra từ/sổ tay 10/10 PASS</summary>

**Vitest:** bộ logic HSK gồm 22 ca, đều PASS trong lượt UI đã lưu.

![Vitest: 22 trên 22 ca đạt](ai-test-tool/experiments/2026-10-19/vitest-ui.png)

**Nhóm tra từ/sổ tay:** 10/10 PASS ở lượt UI riêng. NOTE-04 vẫn FAIL trong lượt Selenium đầy đủ; ảnh này không thay kết quả chính 75/85.

![Nhóm Selenium tra từ và sổ tay: 10 trên 10 ca đạt ở lượt riêng](ai-test-tool/experiments/2026-10-19/selenium-notebook-122623/ui-result.png)

</details>

Các ảnh nguyên bản cũng được chèn vào **phụ lục minh chứng của [BAO_CAO.pdf](BAO_CAO.pdf), trang 47–53**, cùng chú thích, nguồn và giới hạn của từng lượt. Báo cáo có 53 trang sau khi bổ sung phụ lục.

### Các phát hiện từ 10 ca Selenium thất bại

| Vấn đề | Số ca FAIL | Kết luận hiện có |
| --- | ---: | --- |
| Đăng ký chấp nhận tên chỉ có khoảng trắng — REG-09 | 1 | Có căn cứ từ mã nguồn và quan sát tên rỗng sau trim trong dữ liệu kiểm thử |
| Nút quay lại chọn cấp HSK bị thanh điều hướng che — VOC-01-HSK-1…7 | 7 | Xác nhận `ElementClickInterceptedException`; cần tách lỗi bố cục với thời điểm tự cuộn/Selenium |
| Lịch thống kê không chứa ngày hiện tại — STATS-03 | 1 | Đã đối chiếu hàm tạo lưới ngày với dữ liệu ngày 19/10/2026 |
| Xóa sổ tay qua API thành công nhưng giao diện còn thẻ — NOTE-04 | 1 | Chưa ổn định giữa các lượt; chưa xác định nguyên nhân gốc |

[Dữ liệu từng module và lỗi](ai-test-tool/experiments/2026-10-19/selenium-full-results.json) giữ nguyên kết quả ban đầu. Đợt này chưa sửa chức năng website hoặc assertion để đổi FAIL thành PASS. Website **chưa đáp ứng đầy đủ bộ E2E hiện có**; tỷ lệ 88,24% không phải tỷ lệ bao phủ mã nguồn hoặc kết luận chất lượng toàn hệ thống.

## HSK Test Lab làm được gì?

- Chọn nhóm test có sẵn, chạy/dừng và giới hạn thời gian; mỗi thời điểm chạy một nhóm.
- Đọc JUnit XML và hiển thị PASS/FAIL/ERROR/SKIP, chi tiết ca lỗi và nhật ký.
- Nhập/tải XML, lưu lịch sử trên đĩa và mở lại kết quả sau khi khởi động công cụ.
- Dùng Gemini giải thích bằng chứng lỗi, đưa giả thuyết và gợi ý bước kiểm tra.
- Chạy test và đọc XML bình thường khi chưa có Gemini API key.
- Kiểm tra môi trường Selenium và dùng snapshot HSK với endpoint Neon kiểm thử riêng.

Luồng sử dụng: **chọn nhóm → chạy test → đọc XML → xem kết quả/lưu lịch sử → yêu cầu AI phân tích khi cần**.

AI nhận dữ liệu lỗi và nhật ký rút gọn khi người dùng bấm phân tích. Nội dung phân tích được lưu cùng lần chạy; AI không sinh test, tự đánh giá assertion hoặc thay đổi PASS/FAIL. Phần tích hợp ở [gemini.ts](ai-test-tool/src/gemini.ts); key/model cấu hình qua biến môi trường của công cụ.

## Công nghệ

| Phần | Công nghệ |
| --- | --- |
| Website HSK | Next.js 14, React, TypeScript, Tailwind CSS, Prisma và PostgreSQL/Neon |
| Kiểm thử website | Python, pytest, Selenium WebDriver/Chrome và Vitest |
| Công cụ hỗ trợ | Node.js/TypeScript, HTML/CSS/JavaScript, JUnit XML, lưu JSON local |
| Phân tích lỗi | Gemini API qua REST `generateContent` |
| Minh chứng hiệu năng có sẵn | JMeter: JMX, JTL và các thư mục `PERF*-report/` |

## Chạy công cụ local

Cần **Node.js 22.18 trở lên**; môi trường thực nghiệm đã dùng Node 24. Chạy từ thư mục gốc repository:

```powershell
npm --prefix hsk-app/frontend ci
npm --prefix ai-test-tool ci
npm --prefix ai-test-tool start
```

Mở **http://localhost:4317**. Có thể chạy Vitest hoặc nhập XML có sẵn mà chưa cần Gemini key hay khởi động website. Hướng dẫn chi tiết về Python/Chrome, Gemini và giao diện ở [ai-test-tool/README.md](ai-test-tool/README.md).

Để chạy Selenium, cấu hình **Neon kiểm thử riêng** theo [NEON-TEST-SETUP.md](ai-test-tool/docs/NEON-TEST-SETUP.md), sau đó mở terminal khác:

```powershell
npm --prefix ai-test-tool run hsk:test
```

HSK kiểm thử chạy tại `http://localhost:3000`. Công cụ chỉ chạy Selenium khi marker môi trường khớp launcher. Các test có tạo/xóa dữ liệu nên phải dùng môi trường kiểm thử; giữ nguyên kết nối của website đang sử dụng.

Kiểm tra công cụ và đối chiếu minh chứng đã lưu:

```powershell
npm --prefix ai-test-tool run check
npm --prefix ai-test-tool test
python ai-test-tool/experiments/build-traceability.py --check
python ai-test-tool/experiments/freeze-evidence.py --check
```

Hai lệnh Python chỉ đối chiếu dữ liệu đã có, không chạy lại website hoặc gọi Gemini/DB.

## Cấu trúc repository

```text
DGVKDCLPM/
├── BAO_CAO.pdf                  # Báo cáo và phụ lục ảnh minh chứng
├── README.md                    # Giới thiệu dự án và kết quả đã kiểm chứng
├── hsk-app/                     # Website HSK, schema và các test liên quan
├── selenium-tests/              # Test Selenium có sẵn và minh chứng lịch sử
├── ai-test-tool/
│   ├── src/                     # Runner, XML, lịch sử, API và Gemini
│   ├── public/                  # Giao diện tiếng Việt
│   ├── tests/                   # Kiểm thử chính công cụ
│   ├── docs/                    # Hướng dẫn cấu hình Neon kiểm thử
│   ├── experiments/             # Script, XML, log, ảnh và metadata thực nghiệm
│   └── data/                    # Lịch sử/snapshot local; Git bỏ qua
├── HSK-performance.jmx          # Kế hoạch JMeter đã có
├── HSK-progress-performance.jmx
└── PERF*                        # Kết quả JMeter lịch sử
```

## Phạm vi và giới hạn

Selenium đã chạy trên Chrome với endpoint kiểm thử riêng. Các file `PERF` là minh chứng JMeter lịch sử; chưa chạy lại hoặc tích hợp JMeter vào HSK Test Lab trong đợt này. Chưa có kết luận về code coverage, tải của phiên bản hiện tại, accessibility, nhiều trình duyệt hay bảo mật toàn hệ thống. Các module học mở rộng chưa được kiểm thử E2E đầy đủ trong bộ 85 ca.

Chưa đo thời gian thao tác của người dùng thật, nên chưa kết luận giao diện làm Selenium nhanh hơn. AI chưa được người chấm độc lập đánh giá; phần lớn mẫu chấm sơ bộ là lỗi có kiểm soát. NOTE-04 cần kiểm tra độ ổn định thêm.

Metadata thực nghiệm ghi HEAD `197b220` khi công cụ còn ở working tree; commit `ce3290a` lưu mã/minh chứng sau thực nghiệm. Chi tiết phiên bản, hash và các lượt riêng nằm trong [manifest minh chứng JSON](ai-test-tool/experiments/2026-10-20/evidence-baseline.json). Các lượt chạy lại và báo cáo lịch sử được giữ riêng, không cộng thành kết quả mới.
