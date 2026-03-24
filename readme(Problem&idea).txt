# 新增功能memo
# 1.添加排行榜，透明化評分標準。鎖定個人身分資料，讓使用者從排行中看到位置在何處。
# 2.資料庫功能，持久化存儲候選人資料。比對舊有資料，確認文檔真實性。
# 3.資料庫抓取網路上評分校際成績，分析學校背景對職涯的影響。

請建立requirements.txt方便函式庫下載&removeTracking .vevn

Bug
1.修正PDF閱讀時人名附帶副檔名問題->可能出現機器學習問題人名前有Name:...
    ann white極度無法辨認，可用於測試
    新功能讀取時間長...
2.修正PDF閱讀年資問題，整合功能完成(parser.py & file_parser & candidate_profile)
    file_parser is Not working now.
    parser only doing extract file.
    candidate_profile is only making resume package.

incorrect startxref pointer(1)，PDF讀取錯誤。可嘗試新套件?

analytics 尚未完成。