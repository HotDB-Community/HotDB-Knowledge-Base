# 概述

## 背景

随着互联网的崛起，海量数据的存储、计算、分析需求越来越普遍。在各种计算机应用场景中，传统集中式数据库面临着理论升级和技术升级两大难题。21世纪以来，随着以 Hadoop及其衍生技术为代表的大规模数据处理技术的崛起，数据库技术开始由集中式走向分布式计算与存储的模式。经过10余年的产业实践，分布式事务数据库的多种架构逐渐成熟。

近年来国际信息安全形势日益严峻，国家信息安全战略逐步深入。为了应对核心技术受制于人的严峻形势，政府相继推出加快推进核心技术自主可控替代计划，以满足构建安全可控的信息技术体系的要求。然而，当前仍有不少企业的核心系统依赖于国外IT巨头的集中式数据库产品和配套的底层硬件，核心技术缺乏突破，无法做到完全自主可控。这就要求企业的信息化技术急需进行革新，全面提升服务海量用户和处理海量数据的能力，确保信息化系统自主可控与稳定可靠。

## 分布式关系型数据库服务

DRDS(Distributed Relational Database Service)即分布式关系型数据库服务，是指物理上分散的多个关系型数据存储单元通过计算机网络连接起来组成一个逻辑上统一的数据库服务。分布式事务数据库的基本思想是将原来集中式数据库中的数据分散存储到多个数据存储节点上，以获取更大的存储容量和更高的并发访问量。

# 分布式事务数据库

## HotDB Server

HotDB Server是一款专注MySQL数据库服务的高可靠、高吞吐和强一致的分布式事务数据库产品。支持在分布式环境下为应用提供类似集中式数据库的操作体验，为海量数据、海量用户、高并发、高可用和高性能的业务系统提供强有力的支撑。同时具备强透明、易扩展、无学习成本等特点。HotDB Server的数据服务端口可以像MySQL数据库一样访问，应用程序连接HotDB Server的数据服务端口与连接MySQL的方式一致。从MySQL替换为HotDB Server只需修改应用的数据库配置文件中host、port、database、user、password信息即可。同时支持不同开发语言的MySQL数据库驱动、连接池，例如JAVA的JDBC驱动，c3p0、DHCP、DRUID连接池。

![HotDB Server 架构示意图](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image4.png)

## 集群组成说明

完整的分布式事务数据库HotDB Server集群体系包括以下组件：

**计算节点：**计算节点是分布式事务数据库HotDB Server集群体系的核心，承担所有数据库服务相关工作，是整个分布式服务的命脉所在。

**管理平台：**分布式事务数据库平台又称为HotDB Management，可实现对计算节点数据库用户、数据节点、表类型、分片规则等信息的易用性配置。同时可提供计算节点服务状态监控、异常事件提醒、报表查看、任务管理等智能运维相关服务。

**存储节点：**实际存储业务数据的MySQL数据库，通过IP、Prot、Database三者可确定一个存储节点。另外，在HotDB Server集群体系中有一个虚拟的数据节点概念，数据节点用于表述一组具有主备关系的存储节点。

**管理平台配置库：**负责存储管理平台元数据的MySQL数据库。

**计算节点配置库：**负责存储计算节点元数据的MySQL数据库。

**高可用组件：**HotDB Server的计算节点可配合Keepalived高可用解决方案，实现主备模式的计算节点可用性检查以及高可用切换。

**负载均衡组件：**多计算节点集群可选择使用LVS等方式进行SQL请求的分发。应用端可借助LVS的VIP访问HotDB Server的计算节点服务，同时保证使用透明与服务不间断。也可使用其余负载均衡方案进行处理，例如F5加自定义检测、应用直连计算节点等方式。

**备份程序：**热璞科技自研的分布式事务数据库备份程序，负责业务数据的备份。

## 特性

### 负载均衡

- 多计算节点集群支持使用通用的负载均衡解决方案进行SQL请求的分发。
- 同一集群下的多个计算节点的数据服务对等，均支持所有类型的数据操作。
- 同一集群下少于半数的计算节点同时发生故障时，集群服务依旧可用；特别地，当集群节点依次故障至仅剩两个计算节点后，其中一个计算节点再发生故障，另一个计算节点依然能够提供服务。

### 高可用

- HotDB Server的计算节点支持高可用架构，运维管理良好的集群不会因为主计算节点宕机而造成整体分布式事务数据库服务不可用的问题。且运维管理良好的集群的计算节点可保证一年的总故障时间一般情况下不超过53分钟。
- 运维管理良好的集群的计算节点故障判断及切换服务的总时长一般情况下小于7秒，最佳实践是5秒左右。MySQL层故障判断及切换服务的总时长一般情况下小于3秒。
- HotDB Server支持通过可视化的方式对故障切换或手动切换后的计算节点进行高可用重建操作，减少人工手动修改回切配置的繁琐工作。
- HotDB Server的存储节点支持使用MySQL数据库原生的主从复制与MGR(MySQL Group Replication)复制模式。
- 正确部署且配置了数据节点故障切换规则的一组存储节点，当主存储节点服务出现异常时，计算节点可及时感知并执行存储节点高可用切换，并将新的请求发送至高可用切换后的存储节点。
- HotDB Server的配置库支持使用MySQL数据库原生的主从复制与MGR(MySQL Group Replication)复制模式。
- 正确部署且具有复制关系的一组配置库，当主配置库出现异常后，计算节点可及时感知并高可用切换到备用的配置库。

### 高性能

- HotDB Server的单计算节点模式中，性能测试转账场景在并发数为256时计算节点吐量可达到 20万+TPS ，50万+QPS。

- 并发数目前性能测试结果为可稳定支持2048以上。

