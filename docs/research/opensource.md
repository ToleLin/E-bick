# 研究報告：opensource

# 開源自行車摩擦驅動專案調查（截至 2026-11-07）

## 一、結論

**沒有任何一個現成專案同時符合 (a) 免工具快速換車、(b) 以 PETG-CF / PETG 為主列印、(c) 零件可在台灣買到、(d) 開放授權這四項。**

- **快拆做得最好的是 Bicycle BoosterPack。** 它用手鎖夾具，適用 21–39 mm 的座管或車架管，作者說「幾秒就能拆下」。但 STL 是在 Cults3D 付費下載（US$3），授權是 CULTS PU，不能散布改作。原作者也已停售套件。
- **授權最乾淨、又有可編輯原始檔的只有兩個 GitHub 專案。** MikeKaiser/eBike_v1 是 MIT 授權、OpenSCAD 參數化；BijouBoost 是 GPL-3.0、FreeCAD 原始檔。兩者都要用螺栓固定，也幾乎沒有實際騎乘紀錄。
- **最新、而且已經用 PETG 印過的是 JK_Prints（2026-08，CC BY-SA）。** 但它只有 3 個 STL，沒有可編輯 CAD，也要用 4 支螺栓固定。
- **零件是否能在台灣買到，這次沒有查證（UNVERIFIED）。** 所有開源案都用 5065 / 6354 / 6374 級的電動滑板外轉子馬達，加上 VESC 類控制器，例如 Flipsky。蝦皮、露天、淘宝的實際賣場要另外確認。

**建議**：不要直接照做任何一個。以 MikeKaiser 的 MIT 參數化架構當骨架，借用 JK_Prints 的 PETG 列印參數和零件組合，再自己加上「每台車一個固定底座 + 主機免工具快拆」（概念來自 Piotr 的 fdrive）。

---

## 二、候選專案逐項比較

### A. 開源或半開源、有公開檔案

