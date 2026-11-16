# Sổ tay Backend

Tài liệu tiếng Việt, trình bày dạng một trang web có 5 tab:

| Tab | Nội dung |
|---|---|
| **NestJS** | Toàn bộ docs (v12, ghi chú khác biệt v11): controller, DI, module, guard, pipe, interceptor, kỹ thuật, bảo mật, microservices + 18 pattern kiến trúc |
| **Java** | Java hiện đại JDK 21–27: ngôn ngữ, thư viện chuẩn, virtual threads, công cụ JVM + design patterns (GoF và hiện đại) |
| **RabbitMQ** | Exchange, queue type, confirm/ack, DLX, retry + cách dùng trong NestJS và Java + pattern |
| **Kafka** | Topic/partition/consumer group, delivery semantics, transaction, share group + NestJS/Java/Spring/Kafka Streams + pattern |
| **Redis** | Kiểu dữ liệu, persistence, eviction, cluster + ioredis/Lettuce/Jedis/Redisson + pattern (cache, lock, rate limit, stream) |

## Xem

Mở `index.html` bằng trình duyệt, hoặc bật GitHub Pages (Settings → Pages → Deploy from a branch → `main` / root).

## Sửa nội dung

Nội dung nằm trong `src/`, ghép theo thứ tự tên file. Sau khi sửa:

```bash
python3 build.py   # tạo lại index.html
```

Quy ước viết trong `src/`:

- Khối code: `<pre data-lang="ts" data-file="tên-file.ts">…</pre>` (viết code thô, script tự escape).
- Code inline: `<c>…</c>`.
- Mỗi chủ đề là `<section class="doc" id="…" data-group="Nhóm">` với một `<h2>`; mục lục sinh tự động.
- ID chủ đề phải duy nhất trên toàn trang (tiền tố: Java `j-`, RabbitMQ `r-`, Kafka `k-`, Redis `rd-`).

Script dừng với lỗi nếu có link `#id` hỏng hoặc còn sót cú pháp chưa xử lý.

## Lưu ý

Tổng hợp tháng 11/2026 từ docs chính thức (docs.nestjs.com, dev.java, docs.oracle.com, rabbitmq.com, kafka.apache.org, redis.io) và các nguồn pattern. Ví dụ code mang tính minh họa, chưa được biên dịch thử; số phiên bản thư viện cần kiểm tra lại trước khi dùng.
