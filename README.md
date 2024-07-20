***量子金鑰模擬實驗***
===
**此程式是專門給剛接觸QKD的同學觀察BB84協議的模擬運作過程**
---
<font size=1> ※註:此程式並非使用qiskit去模擬，而是用傳統古典電腦以概念的方式去模擬的，\
Random模組也並不是真正的隨機，而是生成偽隨機數。\
在隨機選擇的情況下並不是真正的隨機，而是可以透過演算法進行反推的!\
真正的量子加密是不允許此等事發生的!!!</font>
---
**此模擬程式的靈感來自 [**Quantum key distribution** 的維基百科](https://en.wikipedia.org/wiki/Quantum_key_distribution)，各位同學邊閱讀邊操作此程式會學得更有效率喔!**
---
## 簡單說明一下此程式如何使用:
1. 請輸入一個數字決定訊息傳遞者Alice要建立幾個隨機位元
2. 此時會跳出一個提示視窗會詢問您在本次模擬實驗中要不要發生有第三者監聽的情況，就依使用者需求做選擇即可(會建議同學先了解當只有Alice傳遞者與Bob接收者兩人之間是怎麼產生出金鑰的)
3. 符號說明:
   * 序列編號: $數字
   * 隨機產生的位元: 0 or 1
   * 基底(模板): + or x
   * 觀測得到的結果: 方向箭頭
4. 顏色意義:
   - 淺綠: 使用傳統網路通道進行溝通後，所得出雙方共同使用的加密基底之編號
   - 淺藍: 標記公開討論後得出的編號並標記方便使用者觀察
   - 紅色: 標示出明明在使用相同加密基底時應該會得出相同的答案，然而在Bob接收者觀測之後對照本因得到的答案卻不一樣，證實有第三者Eve在監聽
   - 金色: 說明系統判定的結果應為何
   - 紫色: 重點說明