- 相对单个集中式数据库，HotDB Server的单计算节点吞吐量损耗在5%以内。

- 全局自增序列获取性能大于20万 TPS。

**备注：**以上所述TPS为简单TPS。以上所述性能指标均基于：使用《分布式事务数据库产品HotDB Server硬件配置推荐\-\--热璞科技》所述最高配置硬件规格，规范地安装部署并进行《HotDB Server单计算节点_基础场景性能测试报告》所述调优，不少于12个数据节点，存储节点服务器\\MySQL实例未出现性能瓶颈的前提。

### 强透明

- HotDB Server提供类似集中式数据库的操作体验。应用程序只需连接计算节点数据服务端口，无需关心数据底层存放位置，即可对业务数据进行操作。

- 应用程序从传统数据库替换到分布式事务数据库需要修改的代码量一般不超过5%。

- 强一致分布式事务对应用程序透明，用户操作时无需改动任何SQL命令或事务流程，可像普通事务一样使用。

- 读写分离对应用程序透明，用户无需关心SQL下发的位置，程序自动根据配置的读写分离策略对SQL进行合理路由。

- 全局自增序列对应用程序透明，用户可像使用MySQL自增序列一样使用HotDB Server全局自增序列。

- 支持JDBC协议，支持MySQL原生通讯协议。

### 易运维

- 支持参数可视化配置与在线校验参数合理性。

- 支持计算节点参数修改后动态加载立即生效。

- 支持计算节点版本在线升级。

- 支持多线程备份，以及定时自动备份。

- 支持计算节点资源、流量以及服务器状态监控，实时展示集群的数据量、计算节点与数据节点的吞吐量。

- 动态绘制集群服务状态拓扑图，实时显示计算节点与存储节点的运行状态，方便用户对异常问题的定位与修复。

- 支持OnlineDDL，可做到数据库表结构的变更不阻塞线上业务。

- 支持在线一键迁库对数据节点进行弹性扩容。

- 支持数据节点内主备存储节点数据一致性检测，检测结果可准确定位不一致的信息。

- 支持全局表数据的一致性检测，且提供修复不一致数据的功能入口。

- 支持对创建唯一约束的分片表的历史数据进行唯一性校验。

- 支持计算节点和存储节点的用户密码有效期检测，检测到过期时提醒用户及时更改密码。

- 支持对业务SQL进行摘要式记录，同时根据SQL语句结构、执行时间、执行计划等筛选出待优化的SQL语句并给出优化建议。

- 支持新手导航，快速引导用户上手HotDB Server基础配置。

- 支持不同架构模式的计算节点集群自动化部署。

- 支持集群运行环境的健康体检。

- 支持集群运行信息一键收集，提高集群故障排查的速度与效率。

- 支持基于JOIN SQL日志，可视化地展示各表之间的业务关联关系。

- 支持通过管理平台在线完成对计算节点许可证的更新激活操作。

- 支持对管理平台配置库的自动化升级。

### 安全防护

- 支持过载限流保护机制。可通过限制计算节点前端最大连接数与存储节点最大连接数实现对计算节点与存储节点的保护。

- 支持流控功能，启用后，可以根据存储节点性能表现智能调控SQL流量，保持存储节点工作在最佳状态。

- 支持计算节点数据库用户权限控制，且99%兼容MySQL权限体系。

- 支持配置允许连接计算节点服务的IP白名单，未在白名单范围之内的IP地址访问计算节点服务时会提示拒绝登录。

- 支持集群异常事件邮件报警通知。管理平台将整个集群的运行状态纳入监控范围，一旦检测到集群服务出现故障或预警事件，程序将通过邮件方式告知用户。

- 支持SQL防火墙，对高危SQL进行拦截，防止业务系统被SQL注入、误操作或恶意操作。

- 支持表回收站功能，被执行DROP/DELETE全表的数据可在设定时间范围内保留并恢复。

- 支持账户信息加密管理，HotDB Server对所有服务过程中用到的账户密码进行加密存储。

- 针对部分管理平台高危操作，HotDB Server提供二级密码校验防护机制，防止出现误操作或恶意操作系统数据的问题。

- 管理平台登录认证API支持信息加密传输。

- 提供备份文件的加密与远程存储功能，保证数据安全性。

- 提供审计日志功能。包括管理平台用户操作记录、计算节点防护拦截记录、计算节点管理端口操作记录。

- 支持配置具有sudo功能的非root用户连接集群服务器。

### 扩展能力

- 支持表数据平滑重分布，支持数据节点平滑迁移。

- 支持只读存储节点的增加和读写分离权重的配置。

- 支持MySQL数据库向分布式事务数据库快速（极短停服务时间）迁移。

- 支持MySQL 5.6、5.7、8.0版本。

- 支持类MySQL的INFORMATION_SCHEMA库，方便用户查询计算节点相关信息。

### 故障容灾

- 支持跨机房灾备模式部署，当中心机房服务故障时，可自动由灾备机房接管继续提供服务。且支持中心机房内部故障可由可视化界面引导自动切换至灾备机房及修复原故障中心机房。

# 功能详解

## 数据库基础服务

HotDB Server支持MySQL原生通讯协议，支持数据定义、数据操作、分区表、数据库管理语句、事务、锁、字符集与校对集等常用数据库基础服务。其中在数据操作中解决了跨库查询和跨库数据排序等难点问题。并支持强一致分布式事务与跨库死锁检测。

### 数据定义

支持常用的数据定义操作语句，如：CREATE\\DROP\\ALTER\\RENAME\\TRUNCATE等。同时支持关联已有分片规则直接CREATE业务表，而无需在管理平台上对表事先进行定义。

### 数据操作

#### 跨节点SQL

HotDB Server支持跨数据节点的SQL操作，如：

