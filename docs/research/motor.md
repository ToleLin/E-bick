# 研究報告：motor

# 摩擦驅動助力器：馬達、滾輪、ESC 選型報告

## 0. 結論

- **主推：B 架構，10S 36V。** 小滾輪（Ø35 mm）裝在馬達軸上，軸外側再加一顆 608 軸承支撐。馬達用 Flipsky 6354 140KV 有感（8 mm 圓軸長軸 30 mm 版），控制器用 Makerbase MKSESC MINI V6.7 (Pro) 50A VESC。
  - 80% 空載轉速對應 26.6 km/h，再用 VESC 限速 25 km/h。
  - 6% 坡 12 km/h：相電流約 15.5 A，銅損約 39 W，電池電流約 7 A。
  - 馬達 + 控制器約 NT$4,500–4,700，不含運費。
- **最簡單、最像市售品的做法：A 架構，5S 18V。** Flipsky 6374 140KV 的外殼直接當滾輪，外面包 3 mm 橡膠或 TPU 套，總直徑 Ø69 mm。80% 空載對應 26.2 km/h。缺點是爬坡銅損約 77 W，馬達也直接被輪胎甩起的水噴到。
  - 市售的呂布雲輪 LVBU 就是這種做法：36V 250W 直驅、加厚橡膠圈（宣稱壽命 5000 km）、馬達 1 kg。
- **省錢組合：** 露天的 N5065 270KV 有感（NT$1,529）+ Makerbase MINI V6.7 Pro（NT$2,309），共 NT$3,838。用 5S 配 Ø35 mm 滾輪，80% 空載對應 25.7 km/h。這顆的安裝孔距沒有查到資料，到貨要自己量。

## 1. 物理計算（自己算的，程式放在 scratchpad\calc\*.py）

假設條件：
- 人加車 85 kg，空氣密度 1.2。
- 滾動阻力係數 Crr：公路 0.006（IHPVA 範例值 https://www.ihpva.org/projects/tools/CrrMeas.doc ）；城市車或登山車 0.010（BRR 實測 38–47 mm 胎約 0.0064–0.0069，https://forums.electricbikereview.com/posts/710047/ ）。
- 直立騎姿 CdA 0.45 m²（https://www.bestbikesplit.com/cda-aerodynamic-drag-coefficient-cycling ）；城市車用 0.55。

**1-1 輪胎接地需要的推力**

滾輪接觸的是輪胎外緣，半徑和地面接觸點相同，所以滾輪切向力約等於推進力。

| 情境 | 推力 F (N) | 功率 (W) |
|---|---|---|
| 平路 25 km/h，公路 | 18 | 125 |
| 平路 25 km/h，城市/MTB | 24 | 168 |
| 250 W @ 25 km/h（設計上限） | 36 | 250 |
| 6% 坡 12 km/h，公路 / MTB | 58 / 62 | 193 / 206 |
| 8% 坡 10 km/h，MTB | 77 | 215 |

**1-2 25 km/h 時滾輪要多快、扭力多大**

| 滾輪直徑 (mm) | 30 | 35 | 40 | 50 | 55 | 63 | 69 |
|---|---|---|---|---|---|---|---|
| 轉速 (rpm) | 4421 | 3789 | 3316 | 2653 | 2411 | 2105 | 1922 |
| 推力 36 N 時扭力 (N·m) | 0.54 | 0.63 | 0.72 | 0.90 | 0.99 | 1.13 | 1.24 |
| 推力 58 N 時扭力 (N·m) | 0.87 | 1.01 | 1.16 | 1.45 | 1.59 | 1.83 | 2.00 |

如果要讓「80% 空載轉速 = 25 km/h」，各電壓需要的 KV：

| 滾輪直徑 | 5S 18V | 10S 36V | 12S 43.2V |
|---|---|---|---|
| Ø35 mm | 263 KV | 132 KV | 110 KV |
| Ø69 mm | 133 KV | 67 KV | 56 KV |

**1-3 摩擦係數 μ（滾輪對輪胎沒有正式量測資料，以下是設計假設）**

- 乾燥：
  - Engineering Toolbox：橡膠對橡膠 1.16；橡膠對乾混凝土 0.6–0.85；橡膠對乾柏油靜摩擦 0.9、動摩擦 0.5–0.8。https://www.engineeringtoolbox.com/friction-coefficients-d_778.html
  - 有一篇大學部斜面實驗量到橡膠對鋁 0.89，來源品質低。https://www.ukdr.uplb.edu.ph/etd-undergrad/10416
  - **設計值：μ_dry = 0.6。**
