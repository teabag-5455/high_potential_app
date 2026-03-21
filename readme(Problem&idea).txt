# 新增功能memo
# 1.添加排行榜，透明化評分標準
# 2.資料庫功能，持久化存儲候選人資料。比對舊有資料，確認文檔真實性。
# 3.資料庫抓取網路上評分校際成績，分析學校背景對職涯的影響。

請建立requirements.txt方便函式庫下載&removeTracking .vevn

Bug
修正PDF閱讀時人名附帶副檔名問題->可能出現機器學習問題人名前有Name:...
ann white極度無法辨認，可用於測試
新功能讀取時間長...

要處理PDF或其它檔案年資閱讀問題

incorrect startxref pointer(1)，PDF讀取錯誤。可嘗試新套件?

parser.py & file_parser & candidate_profile 太多相似處理，導致年資、經驗、技能等重複處理、覆蓋等問題?
需要想辦法整合重複工作