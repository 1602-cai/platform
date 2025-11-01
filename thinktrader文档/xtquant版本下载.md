xtquant版本下载 | 迅投知识库

![微信扫码联系客服](/assets/wechat-d90fd08f.png "点击联系客服")

![分享链接](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAAAHqADAAQAAAABAAAAHgAAAADKQTcFAAADjElEQVRIDcVXW0hVQRRdM/fce/OVpfRA8dENDckkMILsYRG9PnqQQUkg9NFfBCFEJJSFRj8R+BP4URREGEVGRNSXWEiE1odoDx+lhkoWpTe1+zrT7KPnes59ddQbDujM7D17rbNn9uzZl8FCqxaC36l1l4iAekgIFDOwDEDIP2psUEAMMoY2ZuONFVUpLdWMqVO66P9ZdBWw/ZZY9GXAfZqpolKCL4+1VtfJj/omOLuWm5VS13SC/dHloX1UYtcld5lA4Lr0MCvUyMpc7sAAg+1M78WUh5HW81ChEIKtqh6rVUXgwVxJCZNsCYOwCDOUxySgBa7LY/dkfzR04XzmjLGG3guLy2UvdByTx3J7a+JNSkSESdg6KfVBj+lMaWuMyniPObMd0c9c85iilwIpHkSZqQyudNNGBmGJg7hIoK2gKzOfQKJt27xawc41dtytSELesijEMuCISyOm5ED3lCazbXaJv6fAjvrjyShcaUPlDidy0mzoHI6eP4hL43TVjG1R/erL2ZAm2IF9ax0oW+9EWiLH0w4PSl02bMhW4PYIFF0diwnHFb5VoTQYc5VBmZrAcLDIgf2FTiQ7p+LyxQcvijO5RkpLO4cDBovIQ+JU5NkWR1bPSFekMByW3u0tcMChBC8Cmrq8yF0iU2ue3ILpZolYckoYliHzsG5n6rOWchwrdqJUAttkDjS2ll4fkuwCB9Y5jWJLHhOnMvPKmOy1yfndichNt4Up2vp9mPAEcGqbdjNM+o6hf281cUaO+2mo2ucTaB/ym4DbB/34/MMfkdQXEOgeiR7RQSAGIYnZYFAQMvj6S8XZR+Ooa5rAuFfg/bAfrX1eVO0K95RMuySpzwIvBBtS6BGXNvkhnKbps04fmrt92CivS315ImSyN+n1iZXAorXEyaly0A1j9eNeYJNLgcIjk5KtVWKJ0CrzNm+MRWjUvekP4KPcztHJyLfAMrHCH3OqkahcMRLEGguZ3uuaPWh466XnzrTUCjFxESenwoxqJBNClEnPSAA3Xk3i5msPzj2ZRPntcfR8n7o+Az9VmS6jGBrExEWc2oHRU9XXP/ppLi+UQ17zkyVOjPxWcf+dz0ARPqQ6LCc7NZ+KwGCkLEghQN9GlQEDvxL+nfGRELZefRBi0GOayGBZmGKPqkCtGoyj55qnIRVmmMck0Bud+f8s6E1brZPq/YL8hNHJqacaKd4/2v4CgdaZJ2zGqYAAAAAASUVORK5CYII= "分享链接")

![智能助手](/assets/AI-41154f2e.png "智能助手")

投研平台 在新窗口打开

迅投社区 在新窗口打开