- 潮濕：
  - Engineering Toolbox：橡膠對濕柏油 0.25–0.75；濕胎對濕路面 0.2。
  - 論壇經驗（非量測）：滾花鋁滾輪乾的時候很好，濕了就打滑。https://endless-sphere.com/sphere/threads/front-wheel-friction-drive.71252 、https://endless-sphere.com/sphere/threads/commuter-booster-1kg-friction-drive.22187/post-584767
  - 專利 US10279865 也提到濕胎會打滑，砂紙類表面雖然 μ 高，但會大幅加速輪胎磨耗。https://patents.google.com/patent/US10279865
  - PU 碰水後 COF 會下降。https://gallaghercorp.com/polyurethane-coefficient-of-friction/
  - **設計值：橡膠或 TPU 套 μ_wet = 0.3；滾花鋁 μ_wet = 0.2。**

**1-4 需要的正向力 N = F × 1.3 / μ（N）**

| 推力 F | μ=0.8 | μ=0.6 | μ=0.4 | μ=0.3 | μ=0.2 |
|---|---|---|---|---|---|
| 36 N（250 W @ 25 km/h） | 58 | 78 | 117 | 156 | 234 |
| 58 N（6% 爬坡） | 94 | 126 | 188 | 251 | 377 |
| 77 N（8% 爬坡） | 117 | 156 | 234 | 312 | 468 |

建議：彈簧預壓約 100–130 N，再把馬達擺臂的樞軸放在「驅動反扭力會把滾輪往輪胎壓」的一側（自增壓），讓正向力隨扭力升到約 250 N。專利 US8151924 就是彈簧預壓加上正向力隨扭力成比例增加。https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8151924

不建議長時間固定壓 250 N：輪胎在滾輪處的額外變形損耗大致和 N 成正比（這點是估計，沒有查證）。另外最好做撥桿或凸輪讓滾輪可以抬離，不用助力時就沒有拖滯。

**1-5 軸承負載與 L10 壽命（概算）**

- 6374 前軸承據論壇說是 698ZZ，後軸承沒查到。https://electric-skateboard.builders/t/maytech-motor-bearings-size/71947
- 額定動負載：MISUMI 經濟款 698ZZ 1131 N；608ZZ 約 3.3 kN（NMB 3297 N / Timken）。https://th.c.misumi-ec.com/book/THA_EconomySeries_e-catalog2025/files/basic-html/page797.html 、https://product.minebeamitsumi.com/en/product/category/bearing/miniature_small/parts/608ZZNRSD06.pdf

| 配置（N = 250 N 濕地全扭力） | 最重那顆軸承的負載 | L10 壽命 |
|---|---|---|
| A：外殼當滾輪，負載落在內部兩軸承之間（約 0.6N） | 150 N | 698 約 3,700 h |
| B：滾輪懸臂在軸上（a=17 mm，軸承跨距假設 30 mm，**未驗證**），前軸承約 1.57N | 392 N | 698 約 **105 h**（不可用） |
| B + 外側 608 支撐（每顆約 0.5N） | 125 N | 698 約 3,260 h；608 約 81,000 h |

結論：B 架構一定要加外側軸承。

## 2. 架構比較

| 項目 | A：外殼就是滾輪（6374/6354/5065 外加套） | B：滾輪裝在軸上 + 外側 608 | B'：獨立滾輪軸，用皮帶傳動 |
|---|---|---|---|
| 零件數 | 最少，最像 LVBU/Rubbee 的外觀 | 多一顆 608 和一個滾輪 | 最多（皮帶、兩個皮帶輪、兩顆軸承） |
| 扭力和銅損 | 直徑 69 mm，扭力大；6374 爬坡約 77 W，6354 約 150 W，5065 約 200 W | 直徑 35 mm，扭力約 1/2，銅損約 1/4（6354 約 39 W） | 有減速比，可以用小顆高 KV 馬達 |
| 熱 | 外殼轉動有風冷，但定子熱靠氣隙傳出去 | 馬達包在殼裡散熱差，但發熱本來就少 | 同 B |
| 進水進砂 | 差：外殼就在輪胎甩水的路線上，6374/6354 官方沒標 IP | 好：馬達可以藏在 PETG-CF 殼裡 | 好 |
| 軸承負載 | 中等，壽命 OK | 有外側軸承就很低 | 低 |
| 噪音 | 主要是滾花或胎紋噪音 | 同左，外加軸承 | 多了皮帶噪音 |
| 換滾輪材質 | 要整圈重套 | 列印 TPU 或鋁芯包膠就能換 | 同 B |

**選 B 當主推的理由：** 銅損和直徑平方成正比，同一顆馬達用 Ø35 滾輪比 Ø69 少約 4 倍銅損，馬達又能藏在殼裡防潑水。

## 3. 各組合在 80% 空載轉速時的車速（km/h，標稱電壓 5S=18V、10S=36V、12S=43.2V）