- 跨节点INNER/LEFT/RIGHT JOIN

- 跨节点的组合JOIN及带括号JOIN

- 跨节点聚合函数

- 跨节点分组+HAVING+排序+分页

- 跨节点UNION/UNION ALL查询

#### 修改分片字段值

HotDB Server允许在不改变分片字段值路由（即修改后的分片字段值与修改前的值路由到相同的数据节点）的前提下，update水平分片表的分片字段值。

#### 透明全局自增序列

在分布式架构下，HotDB Server可保证具有AUTO_INCREMENT属性的列在各个数据节点上全局自增。透明全局自增序列使用方法与MySQL的AUTO_INCREMENT相同，目前透明全局自增序列可保证该字段全局有序递增，但是不保证序列值的连续性。

#### 全局唯一约束

HotDB Server支持全局唯一约束，可保证启用了此功能时拥有唯一约束（UNIQUE、PRIMARY KEY）的列在所有数据节点上全局唯一。若启用相关功能还可以做到当SELECT查询语句中不包含分片字段但包含唯一约束字段时，同样可以定位单一节点。目前支持全局唯一约束设置到表级别。

### 分区表

HotDB Server支持数据库分区表（PARTITION）相关操作，如：CREATE PARTITION TABLE、ALTER PARTITION、INSERT PARTITION、UPDATE PARTITION、SELECT PARTITION、DELETE PARTITION。

### 数据管理语句

支持数据库管理语句SHOW、DESC、USE、KILL以及部分会话级别SET语句。

### 触发器

支持在单库环境下使用触发器功能且支持触发器的备份与恢复。

### 子查询

支持有限场景下的子查询功能。

### 事务与锁

#### 事务

- 支持显式分布式事务与隐式分布式事务。

- 支持弱一致分布式事务与强一致分布式事务。

- 支持会话级事务隔离级别：READ COMMITE、REPEATABLE READ、SERIALIZABLE。

- 支持定义SAVEPOINT，以及设置事务提交回滚属性，如：COMMIT \[WORK\] \[AND \[NO\] CHAIN\] \[\[NO\] RELEASE\]、ROLLBACK \[WORK\] \[AND \[NO\] CHAIN\] \[\[NO\] RELEASE\]。

#### 强一致（XA）分布式事务

HotDB Server利用 MySQL 提供的外部 XA 事务可解决跨数据节点事务场景中数据的强一致性问题，即要么所有数据节点的事务都COMMIT，要么所有数据节点都ROLLBACK；支持REPEATABLE READ、SERIALIZABLE隔离级别且隔离级别功能表现和单机MySQL相同。计算节点在开启XA事务功能后，对于应用程序MySQL命令操作是透明的，对SQL命令、事务流程没有任何改动要求，可像普通事务一样使用。

#### 跨节点死锁检测

在分布式事务数据库系统中，若死锁发生在两个MySQL数据库节点间时，MySQL的死锁检测机制无法检测到这种跨实例死锁。在HotDB Server分布式事务数据库系统中，HotDB Server跨库死锁检测可检测多个MySQL数据库节点间的死锁并回滚开销最少的事务。

### 字符集与校对集

- HotDB Server支持常用字符集，如utf8、gbk、latin1、utf8mb4。

- HotDB Server支持常用校对集，如utf8_general_ci、utf8_bin、latin1_swedish_ci、latin1_bin、gbk_chinese_ci、gbk_bin、utf8mb4_general_ci、utf8mb4_bin。

### 用户权限体系

HotDB Server兼容MySQL的用户权限体系，支持全局权限、库权限、表级权限的多维度配置。此外HotDB Server用户体系中还增加了用户表级拒绝权限功能，方便用户快速为业务系统配置一套高安全性的权限体系。目前对用户权限的配置可以通过管理平台进行操作。

### 拆分算法

HotDB Server提供七种数据拆分算法，满足用户大部分场景的拆分需求。以下是七种拆分算法的具体介绍：

![拆分算法](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image4.png)

### 表类型

HotDB Server提供四种表类型供用户选择，用户可以根据实际业务场景选择合适的数据库表类型。以下是关于四种表类型的具体介绍：

![表类型](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image5.png)

### 兼容Oracle函数与Sequence语法

HotDB Server提供部分常用Oracle函数及Sequence语法兼容功能，用户由Oracle迁移至HotDB Server时，可减少其业务代码的修改量。

## 数据高可用服务

HotDB Server在计算节点、数据节点、配置库等层次提供全面的高可用保障。提供完善的心跳检测、故障切换对存储节点同步追平判断、全局自增序列在故障时自动跳号、客户端连接Hold等机制，保障数据服务的可用性与数据的一致性。

### 计算节点服务高可用

HotDB Server采用keepalived技术实现计算节点服务的高可用。由keepalived实时检测计算节点的健康状态并在计算节点发生故障时进行高可用切换。目前支持通过管理平台对主备模式的计算节点集群进行手动高可用切换。也可以在计算节点集群发生高可用切换之后，重建高可用环境，保证下次故障发生时可正常切换。

### 数据节点服务高可用

HotDB Server提供数据节点内的存储节点高可用。在正确部署且已配置故障切换规则的一组存储节点中，当主存储节点不可用时，程序将自动切换到优先级最高的备存储节点上，且保证主从数据同步追平。使用数据节点高可用要求：必须配置主从存储节点的故障切换规则，并在计算节点中开启心跳功能。

### 配置库服务高可用

HotDB Server支持配置库服务高可用，防止配置库实例出现故障时，计算节点无法正常提供服务。配置库目前支持主从、双主、MGR（MySQL Group Replication）三种复制模式。

### 数据同步

#### 普通Replication模式

