# 商城搭建系统 - Mall Builder

基于「平台侧制作模板 → 品牌方落地使用」的产品思路，实现的**可交互原型**，用于演示运营工作台的核心流程与界面结构。

## 如何运行

> **所有页面都支持直接双击在浏览器打开（file://），无需启动任何本地服务器。**

### 方式一：直接双击打开（推荐，无需服务器）
双击 `src/page-index.html`（原型总入口，导航到所有页面/组件），或直接双击 `src/pages/` 下任意一个页面：
- `src/page-index.html` — **原型总入口**（目录页；同名 `page-index.md` 是其文本目录，便于编辑/版本追踪）
- `src/pages/editor.html` — 完整编辑器（空画布）
- `src/pages/index.html` — 运营工作台（模板管理）
- `src/pages/material-library.html` — 素材库（后台规范）
- `src/pages/page-{home,category,mine,product-detail,cart,custom}.html` — 每个页面类型一个（共 6 个）
- `src/pages/comp-*.html` — 每个组件类型一个（共 16 个）

### 方式二：使用本地服务器（可选）
想用 http 访问时（例如需要 DevTools Network 面板），在项目根目录运行：

```bash
# 使用 Python 简易服务器（在项目根目录运行）
python -m http.server 8080

# 或使用 Node.js 的 http-server
npx http-server -p 8080
```

然后访问 http://localhost:8080/src/page-index.html 。

### 方式三：VS Code Live Server
1. 安装 VS Code 的 Live Server 扩展
2. 右键点击 HTML 文件，选择 "Open with Live Server"

## 功能概览

| 模块 | 说明 |
|------|------|
| **模板列表** | 控制台首页，展示模板名称、封面、状态（草稿/已发布/已推送）、标签、最近修改时间、使用次数；支持按状态、标签筛选；支持批量勾选。 |
| **新建模板** | 两种入口：从空白新建、复制已有模板；填写模板名称后进入编辑器。 |
| **草稿 / 发布 / 删除** | 列表内操作：编辑、发布（会先进入「发布前预览」）、推送、删除；删除已推送模板时有二次确认提示。 |
| **发布前预览** | 发布前强制预览卡点，支持 PC / 移动端切换，确认后再发布。 |
| **批量设置标签** | 勾选多条模板后，可批量设置系统标签与自定义标签（演示用弹窗）。 |
| **模板编辑器** | 独立页面 `editor.html`：左侧组件库、中间画布、右侧属性面板；顶部有设备切换（PC/移动端）、保存、预览、发布。 |
| **推送品牌商城** | 选择模板、推送方式（仅模板 / 模板+数据）、多选品牌方，确认推送；推送记录在「推送记录」页查看。 |
| **推送记录** | 展示推送时间、模板、推送对象、推送方式、操作人、品牌方状态。 |
| **商城列表** | 展示商城名称、关联品牌、状态（运营中/已关闭）、创建时间；支持搜索商城名称或品牌、新建商城、一键复制商城。 |

## 编辑器组件

编辑器支持以下组件类型：

| 组件 | 说明 |
|------|------|
| **轮播图** | 支持多张图片轮播，可设置延伸功能（图片延伸至页面顶部，z-index在下层） |
| **图文导航** | 图标+文字的导航入口 |
| **商品分组** | 商品展示分组，支持多种数据来源配置 |
| **商品列表** | 商品列表展示，支持品牌/标签/分类/单品/API对接五种数据来源 |
| **富文本** | 富文本内容编辑 |
| **标题文本** | 标题和副标题展示 |
| **文本内容** | 普通文本内容展示 |
| **链接** | 可点击链接 |
| **大图** | 大尺寸图片展示 |
| **营销活动** | 营销活动展示区块 |
| **悬浮组件** | 悬浮按钮，支持置顶、购物车、客服等多种功能类型，可自由定位 |
| **分类展示** | 分类页面专属组件，展示分类导航和商品 |
| **底部导航** | Tabbar导航，可配置显示/隐藏 |

## 架构（重构后）

原 `editor.html` 是 14,000+ 行的单体文件（内联 CSS + 内联 JS）。重构后拆为「**共享骨架 + 每个页面类型/组件类型各一个独立 html + 共享应用逻辑**」的多页面结构：

- **通用骨架一致**：编辑器外壳（顶栏 / 左侧栏 / 画布手机框 / 右侧属性面板 / 6 个弹窗）抽成 `common/skeleton.js`，由 `editor-app.js` 启动时自动注入。所有编辑器页面共用同一套骨架，是代码级保证而非复制粘贴。
- **每个页面类型一个 html**：`src/pages/page-{home,category,mine,product-detail,cart,custom}.html`（6 个），各为 ~22 行薄壳，通过 `window.__EDITOR_CONFIG__ = { mode:'page-editor', pageType }` 声明模式，复用骨架与逻辑，打开即预置对应页面。
- **每个组件类型一个 html**：`src/pages/comp-<type>.html`（共 16 个），声明 `{ mode:'component-playground', componentType }`，打开即预置单个组件并选中，专注配置该组件。
- **页面导航拆为 md + html**（参考 mini-program）：`src/page-index.md`（markdown 目录，易编辑/版本追踪）+ `src/page-index.html`（可视化目录，双击总入口）。所有可运行页面集中在 `src/pages/`，共享资源（`common/`、`styles.css`、`data.js`、`app.js`）在 `src/`，页面用 `../` 引用。
- **应用逻辑共享**：`common/editor-app.js`（原内联 IIFE 整体外置）+ `common/data/*.js`（Mock 数据）+ `common/namespace.js`（`window.MallBuilder` 命名空间）。用经典 `<script src>` 加载，**直接双击在浏览器运行（file://），无需服务器**，零构建工具。
- **素材库**：`material-library.html` 按后台设计规范（`#1890ff` / Header 64 / Sider 200 / 5 列网格 / 分页 36px），接入 `styles.css` 共享 token。