| 馬達 / KV | 滾輪直徑 | 5S | 10S | 12S |
|---|---|---|---|---|
| 6374/6354 140KV | 63（外殼直接用） | 23.9 | 47.9 | 57.5 |
| | **69（外殼 + 3 mm 套）** | **26.2** | 52.4 | 62.9 |
| | **35** | 13.3 | **26.6** | 31.9 |
| | 40 | 15.2 | 30.4 | 36.5 |
| 6374 170KV（Flipsky 或副廠） | 69 | 31.8 | 63.7 | 76.4 |
| | 35 | 16.2 | 32.3 | 38.8 |
| 6374 190KV | 69 | 35.6 | 71.2 | 85.4 |
| | 35 | 18.1 | 36.1 | 43.3 |
| 6384 150KV | 69 | 28.1 | 56.2 | 67.4 |
| | 35 | 14.3 | 28.5 | 34.2 |
| Flipsky 5065/5055 200KV | 55（外殼 + 套） | 29.9 | 59.7 | 71.7 |
| | 35 | 19.0 | 38.0 | 45.6 |
| | 30 | 16.3 | 32.6 | 39.1 |
| 副廠 N5065 / N6354 270KV | **35** | **25.7** | 51.3 | 61.6 |
| 5065 輪轂馬達 64KV 附 70 mm PU 輪 | 70 | 12.2 | 24.3 | 29.2 |

超過 25 km/h 的組合都可以用 VESC 限速，但占空比越低，同樣推力需要的電池電流不變、相電流反而沒有優勢。

主要組合的估算（銅損用官方曲線的相電阻 ×2；鐵損用官方空載電流按 n^1.5 換算）：

| 組合 | 巡航 36 N @ 25 km/h | 爬坡 58 N @ 12 km/h |
|---|---|---|
| B：6354-140KV / Ø35 / 10S | 相電流 9.6 A，效率 0.90，電池 8 A | 相電流 15.5 A，銅損 39 W，電池 7 A |
| B：6374-140KV / Ø35 / 10S | 9.4 A，效率 0.87（鐵損 29 W 偏大） | 15 A，銅損 20 W |
| A：6374-140KV / Ø69 / 5S | 18.5 A，效率 0.86，電池 17 A | 30 A，銅損 77 W，電池 16 A |
| A：6354-140KV / Ø69 / 5S | 19 A，效率 0.80 | 31 A，銅損 150 W（太大） |

馬達常數 Km（N·m/√W）：6374-140 = 0.228；6354-140 = 0.163；5055-200 = 0.101。

## 4. 馬達規格與購買管道

圖面都從 Flipsky 官方產品頁下載。

| 型號 | 尺寸 | **安裝孔（CAD 用）** | 軸 | 電氣規格 | 重量 | 價格 |
|---|---|---|---|---|---|---|
| **Flipsky 6374**（140/170/190KV，有感） | Ø63 × 74，含軸總長 108±0.5 | **4×M4，深 5，PCD Ø44**（另有論壇說舊版同時有 Ø30 孔，**未驗證**） | Ø8 圓軸外露 34（根部 Ø10 台階），鍵槽寬 3、長 20，附鍵；另有 10 mm D 軸版 | 3–12S，最大 85 A / 3500 W / 8 N·m；14 極。140KV 曲線：Kt 67.2 mNm/A、相電阻 0.0436 Ω、空載 1.5 A @ 48V | 0.98 kg | 官網 US$87（不含皮帶輪） |
| **Flipsky 6354**（140/170/190KV，有感） | Ø63±0.5 × 54±0.5 | **4×M4，深 5，PCD Ø44.00±0.05** | Ø8 短軸 24 / **長軸 30**，鍵槽 3×14；另有 10 mm D 軸 | 4–14S，最大 65 A / 2450 W / 7 N·m。140KV 曲線：Kt 65.4、相電阻 0.08 Ω、空載 0.7 A @ 36V、最高效率 92.3% | 0.56 kg（經銷商標示，**官方未列**） | 官網 US$71 |
| **Flipsky 5065** 200KV | Ø49.2 × 63.5±0.3 | **4×M4，深 5，PCD Ø38±0.1，孔在 45° 位置、每 90° 一孔** | Ø8 D 軸，削平面 6.5、平面長 18，外露 24.5，距端 10 mm 有 Ø3.2 橫孔 | 6–12S；額定 1000 W / 21 A / 0.95 N·m，最大 1800 W / 38 A / 1.7 N·m；有感；12N14P | 0.475 kg | 官網 US$56.8 |
| Flipsky 5055 200/120KV | Ø49.2 × 55±0.3 | 與 5065 相同 | 與 5065 相同 | 6–12S；額定 700 W / 19 A，最大 31 A；IP54。200KV 曲線：Kt 45.9、相電阻 0.103 Ω | 0.42 kg | 官網 US$43 |
| Flipsky 6384 | Ø63 × 84 | 圖面已下載，孔位未判讀 | Ø8 × 30 | 4–14S，最大 95 A / 4000 W / 9 N·m | 1.3 kg | 官網 US$113 |
| Maytech MTO6374-170-HA-C（密封款） | — | 官方頁沒列，**未驗證** | Ø8 × 26 | 3–12S，額定 60 A、最大 65 A，3550 W；頁面寫 sealed splashproof（IP54 只出現在圖片 alt 文字） | 未列 | US$82.40，頁面顯示缺貨 |

