# 研究報告：bike_standards

# 自行車尺寸標準、幾何與摩擦驅動接觸工程：研究報告（2026-11-07）

說明：標「（搜尋摘要）」的內容只讀到搜尋引擎摘要，沒有打開原頁面。標「計算」的是我用已引用的幾何數據自己推算的。標 UNVERIFIED 的是找不到可靠來源的。firecrawl 免費額度中途用完，我沒有去註冊帳號；Cyclingnews、eBay 部分頁面、Endless-Sphere 部分討論串都擋爬蟲。

---

## 1. 座管規格

### 1-1 圓管直徑與車種對應

| 直徑 (mm) | 常見車種 | 來源 |
|---|---|---|
| 25.4 (1") | 老美系車、BMX、一體曲柄車；部分新鋼管車 | [bikegremlin](https://bike.bikegremlin.com/3114/seat-post-diameter-sizes-standards/) |
| 26.0 / 26.8 / 27.0 | 老車、中低階車，例如 Schwinn Cimarron 1989 用 26.8 | [Sheldon Brown 資料庫](https://www.sheldonbrown.com/seatpost-sizes.html)（群眾提供）、bikegremlin |
| **27.2** | 最常見的公路車尺寸，用在高品質薄壁 1-1/8" 座管；Giant Escape 3 非碟煞版也是 27.2 | bikegremlin、[bikes.fan Escape 3 2023](https://bikes.fan/giant-escape-3-2023/) |
| 27.4 / 28 / 28.6 | 27.4 是舊 MTB 的加大規格，28 是法國老車，28.6 是英義早期鋼管 | bikegremlin |
| 30.0 / 30.4 / 30.8 | 少見；用在哪些車找不到可靠來源 | UNVERIFIED |
| **30.9 / 31.6** | 現代 MTB 主流，也是升降座管最常見的直徑 | bikegremlin、[NSMB](https://nsmb.com/articles/why-all-dropper-posts-should-be-349/) |
| **33.9** | Tern、Dahon 摺疊車（Link、Verge、Eclipse 系列） | [Tern 33.9 伸縮座管](https://www.ternbicycles.com/us/accessories/471/telescopic-seatpost-339)、[Perennial](https://www.perennialcycle.com/telescopic-seatpost-34-9mm-for-gsd-hsd.html) |
| **34.9** | 長行程 trail、enduro、電輔車的升降座管；Tern GSD/HSD | NSMB、Perennial |

**設計結論**：夾具範圍做 **25.4–34.9 mm** 就能涵蓋幾乎所有圓管。各家商品的支援範圍可以參考：
- Rubbee X：22–35 mm（[Consumer NZ](https://www.consumer.org.nz/articles/first-look-rubbee-x-e-bike-conversion-kit)）
- PikaBoost 2：25–35 mm（[手冊](https://manuals.plus/asin/B0FC61XQ7M.pdf)）
- engineerdog BoosterPack：21–39 mm（[engineerdog](https://engineerdog.com/2015/11/13/the-bicycle-boosterpack-kit-a-new-ultralight-portable-electric-assist/)）
- eBay 18V 款：只到 31.6 mm，等於放棄摺疊車的 33.9 和 34.9（[eBay](https://www.ebay.com/itm/127654453389)）

### 1-2 非圓形座管（D 形、氣動）
- **Giant D-Fuse**：Escape Disc、Defy 等車款使用。斷面約 30.2×25.2 mm（[零件商](https://westbrookcycles.co.uk/giant_rsp-am310d_d-form_atb_seatpost_for_small_bikes-33397)），只相容指定車架（[Giant](https://www.giant-bicycles.com/int/d-fuse-composite-seatpost)）。台灣很多 Giant 車都是這種，值得注意。
- 其他品牌：Cervélo SP24/SP33（[Excel](https://www.excelsports.com/cervelo-carbon-seatpost-sp33)）；Cannondale C1 Aero 27，用在 CAAD13、SuperSix Evo、Synapse（[Cannondale](https://www.cannondale.com/en/gear/components/seatposts/road-seatposts/c1-aero-27-seatpost-0mm-offset)）；Specialized Tarmac SL7/SL8 專用座管（[bike-components](https://www.bike-components.de/en/Specialized/S-Works-Tarmac-Carbon-Seatpost-p80050)）。
- PikaBoost 2、Blackburn 都明文不支援 D 形管。要支援的話只能做可換的 D 形橡膠內襯。

### 1-3 碳纖座管：不建議夾配件
- Topeak MTX BeamRack 手冊寫明：「not suitable or intended to be used with carbon fiber seatposts」（[手冊 PDF](https://fortnine.ca/assets/pdf/topeak/mtxbeamrackgb0506.pdf)）。
- Blackburn Interlock：不適用碳纖座管和非圓座管（[手冊](https://www.bellhelmets.com/on/demandware.static/-/Library-Sites-BellHelmets/en_US/dwbb2b4321/pdf/manuals-blackburn/Blackburn-Interlock-Seatpost-Rack-Manual.pdf)）。
- 摩擦助力商品也一樣：PikaBoost 2 不適用碳纖座管、D 形管、後避震車；ASUS Oxiis E250G1 不相容全避震車和碳纖座管（[Digital Trends](https://www.digitaltrends.com/outdoors/asus-made-an-e-bike-conversion-kit-compact-enough-to-slip-into-a-backpack/)）。
- 例外：Arkel 後架宣稱碳纖座管可用，但氣動碳管不行，載重上限 6 kg。它是靠座墊弓夾加 Santoprene 軟座管支架分擔受力（[Arkel](https://arkel.ca/products/randonneur-seat-post-rack)）。
- 車架端的鎖緊扭力參考：Ritchey 碳管上限約 6 N·m；MBR 建議上限 5 N·m 時只鎖到約 3 N·m（[MBR](https://www.mbr.co.uk/videos/maintenance-2/fix-slipping-seatpost?pid=334319)，搜尋摘要）。Cube 手冊要求不要在碳管上裝會施加機械壓力的夾具（[Cube](https://www.manualslib.com/manual/2034512/Cube-Litening-C-68-X.html?page=7)，搜尋摘要）。
- **建議**：規格上直接排除碳纖座管。替代方案是使用者改裝一支便宜的鋁座管專門配這台助力器。

### 1-4 升降座管（dropper）
- 上管是可動的密封面。Wolf Tooth 手冊寫明「Do not clamp stanchion」，刮傷會毀掉油封而且不保固（[Wolf Tooth](https://cdn.shopify.com/s/files/1/0230/9291/files/Wolf_Tooth_Resolve_Dropper_User_Manual_221129.pdf)，搜尋摘要）。RockShox Reverb 也有類似警告（論壇轉述，[mtbr](https://www.mtbr.com/threads/clamping-dropper-posts-in-workstands.1033762)）。
- Consumer NZ 判斷 Rubbee X 不太可能裝在升降座管上。
- **建議**：不支援升降座管。

### 1-5 外露座管長度（夾具可用的空間）
- PikaBoost 2 要求外露至少 50 mm（手冊）。
- 計算：外露長度 ≈ 座高 − 座管 C-T − 約 60 mm（座墊厚度加夾頭）。結果如下：

| 車型 | 外露長度估計 |
|---|---|
| 公路 56 | 約 143 mm |
| 礫石 M | 約 124 mm |
| 城市車 / 26" MTB | 約 200 mm |
| 29"、27.5" MTB | 約 220 mm |

- 經驗法則：外露長度約等於頭管長，斜上管車架外露更多（[BikeForums](https://www.bikeforums.net/road-cycling/1192665-determining-seat-post-length.html)，軼聞）。
- **設計目標**：夾具本體高度 ≤ 45 mm，最少需要 60 mm 外露長度。

---

## 2. 後輪、輪胎與幾何

### 2-1 ISO/ETRTO 胎圈座直徑（BSD）
資料來源：[Sheldon Brown tire sizing](https://www.sheldonbrown.com/tire-sizing.html)

| BSD | 俗稱 | 用途 |
|---|---|---|
| 406 | 20" | 摺疊車、BMX、童車 |
| 451 | 20 x 1-1/8 | 小徑公路、部分摺疊車 |
| 507 | 24" | 青少年 MTB |
| 559 | 26" | 舊 MTB、城市車 |
| 584 | 650B / 27.5" | MTB、礫石車 |
| 622 | 700C / 29" | 公路、混合車、29er |

- 外徑估算：BSD + 2 × 胎寬；深紋胎可能再多約 1 cm（Sheldon Brown）。
- 實際例子：700×30 外徑 682 mm、700×45 為 712 mm、29×2.35 為 741 mm（bikeinsights）。
- 胎寬範圍：PikaBoost 2 支援公路胎 23–32 mm、MTB 胎 45–65 mm；Rubbee 第一、二代支援 20–60 mm（[Wikipedia](https://en.wikipedia.org/wiki/Rubbee_Drive)）。
- **結論**：滾輪需要涵蓋的胎寬是 23–65 mm，輪胎外半徑約 247–370 mm。

### 2-2 代表車款幾何（bikeinsights）

| 類別 | 車款 | 座管角 | 座管 C-T | 後下叉 | BB drop |
|---|---|---|---|---|---|
| 公路 | [Allez 56 (2026)](https://bikeinsights.com/bike-geometries/68a5d3bdcf7d82001ad0e59b-2026-specialized-allez-base-56) | 73.25° | 530 | 425 | 76 |
| 礫石 | [Grizl M (2025)](https://bikeinsights.com/bike-geometries/6a4b67e7d59329001bf72927-2025-canyon-grizl-base-m) | 73.5° | 522 | 435 | 75 |
| 城市 | [FX 2 Disc M (2022)](https://bikeinsights.com/bike-geometries/62a8d8206e9dfd001cf4ad2e-2022-trek-bikes-fx-2-disc-m) | 74° | 445 | 450 | 65 |
| 29" MTB | [Marlin 7 Gen3 M](https://bikeinsights.com/bike-geometries/67a34bbbdc4c21001b96ee82-2023-gen-3-trek-bikes-marlin-7-base-m) | 73.4° | 420 | 438 | 60 |
| 27.5" MTB | [Marlin 7 S (2020)](https://bikeinsights.com/bike-geometries/5eb035874068aa00175f91ff-2020-trek-bikes-marlin-7-s) | 73.5° | 368 | 438 | 48 |
| 26" MTB | [Hardrock 26 M (2014)](https://bikeinsights.com/bike-geometries/6086a174ef2181001cced934-2014-specialized-bicycles-hardrock-26-disc-m) | 73° | 444 | 424.5 | 41 |
| 20" 小徑車 | [Tsunami D20 L](https://bikeinsights.com/bike-geometries/6789a333ccefcc001a70aeb7-2023-tsunami-bicycle-mini-velo-d20-base-l-46) | 73° | 460 | 390 | **−30**（BB 比輪軸高） |

20" 這台是小徑車，不是摺疊車。我找不到 Tern/Dahon 摺疊車的數值幾何（UNVERIFIED）。摺疊車的特徵是座管短、座桿 33.9 mm 而且很長，Tern Link D8 用 50-406 輪胎和 V 煞（[Tern](https://www.ternbicycles.com/uk/bikes/473/link-d8)）。

### 2-3 偏移量表（計算）

**計算假設**：
- 以 BB 為原點，座管軸線通過 BB（使用有效座管角）。
- 量測點 P 在座管頂（車架座管束）上方 s mm 處。
- 使用者指定的胎寬：700×28 / 40 / 35、29×2.3、27.5×2.4、26×1.95、20×1.75。
- 誤差約 ±20–30 mm。MTB 實際座管角比有效值緩，例如 Marlin 出口角 71.9° 對有效值 73°，所以實際 P 點會更偏後。

**欄位說明**：
- 「向後 / 向上」：從 P 到輪胎正上方頂點的水平後移距離，以及 P 比該頂點高多少。
- 「最近距離 @角度」：P 到胎面的最短徑向距離；角度是該最近點在頂點前方幾度。
- 「座管–胎間隙」：輪胎到座管軸線的垂直距離減去輪胎半徑。

| 車款（胎） | 座管–胎間隙 | s=50 向後 / 向上 | s=50 最近距離 @角度 | s=100 向後 / 向上 | s=150 向後 / 向上 |
|---|---|---|---|---|---|
| 公路 700×28 | 40 | 251 / 140 | 202 @28° | 237 / 188 | 222 / 236 |
| 礫石 700×40 | 39 | 266 / 122 | 192 @29° | 252 / 170 | 238 / 218 |
| 城市 700×35 | 64 | 309 / 65 | 168 @37° | 295 / 113 | 281 / 161 |
| 29×2.3 | 29 | 300 / 21 | 123 @38° | 285 / 69 | 271 / 117 |
| 27.5×2.4（S 號） | 51 | 317 / 0 | 121 @42° | 302 / 48 | 288 / 96 |
| 26×1.95 | 63 | 278 / 102 | 184 @33° | 263 / 150 | 249 / 198 |
| 20×1.75 | 133 | 240 / 270 | 323 @25° | 225 / 318 | 210 / 366 |

- 換算公式：s 每增加 1 mm，向後距離減少 0.29 mm，向上距離增加 0.96 mm。
- **擺臂需求**：接觸點的徑向距離要涵蓋 120–400 mm，角度 20–42°。單一固定擺臂做不到，需要「夾具在座管上可上下調」加上「擺臂約 150–220 mm、可擺動 ±25°」的組合。
- 小號 MTB 的 P 點幾乎和胎頂同高，所以夾具一定要裝在較高的位置（s ≥ 100）。

### 2-4 干涉項目
- **後輪框煞夾器（公路 C 夾、V 煞）**：計算出的後上叉連線位在頂點前方 28–47°。框煞夾器的煞車橋就在這一帶，剛好壓在「最近接觸點」約 28–38° 的區域。框煞的 reach 是 39–49 mm（短）或 47–57 mm（長）（[Sheldon/Harris](https://www.sheldonbrown.com/harris/brake-calipers.html)）。V 煞的線管彎頭會跨過胎頂。結論：框煞車只能在約 0–15° 的區域接觸，也就是夾器後方。
- **擋泥板、後貨架**：都必須拆掉。Rubbee 和 Consumer NZ 都證實這點，而且這是安裝時最花時間的步驟。
- **座墊包**：會佔用外露座管的空間。
- **後避震（全避震車）**：輪胎相對座管的位移可達整個避震行程。eBay 款、PikaBoost、ASUS、Spiny 2 全部排除後避震車；Rubbee X 的說法是「potential issues」（[ebikechoices](https://www.ebikechoices.com/rubee-x-e-bike-conversion-kit-overview/)）。**建議**：只支援硬尾車。

---

## 3. 摩擦驅動接觸工程

### 3-1 需要多大的正向力（計算）
- 切向力 F_t = P / v：
  - 250 W：10 km/h 為 90 N，15 km/h 為 60 N，25 km/h 為 36 N。
  - 350 W @10 km/h 為 126 N；500 W @10 km/h 為 180 N。
- 正向力需求 N = 1.3 × F_t / μ（1.3 是安全係數）。以 F_t = 100 N 計算：μ = 0.8 需 162 N，0.6 需 217 N，0.4 需 325 N，0.3 需 433 N。
- 摩擦係數參考：
  - 乾燥輪胎對路面：鎖死約 0.7–0.9，峰值約 1.2（[TRL PPR496](https://www.trl.co.uk/uploads/trl/documents/PPR496.pdf)，搜尋摘要）。
  - 濕路面約 0.4 或更低（搜尋摘要，可信度弱）。
  - 濕的光滑 PU 滾輪幾乎抓不住：有人說「any moisture… back to square one」（[ES 雨天討論串](https://endless-sphere.com/sphere/threads/solution-for-rainy-condition-usage-of-friction-drive.75000)，搜尋摘要）。
- **基準**：Rubbee X 用 **200 N 氣壓彈簧**（製造商在 [pedelecs 論壇](https://pedelecs.co.uk/forum/threads/rubbee-x-introduction.29838/post-411714)的說法）。
- **建議**：250 W 等級的預壓設在 150–250 N，並能調到約 350 N 應付雨天。設計時取 μ_乾 = 0.6、μ_濕 = 0.3（這是假設）。
- 滑動上限實測：一台 63 mm 馬達殼直驅的 DIY 機，在 13 N·m 時才打滑，等於約 412 N 推力；另一台在約 2000 W 時打滑，限制到 1400 W 就正常（[ES「limits to friction drive」](https://endless-sphere.com/sphere/threads/the-limits-to-friction-drive.28634/)）。
- 接觸面積估算（計算，薄膜近似）：面積 ≈ N / 胎壓。200 N 在 6 bar 的公路胎約 3.3 cm²；在 1.8 bar 的 MTB 胎約 11 cm²。

### 3-2 滾輪直徑：轉速、扭矩、阻力（計算）

| 滾輪直徑 | 25 km/h 轉速 | 100 N 所需扭矩 | 18V 需要的 KV（負載 0.8） | 36V 需要的 KV | 壓入阻力倍率 √(1+r胎/r輪) |
|---|---|---|---|---|---|
| 30 mm | 4421 rpm | 1.5 N·m | 307 | 153 | 4.9 |
| 40 mm | 3316 rpm | 2.0 N·m | 230 | 115 | 4.2 |
| 50 mm | 2652 rpm | 2.5 N·m | 184 | 92 | 3.8 |
| 63 mm | 2105 rpm | 3.15 N·m | 146 | 73 | 3.4 |

- 阻力倍率的出處是 ISO 28580:2009 §9.3 的滾筒直徑修正：Kr = [(R1/R2)(R2+rT)/(R1+rT)]^0.5（[ISO 28580](https://law.resource.org/pub/us/cfr/ibr/inc/iso/iso.28580.2009.pdf)）。我把 R2 推到無限大（平地），換算成小滾輪相對平地的倍率。這遠超出公式的適用範圍，只能當數量級參考。小滾筒會誇大遲滯損失的定性結論有來源（[Cycling Weekly](https://www.cyclingweekly.com/news/are-bicycle-tyre-tests-lying-to-you-rethinking-rolling-resistance-and-drum-resting)，搜尋摘要）。
- **常時壓著的阻力**（計算）：阻力 ≈ Crr_平地 × 倍率 × N。假設 Crr 0.004–0.01、N 150–250 N、40 mm 滾輪，阻力約 2.5–10.6 N，在 20 km/h 等於 **14–59 W**，量級和整台車本身的滾阻相當。滾輪自己的 PU/橡膠遲滯還要另外加。
  - Consumer NZ 實測 Rubbee X 滑行時「有一些拖曳感」。
  - eBay 賣家宣稱阻力「可以忽略」（未驗證）。
  - 某零售商說摩擦驅動效率 75–85%、濕地 50–65%，但沒有出處（[levyelectric](https://www.levyelectric.com/resources/transform-your-bike-with-an-electric-scooter-wheel-friction-drive)）。
- DIY 社群常用 1.0–1.25" 滾輪（25–32 mm）配 63 mm 外轉子馬達，或直接拿馬達殼當滾輪（63 mm、170–295 KV）（[ES](https://endless-sphere.com/sphere/threads/the-limits-to-friction-drive.28634/)、[electricbike.com](https://www.electricbike.com/friction-drive/)）。

### 3-3 預壓方式：彈簧、重力、自增壓（關鍵設計發現，計算）
**判斷規則**：畫一條「擺臂樞軸」到「後輪軸」的連線。
- 接觸點在這條線前方（靠座管那側）：驅動反力會把滾輪壓進輪胎，屬於自增壓。
- 接觸點在這條線後方：驅動反力會把滾輪抬離輪胎，屬於自釋放。

**對座管樞軸的影響**：樞軸在座管上 s = 50 mm、接觸點在頂點前 0–15° 時，所有代表車款都是自釋放。這種情況下彈簧預壓必須 ≥ N_需求 + F_t/k，其中 k = 1.8（公路，頂點處）至 0.6（15°）。代價是滑行時整個預壓力都壓在輪胎上，阻力大。

**自增壓的做法**：把樞軸放在接觸點的後上方（外殼往後延伸過輪胎）。這時 N ≈ F_t × (b/a)，取 b/a ≥ 1/μ_濕 ≈ 3。只用力時才重壓，滑行時幾乎沒有壓力；被輪胎反向帶動時（滑行、回充）會自動抬起。

**現有做法**：

| 產品 / 設計 | 預壓方式 | 來源 |
|---|---|---|
| Rubbee X | 拉桿放下滾輪，200 N 氣壓彈簧維持接觸 | [New Atlas](https://newatlas.com/rubbee-x/52228/)、pedelecs |
| Kepler 殼驅動 / engineerdog | 彈簧把馬達拉離輪胎；馬達起轉的反扭矩把它擺進輪胎；不供電時不接觸、零拖曳 | electricbike.com、engineerdog |
| PikaBoost 2 | 避震彈簧 | [The Gadgeteer](https://the-gadgeteer.com/2025/08/05/livall-pikaboost-2-e-bike-conversion-kit-review/) |
| 訓練台專利 | 用摩擦力把驅動輪壓進輪胎，使 N/F_t ≥ 1/μ | [US9486687](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9486687) |

**建議**：把座管夾當作「固定基座」，擺臂樞軸放在胎頂後上方，用小彈簧提供 20–40 N 的初始接觸力，主要壓力靠自增壓幾何。需要加行程止擋和可調的 b/a 比。這個建議是推論，還沒有實測驗證。

### 3-4 滾輪材質取捨

| 材質 | 優點 | 缺點 | 來源 |
|---|---|---|---|
| 滾花鋁 | 便宜、遲滯低 | 6061 滾花會比輪胎先磨平；粗紋會磨胎 | [motorbicycling](https://motorbicycling.com/posts/711746)、[tire life 討論串](https://motorbicycling.com/threads/tire-life-on-friction-drive.11178/)（搜尋摘要） |
| 滾花淬火鋼 | 數百英里胎磨很少 | 重；滑動時傷胎 | 同上（軼聞） |
| 光滑 PU / 橡膠 | 安靜、胎磨少 | 濕地抓地很差；本身遲滯會增加阻力 | ES 雨天討論串（搜尋摘要） |
| 砂紙 / 止滑膠帶 | 濕地明顯改善 | 胎磨明顯增加，膠帶本身也很快磨掉 | engineerdog、[EBR QR-E 評測](https://forums.electricbikereview.com/threads/review-qr-e-250w-electric-booster-bicycle-motor-and-b60i-and-b70-battery.35201/page-5)（搜尋摘要） |
| Rubbee：含氧化鋁顆粒的特殊材質 | 終身保固 | 製造商自己說輪胎會**加快磨損 10–20%** | pedelecs |
| PikaBoost：V 形驅動胎 | 抓兩側胎肩，適用 25–65 mm | 驅動胎壽命 3000–5000 km，屬消耗品 | 手冊 |

- 胎磨的頭號原因是打滑，而且「打滑一秒就可能毀胎」（motorbicycling，搜尋摘要）。所以韌體需要做防滑控制：Rubbee 有類似汽車 ESC 的電子防滑，ASUS 有 anti-slip 機構。

### 3-5 越野齒胎、噪音、濕地
- 越野齒胎：Rubbee 說可用但「噪音會大一些」；PikaBoost 說紋路越平越安靜；engineerdog 的設計不支援越野齒胎。
- 噪音頻率估算（計算）：齒距 10 mm、25 km/h 時約 700 Hz。
- 濕地：Consumer NZ 測 Rubbee X 沒有打滑；engineerdog 原型「濕胎完全帶不動」；eBay 18V 款要求「不要在雨天使用」。

---

## 4. 商品規格整理

| 項目 | Rubbee X | eBay「18V … Friction Drive eBike 50km DIY HX」 | PikaBoost 2 | ASUS Oxiis E250G1 | Spiny 2 |
|---|---|---|---|---|---|
| 功率 | 250 W；3 顆電池模組時 350 W | 18V 無刷（瓦數不明） | 250 W 額定 / 500 W 峰值 | 250 W 連續（搜尋摘要） | 250 W 額定 / 750 W 峰值（美規），35 N·m |
| 速度 | 25 km/h；350 W 時 32 km/h | 5–35 km/h 有助力，超過 35 km/h 停止 | 未載明 | 未載明 | 32 km/h（美規） |
| 電池 | 36V 93.6 Wh/模組，最多 3 顆 | 不明（UNVERIFIED） | 220 Wh 或 158 Wh | 36V；USB-C 100W PD 約 2 小時充飽 | — |
| 里程 | 每模組 16 km，最多 48 km | 標題宣稱 50 km | 最高 70 km（220 Wh） | 最高約 50 km | 最高 90 km |
| 重量 | 2.8 / 3.4 / 4.0 kg | 不明；尺寸 305×100 mm | 約 3 kg | 約 3.7 kg | 2.2 kg |
| 滾輪 | 氧化鋁顆粒材質；直徑 UNVERIFIED | 不明 | V 形驅動胎 | 不明 | 可換雙配方摩擦墊 |
| 安裝 | 四螺栓座管基座留在車上，主機免工具卡入；備用基座 NZ$179 | 只限圓管、≤31.6 mm；不適用後避震；可用於 20" 摺疊車 | 圓管 25–35 mm、外露 >50 mm；不適用碳管、D 形管、後避震 | 夾座管；不適用碳管、全避震；適用 16"–700C | **車架基座**，不是座管夾；用鑰匙鎖定 |
| 預壓方式 | 200 N 氣壓彈簧 | 不明 | 避震彈簧 | 「防滑機構」 | 不明 |
| 其他 | 回充煞車；無線踏頻 | App 控制；照片說明寫 USB-C 輸出入；有一張照片說明出現「BOOM」字樣（eBay 自動產生的描述，UNVERIFIED）；售價 US$339，廣州出貨 | 65W USB-C；IP66（初代） | IPX4 | IP65 |

各欄來源：
- **Rubbee X**：[New Atlas](https://newatlas.com/rubbee-x/52228/)、[ebikechoices](https://www.ebikechoices.com/rubee-x-e-bike-conversion-kit-overview/)、[Consumer NZ](https://www.consumer.org.nz/articles/first-look-rubbee-x-e-bike-conversion-kit)、[pedelecs](https://pedelecs.co.uk/forum/threads/rubbee-x-introduction.29838/post-411714)。注意：官網 en.rubbee.ch 今天實測會 301 轉址到一個旅館網站，品牌可能已經停止營運（UNVERIFIED）。第一、二代 Rubbee 是 6.8 kg、14.4 V 20 Ah LiFePO4（[Wikipedia](https://en.wikipedia.org/wiki/Rubbee_Drive)）。
- **eBay 18V**：[eBay #127654453389](https://www.ebay.com/itm/127654453389)。另有 AliExpress 18V 10Ah、200 W、座管 25.4–31.6 mm、15.5 mph 的同類商品（[AliExpress](https://www.aliexpress.us/item/3256806438012497.html)，搜尋摘要，頁面打不開）。
- **PikaBoost 2**：[手冊](https://manuals.plus/asin/B0FC61XQ7M.pdf)、[BikeRadar（初代）](https://www.bikeradar.com/news/livall-pikaboost/)。
- **ASUS Oxiis**：[Digital Trends](https://www.digitaltrends.com/outdoors/asus-made-an-e-bike-conversion-kit-compact-enough-to-slip-into-a-backpack/)。
- **Spiny 2**：[Bikerumor](https://bikerumor.com/the-spiny-2-claims-to-convert-any-bike-into-a-750w-e-bike-in-3-seconds/)、[Zag Daily](https://zagdaily.com/micromobility/spiny-launches-second-generation-of-e-bike-conversion-kit/)（搜尋摘要）。
- **Add-e**：原始的摩擦輪版是 250–600 W（[Bikerumor](https://bikerumor.com/the-add-e-electric-motor-kit-is-generating-watts-of-interest-on-indiegogo/)，搜尋摘要）；現行的 add-e NEXT 已改成 BB 驅動，不是摩擦輪。

---

## 5. 座管夾具設計

### 5-1 參考設計
- **Topeak MTX BeamRack**：快拆凸輪加上兩種厚度的橡膠墊組合，對應 31.8–30.6、28.6、≤27.2 mm。用 5 mm 內六角調整凸輪張力，手冊註明「Heavier loads may require more bolt tension to prevent rack from twisting」。載重 9 kg。（[手冊](https://fortnine.ca/assets/pdf/topeak/mtxbeamrackgb0506.pdf)）
- **Blackburn Interlock**：M6 螺栓，扭力 6.5–9 N·m。
- **Arkel**：座墊弓加座管的雙點固定，比較能抗旋轉。
- **Rubbee X、Spiny 2**：每台車裝一個便宜的永久基座，主機用免工具卡榫裝上。這最符合「一分鐘內換車」的需求。
- 直徑轉換墊片有現成品，例如 Cane Creek 25.4→27.0、27.2→30.8（[eBay](https://www.ebay.com/p/2283109985)、[Performance](https://www.performancebike.com/cane-creek-seatpost-shims-black-31.6mm-to-34.9mm-aae0008/p1271650)）。

### 5-2 受力估算（計算，公路車案例，N = 250 N、F_t = 100 N）
- **軸向力**：輪胎把整台機器往座管上方推，約 265 N；最壞情況（N 400、F_t 130）約 410 N。夾具不能靠車架座管束擋住，因為受力方向是往上，只能靠摩擦力抓住。
- **俯仰力矩**：接觸點在 15° 時約 49 N·m，最壞約 72 N·m；接觸點在 30° 時只有約 15 N·m。結論：施力線越接近通過夾具，力矩越小。
- **需要的徑向夾緊力**：取安全係數 2、μ = 0.3–0.5（橡膠墊對鋁的假設值），需要約 1.0–2.7 kN。M6 鎖 8 N·m 估算可得約 6.7 kN（假設 K = 0.2），夾緊力本身綽綽有餘；但對碳管或薄壁鋁管會太大。
- **抗旋轉（左右扭轉）**：假設側向力 30–50 N、力臂 150–250 mm，需求約 4.5–12.5 N·m。27.2 mm 座管在上述夾緊力下，純摩擦只能提供約 7–11 N·m，處於邊緣。
- **建議**：
  - 夾具高度做到 40–45 mm，以降低邊緣壓力。
  - 使用高摩擦彈性內襯（TPU 95A 或橡膠）。
  - 另外加一個機械止轉點：往座墊弓拉一條繫帶或支撐，或用 Velcro / 魔鬼氈固定到後上叉。
  - 夾緊力由金屬凸輪或螺栓提供，3D 列印件只承受壓應力。PETG-CF 長期受 1–2 kN 預壓會潛變，台灣夏天黑色件曝曬後的溫度也要考慮（UNVERIFIED，需要另外查證）。

---

## 主要缺口（UNVERIFIED）
- Rubbee X、eBay 18V 款、ASUS 的滾輪直徑。
- eBay 18V 款的電池容量和預壓機構。
- Tern/Dahon 摺疊車的數值幾何。
- 30.0、30.4、30.8 mm 座管用在哪些車種。
- 滾輪對輪胎、濕地條件下的實測 μ。
- 滾輪壓入造成的滾阻實測（目前只有用 ISO 公式外推的數量級）。

本報告的計算腳本：
- `C:\Users\user\AppData\Local\Temp\claude\331f5373756cbd02\c95f4efe-559a-4251-aa6f-aaacc223e7e4\scratchpad\geom3.py`
- `C:\Users\user\AppData\Local\Temp\claude\331f5373756cbd02\c95f4efe-559a-4251-aa6f-aaacc223e7e4\scratchpad\geom2.py`
- `C:\Users\user\AppData\Local\Temp\claude\331f5373756cbd02\c95f4efe-559a-4251-aa6f-aaacc223e7e4\scratchpad\clamp.py`


---

# 查證結果：bike_standards

# bike_standards 報告查核結果（2026-11-07）

查核範圍：這份報告裡設計會用到的 16 項主張，每項都重新查過網路。查到一半時這一輪的 WebSearch 額度（每輪 200 次）就用完了，所以 Dahon 33.9 mm、NSMB 的升降座管直徑、Perennial 34.9 mm 這三項沒有另外查。

## 逐項查核

1. **PikaBoost 2 相容規格：CONFIRMED**
   - 手冊圖表寫的是：圓管、外露長度 >50 mm、直徑 25–35 mm。
   - 胎寬：V 形胎 25–65 mm、公路胎 23–32 mm、MTB 胎 45–65 mm。
   - 不適用：D 形管、碳纖座管、後避震車，另外還列了三輪車和輪椅。
   - 電池：220 Wh 最遠 70 km，158 Wh 最遠 50 km。
   - 來源：https://manuals.plus/asin/B0FC61XQ7M.pdf
   - 補充：FCC 文件寫的直徑範圍是 25.4–34.9 mm（只讀到搜尋摘要）：https://fcc.report/FCC-ID/2AEKF-L4P01/7748101.pdf

2. **Rubbee X 用 200 N 氣壓彈簧、滾輪含氧化鋁顆粒、輪胎多磨 10–20%：CONFIRMED**
   - 原文分別是「200N pneumatic spring」「aluminum oxide particles」「tire can wear off 10-20% faster」。
   - 發文者是自稱 Rubbee 創辦人的論壇帳號 Gedas，所以這是製造商自己的說法。
   - 來源：https://pedelecs.co.uk/forum/threads/rubbee-x-introduction.29838/post-411714

3. **Rubbee X 支援座管 22–35 mm、備用基座 179、必須拆擋泥板和後貨架：CONFIRMED，但有一處要更正**
   - 頁面寫的是 179，沒有標幣別。網站在紐西蘭，推測是紐幣。
   - 更正：報告說「Consumer NZ 判斷 Rubbee X 不太可能裝在升降座管上」，這篇文章裡找不到相關內容。「不支援升降座管」只剩 Wolf Tooth 手冊和論壇這兩個依據。
   - 來源：https://www.consumer.org.nz/articles/first-look-rubbee-x-e-bike-conversion-kit

4. **Rubbee X 功率、速度、續航、重量：CONFIRMED**
   - 250 W、25 km/h。350 W 版要三顆電池全裝，時速 32 km/h。
   - 續航：一顆電池 16 km，三顆 48 km。
   - 重量：一顆電池 2.8 kg，三顆 4 kg。
   - 拉桿放下滾輪，靠氣壓彈簧維持接觸。
   - 來源：https://newatlas.com/rubbee-x/52228/

5. **「Rubbee 官網轉址到旅館，品牌可能已停業」：轉址 CONFIRMED，停業推論 CORRECTED**
   - en.rubbee.ch 確實回 301，轉到 hotellacouronne.com。
   - 但 road.cc 在 2024-09-20 的報導說「it seems that the Rubbee X is still available」。報導寫基本款 €579、每顆加購電池 €99，品牌網站連到 rubbee.co.uk。
   - 2026 年是否還在賣：UNVERIFIABLE。rubbee.co.uk 抓回來幾乎是空的，無法判斷。
   - 來源：https://road.cc/?p=501987

6. **Giant D-Fuse 斷面約 30.2×25.2 mm：CORRECTED**
   - 30.2/25.2 這個尺寸是 Giant RSP-AM310D 鋁合金 D 形座管（小尺寸車架用）的。適用車款是 2020–2022 年的 Escape 1/2/3 Disc、Escape 2 City Disc。
   - 碳纖 D-Fuse 座管（Defy、Contact SLR 等）查不到官方斷面尺寸。零售商只標「30.9」或「Oval」。
   - 結論：D-Fuse 沒有單一斷面。要做 D 形內襯，必須依車款分別量測。
   - 搜尋摘要另外提到，部分 D-Fuse 車架可以改用 27.2 或 30.9 的圓管（未打開原頁）。
   - 來源：https://westbrookcycles.co.uk/giant_rsp-am310d_d-form_atb_seatpost_for_small_bikes-33397 （頁面擋爬蟲，內容來自搜尋摘要）、https://www.giant-bicycles.com/int/d-fuse-composite-seatpost

7. **Giant Escape 3（非碟煞）用 27.2 mm 座管：CONFIRMED**
   - bikes.fan、Bicycle Blue Book、Giant India 都寫 27.2 mm（搜尋摘要）。
   - 來源：https://bikes.fan/giant-escape-3-2023/

8. **Tern 33.9 mm 座管：CONFIRMED**
   - Tern 官方寫「compatible with 33.9 mm seat tubes」，適用 Verge 和 Link 系列。
   - 來源：https://www.ternbicycles.com/us/accessories/471/telescopic-seatpost-339

9. **Tern Link D8 用 50-406 輪胎、V 煞：CONFIRMED**
   - 規格頁的座管只寫「SuperOversize」，沒有毫米數。
   - 來源：https://www.ternbicycles.com/uk/bikes/473/link-d8

10. **Topeak MTX BeamRack：CONFIRMED**
    - 手冊寫明「not suitable or intended to be used with carbon fiber seatposts」。
    - 橡膠墊組合對應 31.8–30.6、28.6、≤27.2 mm；用 5 mm 內六角調整；手冊有防扭轉的提醒。
    - 載重 20 lbs（9 kg）。報告沒提到 EX 款上限只有 7 kg。
    - 來源：https://fortnine.ca/assets/pdf/topeak/mtxbeamrackgb0506.pdf

11. **Blackburn Interlock：CONFIRMED**
    - M6 螺栓，建議扭力 6.5–9 N·m。
    - 不適用碳纖座管，也不適用非圓形座管。
    - 來源：https://www.bellhelmets.com/on/demandware.static/-/Library-Sites-BellHelmets/en_US/dwbb2b4321/pdf/manuals-blackburn/Blackburn-Interlock-Seatpost-Rack-Manual.pdf

12. **框煞 reach 39–49 mm（短）和 47–57 mm（長）：CONFIRMED**
    - 來源：https://www.sheldonbrown.com/harris/brake-calipers.html

13. **ISO 28580:2009 §9.3 滾筒直徑修正：CONFIRMED**
    - 條號、公式（Eq. 11、12）和變數定義都對得上：R1、R2 是兩個滾筒的半徑，rT 是輪胎標稱直徑的一半。
    - 把 R2 推到無限大後，倍率 √(1+rT/r輪)，40 mm 滾輪約 4.2，跟報告一致。
    - 但標準要求滾筒直徑至少 1.7 m，用在 20 mm 半徑的小滾輪確實是外推。報告自己已經註明這點，只能當數量級參考。
    - 來源：https://law.resource.org/pub/us/cfr/ibr/inc/iso/iso.28580.2009.pdf

14. **Spiny 2 規格：大部分 CONFIRMED，IP65 為 UNVERIFIABLE**
    - 安裝在車架上，不是夾座管：配件有一個 frame mount/positioner 和 4 個 frame adapters；法文報導寫用鑰匙鎖定。
    - 2.2 kg；250 W 額定，美國峰值 750 W（加拿大 500 W）；35 N·m。
    - 速度：美國 32 km/h，其他多數市場 25 km/h。續航 90 km。
    - 售價：早鳥 US$339，之後 US$409。報告沒寫價格。
    - IP65：Zag Daily 沒有提到，無法確認。
    - 來源：https://zagdaily.com/micromobility/spiny-launches-second-generation-of-e-bike-conversion-kit/

15. **eBay 18V 款（≤31.6 mm、US$339、廣州出貨等）：UNVERIFIABLE**
    - eBay 頁面回 403，搜尋也找不到這個商品。
    - 不建議把它當設計基準。報告寫的 US$339 剛好跟 Spiny 2 早鳥價一樣，要小心是不是記混了。

16. **ES 論壇「63 mm 馬達在 13 N·m 打滑」：UNVERIFIABLE**
    - 論壇有 Anubis 防爬蟲，抓不到內容。
    - 只能確認換算本身正確：13 N·m ÷ 0.0315 m ≈ 413 N。

## 報告漏掉的重要缺口

1. **台灣法規完全沒寫，這是最大的缺口。**
   - 依《電動輔助自行車及微型電動二輪車型式安全審驗管理辦法》（最新修正 2022-11-28），電動輔助自行車必須同時符合：經型式審驗合格、以人力為主電力為輔、最高時速 25 km/h 以下、車重 40 kg 以下。上路前要在下管明顯處貼合格標章。
   - 微型電動二輪車：時速 25 km/h 以下；車重不含電池 40 kg 以下，或含電池 60 kg 以下；必須登記並掛牌。
   - 型式審驗是由製造商、代理商或進口商申請，而且要求有防止擅改速限的設計。
   - 所以自己做、可在多台一般自行車之間換裝的助力器，實際上拿不到標章，在公路上使用屬於不合規或灰色地帶。
   - 舊版處罰條例第 72 條「擅自變更裝置」罰 NT$180；現行金額沒查到。
   - 對設計的影響：
     - 韌體要硬性限制 25 km/h 斷電。Rubbee 的 350 W/32 km/h 模式和 Spiny 美規 32 km/h 都不符合台灣規定。
     - 只做踏頻助力（PAS），不做手把油門。
     - 開源文件要寫清楚法規聲明。
   - 來源：https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=K0040068

2. **輪徑範圍漏了 14–16 吋摺疊車。**
   - PikaBoost 2 支援 14–29 吋（35.6–73.7 cm）。
   - 報告的 BSD 表從 406 開始，沒有 254、305、349 這幾種小輪徑，偏移量表也沒有涵蓋。

3. **D 形座管的處理方式要改。**
   - 因為沒有單一斷面，與其做通用的 D 形內襯，不如建議 Giant 車主換一支 27.2 或 30.9 的便宜鋁圓管，跟碳管的處理方式一樣。
   - 這個做法有沒有適用全部 D-Fuse 車款還要確認。

4. **Rubbee X 的售價和供貨。**
   - 2024 年資料：€579，每顆加購電池 €99。報告的商品表沒有寫這兩個數字。

5. **報告可能誤導的地方。**
   - 「Spiny 2 用車架基座」是對的。但報告把它跟 Rubbee 的「座管永久基座」並列成同一種快拆方案，其實兩者的安裝位置不同。

6. **沒查證的項目（額度用完）。**
   - Dahon 33.9 mm、Tern GSD/HSD 34.9 mm（Perennial 擋爬蟲，只有網址字串支持）、NSMB 的升降座管直徑、Wikipedia 上 Rubbee 第一、二代支援胎寬 20–60 mm。

暫存檔：`C:\Users\user\AppData\Local\Temp\claude\331f5373756cbd02\c95f4efe-559a-4251-aa6f-aaacc223e7e4\scratchpad\iso28580.txt` 是 ISO 28580 的全文文字。