## 目录结构

```
mall-builder/
├── src/                       # 源码
│   ├── page-index.html        # 原型总入口（可视化目录，双击打开）
│   ├── page-index.md          # 同名 markdown 目录（易编辑/版本追踪）
│   ├── styles.css             # 全局样式 + :root 设计 token（权威源）
│   ├── app.js / data.js       # 工作台专属逻辑与 Mock 数据
│   ├── common/                # 共享层（所有编辑器页面复用）
│   │   ├── admin-layout.css   # 编辑器外壳样式
│   │   ├── skeleton.js        # 通用页面骨架（注入 chrome）
│   │   ├── namespace.js       # window.MallBuilder 命名空间 + 组件注册表
│   │   ├── editor-app.js      # 编辑器全部应用逻辑（原内联 IIFE）
│   │   └── data/              # Mock 数据（taxonomy / material-library / goods）
│   └── pages/                 # 所有可运行页面 html（25 个）
│       ├── editor.html  index.html  material-library.html
│       ├── page-{home,category,mine,product-detail,cart,custom}.html  # 6 个页面类型
│       └── comp-*.html        # 16 个组件 playground
├── assets/                    # 静态资源（图片素材，页面用 ../../assets/ 引用）
├── docs/                      # 项目文档（PRD / 组件配置 / 功能清单）
├── tests/                     # Playwright 脚本与截图
├── archive/
│   └── legacy-root-copies/    # Phase 0 归档的根目录陈旧副本
└── README.md
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `src/page-index.html` | 原型总入口（可视化目录），双击打开导航到所有页面 |
| `src/page-index.md` | 同名 markdown 目录（页面/组件清单，易编辑） |
| `src/pages/editor.html` | 完整编辑器（19 行薄壳，外壳由 `common/skeleton.js` 注入） |
| `src/pages/index.html` | 运营工作台（模板列表、商城列表、推送记录） |
| `src/pages/material-library.html` | 素材库（后台规范） |
| `src/pages/page-*.html` | 每个页面类型一个 html（home/category/mine/product-detail/cart/custom，共 6 个） |
| `src/pages/comp-*.html` | 每个组件类型一个 html playground（16 个） |
| `src/common/skeleton.js` | 通用编辑器骨架（顶栏/左侧栏/画布/属性面板/弹窗），所有编辑器页面共享 |
| `src/common/editor-app.js` | 编辑器全部应用逻辑（原内联 IIFE，含 `__EDITOR_CONFIG__` 钩子） |
| `src/styles.css` | 全局样式 + `:root` 设计 token（权威源，所有页面引用） |
| `src/common/data/*.js` | Mock 数据（品牌/标签/分类/商品/素材库） |
| `src/app.js` / `src/data.js` | 工作台（index.html）专属逻辑与 Mock 数据 |

## 商品数据来源配置

商品分组和商品列表组件支持五种数据来源：

| 来源类型 | 说明 |
|----------|------|
| **按品牌** | 选择品牌，展示该品牌下的商品 |
| **按标签** | 选择标签，展示带有该标签的商品 |
| **按分类** | 选择分类，展示该分类下的商品 |
| **按单品** | 直接选择具体商品，支持搜索和分页 |
| **API对接** | 输入API链接获取商品数据，显示商品预览列表供选择 |

## 页面类型

编辑器支持多种页面类型：

| 页面类型 | 说明 |
|----------|------|
| **首页** | 默认主页，展示商城首页内容 |
| **分类页** | 商品分类展示页面 |
| **我的** | 个人中心页面 |
| **商品详情** | 单个商品详情展示 |
| **购物车** | 购物车页面 |
| **自定义页面** | 自定义内容的空白页面 |

## 产品要点在本原型中的体现

- **模板即品牌商城配置载体**：列表与编辑均围绕「模板」这一实体
- **状态与标签并存**：状态筛选控制工作流（草稿→发布→推送），标签筛选做业务分类
- **新建支持空白 + 复制**：新建弹窗中两种方式可选
- **发布前强制预览**：发布前先弹预览弹窗，再确认发布
- **推送支持多选品牌与两种方式**：仅模板 / 模板+数据，并有多选品牌列表
- **推送记录与商城列表**：独立页面展示推送记录与商城列表；商城列表支持搜索、新建、一键复制

## 相关文档

- [组件&配置项文档](docs/组件&配置项V1.4-20260401.md) - 最新组件配置详细说明
- [功能清单](docs/组件&功能清单V2.0-20260331.md) - 组件功能清单
- [素材库页面](src/material-library.html) - 素材库功能页面

---

本原型仅用于产品演示与评审，数据为前端 Mock，不连接真实后端。