Flipsky 6374/6354 頁面都註明用 M4 螺絲固定。

**台灣露天（API 實際抓到的標價，賣家大多是代購，出貨可能較慢）：**

| 商品標題（節錄） | 規格選項與價格 | 網址 |
|---|---|---|
| 【台灣現貨】板車外轉子無刷大電機馬達 N5065 6354 N6364 C6374 皮帶麥太保 | N5065-270KV 無感 1,381 / 有感 1,529；N6354-270KV 無感 1,940 / 有感 2,043；6374-170KV 無感 2,126 / 有感 2,228；N6364-200KV 有感 2,146 | https://www.ruten.com.tw/item/show?22543223395022 |
| 【可開統編】6374 170KV無刷馬達滑板車馬達衝浪板電機… | 無感 2,100 / 有感 2,220 | https://www.ruten.com.tw/item/show?22632318875322 |
| 滑板車外轉子無刷電機 8352 80kv 帶輪皮 6374 170kv 5055 330kv 6354 270kv | 6374-170KV 2,105；6354-270KV 2,115；5065-270KV 1,545；6384-150KV 2,524（有感無感未標） | https://www.ruten.com.tw/item/show?22638688010015 |
| 台灣現貨6374 170KV無刷電機無傳感器… | 1,388（無感） | https://www.ruten.com.tw/item/show?22512978152093 |
| 【萬品惠】電動滑板用Flipsky…戰鬥硬化升級6354 140 KV | 5,124（正牌 Flipsky，貴） | https://www.ruten.com.tw/item/show?22643975192594 |
| 【滿額免運】5065輪轂低轉速電機…帶霍爾一體輪70…帶PU輪 | 64KV 1,358；賣家寫 24V/10A/120W、1440 rpm、70×52 | https://www.ruten.com.tw/item/show?22545392912262 |
| 呂布雲輪 腳踏車助力摩擦輪（市售對照組） | 摩擦輪+KF控制器 7,365；整套含 F30 電池 17,606–19,003 | https://www.ruten.com.tw/item/show?22631285885965 |

- 副廠 N5065、6354、6374 的安裝孔、軸徑、重量都**未驗證**。CAD 的轉接板建議開長孔，同時涵蓋 PCD 25/30/38/44。論壇說 50 mm 級多半是 25 或 30（https://electric-skateboard.builders/t/sk3-245kv-measurements-for-motor-mount/7511 ）。
- 蝦皮：搜尋引擎沒有索引到 6374/6354 馬達的商品頁，**價格未驗證**。
- 淘寶：只有聚合頁摘要，一般 6374 約 ¥140–210，翻天 Flipsky 6374 約 ¥568，**未驗證**（https://www.1688.com/huo/b-36333734CEDECBA2B5E7BBFA.html ）。

## 5. 控制器（ESC）

| 型號 | 電壓 | 連續 / 峰值電流 | 尺寸 (mm) | 重量 | 介面 | ERPM 上限 | 價格 |
|---|---|---|---|---|---|---|---|
| **Makerbase MKSESC MINI V6.7 (Pro)** | 8–60V（3–13S，安全 3–12S） | 50 / 150 A | **67×39×20** | — | USB/CAN/UART；輸入支援 PPM/ADC/NRF/UART/SPI/IIC | 150k | 露天 **NT$2,309**（zhuhongtong）https://www.ruten.com.tw/item/show?22641852738525 ；NT$2,430（已售 4）https://www.ruten.com.tw/item/show?22521646076876 |
| Flipsky Mini FSESC6.7 PRO 70A | 14–60V（4–13S，安全 4–12S） | 70 / 200 A | 67×39×18.7（含散熱片） | 130 g | USB/CAN/UART/SPI/IIC；PPM/ADC/NRF/UART；Hall/ABI/AS5047 | 150k | 官網 US$57 |
| Flipsky / Makerbase Mini FSESC 4.20 50A | 8–60V（3–13S） | 50 / 150 A | 67×39×18.3（PCB 39×46×17.4） | 80 g | 輸入：PWM（官方頁只寫這項，其餘介面**未驗證**） | **60k**（7 對極約 8,500 rpm 上限，對本案夠用） | 官網 US$56；露天 NT$3,465 https://www.ruten.com.tw/item/show?22640764206010 |
| Makerbase MKSESC 75100（V1/V2） | 14–84V（4–20S） | 100 / 120 A | 103×58×18.5 | — | USB/CAN/UART；PPM/ADC/NRF/UART | 150k | 露天 NT$3,029（nw3660，版本未標）https://www.ruten.com.tw/item/show?22547496681835 ；蝦皮小可洋的店 V2（價格未驗證）https://shopee.tw/%E5%B0%8F%E5%8F%AF%E6%B4%8B%E7%9A%84%E5%BA%97Makerbase-VESC-75V100A-V2%E6%9C%AC%E5%82%91%E6%98%8E%E9%9B%BB%E8%AA%BF%E8%88%AA%E6%A8%A1FOC%E7%84%A1%E5%88%B7%E9%9B%BB%E6%A9%9FVESC75-i.789345437.27433687849 |
| Flipsky 75100 | 14–84V | 100 / 120 A | 85×50.7×33.8 | — | USB/CAN/UART；PPM/ADC/NRF/UART；BEC 5V/1A | 150k | 官網 US$65 |

