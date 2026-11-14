# 996.ICU Comprehensive Labor Rights & Ecosystem Intelligence Report

> **Analysis Date:** 2026-11-14 | **Source:** `996.ICU` Official Repository Archive

## Executive Summary

The **996.ICU** movement began as a grassroots open source initiative addressing unlawful overtime practices in technology enterprises. 
Under Chinese labor law (Articles 36, 41, and 44 of the *Labor Law of the PRC*), the statutory standard work week is **40 hours** (8 hours/day, 5 days/week), with daily overtime capped at **3 hours** and monthly overtime strictly capped at **36 hours**, requiring overtime premiums of 150% (weekdays), 200% (rest days), or 300% (statutory holidays). 
A **996 schedule** entails at least **72 hours per week** (over 128 hours of overtime monthly), representing a direct breach of statutory thresholds when enforced without compensation or union negotiation.

### Key Intelligence Metrics

| Metric | Count | Context |
| :--- | :--- | :--- |
| **Active Blacklisted Companies** | **235** | Documented companies enforcing unlawful overtime |
| **Canceled / Remediated Companies** | **6** | Companies that formally revoked 996 policies with proof |
| **Whitelisted (955/965) Companies** | **10** | Verified standard work-life balance employers |
| **Remote-Friendly Employers** | **3** | Distributed tech employers across Tier-1 metro areas |
| **Anti-996 Licensed Open Source Projects** | **160** | OSS repositories incorporating the Anti-996 license clause |
| **Statutory & Community Reform Proposals** | **6** | Concrete legal, union, and blockchain proposals |

---

## 1. Geographic & Overtime Pattern Distribution

### Top Cities with Reported 996 Practices
| City | Reported Companies | Primary Sectors |
| :--- | :--- | :--- |
| **北京** | 58 | Internet, E-commerce, Gaming, Fintech |
| **深圳** | 33 | Internet, E-commerce, Gaming, Fintech |
| **上海** | 29 | Internet, E-commerce, Gaming, Fintech |
| **杭州** | 16 | Internet, E-commerce, Gaming, Fintech |
| **成都** | 9 | Internet, E-commerce, Gaming, Fintech |
| **广州** | 9 | Internet, E-commerce, Gaming, Fintech |
| **天津** | 7 | Internet, E-commerce, Gaming, Fintech |
| **武汉** | 7 | Internet, E-commerce, Gaming, Fintech |
| **南京** | 6 | Internet, E-commerce, Gaming, Fintech |
| **大连** | 5 | Internet, E-commerce, Gaming, Fintech |

### Breakdown of Overtime Regimes
| Overtime Regime | Incident Count | Typical Weekly Hours | Statutory Overrun |
| :--- | :--- | :--- | :--- |
| **Unpaid Mandatory Overtime** | 1 | ~48-60h | +8-20h over legal limit |
| **Alternating 6-day (大小周)** | 30 | ~50-60h | +10-20h over legal limit |
| **996 Standard (72h/wk)** | 121 | ~72h | +32h over legal limit |
| **11-11-6 / Two-Shift Extreme** | 1 | ~84h+ | +44h+ over legal limit |
| **Other 6-day Schedules (966/10106)** | 16 | ~48-60h | +8-20h over legal limit |
| **997 (7 Days/Week)** | 5 | ~84h+ | +44h+ over legal limit |
| **Custom Excessive Overtime** | 61 | ~48-60h | +8-20h over legal limit |

---

## 2. Whitelist: Verified 965 / 955 Work-Life Balance Directory

The following employers maintain verified records of standard working hours (9:00 AM – 5:00 PM or 9:00 AM – 6:00 PM with lunch break):