| # | 專案 / URL | 授權 | 年份與活躍度 | 安裝位置與拆裝方式 | 馬達 / KV | 滾輪 | 壓緊方式 | 控制器 / 電池 / 油門 | 列印件與材料 | 可編輯 CAD |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Bicycle BoosterPack**（MechEngineerMike）[Instructables](https://www.instructables.com/Bicycle-BoosterPack-a-3D-Printed-Portable-Electric/)、[Cults3D](https://cults3d.com/en/3d-model/gadget/bicycle-boosterpack-clamp-on-and-go-electric-vehicle) | 說明頁 CC BY-NC-SA 4.0；STL 為 **CULTS PU、付費 US$3** | 2016-04；STL 2020-10 移到 Cults；套件已停售 | 座管、車架中段或高車架三種配置；可調夾具 21–39 mm、手鎖把手；「Can be Removed in Seconds」 | Maytech MTO5065-220KV（50 mm）；60 mm 的 MTO6355-200KV 失敗 | 馬達外殼直接接觸輪胎 | 彈簧把馬達拉離輪胎，啟動扭矩把它甩進去；用止付螺絲限位 | Maytech MTC150A 電變；6S 5Ah LiPo；伺服測試器改成按鈕油門 | 23 個 STL；ABS/PLA；需要攻牙 1/4"-20 | ✗（只有 STL） |
| 2 | **Gryphe 3D printed friction drive** v1 [ES 63197](https://endless-sphere.com/sphere/threads/a-3d-printed-friction-drive.63197/) / v2 [ES 67461](https://endless-sphere.com/sphere/threads/return-of-the-3d-printed-friction-drive.67461/) | 非正式：「Feel free to do whatever… mention me」 | 2014-09 / 2015-03；**Dropbox 連結已失效**（2026-11-07 查證回傳錯誤頁） | 座管或車架管（32.5 mm）；v1 用手柄當鎖緊螺帽，拆下後只剩夾具；v2 改用管夾 | v1 SK3 42 mm 350kv；v2 SK3 59 mm 168kv，另有 50 mm 5065 236kv 版 | 馬達外殼（雨天加止滑帶） | 無彈簧，靠兩顆滑板軸承樞軸 + 限位凸耳；v2 有 20° 可調限位 | Arduino 控制；4S 或 6S LiFePO4 8400 mAh | Colorfabb XT（PET 共聚酯）；幾乎實心 | v2 有 STL + **STP**（已無法下載） |
| 3 | **Friction Drive E-Bike**（Macaca / fpv99）[Thingiverse 2271941](https://www.thingiverse.com/thing:2271941)、[MMF 鏡像](https://www.myminifactory.com/object/3d-print-friction-drive-e-bike-39781) | Thingiverse **CC BY**；MMF 上為 Credit-Remix-Noncommercial | 2017-04；沒有更新 | 座管後方，[照片](https://cdn.thingiverse.com/assets/e3/2d/08/f3/23/P1100146.JPG)顯示壓在後輪前緣；4×M4 加 M8 樞軸螺栓 | 頁面沒寫型號（UNVERIFIED） | 馬達外殼 | 兩條 1.2 mm 拉簧，另一端用束帶調整 | VESC；Arduino 把類比油門轉 PWM；油門握把 | 3 個 STL（FD_Base_Top / Bottom、Motor_Mount） | ✗；組裝指南另外放在 [Gumroad](https://fpv99.gumroad.com/l/LqmWJ) |
| 4 | **PU Wheel Friction Drive**（同一作者）[Thingiverse 2556492](https://www.thingiverse.com/thing:2556492)、[Instructables](https://www.instructables.com/PU-Wheel-Friction-Drive-E-Bike/) | **CC BY-NC**；Instructables CC BY-NC-SA | 2017-09 / 2019-06 | 同 #3 | 滑板 PU 輪轂馬達 75×83 mm、110KV、24–36 V | PU 輪 | 同 #3 | VESC；6S2P VTC6（22.2 V 6000 mAh） | STL | ✗ |
| 5 | **Ebike friction drive unit**（Darazsweb）[Thingiverse 3449552](https://www.thingiverse.com/thing:3449552) | **CC BY** | 2019-02 進行中，v3 一直沒發布（2019–2021 留言追問） | 「limited space」，位置沒寫（UNVERIFIED） | SK3 4240 620KV | 齒輪減速，加上印製的 RubberRing | 靠幾何自鎖，沒有彈簧 | Redbrick 60A；4S LiPo；伺服測試器 | 12 個 STL，含 Pinion、Spur、Internal 齒輪 | ✗ |
| 6 | **Electric Brompton DIY Friction Drive** 與 **eBike Friction Drive Build**（CorrugatorSupercilii）[Cults 285446](https://cults3d.com/en/3d-model/various/electric-brompton-diy-friction-drive-solution)、[Cults 285454](https://cults3d.com/en/3d-model/various/ebike-friction-drive-build) | **CC BY-NC-ND**（不可改作） | 2019（Cults 2021 上架） | **前叉**卡鉗孔，借用 Brompton 前反光片支架；鬆兩支螺栓「takes just a minute」 | KEDA 6364 190KV；SK3 6364/6374 190KV | 馬達外包 **2 mm SBR 橡膠** | 支架本身的彈性 + 8 mm 槓桿螺栓 | VESC 4.12；36 V 4.4 Ah 平衡車電池 | ABS、0.2 mm 層高、100% 填充；另有散熱風扇、VESC 盒 | ✗（附 Fusion360 200 N 靜力分析 PDF） |
| 7 | **friction drive bicycle motor mount**（xxdavexx）[Cults](https://cults3d.com/en/3d-model/various/friction-drive-bicycle-motor-mount-ebike-conversion) / Thingiverse 4125068 | **CC BY** | 2020-01 | UNVERIFIED | 頁面只有 AliExpress 連結 | 馬達外殼 | 有 MotorIdler 零件，細節不明 | VESC V4.12 | 4 個 STL | ✗ |
| 8 | **MikeKaiser/eBike_v1** [GitHub](https://github.com/MikeKaiser/eBike_v1) | **MIT** | 2020-07-18 最後一次 commit | 夾在座管 Ø27.1 與座管套管 Ø32 的接合處；有 6 個 r=3.1 mm（約 M6）螺栓孔，**不是免工具** | Turnigy SK3-6354 | 馬達外殼 | 可選自由擺臂或鎖死臂；有可調止轉「locking splines」 | Hobbywing SkyWalker 80A；Arduino Nano + 電位器油門 + 霍爾輪速 + **霍爾踏頻（PAS）** + 低電壓切斷 + 堵轉電流切斷；電池寫「4x 6S 8mAh LiPo」（原文如此） | 擺臂、支架、電變盒、電池座、把手油門；Ender 3 設定檔：80% 填充 | **✓ OpenSCAD 參數化** |
| 9 | **BijouBoost-P14_00_00**（KionoKitse）[GitHub](https://github.com/KionoKitse/BijouBoost-P14_00_00) | **GPL-3.0** | 2022-01 到 03；最後 commit 為「New Motor Mount in Wood」 | UNVERIFIED（有 BikeMountPt1/Pt2、MotorKnob 等零件） | 6374（附 6374_bldc_motor.stp） | 馬達外殼 | UNVERIFIED | Arduino 把電位器轉成 1000–2200 µs 伺服脈衝給航模電變 | Rev2 為 STL；Rev3 為光固化 .cbddlp | **✓ FreeCAD .FCStd** |
| 10 | **Universal Friction Drive Ebike**（JK_Prints）[Thingiverse 7398135](https://www.thingiverse.com/thing:7398135) | **CC BY-SA** | **2026-08-19**，最新 | 4 支 5/16"×3.5" 螺栓夾在後輪旁的直立管，見[照片](https://cdn.thingiverse.com/assets/ae/c6/b3/93/0b/1000029288.jpg)；有沒有樞軸看不出來（UNVERIFIED） | **6374 170kv** | 馬達外殼包**樓梯止滑帶** | UNVERIFIED | **Flipsky 75100 Pro VESC**；48 V 13 Ah；拇指或轉把油門 | 3 個 STL；**PETG、8 層牆、上下各 8 層、50% 填充、0.6 噴嘴** | ✗ |
| 11 | **F-drive**（Piotr Strzałka）[部落格](https://piotrstrzalka.github.io/2021/01/31/fdrive-e-bike-conversion-system.html) | 機構檔**未公開**；韌體 [app_fdrive.c](https://github.com/PiotrStrzalka/bldc/blob/friction_drive/applications/app_fdrive.c) 是 VESC bldc 的 fork（上游 GPL-3.0；此 repo 沒標授權） | 2021-01 | **固定件留在每台車上，電池和馬達+控制器可拔下換車** | 5065 270kV 無感，峰值約 1.5 kW | **散熱器水管**套在馬達外（較安靜） | 馬達扭矩把自己拉上輪胎 | VESC 自寫 app（用 PAS 倒踩來啟用/解除、attach_time_ms 等參數）；10S5P 約 508 Wh | Fusion 360 設計、3D 列印 | ✗ |
| 12 | **Ebike Friction Drive Build for Bikes**（machinecrafted）[Instructables](https://www.instructables.com/Friction-drive-build-for-bikes/) | CC BY-NC-SA | 2015-04 | 座管、後下叉、後上叉之間（Commuter Booster 仿製） | C6374/09 KV170 | 馬達外殼 | 琴鋼線彈簧 | HobbyKing 85A；5S 5000 mAh；伺服測試器 + 拇指油門 | **CNC 鋁件 + 尼龍 66，不是列印** | 有安裝模板 PDF |
| 13 | **FixedE-bike**（tychobarendse）[hackaday.io](https://hackaday.io/project/18669-fixede-bike) | 沒標 | 2016，中斷 | 後輪 | 1900KV 航模馬達 | 滑板輪，加 GT2 60/16 皮帶減速 3.75 | 扭簧（拆自握力器） | 80A 電變 + Arduino | 沒有 | 只有 ESC.ino |

補充：MakerWorld [「单车助力器」#3104448](https://makerworld.com/en/models/3104448)（2026-07）用 Standard Digital File License，不是開放授權。列印設定約 443 g，作者建議 PETG 或 PA6-CF。驅動方式沒有寫明（UNVERIFIED）。

**實測數據與已知問題**

- **#1 BoosterPack**
  - 含電池 4 lbs；含踩踏最高 25 mph；660 W。
  - 111 Wh 電池：純動力約 5 mi，輔助約 10 mi 以上。
  - 濕胎、越野胎、後避震車都不能用。
  - 車速要先到 5 mph 以上才能啟動。
  - 60 mm 馬達搭航模電變時一壓到輪胎就尖叫，無法使用。
  - 作者測過砂紙、塗層、網布：「ANY material able to grip a wet tire will quickly wear the tire」。
- **#2 Gryphe**
  - v2 時速 30 km/h，馬達不超過約 40 °C。
  - 4S 版：25 km/h、約 18 km。
  - 印製滾輪版曾經卡死後碎裂。
  - 42 mm 馬達長途會過熱。
  - [有人質疑](https://endless-sphere.com/sphere/threads/return-of-the-3d-printed-friction-drive.67461/)塑膠件長期承受馬達熱的耐久性。
- **#4 PU 輪版**：平路 15 km/h（Instructables）；Thingiverse 寫「18km/h above」。
- **#5 Darazsweb**
  - 位置太高時，輪胎受壓會讓驅動輪「jump over」，需要限位。
  - 輪圈不圓會在高速時振動，作者打算加避震。
- **#6 Brompton**：16 吋輪踩踏輔助可超過 45 km/h；實測超過 100 km（晴雨都有），但「does not fair well in wet weather」。
- **#8 MikeKaiser**：SCAD 檔內寫明：擺臂與「樞軸到輪心連線」夾角小於 45° 才會自動咬緊，但需要止轉擋塊，否則會翻過頭。
- **#11 F-drive**：作者試過止滑帶、砂紙、內胎，「all of them fails after some time」。

### B. 沒有開放授權或沒有檔案，但經驗很有用

| 專案 | 重點 |
|---|---|
| **Kepler eBoost（2010，座管式，商品）** [ES 22026](https://endless-sphere.com/sphere/threads/eboost-kepler-friction-drive-review-and-testing.22026/) | 靠鋁墊片配合不同座管徑。買家的墊片一個太小、一個太大，騎幾分鐘後**整組鬆脫撞到輪子**。驅動器 + 馬達 + 電變共 4.6 lbs；5S 平路 22.9 mph。 |
| **Kepler 五通式（2017，不鏽鋼，US$100 機構套件）** [販售帖](https://endless-sphere.com/sphere/threads/kepler-bottom-bracket-friction-drive-for-sale-finally.86961/)、[開發帖](https://endless-sphere.com/sphere/threads/kepler-friction-drive-comes-of-age.84905/) | 「gravity spring」抵消馬達重量；啟動扭矩讓馬達碰到胎、受載後爬上輪胎咬緊，斷電就掉開。建議 KV 低於 280、最多 6S LiPo 或 7S 18650、限流約 14 A。VESC FOC 模式讓噪音減半。用 63 mm 馬達時，限位板在顛簸路上會移位，要加回第三支鎖螺絲。 |
| **Kepler 2021 列印版原型**（同上帖 page-17） | 擺臂裝雙 8 mm 密封軸承，轉動夠順，不需要重力彈簧；凸輪式限位調整；有拉線可鎖在咬合位置。只用 4 個列印件、2 顆軸承、2 個墊圈、7 個標準扣件；支架從 200 g 減到 100 g。舊版金屬直接互磨的樞軸會卡黏又會異響。一開始用 PLA 試印，有人提醒 PLA 不適合戶外；另一位用戶說 PETG 支架很耐用。 |
| **Commuter Booster**（adrian_sm）[FAQ](https://sites.google.com/site/commuterbooster/faq)、[原理](https://sites.google.com/site/commuterbooster/how-does-it-work) | 驅動器約 1 kg，含電池加 3–4 kg；巡航約 40 kph、約 30 km。調好時輪胎磨耗仍是一般的 **2–3 倍**。10 kph 以下不要給輔助。用上限位決定最大咬入量。 |
| **jd_3d 後三角內側**（2017）[ES 91293](https://endless-sphere.com/sphere/threads/metal-3d-printed-rc-friction-drive-development-build-log.91293/) | 列印件只有 75 g，含電池 1,025 g；KEDA 56-63 195KV。改成旋轉式設計後陡坡零打滑。陡坡反覆爬升時馬達接近退磁溫度。塑膠版耐用到作者放棄改金屬。6S 6.6Ah 約 10 mi，平路 24 mph。 |
| **vell001（中文，2018）** [騰訊雲](https://cloud.tencent.com.cn/developer/article/1334178) | 座管式；N5065 外套 PU 管；ABS 列印（作者說 PLA 耐熱不足）；電變偏熱；沒有公開檔案。 |
| **Andre（2022）**（Kepler 帖 page-17） | 掛在 Nitto 貨架上、自動放下與收回，「convert… in less than 30sec」。公開檔案未見（UNVERIFIED）。 |
| **furp 16 吋摺疊車滑軌式** [ES 102371](https://endless-sphere.com/sphere/threads/16-folding-bike-sliding-friction-drive.102371/) | 滑軌式無法靠啟動扭矩自動咬合，只好改腳踏桿。爬坡無力；VESC 放在座墊袋裡過熱降功率。 |
| **Skike** [esk8.news](https://forum.esk8.news/t/skike-a-esk8-parts-based-ebike/7518) | 手壓固定、沒有彈簧；馬達在 70 m 爬坡就燙到手指放不住。 |
| **商品對照**：Rubbee X [road.cc](https://road.cc/content/tech-news/rubbee-x-another-friction-drive-e-bike-conversion-kit-310443)、Velospeeder [官方](https://www.velogical-engineering.com/velospeeder/technical-information/?lang=en) | Rubbee X：座管快拆；250 W、25 km/h；基本款 94 Wh。Velospeeder：PU 環驅動輪圈側面，接觸壓力自動調整，有雨天加壓開關；廠商稱 PU 環 7,000–10,000 km 要換（廠商說法）。 |

---

## 三、四項條件判定

| 專案 | (a) 免工具換車 | (b) 主要列印、PETG 類 | (c) 台灣可購 | (d) 開放授權 |
|---|---|---|---|---|
| BoosterPack | **△+**（手鎖夾，21–39 mm） | △（ABS/PLA，金屬件多達 70 個） | UNVERIFIED（Maytech 指定件） | ✗（CULTS PU、付費） |
| MikeKaiser | ✗（約 M6 螺栓） | ✓（但沒寫材料） | 通用件，UNVERIFIED | **✓ MIT + 原始檔** |
| BijouBoost | ✗ / UNVERIFIED | △（光固化、木頭） | 通用件，UNVERIFIED | **✓ GPL-3.0 + 原始檔** |
| JK_Prints | ✗（4 支螺栓） | **✓ PETG** | 通用件，UNVERIFIED | ✓ CC BY-SA（只有 STL） |
| Macaca #3 | ✗ | ✓ | 通用件，UNVERIFIED | ✓ CC BY（只有 STL） |
| Brompton #6 | △（約 1 分鐘、2 支螺栓） | ✓（ABS） | UNVERIFIED | ✗（ND，不可改作） |
| Gryphe | △（v1 有手柄） | ✓（PET 類） | 通用件 | 非正式授權，**檔案已失效** |

---

## 四、建議作為改良基底的前三名

1. **MikeKaiser/eBike_v1（MIT）**
   - 優點：
     - 唯一用參數化原始碼做座管式夾具的專案，管徑、擺臂長、限位角都是變數。
     - 電子架構已經包含 PAS、輪速、低壓切斷、堵轉電流切斷。
     - MIT 授權可以自由改作、商用，也能再開源。
   - 要改的地方：
     - 螺栓夾改成「固定座 + 快拆」。
     - 航模電變換成 VESC。
     - 依 PETG-CF 重新設計壁厚與熱隔離。
     - 擺臂幾何要涵蓋 20 吋到 29 吋輪。
2. **JK_Prints Universal Friction Drive（CC BY-SA）**
   - 優點：
     - 2026 年最新，已經用 PETG 實際騎乘。
     - 列印參數（0.6 噴嘴、8 層牆、50% 填充）可以直接套到 A1 + PETG-CF。
     - 零件組合是現行 6374 + Flipsky 75100 Pro。
   - 缺點：
     - 只有 STL，要重新建模。
     - 改作必須維持 CC BY-SA。
     - 48 V 的設定遠超過 250 W 法規級。
     - 還沒有長期騎乘報告。
3. **Macaca Friction Drive E-Bike（CC BY）**
   - 優點：只有 3 個零件的座管後方方案；用拉簧加束帶調預壓；搭 VESC；授權寬鬆。
   - 缺點：只有 STL，要用螺栓固定，2017 年後沒有更新。

另外有三個值得參考、但不能當基底的對象：

- **BoosterPack**：參考它的夾具範圍、手鎖把手、用管夾當定位記憶點，以及 fit-check PDF 模板的做法。授權不能拿來改。
- **Kepler 2021 列印擺臂**：參考雙密封軸承、凸輪限位、只用 4 個列印件的設計。這是商品，沒有開放授權。
- **Piotr F-drive**：參考「多台車各裝底座、一套主機輪流用」的架構，以及開源的 VESC 咬合 app。

---

## 五、新設計應該採用的教訓

1. **自咬緊幾何，並一定要有雙向限位。**
   - 擺臂角度小於 45°，馬達受載時會「爬上」輪胎自動加壓（[MikeKaiser SCAD](https://github.com/MikeKaiser/eBike_v1)、[Kepler](https://endless-sphere.com/sphere/threads/kepler-bottom-bracket-friction-drive-for-sale-finally.86961/)）。
   - 馬達中心不可越過「樞軸到輪心」連線（[BoosterPack](https://www.instructables.com/Bicycle-BoosterPack-a-3D-Printed-Portable-Electric/)）。
   - 沒有上限位會翻過頭（[Darazsweb](https://www.thingiverse.com/thing:3449552)）。
   - 上限位決定最大咬入量；輪胎氣壓變低或下雨時，可用它快速增加咬入（[Commuter Booster](https://sites.google.com/site/commuterbooster/how-does-it-work)）。
2. **樞軸用密封滾珠軸承，不要塑膠或金屬直接互磨。** 互磨會卡黏、異響；軸承夠順就可以省掉重力彈簧（Kepler 2021）。要讓馬達平常離開輪胎，可用彈簧抵消重量，或像 BoosterPack 用彈簧把馬達拉開。
3. **夾具是失敗率最高的地方。**
   - 座管墊片不合會鬆脫撞輪（[eBoost](https://endless-sphere.com/sphere/threads/eboost-kepler-friction-drive-review-and-testing.22026/)）。
   - 夾具不乾淨、不均勻會整組旋轉（BoosterPack）。
   - 63 mm 馬達會震鬆限位板（Kepler）。
   - 建議做法：每台車裝一個便宜的固定座，內含止轉鍵與定位記憶，用 PETG-CF 列印並配橡膠墊；主機用燕尾槽加快拆把手加彈簧定位銷，換車後不必重調。
4. **滾輪表面目前沒有完美解。**
   - 裸露馬達外殼遇濕胎幾乎失效。
   - 砂紙、止滑帶抓得住濕胎，但很快磨壞輪胎或自己磨光（BoosterPack 實驗、[pedelecs](https://pedelecs.co.uk/forum/threads/experimenter.23447)）。
   - 實際用過的套管：2 mm SBR 橡膠（超過 100 km）、散熱器水管（也比較安靜）、PU 管、樓梯止滑帶。
   - 輪胎磨耗約 2–3 倍；越野胎不能用。
   - 新設計應做成可更換的滾輪套管，並把 TPU 套管列為實驗選項。
5. **馬達選型。**
   - 選 50–63 mm 外轉子，KV 低於 280，最多 6S LiPo 或 7S 18650，限流約 14 A 已足夠 250 W 級（Kepler）。
   - KV 太高會讓人失望：Gryphe 的 350kv 後來換成 168kv；Darazsweb 用 620KV。
   - 42 mm 太小會過熱。
6. **散熱與材料。**
   - 陡坡反覆爬升會讓馬達接近退磁溫度（[jd_3d](https://endless-sphere.com/sphere/threads/metal-3d-printed-rc-friction-drive-development-build-log.91293/)）。
   - 控制器不要悶在座墊袋裡（furp）。
   - 可以加印製散熱扇（Gryphe、Brompton、BoosterPack 都有）。
   - PLA 不適合戶外；PETG 或 PET 類實際用過沒問題。
   - 接觸馬達的部位要留空氣隙或加隔熱片，因為 PETG 的熱變形溫度比 ABS 低（這一點是推論，未查證）。
7. **控制器用 VESC，跑 FOC 模式。**
   - FOC 讓噪音減半（Kepler）。
   - 航模電變搭大馬達會失步尖叫（BoosterPack）。
   - 要設最大 ERPM，否則容易燒 DRV（[ES 論壇](https://endless-sphere.com/sphere/threads/kepler-friction-drive-comes-of-age.84905/page-9)）。
   - FOC 模式下輸入固定 PWM 約 10 秒後會掉油門，要改用斜坡輸入（Kepler 2018）。
8. **操作邏輯。**
   - 10 kph 或 5 mph 以下禁止出力。
   - 按鈕加踏頻感測：Kepler 用短按約 150 W 輔助、長按 250 W 加速。
   - 可直接參考 Piotr 的 [app_fdrive.c](https://github.com/PiotrStrzalka/bldc/blob/friction_drive/applications/app_fdrive.c) 處理咬合重試與冷卻。
9. **列印結構。**
   - 用厚壁：JK 用 8 層牆；Brompton 用 100% 填充並做 200 N 有限元素分析。
   - 塑膠攻牙容易滑牙（BoosterPack），改用熱壓銅螺母。
   - 輪圈不圓會引起振動，結構要留一點柔性或阻尼（Darazsweb）。
10. **相容性要誠實標示。**
    - 後避震車不適用（BoosterPack、machinecrafted）。
    - 提供可列印的 1:1 fit-check 模板，涵蓋 20 吋到 700c/29 吋。
    - 不要用滑軌式，它無法靠扭矩自動咬合（furp）。

---

MikeKaiser 的參數化原始檔已下載到 `C:\Users\user\AppData\Local\Temp\claude\331f5373756cbd02\c95f4efe-559a-4251-aa6f-aaacc223e7e4\scratchpad\fc\mk_mount.scad`，可直接當改寫起點。


---

# 查證結果：opensource

**查核結果**

說明：查到一半時，WebSearch 的搜尋額度已經用完。後面的項目都是直接抓已知網址查證，用過 GitHub API、Thingiverse、Flipsky 官網、露天、全國法規資料庫、Endless-Sphere 論壇。蝦皮和淘寶沒有查。

1. **MikeKaiser/eBike_v1：MIT 授權、OpenSCAD 參數化、最後 commit 為 2020-07-18、約 M6 螺栓、45° 自咬緊註解、霍爾踏頻 → CONFIRMED**
   - GitHub API 回傳 license 為 MIT，pushed_at 為 2020-07-18，最後一筆 commit 是「Locking splines.」。
   - `bike_motor_mount.scad` 的參數：
     - `seatPostRadius=(27.1+0.4)/2`
     - `downTubeRadius=(32+0.4)/2`
     - `boltHoleRadius=3.1`，共 6 個 BoltPin
   - 第 5–9 行寫「less than 45 degrees… dig in」。
   - Electronics/readme.md 列有「Hall Effect Switch… for crank speed」。
   - 報告漏掉兩點：
     - SCAD 開頭寫「free to rotate… you really need a spring to push the motor against the wheel」，表示原設計需要彈簧加上止轉擋塊。
     - 馬達參數 `motorRadius=30`、`motorLen=66` 是照 SK3-6354 設的。改用 6374 時必須改長度。
   - 來源：https://github.com/MikeKaiser/eBike_v1 、https://raw.githubusercontent.com/MikeKaiser/eBike_v1/master/Mechanical/bike_motor_mount.scad

2. **BijouBoost：GPL-3.0、FreeCAD 原始檔 → CONFIRMED**
   - license 為 GPL-3.0。
   - Rev1、Rev2、Rev3 都有 .FCStd 檔，另有 `6374_bldc_motor.stp` 和 `Controller/Controller.ino`。
   - 最後 commit 是 2022-03-23 的「New Motor Mount in Wood」。
   - 來源：https://github.com/KionoKitse/BijouBoost-P14_00_00

3. **JK_Prints Universal Friction Drive：CC BY-SA、6374 170kv、Flipsky 75100 Pro、48 V 13 Ah、4 支 5/16"×3.5" 螺栓、PETG 8 層牆、上下各 8 層、50% 填充、0.6 噴嘴、3 個檔案 → CONFIRMED**
   - 只有日期小差異：頁面顯示 2026-08-20，報告寫 08-19，應是時區造成。
   - 安裝位置和有沒有樞軸，文字裡都沒寫，維持 UNVERIFIED。
   - 來源：https://www.thingiverse.com/thing:7398135

4. **Kepler 建議「KV 低於 280、最多 6S LiPo 或 7S 18650、限流約 14 A」→ CORRECTED（出處錯，背景也要補）**
   - 這段原文其實在開發帖 84905 的 page-5，不在報告引用的販售帖 86961。
   - 那個 14 A 是 KU65 電動車控制器的限流，7S 時峰值約 350 W。
   - Kepler 後來改用 VESC，在販售帖 page-10 寫「15A Battery 30A motor, 6S or 7S is the sweet spot」。
   - 販售帖 page-8 又說，用 7S 或 8S 時「keep motor kv… no higher than 200kv」。
   - 他也寫「A 63-74 doesn't fit the drive」，這句是針對他自己的機構。
   - 來源：https://endless-sphere.com/sphere/threads/kepler-friction-drive-comes-of-age.84905/page-5 、https://endless-sphere.com/sphere/threads/kepler-bottom-bracket-friction-drive-for-sale-finally.86961/page-10

5. **Piotr F-drive：底座和 PAS 留在每台車上，電池和馬達加控制器可拔下換車；5065 270kV；散熱器水管；app_fdrive.c 有 attach_time_ms 等參數；用倒踩 PAS 解除 → CONFIRMED，授權要更正**
   - `friction_drive` 分支存在。檔案裡確實有 `attach_time_ms`、`cool_down_time_ms`、`attempt_count_limit`、`speed_goal_kmh`，也有 `FEVENTS_TURN_BACK_DET`。
   - 授權：repo 的 license 欄位是 null，但檔案開頭是 GPL-3.0 宣告，應視為 GPL-3.0。
   - 報告漏掉兩點：
     - 這支程式依賴作者自製的雙向 PAS 編碼器（`app_pas_encoder`）。
     - 它是 2020 年左右的 VESC 韌體 fork，要移植到 Flipsky 目前的 FW 6.06 需要改寫。
   - 來源：https://piotrstrzalka.github.io/2021/01/31/fdrive-e-bike-conversion-system.html 、https://github.com/PiotrStrzalka/bldc/blob/friction_drive/applications/app_fdrive.c

6. **Macaca #3：CC BY、兩條 1.2 mm 拉簧加束帶 → CONFIRMED**
   - 扣件清單：M8×60 一支、M3×30 兩支、M4×35 四支、M4 防鬆螺帽四顆。
   - 馬達只附 Banggood 連結，型號仍是 UNVERIFIED。
   - 來源：https://www.thingiverse.com/thing:2271941

7. **MakerWorld #3104448：非開放授權、約 443 g、作者建議 PETG 或 PA6-CF → CONFIRMED**
   - 授權是 SDFL-C，發布日 2026-07-28。
   - 443 g 的組成是 PA6-CF 354 g、PETG 46 g、TPU 43 g。
   - 有 TPU 件，可能是滾輪套，並附一份「单车助力.pdf」。這兩點報告漏了；驅動方式仍不明。
   - 來源：https://makerworld.com/zh/models/3104448-bike-booster

8. **「48 V 遠超過 250 W 法規級」→ CORRECTED：台灣法規沒有 250 W 這個功率上限**
   - 依道路交通管理處罰條例第 69 條，電動輔助自行車要同時符合：
     - 經型式審驗合格
     - 以人力為主、電力為輔
     - 最大行駛速率每小時 25 公里以下
     - 車重 40 公斤以下
   - 第 72 條的罰則：
     - 慢車未經核准擅自變更裝置：罰 300–1,200 元。
     - 電動輔助自行車擅自增減或變更電子控制裝置：罰 3,600–7,200 元，並禁止行駛。
   - DIY 改裝拿不到型式審驗，所以法律上不算電動輔助自行車。
   - 來源：https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=K0040012&flno=69 、https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=K0040012&flno=72

9. **「零件在台灣能否買到：UNVERIFIED」→ 已部分查證，露天確定買得到**
   - 6374 170KV：露天賣場 NT$1,599–2,365，分無感和有感版，從海外出貨約 7–9 天。https://www.ruten.com.tw/item/22634428969825/
   - 另有多個標「台灣現貨」的 N5065 / 6354 / C6374 賣場，例如 https://www.ruten.com.tw/item/22611256739925/
   - VESC 類控制器：露天有 Makerbase 75V100A、MKS 84100HP、VESC 6.7 等，例如 https://www.ruten.com.tw/item/22603992088278/
   - Flipsky 75100 Pro 在露天沒查到，官網價 US$89（V1）或 US$98（V2.0）。
   - 蝦皮和淘寶未查。

10. **BoosterPack：Cults3D 售價 US$3、CULTS PU 授權、夾具 21–39 mm → UNVERIFIABLE**
    - Cults3D 被 Cloudflare 擋（403），Instructables 連線被重設，兩邊都沒讀到內容。

**報告漏掉、設計會直接用到的重要缺口**

- **6374 馬達安裝尺寸（Flipsky 官方圖）**
  - 外殼 Ø63 mm、長 74 mm。
  - 固定孔：4×M4，孔位圓直徑 44 mm（±0.05），**螺孔深只有 5 mm**，螺絲要算好長度。
  - 軸有兩種：8 mm 圓軸附鍵槽（伸出 34 mm，全長 108 mm），或 10 mm D 軸（伸出 25 mm）。
  - 重 0.98 kg、14 極、3–12S、最大電流 85 A，Flipsky 售價 US$87。
  - 便宜的中國 6374 尺寸可能不同，到貨要實際量。
  - 來源：https://flipsky.net/products/flipsky-bldc-belt-motor-battle-hardened-6374-140kv-170kv-190kv-3500w-for-electric-skateboard
- **比較輕的馬達選項**
  - Flipsky 6354：Ø63×54 mm，同樣用 M4。
  - Flipsky 5065：實際 Ø49×63.5 mm，重 0.475 kg，有感測器，US$56.8。
  - 快拆主機重量有限，以 Kepler 約 14–15 A 的經驗，6374 對 25 km/h 等級來說偏大。
- **Flipsky 75100 Pro V2.0**
  - 尺寸 103×58×27.7 mm，電壓 14–84 V，連續 100 A，ERPM 上限 150000。
  - 輸入介面為 PPM、ADC、NRF、UART。商品頁沒提到 PAS。
  - 官方警告：韌體 5.3 以上要關掉 phase filter，否則會損壞電變。
  - 來源：https://flipsky.net/products/flipsky-75100-pro-v2-0-with-aluminum-pcb-based-on-vesc-for-electric-skateboard-electric-scooter-ebike-speed-controller
- **25 km/h 限速換算**
  - 用 Ø63 滾輪，25 km/h 約等於 2,105 rpm；6374 是 7 對極，換成 ERPM 約 14,700。
  - JK 的配置（170 kv、48 V）空載約 8,160 rpm，滾輪表面速度約 97 km/h。
  - 結論：必須在 VESC 設定最大 ERPM，或改用低 KV、低電壓。
- **MikeKaiser 的擺臂原本就需要彈簧**
  - SCAD 註解說自由擺臂需要彈簧加上止轉擋塊。
  - 報告第五節第 2 點說「軸承夠順可省彈簧」，出自 Kepler 2021 版，兩者要分清楚。