- **踏頻助力（PAS）：** VESC 韌體內建 app_pas，支援踏頻型和扭力型（https://github.com/vedderb/bldc/blob/master/applications/app_pas.c ）。預設把 PAS1/PAS2 接在 **UART 的 RX/TX 腳**（hw.h：`#define HW_PAS1_PORT HW_UART_RX_PORT`，https://github.com/vedderb/bldc/blob/master/hwconf/hw.h ），所以 PAS 和 UART 藍牙模組不能同時用。
- **非 VESC 的便宜選項：**
  - 露天「350W 5-36V 三相 BLDC 控制器（有霍爾/無霍爾）」NT$490，https://www.ruten.com.tw/item/show?22113405865692 。上限 36V，10S 充滿 42V 不能用，只適合 5S–8S，也沒有 PAS 邏輯。
  - 「智能無刷雙模控制器（無霍爾）36/48V 350W」NT$500，https://www.ruten.com.tw/item/show?22517278879143 。這是為低轉速輪轂馬達設計的，能不能跑本案約 3–5 萬 ERPM 的外轉子**未驗證**。
  - RC 車電調 FVT 120A 2–6S 有感/無感 NT$2,555–2,755，https://www.ruten.com.tw/item/show?22638658435327 。只吃 PWM 舵機訊號，要另外用 MCU 做 PAS。
- **無感控制器為什麼會卡：** 靜止時沒有反電動勢可以偵測，只能開迴路強制啟動，負載大就會抖或失步（https://vedder.se/2014/08/startup-torque-on-sensorless-bldc-motors/ 、https://applied-ee.github.io/embedded/docs/motor-control/brushless-motors/sensorless-back-emf/ ）。不過摩擦驅動的滾輪一直貼著輪胎，車子一動馬達就在轉。只要設定「車速超過約 5 km/h 才介入」，無感 FOC 就能接手。但原地坡道起步還是需要霍爾感測器，所以建議買有感版。

## 6. 推薦組合與搜尋關鍵字

**主推（10S 36V）：** Flipsky 6354 140KV 有感，8 mm 長軸，不含皮帶輪，US$71（以 1 USD ≈ 31 TWD 粗估約 NT$2,200，匯率未查證，未含運費與關稅）。搭 Makerbase MINI V6.7 Pro NT$2,309。

**主推的 5S 版本：** 改用露天 N6354-270KV 有感 NT$2,043，滾輪同樣 Ø35 mm（25.7 km/h）。或向 Flipsky 下單時備註客製 KV 約 260。

**A 架構備案（5S）：** Flipsky 6374 140KV US$87，外殼包 3 mm TPU 95A 或橡膠套，搭 MINI V6.7。馬達部分要另外做擋水罩。

**省錢組合：** N5065-270KV 有感 NT$1,529 + MINI V6.7 Pro NT$2,309 = **NT$3,838**。5S、Ø35 滾輪。爬坡時建議把馬達電流限制在約 30 A。

**搜尋關鍵字：**
- 蝦皮／露天：`6354 無刷 有感 140KV`、`6374 170KV 有感`、`N5065 270KV 有感`、`Makerbase VESC MINI V6.7`、`班傑明電調 VESC`、`Flipsky Mini FSESC`、`呂布雲輪 摩擦輪`
- 淘寶：`翻天 Flipsky 6354 电机`、`6354 外转子无刷电机 有感 140KV`、`5065 无刷电机 270KV 有感 滑板`、`Makerbase VESC MINI 6.7 本杰明电调`、`吕布云轮 摩擦轮 助力`

**法規：** 電動輔助自行車的定義是「經型式審驗合格、以人力為主電力為輔、最大速率每小時 25 公里以下、車重 40 公斤以下」（道交條例第 69 條，https://www.dsps.chc.edu.tw/storage/074686/posts/179/files/b1.pdf ）。DIY 改裝不會有型式審驗。

