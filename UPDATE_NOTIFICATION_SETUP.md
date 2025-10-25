# Update Notification Feature Setup

## Overview
এই feature আপনার bot এ নতুন movie/series add হলে automatically আপনার specified **Channel** অথবা **Group** এ notification পাঠাবে।

## ⚠️ গুরুত্বপূর্ণ: Channel vs Group

### 🔴 Group ব্যবহার করলে সমস্যা:
- Bot সেই group এর সব message এ respond করবে
- Inline search activate হয়ে যাবে
- Group spam হয়ে যেতে পারে

### ✅ Channel ব্যবহার করুন (Recommended):
- Bot শুধু notification পাঠাবে
- কোন unwanted response হবে না
- Clean এবং professional

## Configuration

### Environment Variables
আপনার `.env` file এ নিচের variables add করুন:

```env
# Update Channel Configuration (RECOMMENDED)
UPDATE_GROUP_ID=-1001234567890  # আপনার update channel এর ID
UPDATE_NOTIFICATIONS=True       # Enable/disable notifications (True/False)
```

### How to Get Channel/Group ID
1. **Method 1:** আপনার channel/group এ `@userinfobot` add করুন এবং `/start` command দিন
2. **Method 2:** আপনার channel/group এ `@RawDataBot` add করুন এবং কোন message forward করুন
3. **Method 3:** আপনার bot কে channel/group এ admin বানিয়ে `/groupid` command ব্যবহার করুন

### Channel vs Group ID Format:
- **Channel ID:** `-1001234567890` (13 digits, starts with -100)
- **Group ID:** `-1234567890` (10 digits, starts with -1)

## Features

### Individual File Notifications
- যখন একটি file add হয়, তখন notification পাঠানো হয়
- File name, size, এবং caption দেখানো হয়
- Clean format এ channel এ post হয়

### Bulk Notifications
- যখন indexing এর মাধ্যমে multiple files add হয়, তখন bulk notification পাঠানো হয়
- Total file count এবং source chat দেখানো হয়

## Notification Format

### Individual File:
```
🎬 নতুন ফাইল যুক্ত হয়েছে!

📁 ফাইলের নাম: Movie Name (2024)
📊 সাইজ: 1.5 GB
📝 বিবরণ: Movie description...

✅ ফাইলটি সফলভাবে ডাটাবেসে সংরক্ষিত হয়েছে।
```

### Bulk Update:
```
📦 বাল্ক আপডেট সম্পন্ন!

📊 যুক্ত হয়েছে: 25 টি নতুন ফাইল
📂 সোর্স: Channel Name

✅ সকল ফাইল সফলভাবে ডাটাবেসে সংরক্ষিত হয়েছে।
```

## How It Works

1. **Channel Auto-Save:** যখন configured channels থেকে media files আসে, automatically notification পাঠানো হয়
2. **Manual Indexing:** যখন admin manually indexing করে, bulk notification পাঠানো হয়
3. **Error Handling:** Notification fail হলেও main functionality affected হয় না

## Troubleshooting

### Notifications Not Working?
1. Check করুন `UPDATE_GROUP_ID` সঠিক আছে কিনা
2. Bot কে update channel/group এ add করা আছে কিনা verify করুন
3. Bot এর update channel/group এ message send করার permission আছে কিনা check করুন
4. `UPDATE_NOTIFICATIONS` True set করা আছে কিনা confirm করুন
5. **Channel ব্যবহার করলে:** Bot কে channel এ admin বানান
6. **Group ব্যবহার করলে:** Bot এর message send permission আছে কিনা check করুন

### Bot Logs
Notification related errors bot logs এ দেখা যাবে:
- "Update notification sent for file: [filename]" - Success
- "Failed to send update notification: [error]" - Error

## Files Modified
- `info.py` - Configuration variables added
- `utils/notifications.py` - Notification functions created
- `database/ia_filterdb.py` - save_file function modified
- `plugins/index.py` - Bulk notification integration
- `plugins/channel.py` - Individual notification integration