HotDB Server支持配置库与存储节点使用MySQL Replication。支持BINLOG格式为MIXED和ROW，同时支持使用半同步复制、GTID、多线程复制。

#### MGR实时同步

HotDB Server支持配置库与存储节点使用MGR(MySQL Group Replication)复制模式。目前只支持single primary模式。相比半同步复制可略微提升故障场景下主从数据一致性（半同步复制可保证收到commit ok的事务不丢失，但不保证主机执行崩溃恢复流程后数据和从机一致）。

#### 多源复制

HotDB Server兼容但不支持存储节点的多源复制功能。

### 数据追平策略

在分布式事务数据库存储节点高可用机制中，当主库宕机时计算节点的切换策略会根据备库设置的优先级进行切换并且计算节点会保证可用的备库追完所有可应用的relaylog后才将服务切换到备库上。结合使用半同步复制，可保证"已收到commit ok的事务不丢失，未发出commit的事务回滚"；在此基础上再启用HotDB Server的强一致模式，则可额外保证"已发出commit但未收到commit ok的事务，全提交或者全回滚"。

![存储节点故障切换过程示意图](assets/image4.png)

## 数据库运维管理

HotDB Server在参数配置、服务监控、数据检测、安全防护、故障告警等多方面提供智能化运维服务。

### 主备数据一致性检测

管理平台提供逻辑库、存储节点、配置库维度的主备数据一致性校验功能。主从数据一致性检查，可校验主库与从库之间的表结构与表数据是否一致。当检测存在少量的数据不一致时，主从数据一致性检查可定位到数据行不一致的主键值；有大量不一致时，则显示不一致的主键值区间或显示全表大量不一致的提示。此外，还可以添加定时计划，定期检测所选逻辑库中的数据一致性情况。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image7.png)

### 全局表数据检测

管理平台提供全局表数据检测功能，可选择具体逻辑库中的全局表并检测该表在所有数据节点中数据是否一致。如存在不一致的数据，可以通过修复功能进行数据修复。此外，还可以通过添加定时检测计划，定期检测全局表数据的一致性，如检测发现异常，将在事件通知中告知用户。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image8.png)

### 数据分片路由正确性校验

HotDB Server支持对水平分片表的历史数据的路由正确性进行校验。可检测业务数据是否按配置的分片规则正确路由，也可校验从其他分布式事务数据库系统导入至HotDB Server的分片数据是否存在路由错误的问题。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image9.png)

### 数据唯一约束检测

HotDB Server支持对水平分片表或子表发起数据唯一约束检测。可及时发现集群中已开启唯一约束的表的历史数据是否存在不唯一的情况。对检测出违反唯一约束的表的重复数据进行可视化展示，方便用户进行修复。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image10.png)

### 数据分片方案推荐

HotDB Server支持基于仿真压测生成的SQL日志，进行分片方案推荐计算，帮助用户通过实际业务场景找到合适的表分片字段。结合少量人工调优，例如更换合适的分片算法，最终可为用户生成适合生产环境的业务表分片方案。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image11.png)

### 分片方案在线变更

提供对业务表的表类型、分片规则、分片字段、分片所属数据节点四个维度的在线变更支持。同时可结合智能分片方案推荐结果进行单个或批量表变更操作。支持变更业务表时设置数据复制暂停时段规避业务高峰期，减少对系统性能的影响。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image12.png)

### 表结构变更

#### 普通DDL

管理平台支持执行普通DDL功能，支持对数据库表的创建与修改。同时，针对敏感操作，例如"drop、truncate"等SQL进行二次口令校验，防止误操作与恶意操作。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image13.png)

#### 在线DDL

管理平台支持执行在线DDL（OnlineDDL）功能，保证在进行表变更时，不会阻塞线上业务读写。并且所有正在执行的或执行完成的变更记录可在在线变更检测页面查看。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image14.png)

### SQL路由计划查看

HotDB Server提供SQL路由计划查看功能。可查看被执行SQL语句的路由计划，展示SQL通过计算节点路由分析后具体下发的数据节点，为用户提供SQL下发情况预测信息。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image15.png)

### 配置参数校验

HotDB Server支持对当前已配置的数据节点、存储节点、逻辑库、分片规则、数据库用户等信息进行一键式检测。如有异常或错误，则提示错误信息并定位到具体的错误源位置。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image16.png)

### 多集群服务管理

管理平台支持管理多套计算节点集群。用户可在登录管理平台后在"计算节点选择"页面选择具体的集群进入管理。同时"计算节点选择"页面支持对集群内所有的计算节点实例运行状态以及配置库所有实例运行状态进行实时展示。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image17.png)

### 智能逻辑拓扑

- 管理平台基于计算节点的应用连接池和数据库连接池信息，动态生成每个应用程序客户端的：连接数、QPS；每个数据节点的：复制状态、数据容量、连接数、QPS；每个存储节点的：复制时延、连接数、QPS；每个逻辑库的：连接数、QPS以及计算节点的各个参数状态值。这些信息在拓扑图中集中展示。

- 用户可为拓扑图中监控的对象设置报警阈值。当达到阈值时图标会以闪烁与颜色变化（黄色警告、红色报警）的方式提示系统出现的异常。用户可以通过鼠标悬停具体报警的图标了解报警原因，帮助用户快速准确定位出现问题的位置。

- 拓扑图支持记录并展示前端应用、计算节点、存储节点产生的INFO、WARNING、ERROR信息。

- 支持2D与2.5D拓扑图切换查看。

- 用户可通过拓扑图直接对具备主从或双主复制关系的数据节点进行手动高可用切换，也可以右键复制每一个存储节点的数据库连接信息。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image18.png)

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image19.png)

### 智能物理拓扑