## 7. 還沒確認、要自己量或測的項目

- 副廠馬達的安裝孔 PCD、軸徑和鍵槽。
- 6354 的重量（官方沒列）。
- 6374/6354 的後軸承型號和內部軸承跨距（影響 1-5 的懸臂計算）。
- Maytech 6374 的孔位。
- 滾輪對輪胎的實際 μ：建議用 TPU 95A 印幾個滾輪套，拿彈簧秤在乾、濕兩種狀態實測。
- 蝦皮和淘寶的即時價格。
- 便宜 e-bike 控制器能不能跑高 ERPM 外轉子。

## 8. 本機已下載的圖面與曲線（可直接拿去畫 CAD）

資料夾：`C:\Users\user\AppData\Local\Temp\claude\331f5373756cbd02\c95f4efe-559a-4251-aa6f-aaacc223e7e4\scratchpad\`

- `img\d6374_1.jpg`、`img\d6374_2.jpg`
- `img\d6354_2.jpg`、`img\d6354_3.jpg`
- `img\d5065.jpg`、`img\d5055.png`、`img\d5048.jpg`、`img\d6384.jpg`
- 馬達曲線：`img\c6374_190.pdf`、`img\c6374_140.pdf`、`img\c6354_140.pdf`、`img\c5055_200.pdf`
- Makerbase 手冊：`mks\mini67.pdf`、`mks\m75100v2.pdf`、`mks\v420.pdf`
- 計算程式：`calc\phys.py`、`calc\kv.py`、`calc\loss.py`、`calc\fin.py`
- 露天查詢腳本：`fc\ruten.py`、`fc\rspec.py`

## 主要來源

- Flipsky 馬達頁：https://flipsky.net/collections/hobby-motors-for-esk8-ebike-efoil/products/flipsky-bldc-belt-motor-battle-hardened-6374-140kv-170kv-190kv-3500w-for-electric-skateboard 、…/flipsky-bldc-belt-motor-battle-hardened-6354-140kv-190kv-2450w-for-electric-skateboard 、…/flipsky-sensored-outrunner-brushless-dc-motor-battle-hardened-5065-200kv-1800w 、…/lipsky-sensored-outrunner-brushless-dc-motor-battle-hardened-5055-200kv-1500w
- 6374 圖面：https://cdn.shopify.com/s/files/1/0011/4039/1996/files/6374.1_1024x1024.jpg
- 6374 190KV 曲線：https://cdn.shopify.com/s/files/1/0011/4039/1996/files/6374-190KV-48V.pdf
- 6354 140KV 曲線：https://cdn.shopify.com/s/files/1/0011/4039/1996/files/6354-140KV-36V.pdf
- Flipsky ESC：https://flipsky.net/collections/v4-series/products/mini-fsesc4-20-50a-base-on-vesc%C2%AE-4-12-with-aluminum-anodized-heat-sink 、https://flipsky.net/collections/v6-series/products/mini-fsesc6-7-pro-70a 、https://flipsky.net/collections/v75-series/products/flipsky-75100-75v-100a-single-esc-based-on-vesc-for-electric-skateboard-electric-scooter-ebike-speed-controller
- Makerbase 手冊：https://github.com/makerbase-motor/VESC-MKS （02_Makerbase VESC related documents）
- Maytech：https://maytech.cn/products/brushless-hall-sensor-motor-mto6374-170-ha-c
- 其餘露天、蝦皮、Engineering Toolbox、專利、論壇、法規的網址已在各段內文標出。


---

# 查證結果：motor

## 事實查核結果（主題：馬達／滾輪／ESC）

說明：這次查核做到一半時，整個流程的 WebSearch 額度用完了。之後只靠 WebFetch 讀已知網址、直接下載官方圖面與 PDF、呼叫露天 API、讀 VESC 原始碼來查。所以蝦皮和淘寶價格、LVBU 規格、698ZZ 軸承這幾項沒有再查。

### 一、逐項查核

**1. Flipsky 6354 安裝孔：4×M4、深 5、PCD Ø44.00±0.05，外形 Ø63×54 → CONFIRMED**
- 來源：官方圖面 https://cdn.shopifycdn.net/s/files/1/0011/4039/1996/files/6354.3_b733fd59-a2f4-4602-bd78-27ad4590b5b0_1024x1024.jpg 與 6354.2 圖面。
- CAD 要注意：霍爾線和相線是從馬達「前端（安裝面）」的一個凸座往徑向出線，凸座超出 Ø63 的外圓。轉接板要留缺口，報告沒有提到。

**2. Flipsky 6354「8 mm 長軸 30 mm、鍵槽 3×14」→ CORRECTED**
- 正確值：
  - 長軸外露 **34.0±0.5 mm**，根部有 Ø10 台階，Ø8 段長 **26 mm**，鍵槽 **3 寬 × 20 長**。
  - 「3×14」是**短軸**的數字（短軸外露 24，Ø8 段 23）。
- 產品頁文字寫 30 mm，但官方圖面和尺寸照片都標 34 mm（總長 88）。
- 來源：上面的 6354.3 圖面；https://cdn.shopifycdn.net/s/files/1/0011/4039/1996/files/2_92c73140-76e5-4fce-b093-c5d66a7dd7ce_1024x1024.jpg
- 對設計的影響：B 架構的「滾輪 + 外側 608（寬 7 mm）」只能放在 26 mm 的 Ø8 段上，所以**滾輪寬度最多約 18–19 mm**。懸臂距離 a 要用這個數字重算。

**3. Flipsky 6354 電氣規格：4–14S、65 A、2450 W、7 N·m、US$71（不含皮帶輪）→ CONFIRMED**
- 140KV/36V 曲線的 Kt 65.4 mNm/A、相電阻 0.08 Ω、空載 0.7 A、最高效率 92.3% 也都對得上。
- 補充 1：產品頁標的電阻是 0.053 Ω，和曲線的 0.08 Ω 不一致。報告用 0.08 算，偏保守。
- 補充 2：曲線上 36 V 空載轉速是 **5500 rpm**，換算實際約 **153 KV**，不是 140。
  - 80% 空載配 Ø35 滾輪的車速應為約 **29.0 km/h**，報告寫 26.6 km/h，需要更正。
  - 雖然仍可以用 VESC 限速，但 KV 表要用實測值重算。
- 來源：https://flipsky.net/collections/hobby-motors-for-esk8-ebike-efoil/products/flipsky-bldc-belt-motor-battle-hardened-6354-140kv-190kv-2450w-for-electric-skateboard 、https://cdn.shopify.com/s/files/1/0011/4039/1996/files/6354-140KV-36V.pdf

**4. Flipsky 6374 → CONFIRMED**
- 尺寸：Ø63×74，含軸總長 108±0.5，4×M4 深 5，PCD Ø44。
- 軸：Ø8 外露 34，Ø10 台階，鍵槽 3×20。
- 價格：US$87（不含皮帶輪）；最大 85 A、3–12S。
- 140KV/48V 曲線：Kt 67.2、相電阻 0.0436 Ω、空載 1.5 A 都正確。48 V 空載 7000 rpm，換算實際約 146 KV。
- 產品頁沒有寫「有感」，但圖面畫了感測器線，可以視為有感。
- 來源：https://cdn.shopify.com/s/files/1/0011/4039/1996/files/6374.1_1024x1024.jpg 、https://cdn.shopify.com/s/files/1/0011/4039/1996/files/6374-140KV-48V.pdf

**5. Flipsky 5065 → CONFIRMED**
- 尺寸：PCD Ø38±0.1，孔在 45° 位置、每 90° 一孔，4×M4 深 5；Ø49.2×63.5。
- 軸：Ø8 D 軸，削平面 6.5、平面長 18，外露 24.5，距端 10 mm 有 Ø3.2 橫孔。
- 規格：0.475 kg、US$56.8。
- 補充：官方電壓是 **6–12S**。報告第 3 節表格裡 Flipsky 5065/5055 的「5S」欄位低於規格下限。
- 來源：https://cdn.shopify.com/s/files/1/0011/4039/1996/files/5065_346a6613-096a-4975-84f8-f701025bfbaf_1024x1024.jpg

**6. Makerbase MKSESC MINI V6.7：8–60V（3–13S，安全 3–12S）、50/150 A、ERPM 150k、67×39×20 mm、USB/CAN/UART、輸入 PPM/ADC/NRF/UART/SPI/IIC → CONFIRMED**
- 來源：官方手冊 https://raw.githubusercontent.com/makerbase-motor/VESC-MKS/main/02_Makerbase%20VESC%20related%20documents/MKSESC%20MINI%20V6.7%20Manual%20V1.0_002.pdf
- 補充：手冊型號是「MINI V6.7」，露天賣的是「MKSESC MINI V6.7 Pro」。Pro 版沒有另外的官方規格書。
- 補充：手冊寫 BEC 5V@1A。

**7. 露天價格 → CONFIRMED（API 即時查詢，2026-11-07）**
- MINI V6.7 Pro：NT$2,309（22641852738525），**已售 0**。
- 馬達賣場（22543223395022）各規格價格都正確：
  - N5065-270KV 有感 1,529、N6354-270KV 有感 2,043、6374-170KV 有感 2,228、N6364 有感 2,146。
  - 另有「紅N5065 帶槳座」1,632/1,735。
  - 這個賣場同樣**已售 0**。
- 呂布雲輪 7,365–19,003（22631285885965）正確。

**8. VESC PAS：腳位預設借用 UART RX/TX → CONFIRMED；「支援扭力型」→ CORRECTED**
- 腳位：hw.h 第 660–665 行確實是 `HW_PAS1_PORT HW_UART_RX_PORT`，所以 PAS 和 UART 藍牙不能同時用。
- 扭力型要硬體定義 `HW_HAS_PAS_TORQUE_SENSOR` 才會編譯進去。目前官方韌體只有 Luna M600（hwconf/luna/m600/hw_luna_m600.h）有定義。**MINI V6.7 這類通用硬體只能用踏頻型。**
- 來源：https://github.com/vedderb/bldc/blob/master/hwconf/hw.h 、https://github.com/vedderb/bldc/blob/master/applications/app_pas.c

**9. 法規：道交條例第 69 條，電動輔助自行車「經型式審驗合格、人力為主電力為輔、最大速率 25 km/h 以下、車重 40 kg 以下」→ CONFIRMED**
- 來源：https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=K0040012&flno=69

**10. 匯率「1 USD ≈ 31 TWD」→ CORRECTED**
- 臺銀 2026/11/07 牌告即期賣出 **32.84**。
- US$71 約 NT$2,330（不含運費與關稅）；US$87 約 NT$2,860。
- 來源：https://rate.bot.com.tw/xrt?Lang=zh-TW

**11. Mini FSESC 4.20：ERPM 60k、67×39×18.3 mm、80 g、US$56、輸入只寫 PWM → CONFIRMED**
- 來源：https://flipsky.net/collections/v4-series/products/mini-fsesc4-20-50a-base-on-vesc%C2%AE-4-12-with-aluminum-anodized-heat-sink

**12. 無法查證（UNVERIFIABLE）**
- LVBU 規格（36V 250W、橡膠圈 5000 km、馬達 1 kg）：官網連不上，額度也已用完。只有露天價格確認過。
- 6374 前軸承是 698ZZ：引用的論壇回 HTTP 530。
- 6354 重量 0.56 kg：官方只有沒標單位的 variant weight「1000」。
- 蝦皮與淘寶價格：沒有再查。

### 二、報告漏掉的重要問題

1. **VESC PAS 只能接雙霍爾（正交）PAS 感測器。**
   - 我讀 app_pas.c 推導的結果：只有在 PAS1/PAS2 往同一方向連續 4 次正交轉換、而且狀態到 3 時，才會算出踏頻。
   - 便宜的單霍爾 PAS 只有一條訊號線，另一條被上拉成固定高電位，方向計數會一直被歸零，**踏頻永遠是 0**。
   - 採購時要找「雙霍爾／雙訊號」PAS（訊號線 4 條）。這是從原始碼推導的，沒有實測。

2. **下坡反電動勢。**
   - 6354 實際約 153 KV、配 Ø35 滾輪時：滾輪貼著輪胎，車速超過約 36 km/h（36 V）到 42 km/h（10S 滿電 42 V），反電動勢就會高過電池電壓。這時電流會經 MOSFET 本體二極體不受控地回灌，造成制動或過壓。
   - 所以抬離機構不只是為了減少拖滯，**下長坡時一定要抬離**。也可以把滾輪改大或 KV 改低。

3. **法規罰則。**
   - 第 72 條第 1 項：慢車擅自變更裝置，罰車主 NT$300–1,200。
   - 第 72 條第 2 項：電動輔助自行車或微型電動二輪車「擅自增、減、變更電子控制裝置或原有規格」，罰 NT$3,600–7,200 並禁止騎乘。
   - 第 72-1 條：微型電動二輪車超過 25 km/h，罰 NT$900–1,800。
   - DIY 助力器上路至少會碰到第 72 條第 1 項。會不會被認定為「微型電動二輪車」而需要掛牌登記，**這次沒有查證**。
   - 來源：https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=K0040012&flno=72 、…&flno=72-1

4. **6354 的出線凸座在安裝面那一側（見第 1 項）**，座管夾與轉接板的 CAD 要避開它。

5. **露天兩個主力賣場（馬達、MINI V6.7 Pro）都是已售 0**，沒有成交紀錄可以參考，出貨與真偽有風險。另一個 MINI V6.7 Pro 賣場（22521646076876，NT$2,430）報告寫已售 4，這次沒有重查。

6. **KV 表要用實測空載轉速重算。** Flipsky 標稱 140KV，實際約 146–153 KV，所以報告第 3 節表格的車速都偏低約 5–9%。

驗證時下載的圖面、曲線、手冊放在 `C:\Users\user\AppData\Local\Temp\claude\331f5373756cbd02\c95f4efe-559a-4251-aa6f-aaacc223e7e4\scratchpad\fc_verify\`。
