# Blogtrans

Blogtrans是一套轉換blog資料格式的開放源碼軟體，目前支援：

* [MovableType](http://www.movabletype.org/documentation/appendices/import-export-format.html) 匯入及匯出
* [無名小站XML](http://www.wretch.cc/blog/) 匯入
* [Blogger Atom](http://www.blogger.com) 匯出

## 注意：已知問題

* 無名XML檔會有日期、格式不正確的問題（如2月31日、XML損壞）
* 無法匯入所有文章至Blogger：可能是由於文章類別有特殊符號。可試著「清除所有文章類別」

細節及其他已知問題詳見[FAQ](http://miaout17.github.io/blogtrans/faq.html)，如無法解決歡迎[回報問題](http://miaout17.github.io/blogtrans/report.html)。

## 更新記錄

Blogtrans 1.1.0 (2013/09/13)

* 自動修正無名XML檔日期錯誤的問題（如自動將2/31修正為2/28）
* 新增「工具：清除所有文章類別」功能（無法匯入所有文章至Blogger時可嘗試使用）
* 修正留言附加於錯誤文章的bug

## Running Blogtrans

### Windows

There is only official build for Windows system.
The Windows build is available on SourceForge.
Visit [project download page](https://sourceforge.net/project/showfiles.php?group_id=211548) to get newest build.

### Linux and Mac

Linux and Mac user can get the source code and build by yourself.
Please refer to **Build from Source** section.

## Usage

Please refer to the [Blogtrans Homepage](http://miaout17.github.com/blogtrans/) (Traditional Chinese).

## Build from Source

The code is mainly hosted on [Github](https://github.com/miaout17/blogtrans)
(There is also a mirror on Sourceforge, but it's not always up-to-date).

You can get the source code via git:

    git clone git@github.com:miaout17/blogtrans.git

or directly download the [tarball](https://github.com/miaout17/blogtrans/tarball/master).

### Dependencies

Please install following items:

* [Python](http://www.python.org/) 2.6 or above (but not 3.x)
* [wxPython](http://www.wxpython.org/) 2.8 or above
* [psyco](http://psyco.sourceforge.net/) (optional)

After that, you can execute BlogTrans:

    python blogtrans.py

### Testing

Document TBD..

## Liecnse

Blogtrans is released with MIT LICENSE, see LICENSE file for details.

