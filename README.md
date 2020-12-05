# Life In Tkk

<p align="left">
<a href="https://github.com/Mirasire"><img src="https://img.shields.io/badge/XUJC-Life%20In%20Tkk-blue.svg" alt="github"></a>
<a href="https://github.com/Mirasire"><img src="https://img.shields.io/github/languages/top/Mirasire/Life-In-Tkk.svg" alt="github"></a>
<a href="https://github.com/Mirasire"><img src="https://img.shields.io/github/license/Mirasire/Life-In-Tkk.svg" alt="github"></a>
</p>

## 简介

用于厦门大学嘉庚学院`TKK`的综合信息查询的第三方`Python3`库。

## 如何使用

> __!!注意: 还需安装 `firefox`, `geckodriver`, `tesseract`!!__

__1. 直接使用__

将项目中的`life_in_tkk` 放入所调用的`xx.py`的同级目录。

```python
# 需要import
from life_in_tkk import Tkk_html
from life_in_tkk import Tkk_schedule
# ....
import life_in_tkk
```

__2. 基于pip安装使用__

使用 `pip3` 进行下载，之后具体使用方式与直接使用相同。

```
pip3 install life_in_tkk
```

## 相关依赖

> 版本为开发时使用的版本，未对其他版本进行测试~~其他应该也没什么问题~~

### `Python3`所需的依赖

`Python3`所需的依赖包，详情可见[**依赖目录**](#依赖目录)。

### 其余依赖

- firefox`83.0`
  - geckodriver`0.27.0`
- tesseract`4.1.1`

#### GNU/Linux

__Ubuntu/Mint:__

```bash
sudo apt-get install firefox firefox-geckodriver 
sudo apt-get install tesseract tesseract-ocr-eng
```
__Arch Linux/Marjorn:__

```bash
sudo pacman -S tesseract  tesseract-data-eng
sudo pacman -S firefox geckodriver 
```
#### Windows 10

可以在`Github`仓库的 [**UB-Mannheim/tesseract**](https://github.com/UB-Mannheim/tesseract/wiki) 和 [**mozilla/geckodriver**](https://github.com/mozilla/geckodriver/releases) 中找到对应的 window32/64 安装包，安装即可。

__!!注意: 十分重要!!__

安装完毕后, 需要将软件的 __安装目录__ 添加到 `windows 10` 系统的 __环境变量__（`此电脑|属性|高级系统设置|环境变量|Path`）中。

## 依赖目录

> 均为开发时所用的版本，仅提供参考。

| 库名             | 版本    |
|:-----------------|:--------|
| `Pillow`         | 8.0.1   |
| `selenium`       | 3.141.0 |
| `requests`       | 2.22.0  |
| `beautifulsoup4` | 4.8.2   |
| `pytesseract`    | 0.3.6   |
| `tesseract`      | 0.1.3   |
| `numpy`          | 1.17.4  |


## Plan

- [X] 课表库
   - [X] 自动识别验证码
   - [X] 调课
   - [X] 补课
- [ ] 电费查询库

## LICENSE

MIT &copy; Mirasire