| City | Company | Schedule | Verification Proof |
| :--- | :--- | :--- | :--- |
| 杭州 | [杭州复杂美科技有限公司](https://github.com/33cn/chain33/) | `9-6-5` | [员工手册](img/chain33.jpg) |
| 成都 | [四川锦程消费金融有限责任公司](http://www.jccfc.com/) | `915-530-5` | [考勤规则通知邮件](img/timing_20190401111520.png) |
| 深圳 | [深圳市凉屋游戏科技有限公司](http://www.chillyroom.com/) | `上午10:00 - 下午1:00；下午2:30 - 下午7:00` | [内部wiki员工手册截图](img/chillyroom_prove.png) |
| 长沙 | [湖南快乐阳光互动娱乐传媒有限公司](http://www.mgtv.com) | `965;中午休息2小时` | [邮件通知](img/mgtv.png) |
| 北京 | [长城宽带](https://www.96090090.com/) | `9:00-5:30-5` | [考勤规则通知邮件](img/gwbn.jpeg) |
| 上海 | [三零卫士](http://www.30wish.net) | `9:30-17:30-5` | [钉钉考勤规则说明](img/30wish.png) |
| 北京 | [语知科技](http://http://yuzhinlp.com/) | `9:00-18:00-5;上下班弹性半小时;午休1h;` | [员工手册截图](img/yuzhi_nlp.png) |
| 北京 | [北京优锘科技有限公司](http://www.uinnova.cn/) | `9-6-5;弹性工作;午休一个钟;` | [员工手册截图](img/uinnova.png) |
| 北京, 西安 | [北京庖丁科技有限公司](https://www.paodingai.com/) | `9-6-5;弹性工作;午休一小时;` | [内部 WiKi 截图](img/PaodingAI-wiki.png) |
| 上海 | [IBM](https://www.ibm.com/cn-zh) | `9-6-5;弹性工作;午休一小时;` | [内部 WiKi 截图](img/PaodingAI-wiki.png) |

---

## 3. Remote-Friendly Employers

| City Hub | Company | Website | Eligible Roles |
| :--- | :--- | :--- | :--- |
| 北京市 | [新义互联（北京）科技有限公司](https://adtalos.com/) | https://adtalos.com/ | 程序员 |
| 上海市 | [一线科技](https://1wire.com) | https://1wire.com | 所有职位 |
| 上海市 | [微辣生活](https://weila.life) | https://weila.life | 技术与视频编辑 |

---

## 4. Notable Anti-996 Open Source Projects

A growing catalog of open source tools, frameworks, and developer utilities that protect worker sovereignty by conditioning code reuse on labor law compliance:

| Project | Description | Stars / Status |
| :--- | :--- | :--- |
| **[Make Zero](https://github.com/sheepzh/make-zero)** | 便捷加解密文字的浏览器插件，支持自定义密码，多种密文格式。 | Protected under Anti-996 |
| **[Easy Mybatis](https://github.com/onlyGuo/easymybatis)** | 在内存中自动生成Mapper 但不会释放文件到硬盘. | Protected under Anti-996 |
| **[在线视频字幕（ASS）编辑器](https://ass-editor.js.org)** | 在线编辑视频字幕 | Protected under Anti-996 |
| **[HadoopHADeploymentScript](https://github.com/Fa1c0nSec/HadoopHADeploymentScript)** | Hadoop 双机集群高可用系统自动化部署脚本 | Protected under Anti-996 |
| **[tsmon](https://www.npmjs.com/package/tsmon)** | TypeScript版本的nodemon和ts-node集合体，缓存编译结果，支持增量编译，TypeScript开发利器 | Protected under Anti-996 |
| **[async-retry.ts](https://www.npmjs.com/package/async-retry.ts)** | Retry Pattern 的 TypeScript 实现 | Protected under Anti-996 |
| **[yasio](https://github.com/yasio/yasio)** | A cross platform & lightweight socket io service | Protected under Anti-996 |
| **[WAF](https://github.com/chengdedeng/waf)** | Web Application Firewall or API Gateway(应用防火墙/API网关) | Protected under Anti-996 |
| **[ID Card](https://github.com/ofcold/identity-card)** | 身份证号码信息 | Protected under Anti-996 |
| **[dura](https://github.com/CN-YUANYU/dura)** | 基于 redux、typescript 的前端数据流方案 | Protected under Anti-996 |
| **[vue-apis](https://github.com/ChangedenCZD/vue-apis)** | 集成axios的vue插件 | Protected under Anti-996 |
| **[optimize-vue](https://github.com/ChangedenCZD/optimize-vue)** | 基于 vue-cli 3.0 构建的快速开发框架 | Protected under Anti-996 |
| **[optimize-vue-cli](https://github.com/ChangedenCZD/optimize-vue-cli)** | 基于 vue-cli 3.0 构建的快速开发框架的脚手架 | Protected under Anti-996 |
| **[thinkphp5-restfulapi](https://github.com/Leslin/thinkphp5-restfulapi)** | 基于 thinkphp5 开发的restful api快速开发框架 | Protected under Anti-996 |
| **[HookPHP](https://github.com/letwang/HookPHP)** | 一款基于C扩展搭建支持AI在线编程的PHP框架！ | Protected under Anti-996 |
| **[server](https://github.com/wildfirechat/server)** | 野火IM解决方案，server端 | Protected under Anti-996 |
| **[WeChatBlog](https://github.com/NiZerin/WeChatBlog)** | 微信小程序 & 个人博客 & WordPress REST API | Protected under Anti-996 |
| **[Yearning](https://github.com/cookieY/Yearning)** | Mysql SQL审核平台 | Protected under Anti-996 |
| **[java-multi-thread-programming](https://github.com/loveincode/java-multi-thread-programming)** | 《Java多线程编程核心技术》源码 | Protected under Anti-996 |
| **[notes](https://github.com/loveincode/notes)** | 一个Java后端工程师的学习笔记 | Protected under Anti-996 |
| **[Atom.css](https://github.com/isVertical/atom.css)** | Atom.css 一个提供原子化风格Class的UI库 | Protected under Anti-996 |
| **[mina-gulp-cli](https://github.com/milobluebell/mina-gulp-cli)** | 一个轻量级的小程序开发脚手架，基于gulp | Protected under Anti-996 |
| **[aya-store](https://github.com/milobluebell/aya-store)** | 小程序状态管理模块 | Protected under Anti-996 |
| **[eppdev-jee-pom](https://github.com/eppdev/eppdev-jee-pom)** | 数据驱动的JavaEE代码生成程序 | Protected under Anti-996 |
| **[You-need-to-know-css](https://github.com/l-hammer/You-need-to-know-css)** | 💄CSS tricks for web developers\~ | Protected under Anti-996 |

---

## 5. Anti-996 License Legal Analysis

### Clause Mechanics
The Anti-996 License combines permissive software usage rights with mandatory labor compliance obligations:
1. **Condition 2 (Labor Law Compliance):**
   > *"The individual or the legal entity must strictly comply with all applicable laws, regulations, rules and standards of the jurisdiction relating to labor and employment... In case that the jurisdiction has no such laws... required to comply with Core International Labor Standards."*
2. **Condition 3 (No Rights Waivers):**
   > *"Shall not induce, suggest or force its employee(s)... to agree in oral or written form, to directly or indirectly restrict, weaken or relinquish his or her rights... nor limit the rights of reporting violations."*

### Legal Enforcement Model
- **Condition vs. Covenant:** When structured as a condition precedent to the copyright grant, a licensee in breach of labor laws automatically loses license permission, rendering continued deployment of the software an act of copyright infringement under applicable copyright acts (such as 17 U.S.C. § 101 et seq. or PRC Copyright Law).
- **Dual-Licensing Strategy:** Projects can offer a dual-licensing structure (e.g., MIT + Anti-996 Rider, or Apache 2.0 with Labor Rights Rider) allowing seamless compliance validation across enterprise CI/CD.

---

## 6. Community Proposals & Roadmaps

### Use Blockchain to Collect Evidence 用區塊鏈建設網上證據鏈
- **File:** [`996.ICU\proposal\proposal_blockchain_evidence_online.md`](file:///E:/2027 nov/996.ICU\proposal\proposal_blockchain_evidence_online.md)
- **Summary:** # Use Blockchain to Collect Evidence 用區塊鏈建設網上證據鏈 HEAD | SUMMARY -----|-------- Title:| Use Blockchain to Collect Evidence 用區塊鏈建設網上證據鏈 Author:| Eric Chow Status:| Draft Type:| Technical Created:| 19-April-2019 Post-History:| None ## Why this Proposal? Some companies only hire people who accept 996...

### Proposal for Expanding the Anti 996 License for more Fields
- **File:** [`996.ICU\proposal\proposal_for_expanding_the_anti996license_for_more_fields.md`](file:///E:/2027 nov/996.ICU\proposal\proposal_for_expanding_the_anti996license_for_more_fields.md)
- **Summary:** # Proposal for Expanding the Anti 996 License for more Fields HEAD | SUMMARY -----|-------- Title:| Proposal for Expanding the Anti 996 License for more Fields 题目: | 提案关于扩展Anti 996 License的适用范围 Author:| ChuangSheep Status:| Draft Type:| Proposal Created:| 07-Apr-2019 Post-History:| None ## 提案目的 为...

### Proposal Template for 996.icu Projects
- **File:** [`996.ICU\proposal\proposal_for_other_types_of_work.md`](file:///E:/2027 nov/996.ICU\proposal\proposal_for_other_types_of_work.md)
- **Summary:** # Proposal Template for 996.icu Projects HEAD | SUMMARY -----|-------- Title:| 添加其他工种的文件夹或目录 Author:| xloypaypa Status:| Draft Type:| Proposal Created:| 31-04-2019 Post-History:| None ## Why this Proposal? 我们好像获得了法律界的一些支持（我不懂，我没有太关注，我啥都不知道啊！）<br> 只是我比较蠢（也许是比较坏），所以建议如果可能，也许我们也能顺手帮下其他可能也受到不算特别公正待遇的...

### 成立无产阶阶级联合工会的倡议
- **File:** [`996.ICU\proposal\proposal_gonghui.md`](file:///E:/2027 nov/996.ICU\proposal\proposal_gonghui.md)
- **Summary:** ## 成立无产阶阶级联合工会的倡议 今天是毛主席逝世44周年忌日。教员为了无产阶级的革命事业奋斗了一生。我们作为共产主义的后来者应当继承教员留下的革命遗产。 教员晚年间经常说“大不了再上一次井冈山”。面对这边压下去那边又起来的官僚主义，特权阶级，教员表现出了如此强悍的革命气魄。作为他的学生的我们，更应该以教员为榜样。 今天，在他的忌日里，我们作为互联网世界的一员，也要跟随教员的脚步，上一次互联网的井冈山————在互联网上成立一个无产阶级联合工会。 ## 为什么要成立这个工会 前一段时间我又看了一遍姜文导演的《邪不压正》。电影中有一句话令我印象深刻“你先别管你爸爸是谁了！你该有你自己的...

### 路线图
- **File:** [`996.ICU\proposal\proposal_roadmap.md`](file:///E:/2027 nov/996.ICU\proposal\proposal_roadmap.md)
- **Summary:** # 路线图 HEAD | SUMMARY -----|-------- Title:| 路线图 Author:| Tooodis Status:| Draft Type:| Roadmap Created:| 15-April-2019 Post-History:| None ## Why this Proposal? 996的抗争本质上是劳动者与资本家之间的斗争<br> 在现代化，工业化的背景下，劳动者在这场斗争中是处于劣势地位的。<br> 因此想要在这场斗争中获得胜利就必须理清思路，讲究方法。 ## Community Value 提出一个更明确，更有操作性的路线图。<br>...

### Proposal for Requesting GitHub Official Including 996ICU License
- **File:** [`996.ICU\proposal\proposal_to_request_github_official_including_996icu_license.md`](file:///E:/2027 nov/996.ICU\proposal\proposal_to_request_github_official_including_996icu_license.md)
- **Summary:** # Proposal for Requesting GitHub Official Including 996ICU License HEAD | SUMMARY -----|-------- Title:| Proposal for Requesting GitHub Official Including 996ICU License 题目: | 提案请求github官方收录996ICU License Author:| ff4415 作者:| ff4415 Status:| Draft 状态:| 草案 Type:| Proposal 类型:| 提案 Created:| 1-April-2...
