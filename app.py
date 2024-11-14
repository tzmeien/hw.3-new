import lib

movie = []
total = []
select = 0

print("\n***如要輸入名稱請輸入全名***")
while select != 7:
    print("\n----- 電影管理系統 -----\n1. 匯入電影資料檔\n2. 查詢電影\n3. 新增電影\n\
4. 修改電影\n5. 刪除電影\n6. 匯出電影\n7. 離開系統\n------------------------")
    select = (int)(input("請選擇操作選項 (1-7):"))
    lib.mode(select)