[迅投官网 在新窗口打开](http://www.thinktrader.net)

*   xtquant文档
    
    *   [快速开始](/nativeApi/start_now.html)
    *   [XtQuant.XtData 行情模块](/nativeApi/xtdata.html)
    *   [XtQuant.Xttrade 交易模块](/nativeApi/xttrader.html)
    *   [完整实例](/nativeApi/code_examples.html)
    *   [常见问题](/nativeApi/question_function.html)
    *   [xtquant版本下载](/nativeApi/download_xtquant.html)

更新日期

版本

下载

更新说明

20250516

xtquant\_250516

[点击下载](/packages/xtquant_250516.rar)  
压缩包目录结构已调整到和之前一致，带有xtquant文件夹

支持python3.13版本  
  
xttrader 支持银证转账  
银行信息查询 xttrader.query\_bank\_info()  
银行账户余额查询xttrader.query\_bank\_amount()  
银证转账转入 xttrader.bank\_transfer\_in()  
银证转账转出 xttrader.bank\_transfer\_out()  
银行卡流水记录查询xttrader.query\_bank\_transfer\_stream()  
  
xttrader 支持期货和期权资金划转  
权资金转期货 xttrader.ctp\_transfer\_option\_to\_future()  
期货资金转期权 xttrader.ctp\_transfer\_future\_to\_option()  
  
xttrader支持北交所  
xtconstant 添加北交所市价报价方式说明  
  
xttrader 交易数据字段调整  
委托 XtOrder 新增  
股东代码 secu\_account  
证券名称 instrument\_name  
成交 XtTrade 新增  
股东代码 secu\_account  
证券名称 instrument\_name  
持仓 XtPosition 新增  
股东代码 secu\_account  
证券名称 instrument\_name  
当前价 last\_price  
盈亏比例 profit\_rate  
浮动盈亏 float\_profit  
持仓盈亏 position\_profit  
开仓日期 open\_date（只对期货可用）  
账号资金 XtAsset 新增  
可取余额 fetch\_balance  
当前余额 current\_balance（当前余额 = 可用资金 + 冻结资金）  
  
xtdata获取数据函数支持以datetime形式传入时间范围  
  
合约信息添加交易日字段 TradingDay  
xtdata.get\_instrument\_detail()  
  
支持获取大单统计数据（需要vip权限）  
xtdata.get\_transactioncount()  
  
支持获取带有分类信息的板块列表（需要投研版本）  
xtdata.get\_sector\_info()  
  
期权合约信息添加期权预估保证金 OptEstimatedMargin（需要投研版本）  
xtdata.get\_option\_detail\_data()  
  
郑商所期货、期权品种提供标准化代码的字段（如 MA2504.ZF）（需要投研版本）  
  
xtdata获取数据函数支持ATM市场  
xtdata.get\_market\_data()  
xtdata.get\_market\_data\_ex()  
  
BugFix: 订阅数据问题

20241017

xtquant\_241014

[点击下载](/packages/xtquant_241014.rar)

xtdata.get\_option\_detail\_data()期权多空方向类型判断调整  
  
xtdata.get\_trading\_calendar() 自动下载所需的节假日数据  
  
xtdata.get\_instrument\_detail() 字段ExpireDate类型由int调整为str  
  
tick数据增加现手字段(tickvol)，即当前tick累计成交量与上条数据的差值  
  
新增函数xtdata.get\_formula\_result()，用于获取subscribe\_formula()的模型结果  
  
修复token模式下启用K线全推后单支订阅数据周期错误的问题

20240926

xtquant\_240920a

有已知缺陷，暂不提供下载  
  
在token模式下，启用K线全推后单支订阅数据周期错误

修复xtdata.subscribe\_quote()返回订阅号为None的问题

20240923

xtquant\_240920

有已知缺陷，暂不提供下载

token模式，可以设置初始化的市场列表  
xtdatacenter.set\_init\_markets()  
  
函数xtdata.get\_period\_list() 结果结构调整  
  
添加函数 xtdata.get\_trading\_contract\_list()  
获取当前主力合约可交易标的列表  
  
添加用于获取交易时段的系列函数  
xtdata.get\_trading\_period()  
xtdata.get\_all\_trading\_periods()  
xtdata.get\_all\_kline\_trading\_periods()  
  
添加函数 xtdata.subscribe\_quote2()  
支持复权方式参数

20240822

xtquant\_240812

[点击下载](/packages/xtquant_240812.rar)

期货夜盘显示真实时间功能默认开启  
未开启时， 周六凌晨的行情数据时间为周一  
开启时，周六凌晨的行情数据时间为周六  
  
新增板块：过期上交所、过期深交所  
沪港通深港通板块不再显示历史标的  
  
撤单接口的市场参数支持字符串格式，如SH、SF  
xttrader.cancel\_order\_stock\_sysid()和xttrader.cancel\_order\_stock\_sysid\_async()  
  
添加函数xtdata.get\_his\_option\_list\_batch()和xtdata.get\_his\_option\_list()  
获取历史上某段时间的指定品种期权信息列表  
依赖数据'optionhistorycontract'  
  
期权函数支持商品期权品种 xtdata.get\_option\_undl\_data()和xtdata.get\_option\_list()  
  
郑商所期权标的代码调整为4位 xtdata.get\_option\_detail\_data()  
  
移除郑商所过滤重复tick的逻辑

20240617

xtquant\_240613

[点击下载](/packages/xtquant_240613.rar)

支持python3.12版本  
  
xtdata支持选择端口范围，在范围内自动连接  
  
添加函数xtdata.get\_full\_kline() 批量获取当日K线数据（需要开启K线全推）  
  
支持获取新闻公告数据  
xtdata.get\_market\_data()系列函数 数据周期：announcement  
  
支持获取涨跌停连板数据  
xtdata.get\_market\_data()系列函数 数据周期：limitupperformance  
  
支持获取港股通持股明细数据  
xtdata.get\_market\_data()系列函数 数据周期：hktdetails,hktstatistics  
  
支持获取外盘的行情数据（需购买相应服务）  
行情订阅xtdata.subscribe\_quote()和行情获取xtdata.get\_market\_data()系列函数，支持美股品种的获取  
  
支持订阅vba模型（连接投研端）  
xtdata.subscribe\_formula()  
  
token模式下初始化全推市场可选  
xtdatacenter.set\_wholequote\_market\_list()  
  
token模式下行情连接优选机制调整  
xtdatacenter.set\_allow\_optmize\_address()会使用第一个地址作为全推连接  
  
token模式下期货周末夜盘数据时间模式可选,可以选择展示为周一凌晨时间或真实的周六凌晨时间  
xtdatacenter.set\_future\_realtime\_mode()  
  

20240329

xtquant\_240329

[点击下载](/packages/xtquant_240329.rar)

郑商所期货品种支持使用4位年月代码（例如：CF2303.ZF）  
xtdata.get\_instrument\_detail()支持使用4位年月代码获取  
历史主力合约数据 新增4位年月代码字段  
  
支持获取etf的iopv数据  
分笔数据添加iopv字段（pe）  
xtdata.get\_market\_data()系列函数 数据周期：etfiopv1m（分钟级） etfiopv1d（日级）  
  
期权函数xtdata.get\_option\_detail\_data() 新增标的品种代码字段 OptUndlCodeFull  
  
新增板块 上证转债、沪深转债、T+0基金  
  
连接状态监听接口回调数据结构调整  
xtdata.watch\_quote\_server\_status()  
xtdata.watch\_xtquant\_status()  
  
新增接口 xtdata.subscribe\_formula() 支持连接投研端调用vba  
  
token模式下支持按用户权限放开并行接入数量  
  
本地python回测支持多线程  
  
优化7\*24连续交易的问题

20240205

xtquant\_240119b

[点击下载](/packages/xtquant_240119b.rar)

修复token模式下偶发的订阅数据异常问题  
有问题的版本：240119, 240119a  
  
token模式下并行接入数量放宽至10个

20240129

xtquant\_240119a

[点击下载](/packages/xtquant_240119a.rar)

合约信息接口支持参数控制获取全部字段  
xtdata.get\_instrument\_detail(iscomplete = True)并添加以下字段  
期货和期权手续费方式(ChargeType)  
开仓手续费(率)(ChargeOpen)  
平仓手续费(率)(ChargeClose)  
开今仓(日内开仓)手续费(率)(ChargeTodayOpen)  
平今仓(日内平仓)手续费(率)(ChargeTodayClose)  
交割月持仓倍数(OpenInterestMultiple)  
  
添加客户端连接状态监听接口 xtdata.watch\_xtquant\_status()  
  
支持获取退市可转债数据  
xtdata.get\_market\_data()系列函数 数据周期：delistchangebond  
  
支持获取待发可转债数据  
xtdata.get\_market\_data()系列函数 数据周期：replacechangebond  
  
优化K线全推的断线重连逻辑

20240119

xtquant\_240119

[点击下载](/packages/xtquant_240119.rar)

xtdata.subscribe\_quote()和xtdata.get\_market\_data()系列函数，添加新的K线数据周期  
新周期包含：周线(1w)、月线(1mon)、季度线(1q)、半年线(1hy)、年线(1y)  
  
支持获取千档委买委卖队列数据（待后续迅投lv2数据源上线后可用）  
订阅函数 xtdata.subscribe\_l2thousand\_queue()  
获取函数 xtdata.get\_l2thousand\_queue()  
  
支持港股lv2数据（待后续迅投lv2数据源上线后可用）  
支持获取港股席位数据  
订阅函数 xtdata.subscribe\_quote(period = 'brokerqueue')  
获取函数 xtdata.get\_broker\_queue\_data()  
  
xtdata.get\_full\_tick()在VIP模式下提供成交笔数字段（transactionNum）  
  
xtdata.get\_option\_detail\_data()支持获取商品期权数据  
  
支持获取历史主力合约数据  
xtdata.get\_market\_data()系列函数 数据周期：historymaincontract  
  
修复 获取上证期权、深证期权tick行情数据价格精度错误的问题  
  
修复 期货夜盘分钟线获取不到的问题  
  
优化下载数据流程  
  
支持设置行情源自动连接目标地址范围  
xtdatacenter.set\_allow\_optmize\_address()  
  
xtdata.get\_local\_data()支持指定数据路径

20231228

xtquant\_231209a

[点击下载](/packages/xtquant_231209a.rar)

修复xtdata.get\_trading\_calendar()获取历史范围返回数据重复的问题  
  
添加xtdata.get\_trading\_calendar()目前仅支持SH,SZ市场的说明（其他市场交易日历陆续对接中）  
  
添加快照指标数据周期 'snapshotindex'（包含量比、涨速、换手等字段）  
  
修复板块指数（BKZS）分钟线获取不到的问题  
  
添加xtdatacenter中的北交所、沪深京A股板块  
  
修复xtdata.subscribe\_whole\_quote()订阅全推数据中的pvolume字段单位错误  
  
（股票、转债的pvolume单位为股，所有品种volume单位均为手，其余品种情况详见网页文档）  
  

20231209

xtquant\_231209

[点击下载](/packages/xtquant_231209.rar)

添加ETF申赎清单信息相关接口  
  
下载数据 xtdata.download\_etf\_info()  
  
获取数据 xtdata.get\_etf\_info()  
  
添加节假日下载的接口 download\_holiday\_data（获取交易日历依赖节假日）  
  
添加涨跌停数据，数据周期'stoppricedata'  
  
添加连接成功时连接状态日志  
  
添加财务数据文档中十大股东、股东数的字段说明  
  
修复历史st数据获取失败的问题  
  
修复xtdatacenter提供数据时，和接收进程运行目录不同出现获取失败的问题  
  
优化模块退出时的表现  
  
移除xtdata.get\_industry()接口  
  

20231124

xtquant\_231101c

[点击下载](/packages/xtquant_231101c.rar)

修复xtdata.get\_market\_data()系列的内存泄漏问题  
  
xtdatacenter.init()在重要市场初始化失败时抛出异常信息  
  
全推数据在第一次使用时订阅，减少不必要的带宽占用  
  
修复xtdatacenter退出时崩溃的问题  
  
修复同目录下xtdatacenter重复启动卡住的问题  
  
补全期货全推的月份连续合约（例如 ag01.SF）和交易合约（例如 ag2401.SF）  
  
日志相关优化

20231110

xtquant\_231101b

[点击下载](/packages/xtquant_231101b.rar)

修复过期合约板块成分为空的问题  
  
优化xtdatatcenter监听端口后连接接入的时序  
  
xtdata.download\_history\_data添加增量下载参数，支持指定起始时间的增量下载  
  
修复token无效时调用接口崩溃的问题

20231106

xtquant\_231101a

[点击下载](/packages/xtquant_231101a.rar)

修复退出时发生异常的问题  
  
优化初始化过程中行情连接和数据订阅的时序

20231101

xtquant\_231101

[点击下载](/packages/xtquant_20231101.rar)

添加xtdatacenter，支持以token方式登录行情服务  
  
添加xtdata.QuoteServer，支持通过xtdata控制、监控行情连接  
  
补充xtdata中对转债交易场景、ETF交易场景的数据支持  
  
调整了一些底层数据交互的实现方式  
  
完善xttrader期货交易场景下的开平仓方向字段

20230920

xtquant\_230825b

[点击下载](/packages/xtquant_0825b_2023-09-20.rar)

对应当前QMT券商版公版的下载python库  
  
券商版会有版本升级跟不上的情况，通常请使用这个公版版本以保证兼容性

20230905

xtquant\_230825a

[点击下载](/packages/xtquant_20230825a.rar)

\-

20230825

xtquant\_230825

[点击下载](/packages/xtquant_20230825.rar)

\-

20230301

xtquant\_230301

[点击下载](/packages/xtquant_20230301.rar)

\-

20220817

xtquant\_220817

[点击下载](/packages/xtquant_20220817.rar)

\-