物理拓扑图主要从服务器的视角展示集群组件与服务器之间的关系。同时，可查看服务器资源使用情况以及集群组件服务的运行状态。需要为服务器配置可用的SSH连接信息，否则只能查看服务器与集群组件的所属关系，无法查看服务器资源使用情况与组件程序的状态。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image20.png)

### 监控面板

管理平台支持对计算节点服务状态、计算节点吞吐量以及计算节点服务器资源的监控。

- 计算节点服务状态监控：客户端连接总数、计算节点线程使用情况、后端连接状态、计算节点直接内存使用率、实时数据量、计算节点堆内存使用率。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image21.png)

- 计算节点吞吐量：网络流量监控、TPS、QPS、客户端操作速率、后端操作速率。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image22.png)

- 计算节点服务器资源：服务器内存使用情况、服务器磁盘空间使用情况、服务器CPU负载情况、服务器CPU使用率、服务器磁盘读写情况、服务器网络流量进出情况、服务器磁盘IO带宽利用率。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image23.png)

- 集群资源监控：包括存储节点及其他有SSH访问权限的服务器。监控项有：CPU使用率、内存使用情况、磁盘使用情况、网络进出流量。对超出配置的监控阈值的服务器进行预警、对无法连接的服务器进行故障显示。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image24.png)

- 数据增量预测：可以根据历史数据记录，提前规划存储节点/配置库数据容量。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image25.png)

### JOIN关系分析

管理平台基于计算节点记录的SQL日志，利用符合JOIN查询场景的SQL日志，以可视化的形式展现各业务表之间的关联关系。用户通过图形化的展示可快速定位业务中存在高频JOIN的表，以及定位因种种原因而成为跨库有交叉类型JOIN的SQL。为用户调整分片规则与优化JOIN查询SQL，提升系统性能提供可靠依据。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image26.png)

### 数据报表

支持集群数据量、计算节点吞吐量、数据节点吞吐量、计算节点连接信息的报表展示。展示形式可选择图形模式或者表格模式，同时可将报表数据直接导出到本地。

- 集群数据量报表：集群数据量变化趋势图、集群数据量分布图、逻辑库数据量分布图、表数据量分布图。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image27.png)

- 计算节点吞吐量报表：计算节点吞吐量变化趋势图、计算节点吞吐类型对比图、逻辑库吞吐量对比图、表吞吐量对比图。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image28.png)

- 数据节点吞吐量报表：数据节点吞吐总量对比图、数据节点吞吐量变化趋势、集群吞吐类型对比图、逻辑库吞吐量对比图、表吞吐量对比图。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image29.png)

- 计算节点连接报表：总连接数、连接时长最长的连接、操作次数最多的连接、连接次数最多的连接、连接总时长占比、连接总次数占比、操作次数占比、前端应用IP连接分布图、连接用户分布图、逻辑库分布图。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image30.png)

### 表结构与索引检测

管理平台支持按逻辑库为单位，检测逻辑库下的表，在所属数据节点中的表结构与索引定义是否一致。检测到不一致的表则在检测结果中显示出不一致的原因。此外还可以通过添加定时任务监测业务表状态，发现表结构或索引存在定义异常系统将立即在事件通知中提醒，帮助用户及时发现有问题的表。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image31.png)

### 审计日志

管理平台支持对用户操作的审计记录，包括：管理平台基本操作、安全防护操作、管理端口命令操作等。有助于系统出现异常时，进行问题排查、分析。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image32.png)

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image33.png)

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image34.png)

### 操作日志智能分析

管理平台提供统计select、insert、update、delete、事务开启、提交、回滚等SQL语句执行耗时及执行次数详情的操作日志智能分析功能。通过内部算法自动分析出需要优化的SQL语句，并通过待优化标志以及SQL优化建议辅助用户对业务SQL进行调优。用户也可以自主查询页面统计结果得到SQL执行的情况，分析出哪些SQL语句需要优化，有利于系统性能提升。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image35.png)

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image36.png)

### 业务数据汇报

可对年度集群运行状况的关键数据进行汇总报告，以便了解集群运行状况。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image37.png)

### 历史事件与计算节点日志

#### 历史事件

主要记录服务器时间差异、参数感知、存储节点被共用、主备数据一致性检测、一键迁库、全局表数据检测、表结构与表索引检测、配置修改导致备份失效、全局唯一约束异常等相关事件信息。不同事件信息对应不同的报警级别包括：ERROR、WARNING、INFO、UNKNOW。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image38.png)

#### 计算节点日志

主要提供计算节点运行过程中产生的日志信息。管理平台默认只获取计算节点中ERROR级别的日志信息（可自定义获取日志级别）。可通过时间范围、日志类型、日志级别、查看状态、日志内容对日志信息进行筛选。多节点模式集群可支持查看多个计算节点上的日志信息。同时支持将日志文件导出到本地保存。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image39.png)

### 分片合理性评分

管理平台提供对已创建的水平分片表的分片方案进行合理性评分，展示业务表在当前分片方案中各个维度的得分表现，帮助用户及时发现拆分不合理的业务表。

> **五个评判维度：**

- 数据量分布均匀得分

> 根据各节点数据量分布是否均匀、增长量是否均匀计算得分。

- 跨库事务占比得分

> 根据跨节点事务查询次数占比计算得分。

- SELECT操作均匀得分

> 根据各个节点查询总量是否均匀、跨库join查询比例、单库查询比例、无法路由导致查询所有节点的查询比例计算得分。

- IUD（Insert/Update/Delete）操作均匀得分

> 根据各个节点IUD操作量是否均匀、单库IUD操作比例计算得分。

- 其他得分

> 根据查询无法找到节点的次数、分片字段定义是否合理计算得分。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image40.png)

### 系统异常事件邮件提醒

