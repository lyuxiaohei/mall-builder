/* namespace.js — 全局命名空间根。
 *
 * 所有 common/ 下的共享模块把自身挂到 window.MallBuilder 的子命名空间下，
 * 供 pages/*.html（页面编辑器）和 components/*.html（组件 playground）共同复用。
 *
 * 采用经典 <script src> + 单一命名空间（非 ES module），保留 file:// 双击打开、
 * 与 src/index.html 现有 data.js/app.js 加载方式一致，零构建工具。
 *
 * 加载顺序约束：本文件必须在所有其它 common/*.js 之前加载。
 * Phase 1 建立空命名空间；Phase 2+ 逐步把 editor.html 内 IIFE 的私有
 * 函数/状态迁移到对应子命名空间。
 */
(function () {
  if (window.MallBuilder) return; // 幂等：允许重复引入

  window.MallBuilder = {
    // DOM 引用（由 dom-refs.js 按 面板/弹窗 分组填充）
    dom: {},

    // 全局状态：pageStore / currentPageId / selectedFloorId / tabbarConfig /
    // mallSettings / THEME_COLORS / categoryData ...（由 state.js 填充）
    state: {},

    // 通用工具：getCategoryNameById / getBrandNameById / getFloorTypeName /
    // escapeHtml / ...（由 utils/common.js 填充）
    utils: {},

    // 复用配置块：配色 / 内边距 / 圆角 的 markup+bind 片段（由 utils/shared-props.js 填充）
    sharedProps: {},

    // Mock 数据：MOCK_GOODS_DATA / MOCK_BRANDS / MOCK_TAGS / MOCK_CATEGORIES /
    // MATERIAL_LIBRARY ...（由 data/*.js 填充）
    data: {},

    // 组件注册表：每个组件 register 一个描述符 {type,configKey,defaultConfig,
    // propsMarkup,bindProps,canvasMarkup,previewMarkup}，消解原 4 条 if/else 链。
    components: {
      _registry: {},
      register: function (desc) {
        if (!desc || !desc.type) return;
        this._registry[desc.type] = desc;
      },
      get: function (type) {
        return this._registry[type];
      },
      has: function (type) {
        return Object.prototype.hasOwnProperty.call(this._registry, type);
      },
      list: function () {
        return Object.keys(this._registry);
      },
    },

    // 画布组合逻辑：renderCanvas / 楼层拖拽/排序/选中/增删/复制（由 canvas.js 填充）
    canvas: {},

    // 6 个弹窗：新增页面 / 单商品 / 富文本 / 图片选择器 / 商品来源（由 modals/*.js 填充）
    modals: {},

    // 页面类型编辑器启动器（由 pages/_page-editor.js + pages/<type>.js 填充）
    pages: {},

    // 组件 playground 启动器（由 components/_playground.js 填充）
    playgrounds: {},
  };
})();
