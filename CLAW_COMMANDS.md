# OPENCLAW CLI COMMAND REFERENCE & CONFIGURATION EXAMPLES
*Cẩm nang lệnh và cấu hình chuẩn xác cho Uranus - Cập nhật 2026-02-28*

## 1. CLI COMMANDS REFERENCE

### 1.1 Setup & Configuration
- `openclaw onboard`: Wizard tương tác thiết lập gateway, workspace, và skills.
  - `--install-daemon`: Cài đặt gateway thành dịch vụ chạy ngầm.
  - `--reset-scope <config|config+creds+sessions|full>`: Reset hệ thống.
- `openclaw config get <path>`: Lấy giá trị cấu hình (VD: `agents.defaults.model`).
- `openclaw config set <path> <value>`: Thiết lập giá trị (JSON5 hoặc chuỗi).
- `openclaw config unset <path>`: Xóa một giá trị cấu hình.
- `openclaw doctor`: Kiểm tra lỗi cấu hình và sửa lỗi tự động (`--fix`).

### 1.2 Gateway & Operations
- `openclaw gateway`: Chạy Gateway WebSocket.
  - `--port <port>`: Cổng (mặc định 18789).
  - `--force`: Kill tiến trình cũ và chạy lại.
- `openclaw gateway service <start|stop|restart|status>`: Quản lý dịch vụ chạy ngầm.
- `openclaw logs --follow`: Theo dõi log của Gateway thời gian thực.

### 1.3 Channel & Pairing
- `openclaw channels list`: Liệt kê các kênh chat đang hoạt động.
- `openclaw channels login --channel <whatsapp|web>`: Đăng nhập (hiện QR).
- `openclaw pairing list <channel>`: Xem danh sách yêu cầu ghép đôi DM.
- `openclaw pairing approve <channel> <code>`: Duyệt yêu cầu ghép đôi.

### 1.4 Agent & Models
- `openclaw agents list --bindings`: Xem danh sách agent và định tuyến.
- `openclaw agents add <name> --workspace <dir>`: Thêm agent mới.
- `openclaw models status`: Kiểm tra trạng thái các mô hình AI.
- `openclaw models set <model_id>`: Đặt mô hình chính.

---

## 2. CONFIGURATION EXAMPLES (openclaw.json)

### 2.1 Cấu hình Gateway & Reload
```json5
{
  gateway: {
    port: 18789,
    bind: "loopback", // loopback | lan | tailnet
    reload: { mode: "hybrid", debounceMs: 300 }, // hybrid tự restart khi cần
  }
}
```

### 2.2 Cấu hình Kênh Telegram
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "TOKEN_CUA_BAN",
      dmPolicy: "pairing", // pairing | allowlist | open
      groups: { "*": { requireMention: true } },
      streaming: "partial", // block | partial | off (hiển thị từng chữ)
    }
  }
}
```

### 2.3 Cấu hình Kênh WhatsApp
```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      allowFrom: ["+84xxxxxxxxx"], // Số điện thoại được phép
      ackReaction: { emoji: "👀", direct: true, group: "mentions" },
    }
  }
}
```

### 2.4 Cấu hình Multi-Agent & Routing (Định tuyến)
```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace" },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" }
    ]
  },
  bindings: [
    // Định tuyến theo kênh
    { agentId: "main", match: { channel: "whatsapp" } },
    { agentId: "coding", match: { channel: "telegram" } },
    // Định tuyến theo người gửi cụ thể (Peer)
    { 
      agentId: "coding", 
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+84xxxxxxxxx" } } 
    }
  ]
}
```

### 2.5 Cấu hình Quyền hạn Công cụ (Tool Allow/Deny)
```json5
{
  agents: {
    list: [
      {
        id: "restricted_agent",
        tools: {
          allow: ["read", "web_search"],
          deny: ["exec", "write", "edit", "gateway"]
        }
      }
    ]
  }
}
```

---
*Ghi chú: Luôn hỏi anh Nguyên trước khi thực hiện các lệnh can thiệp hệ thống phức tạp.*