通过管理平台配置：发件箱参数、添加邮件接收人信息以及勾选系统监控内容后，可使用邮件提醒功能。目前邮件提醒的监控范围包括：计算节点与存储节点故障或切换、计算节点服务器资源状态、计算节点服务状态、存储节点相关检测、系统定时任务检测、许可证授权监控。若本地无法正常接收邮件，也可配置将报警日志内容输出到本地文本中。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image41.png)

### 多线程备份

HotDB Server提供类似Mydumper的多线程备份工具HotDB Backup

**特性：**

- 保证分布式事务数据库全局的时间点和数据状态一致。

- 备份期间对线上业务无阻塞。

- 增量备份自动跟随完整备份。

- 库级别和表级别的双并行备份。

- 备份过程可手动取消正在执行的备份任务。

- 支持添加备份计划定时备份业务数据，也可以手动延迟下一次备份任务时间或设置定时计划内某个时间点不进行备份。

- 支持XA（强一致）模式下数据备份恢复到指定时间点。

- 除此之外，HotDB Backup也支持加密备份文件、计算文件MD5值、备份至远程等功能。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image42.png)

以下是HotDB Backup与传统几款常用的备份工具对比图：

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image43.png)

### 数据恢复

HotDB Server支持数据备份后在界面发起数据恢复请求。可按照恢复时间点对备份数据进行恢复，保证数据完整性。恢复会自动根据选择的时间点带出可用于该时间点恢复的完整备份和增量备份文件。恢复过程中出现的SQL执行错误都可以在界面详细日志中查看。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image44.png)

### SQL防火墙与白名单

用户可以设置SQL防火墙，拦截可疑的操作如："无WHERE条件的DELETE、无WHERE条件的UPDATE"等；也可以设置IP访问白名单，限定允许连接HotDB Server服务的IP地址范围。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image45.png)

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image46.png)

### 一键迁库

HotDB Server支持在线一键迁库功能。当存储节点所在的服务器硬件配置不足或MySQL版本需要停机升级时，可通过一键迁库功能将存储节点数据迁移至新的存储节点服务器上。一键迁库本质上是将数据节点下的存储节点更换为其余有MySQL复制关系的，拥有相同数据的，其它存储节点。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image47.png)

### 过载保护/限流

#### 前端连接限制

HotDB Server支持对前端连接数总数和用户连接数进行限制，当连接数超过限制时将拒绝前端连接并给出错误提示。

#### 存储节点连接限制

HotDB Server支持对存储节点最大连接数进行限制，实现对存储节点的保护。

#### 存储节点智能流控

HotDB Server支持对在后端执行的各类SQL语句进行智能流控。可以根据存储节点性能表现智能调控SQL流量，保持存储节点工作在最佳状态，防止某一个存储节点因并发压力过大而宕机。

### 监控信息管理

管理平台支持通过界面执行部分计算节点管理端口（默认3325）中的管理命令。例如查看计算节点的前后端连接状态、当前会话连接信息、SQL运行情况、计算节点线程资源情况等。方便用户排查问题，快速解决系统故障或隐患。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image48.png)

### 配置参数热加载

HotDB Server 支持配置参数的热加载，当更新计算节点、存储节点、逻辑库、表信息、分片规则等配置时，管理平台将通过页面提示引导用户及时点击动态加载更新计算节点内存中的配置信息。用户可以通过点击页面按钮直接加载参数到计算节点，无需重启计算节点服务。

### 用户权限控制管理

#### 管理平台用户

该用户为分布式事务数据库平台用户，分为管理员用户与普通用户。

- 管理员用户：

可为管理平台添加普通用户以及添加部署计算节点集群。且可对已授权的计算节点集群进行管理，支持在管理平台用户信息中来回切换管理角色与普通用户角色视角。

- 普通用户：

实际管理计算节点集群的用户，对已授权的计算节点集群拥有访问或者控制权限。

#### 数据库用户

该用户为访问计算节点服务的用户。HotDB Server的用户权限体系兼容MySQL提供全局权限、库权限、表级权限多维度配置。同时新增了表级拒绝权限，方便管理员快速隔离用户对安全级别较高的业务表进行操作。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image49.png)

### 高可用环境切换及重建

HotDB Server支持通过管理平台对主备模式的计算节点集群进行可视化的手动高可用切换操作，也可以在计算节点发生高可用切换(手动或故障切换)之后，重建高可用环境，保证下次主计算节点发生故障时程序可正常切换。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image50.png)

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image51.png)

### 安装部署

#### 集群部署

集群部署功能是面向分布式事务数据库集群进行快速部署的整体解决方案，支持对单计算节点、主备计算节点、多计算节点三种集群模式的快速部署。可安装计算节点服务、配置库实例、Keepalived、LVS、NTPD、备份程序、存储节点实例等集群所需的组件。通过集群部署可快速完成整套集群所需的组件安装、组件间关系搭建、服务启动、生成组件拓扑图等工作。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image52.png)

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image53.png)

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image54.png)

#### 单机部署

单机部署可为已部署好的分布式事务数据库集群增加存储节点实例或其他所需组件，也可通过单机部署实现新增组件的关系搭建与服务启动。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image55.png)

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image56.png)

#### 在线升级

支持通过管理平台对HotDB Server版本进行在线升级。满足对单节点、主备节点、多节点集群模式的跨版本或小版本升级迭代。同时为用户提供升级过程突发异常情况时的自动回滚机制，程序尽量保证将集群回滚至升级前的状态，减少对线上业务的影响。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image57.png)

### 部署环境体检

部署环境体检是一套专门为HotDB Server集群量身打造的运行环境体检评分功能。无论是通过手动安装还是管理平台部署的集群，都可以使用该功能为集群运行环境进行评测。评测后将展示出整个集群五大维度接近140个体检细分项目的体检结果，为集群运行环境优化提供更全面的标准的参考信息。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image58.png)

### 信息收集

HotDB Server集群组件较多，运行机制较为复杂。当出现异常问题或故障时，如果信息收集不全面，分析排查比较困难。利用信息收集工具可快速在出现问题时，搜集分析所需的日志与配置文件信息，从而提高问题排查的速度与效率。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image59.png)

### 许可证管理

管理平台支持对计算节点许可证进行在线更新或激活操作。可对试用许可证激活为正式许可证、试用许可证更新、正式许可证更新、许可证首次激活等多种场景提供功能支持。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image60.png)

### 网络感知

计算节点支持定时检测集群内计算节点到存储节点、配置库所在服务器间网络质量。对不符合网络质量的链路进行记录配置库以及日志，并展示在管理平台上，方便用户排查因网络问题导致的集群运行异常或故障。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image61.png)

### 智能巡检

> 支持可视化界面定期巡检计算节点集群运行状态，及时规避线上隐患问题。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image62.png)

## 数据库安全控制

支持使用SSL+SM4国密认证的方式登录连接计算节点。

## 其他

HotDB Server支持通过DNID（DATANODE_ID）查询指定数据节点中的数据。支持读写分离，且可配置主从读写比例与多从机读比例自动均分功能。支持通过第三方数据库管理工具对HotDB Server服务端口进行连接管理。

### DNID

DNID是数据节点DATANODE_ID的缩写。可以在hint中使用相关语法控制SQL下发的节点（使用时需小心谨慎，并注意相关注意事项）。SELECT查询语句中也可以使用DNID作为WHERE子句中的过滤条件，以及在SELECT子句中作为查询项，还可以使用会话变量（session variable）控制是否在结果集中显示每行结果的DNID。

### 读写分离

- HotDB Server支持读写分离功能，并且支持配置读写分离权重。此功能默认设置为关闭，可配置多种模式：
  - 读写操作都在主存储节点，也即关闭读写分离。
  - 可分离的读请求发往所有可用存储节点（包含主存储节点）
  - 可分离的读请求发往可用的备存储节点

**注：**上述"可分离的读请求"主要指未加hint的自动提交的读请求与显式只读事务中的请求。其余未加hint的读请求均为"不可分离的读请求"。

- 事务（非XA模式）中发生写前的读请求与自动提交的读请求发往可用的备存储节点。其余请求在主存储节点上进行。
  - 当存储节点数据同步延迟超过1秒（可配置）或者出现故障时计算节点会摘除该存储节点并阻止参与读操作，此时由其他正常存储节点承担可分离的读任务，直至延迟重新追上才将摘除的存储节点加回读集群。
  - HotDB Server读写分离对应用研发者和数据库管理员完全透明，不要求研发者在SQL执行时添加hint或某些注解；当然，也支持使用hint的方式显式指定读取主机或从机。

### 第三方客户端

HotDB Server支持Navicat、Workbench等第三方数据库管理工具。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image63.png)

Navicat连接HotDB Server数据服务端口示意图

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image64.png)

Workbench连接HotDB Server数据服务端口示意图

### 产品国际化

HotDB Server产品以及配套的管理平台支持中文与英文两种语言模式，可根据用户实际要求进行在线切换。同时为产品的使用提供全英文的产品功能手册，帮助海外用户方便使用产品。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image65.png)

# HotDB Server部署配置

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image66.png)

集群主备模式部署架构示意图

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image67.png)

集群负载均衡模式部署架构示意图

## 配置推荐信息

### 计算节点服务器（兼计算节点配置库）

处理器：Gold 6130\*2颗

内存：8G\*12根（有单条4G内存的情况下建议4G\*12根）

硬盘：2.5\' 800G 写入密集型 SATA\\SAS SSD \*2 RAID 1（选用800G原因为写入寿命更长）

RAID卡：H730P

网卡：万兆网卡

服务器数量：2（集群负载均衡模式则至少3台最多9台）

**注：**集群负载均衡模式建议计算节点配置库单独占用服务器，不与计算节点或存储节点服务器共用。计算节点配置库独占服务器时，配置可参考"[管理平台配置库服务器](#管理平台配置库服务器)"。

### 存储节点服务器

处理器：Silver 4116\*2颗

内存：16G\*12根

硬盘：2.5\' 2.4T 10K SAS HDD \*2 RAID 1（用于系统与备份文件存储）

+2.5\' 800G 写入密集型 SATA\\SAS SSD \*6 RAID 5（用于MySQL）

RAID卡：H730P

网卡：千兆网卡

服务器数量：至少2台（按需添加）

### 管理平台服务器

处理器：Silver 4108\*2颗

内存：8G\*12根（有单条4G内存的情况下建议4G\*12根）

硬盘：2.5\' 240G SATA SSD \*2 RAID 1

RAID卡：H330

网卡：板载千兆

服务器数量：1台或复用

### 管理平台配置库服务器

处理器：Silver 4110\*2颗

内存：8G\*12根（有单条4G内存的情况下建议4G\*12根）

硬盘：2.5\' 400G 写入密集型 SATA\\SAS SSD \*2 RAID 1

RAID卡：H730P

网卡：千兆网卡

服务器数量：1台或复用

### LVS服务器（集群负载均衡模式）

处理器：Silver 4116\*2颗

内存：8G\*12根（有单条4G内存的情况下建议4G\*12根）

硬盘：2.5\' 240G SATA SSD \*2 RAID 1

RAID卡：H330

网卡：万兆网卡

服务器数量：2台

### 交换机

- 建议交换机接口速度和服务器配置的网卡接口速度一致或更高。

- 建议使用汇聚层级别或更高性能等级的交换机，且实测得到的交换机包转发速率超过10Mpps或支持线速转发。

- 建议所有服务器部署在同一交换机（或堆叠）下，若无法做到，应采取网络跳数尽可能少的部署方式。

**注：**不建议集群的网络流量通过任何路由器或者防火墙。

- 若部署高可用网络，建议优先使用Bond0模式。

**注：**性能测试过程中，除关注服务器性能指标外，一定要关注交换机是否丢包，很多交换机实际的pps性能远远低于标称指标。

### 特别说明

- 以上配置以DELL服务器为例，其它厂商机型选择同等配置即可。

- MySQL数据库服务器数量需要以生产环境或性能测试的TPS/QPS目标进行评估，描述的存储节点服务器单台处理能力，且主备延迟控制在1秒以内，可在生产环境稳定支撑运行的数值：TPS 4000-6000，QPS：15000左右

**注：**以上场景若以读为主的情况，则QPS会更高；此处TPS指简单TPS，复杂TPS需要实测才能得出具体数据。

**特殊说明：**性能测试环境中MySQL服务器通常可以测得比此描述更高的数值，但同时一般都会出现严重的主备延迟，或者SQL响应时间异常长，响应时间\\吞吐量抖动等问题。这是由于性能压测一般不控制具体流量，而是控制并发数；足够的并发数可以将MySQL实例的性能压榨到极限。但这样的极限状态，尽管吞吐量大，整体QoS（Quality of Service）却很差，因此这种极限状态下的性能指标并不适合用于评估生产环境。生产环境进行规划时，建议取性能测试得到吞吐量指标的50%与复制追赶速度的80%中较小的数值，可以得到较好的QoS。

- 假设性能测试给出的是至少2台数据库服务器、部署4对mysqld实例，且采用双主复制交叉部署，一般可测试TPS 4万以上、QPS 10万以上的场景。

**注：**此压力下，一般会出现MySQL复制延迟、SQL响应时间差的问题，属于正常现象。这样测试方式得到的性能测试指标对于评估HotDB Server计算节点支撑的吞吐量上限能力有意义，但不适合评估存储节点

吞吐量。

- 以上配置为测试环境（含压力测试环境）HA或集群负载均衡架构的部署环境推荐说明，实际生产环境配置需联系热璞科技具体评估。

# 案例介绍

HotDB Server经过多年研磨，克难攻坚，在金融行业、通讯行业、快递物流行业、广电传媒行业、零售行业等树立良好口碑，帮助众多客户成功走上分布式事务数据库的道路，轻松解决了传统架构中的"两大三高"（海量数据、海量用户、高可用、高性能、高并发）难题，以下是一些比较典型的客户案例。

## 圆通速递

**所属行业：**快递物流业

**项目名称：**金刚核心系统改造

**案例简介：**

圆通速递的金刚核心系统原系统支撑能力峰值达到650万单/天就宕机，经过分布式化改造之后，自实施的第一年2013年顺利支撑峰值1350万单/天，2014年顺利支撑峰值2300万单/天，2015年顺利支撑峰值5300万单/天，2016年顺利支撑8900万单/天。将金刚系统的核心组成部分：高端小型机、高端存储设备、WAS中间件、Oracle数据库，转型改造为：X86服务器、JBOSS中间件、Redis、分布式事务数据库HotDB Server和Hadoop大数据平台组合的分布式架构，轻松地支持了业务量的快速增长。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image68.jpeg)

## 中国人民银行

**所属行业：**金融行业

**项目名称：**中国人民银行征信中心

**案例简介：**

围绕中国人民银行征信中心的MySQL数据库实施服务技术要求，从数据库分布式架构设计、数据分片设计、数据架构治理原则，及MySQL数据库的安装部署、标准初始化、操作系统定制化、开发规范、监控报警定制、配置规范、数据迁移、性能优化、参数优化、高可用设计、研发支持等多个维度，综合保障业务系统的MySQL数据库服务稳定、可靠和高效，同时建立符合征信中心特色的MySQL数据库运维管理体系。实现了对全国6个数据中心，超过8000个物理服务器，300万以上监控项的监控。突破了Zabbix监控软件的NVPS瓶颈，提升了Zabbix的数据处理效率和吞吐量。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image69.png)

## 银联商务

**所属行业：**金融行业

**项目名称：**银联商务大O系统分布式改造

**案例简介：**

银联商务引入分布式事务数据库HotDB Server后，先期从BBS系统、内部管理及办公系统、开放API系统等方面进行MySQL数据库分布式方案改造。根据银联商务系统特征，热璞科技提供了从数据库分布式架构设计、数据分片设计、数据架构治理原则，及数据库的安装部署等方案。同时HotDB Server分布式事务数据库产品提供完备的高可用解决方案，读写分离，容灾备份，监控报警等功能，帮助银联商务成功进行异构数据迁移，并帮助银联商务建立MySQL运维体系。

![](../https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image70.png)

## 国开银行

**所属行业：**金融行业

**项目名称：**国开行助学贷款系统分布式事务数据库替换

**案例简介：**

国家开发银行的学生助学贷款业务系统在开学期间经常遇到高并发高吞吐等问题。因此引入了国产自研的分布式事务数据库HotDB Server。通过多轮测试验证，HotDB Server能够保证分布式事务强一致、主备数据异常场景下强一致、备份强一致、数据服务稳定、智能化运维平台等，保障整个系统的稳定运行，支撑TB-PB级数据访问、高并发、高吞吐的业务场景，大大提升了业务系统提升服务海量用户和处理海量数据的能力。

![](https://hotdb-community.github.io/HotDB-Knowledge-Base/assets/readme/image71.png)
