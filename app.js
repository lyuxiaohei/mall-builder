/**
 * 商城搭建系统 - 原型演示逻辑
 * 负责页面切换、列表渲染、弹窗与模拟操作
 */

(function () {
  /** 当前选中的模板 ID 列表（用于批量操作） */
  let selectedTemplateIds = [];

  /** 当前要发布/推送的模板 ID（用于弹窗流程） */
  let currentFlowTemplateId = null;

  /** 模板列表当前页码与每页数量（前端分页） */
  let currentTemplatePage = 1;
  const TEMPLATE_PAGE_SIZE = 5;

  /** 当前筛选后的模板列表（分页基准） */
  let filteredTemplates = [];

  /** 当前正在查看页面管理的模板 */
  let currentTemplateForPages = null;
  /** 当前页面管理选中的页面类型 */
  let currentTemplatePageType = 'home';

  /**
   * 根据状态码返回显示文案
   * @param {string} status - draft | published | pushed
   * @returns {string}
   */
  function getStatusText(status) {
    const map = { draft: '草稿', published: '已发布', pushed: '已发布' };
    return map[status] || status;
  }

  /**
   * 返回模板封面的渐变样式类
   * @param {string} status - 模板状态
   * @returns {string}
   */
  function getTemplateCoverClass(status) {
    const map = {
      draft: 'cover-draft',
      published: 'cover-published',
      pushed: 'cover-published',
    };
    return map[status] || 'cover-draft';
  }

  /**
   * 返回模板在列表中使用的统一状态值
   * @param {string} status - 原始状态
   * @returns {string}
   */
  function getTemplateDisplayStatus(status) {
    return status === 'pushed' ? 'published' : status;
  }

  /**
   * 更新模板列表勾选摘要
   */
  function updateTemplateSelectionSummary() {
    const summary = document.getElementById('template-selection-summary');
    if (summary) {
      summary.textContent = '已选择 ' + selectedTemplateIds.length + ' 个模板';
    }
  }

  /**
   * 生成小程序首页风格预览图
   * @param {Object} template - 模板数据
   * @returns {string}
   */
  function getTemplatePreviewSrc(template) {
    const paletteMap = {
      beauty: {
        shell: '#FFF6F4',
        panel: '#FFFFFF',
        bannerA: '#FF6B6B',
        bannerB: '#FF9F7F',
        accent: '#FF7875',
        soft: '#FFE7E3',
        icon1: '#FFD8BF',
        icon2: '#FFD6E7',
        icon3: '#FFE58F',
        product1: '#FFF1F0',
        product2: '#FFF7E6',
      },
      food: {
        shell: '#F6FFF1',
        panel: '#FFFFFF',
        bannerA: '#52C41A',
        bannerB: '#95DE64',
        accent: '#389E0D',
        soft: '#E8FCCA',
        icon1: '#D9F7BE',
        icon2: '#B7EB8F',
        icon3: '#FFF1B8',
        product1: '#F6FFED',
        product2: '#FFFBE6',
      },
      fashion: {
        shell: '#FBF5FF',
        panel: '#FFFFFF',
        bannerA: '#9254DE',
        bannerB: '#C792EA',
        accent: '#722ED1',
        soft: '#F3E8FF',
        icon1: '#EFDBFF',
        icon2: '#FFD6E7',
        icon3: '#D6E4FF',
        product1: '#FFF0F6',
        product2: '#F9F0FF',
      },
      promo: {
        shell: '#F2F8FF',
        panel: '#FFFFFF',
        bannerA: '#1677FF',
        bannerB: '#69B1FF',
        accent: '#0958D9',
        soft: '#D6E4FF',
        icon1: '#BAE0FF',
        icon2: '#FFD591',
        icon3: '#FFE58F',
        product1: '#E6F4FF',
        product2: '#FFF7E6',
      },
    };

    let palette = paletteMap.promo;
    if ((template.tags || []).includes('美妆')) palette = paletteMap.beauty;
    if ((template.tags || []).includes('食品')) palette = paletteMap.food;
    if ((template.tags || []).includes('服饰')) palette = paletteMap.fashion;
    if ((template.tags || []).includes('618大促')) palette = paletteMap.promo;

    /**
     * 返回不同业务风格的小程序首页主体布局
     * @returns {string}
     */
    function getPreviewLayout() {
      if ((template.tags || []).includes('食品')) {
        return `
          <rect x="16" y="72" width="160" height="74" rx="16" fill="url(#bannerGradient)" />
          <circle cx="44" cy="108" r="16" fill="rgba(255,255,255,0.28)" />
          <rect x="66" y="94" width="72" height="10" rx="5" fill="#ffffff" opacity="0.92" />
          <rect x="66" y="112" width="56" height="8" rx="4" fill="#ffffff" opacity="0.66" />
          <rect x="16" y="154" width="160" height="68" rx="16" fill="${palette.panel}" />
          <rect x="24" y="164" width="44" height="48" rx="12" fill="${palette.icon1}" />
          <rect x="74" y="164" width="44" height="48" rx="12" fill="${palette.icon2}" />
          <rect x="124" y="164" width="44" height="48" rx="12" fill="${palette.icon3}" />
          <rect x="16" y="230" width="160" height="50" rx="16" fill="${palette.panel}" />
          <rect x="24" y="240" width="46" height="30" rx="10" fill="${palette.product1}" />
          <rect x="78" y="242" width="66" height="8" rx="4" fill="#D9E2F0" />
          <rect x="78" y="256" width="48" height="8" rx="4" fill="#E5EAF1" />
          <rect x="78" y="268" width="30" height="6" rx="3" fill="${palette.accent}" opacity="0.7" />
          <rect x="16" y="288" width="77" height="54" rx="14" fill="${palette.product1}" />
          <rect x="99" y="288" width="77" height="54" rx="14" fill="${palette.product2}" />
        `;
      }
      if ((template.tags || []).includes('服饰')) {
        return `
          <rect x="16" y="72" width="160" height="74" rx="16" fill="url(#bannerGradient)" />
          <rect x="26" y="84" width="78" height="12" rx="6" fill="#ffffff" opacity="0.94" />
          <rect x="26" y="104" width="52" height="8" rx="4" fill="#ffffff" opacity="0.66" />
          <rect x="16" y="154" width="160" height="84" rx="16" fill="${palette.panel}" />
          <circle cx="42" cy="182" r="15" fill="${palette.icon1}" />
          <circle cx="74" cy="182" r="15" fill="${palette.icon2}" />
          <circle cx="106" cy="182" r="15" fill="${palette.icon3}" />
          <circle cx="138" cy="182" r="15" fill="${palette.soft}" />
          <rect x="27" y="206" width="30" height="6" rx="3" fill="#D9E2F0" />
          <rect x="59" y="206" width="30" height="6" rx="3" fill="#D9E2F0" />
          <rect x="91" y="206" width="30" height="6" rx="3" fill="#D9E2F0" />
          <rect x="123" y="206" width="30" height="6" rx="3" fill="#D9E2F0" />
          <rect x="16" y="246" width="77" height="96" rx="14" fill="${palette.product1}" />
          <rect x="99" y="246" width="77" height="96" rx="14" fill="${palette.product2}" />
          <rect x="24" y="254" width="61" height="48" rx="10" fill="#ffffff" opacity="0.65" />
          <rect x="107" y="254" width="61" height="48" rx="10" fill="#ffffff" opacity="0.65" />
        `;
      }
      return `
        <rect x="16" y="72" width="160" height="82" rx="16" fill="url(#bannerGradient)" />
        <circle cx="44" cy="112" r="18" fill="rgba(255,255,255,0.24)" />
        <rect x="68" y="92" width="68" height="10" rx="5" fill="#ffffff" opacity="0.94" />
        <rect x="68" y="110" width="54" height="8" rx="4" fill="#ffffff" opacity="0.68" />
        <rect x="68" y="124" width="40" height="8" rx="4" fill="#ffffff" opacity="0.52" />
        <rect x="16" y="162" width="160" height="68" rx="16" fill="${palette.panel}" />
        <rect x="24" y="172" width="31" height="42" rx="10" fill="${palette.icon1}" />
        <rect x="63" y="172" width="31" height="42" rx="10" fill="${palette.icon2}" />
        <rect x="102" y="172" width="31" height="42" rx="10" fill="${palette.icon3}" />
        <rect x="141" y="172" width="27" height="42" rx="10" fill="${palette.soft}" />
        <rect x="16" y="238" width="160" height="42" rx="16" fill="${palette.panel}" />
        <rect x="24" y="248" width="52" height="22" rx="11" fill="${palette.soft}" />
        <rect x="82" y="248" width="52" height="22" rx="11" fill="${palette.product1}" />
        <rect x="140" y="248" width="28" height="22" rx="11" fill="${palette.product2}" />
        <rect x="16" y="288" width="77" height="54" rx="14" fill="${palette.product1}" />
        <rect x="99" y="288" width="77" height="54" rx="14" fill="${palette.product2}" />
      `;
    }

    const svg = `
      <svg xmlns="http://www.w3.org/2000/svg" width="192" height="360" viewBox="0 0 192 360">
        <defs>
          <linearGradient id="bannerGradient" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="${palette.bannerA}" />
            <stop offset="100%" stop-color="${palette.bannerB}" />
          </linearGradient>
        </defs>
        <rect width="192" height="360" rx="28" fill="#ffffff" />
        <rect x="10" y="10" width="172" height="340" rx="24" fill="${palette.shell}" />
        <rect x="58" y="21" width="76" height="10" rx="5" fill="#111827" opacity="0.10" />
        <circle cx="28" cy="45" r="5" fill="${palette.accent}" opacity="0.24" />
        <rect x="40" y="39" width="86" height="12" rx="6" fill="${palette.panel}" />
        <rect x="136" y="41" width="24" height="8" rx="4" fill="#D9E2F0" />
        <rect x="22" y="57" width="148" height="6" rx="3" fill="#D9E2F0" />
        <rect x="22" y="318" width="148" height="20" rx="10" fill="#ffffff" />
        <rect x="32" y="324" width="24" height="8" rx="4" fill="${palette.icon1}" />
        <rect x="84" y="324" width="24" height="8" rx="4" fill="${palette.icon2}" />
        <rect x="136" y="324" width="24" height="8" rx="4" fill="${palette.icon3}" />
        ${getPreviewLayout()}
      </svg>
    `;
    return 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg);
  }

  /**
   * 渲染模板列表卡片（接收当前页数据）
   * @param {Array} list - 当前页模板列表
   */
  function renderTemplateList(list) {
    const container = document.getElementById('template-tbody');
    if (!container) return;
    if (!list.length) {
      selectedTemplateIds = [];
      container.innerHTML = '<div class="template-empty">暂无符合条件的模板</div>';
      const checkAll = document.getElementById('check-all');
      if (checkAll) {
        checkAll.checked = false;
        checkAll.indeterminate = false;
      }
      updateTemplateSelectionSummary();
      return;
    }
    container.innerHTML = list.map((t) => {
      const displayStatus = getTemplateDisplayStatus(t.status);
      return `
      <article class="template-card" data-id="${t.id}">
        <div class="template-card-cover ${getTemplateCoverClass(t.status)}">
          <label class="template-card-check">
            <input type="checkbox" class="row-check" value="${t.id}" ${selectedTemplateIds.includes(t.id) ? 'checked' : ''} />
          </label>
          <span class="template-card-status status-tag status-${displayStatus}">${getStatusText(t.status)}</span>
          <div class="template-card-preview">
            <div class="template-card-preview-inner">
              <img class="template-card-preview-image" src="${getTemplatePreviewSrc(t)}" alt="${escapeHtml(t.name)} 预览图" />
            </div>
          </div>
        </div>
        <div class="template-card-body">
          <div class="template-card-header">
            <h3 class="template-card-title">${escapeHtml(t.name)}</h3>
            <span class="template-card-used">使用 ${t.useCount} 次</span>
          </div>
          <div class="tags template-card-tags">${(t.tags || []).map((tag) => `<span>${escapeHtml(tag)}</span>`).join('') || '<span>未设置标签</span>'}</div>
          <div class="template-card-meta">
            <span>最近修改：${escapeHtml(t.updatedAt)}</span>
          </div>
          <div class="template-card-actions">
            <button type="button" class="btn btn-sm btn-ghost btn-preview" data-id="${t.id}">预览</button>
            <button type="button" class="btn btn-sm btn-ghost btn-edit" data-id="${t.id}">编辑</button>
            ${t.status === 'draft' ? `<button type="button" class="btn btn-sm btn-ghost btn-publish" data-id="${t.id}">发布</button>` : ''}
            <button type="button" class="btn btn-sm btn-danger btn-delete" data-id="${t.id}">删除</button>
          </div>
        </div>
      </article>
    `;
    }).join('');

    // 行内操作绑定
    container.querySelectorAll('.row-check').forEach((el) => {
      el.addEventListener('change', onRowCheckChange);
    });
    container.querySelectorAll('.btn-preview').forEach((el) => {
      el.addEventListener('click', () => {
        const id = el.dataset.id;
        const tpl = MOCK_TEMPLATES.find((t) => t.id === id);
        alert('演示：预览模板「' + (tpl ? tpl.name : id) + '」，实际可在新窗口打开预览 URL。');
      });
    });
    container.querySelectorAll('.btn-edit').forEach((el) => {
      el.addEventListener('click', () => openEditor(el.dataset.id));
    });
    container.querySelectorAll('.btn-publish').forEach((el) => {
      el.addEventListener('click', () => openPublishPreview(el.dataset.id));
    });
    container.querySelectorAll('.btn-delete').forEach((el) => {
      el.addEventListener('click', () => onDeleteTemplate(el.dataset.id));
    });
    updateTemplateSelectionSummary();
    onRowCheckChange();
  }

  /**
   * 渲染模板列表分页区域
   * @param {number} total - 当前筛选条件下的模板总数
   */
  function renderTemplatePagination(total) {
    const container = document.getElementById('template-pagination');
    if (!container) return;

    if (total === 0) {
      container.innerHTML = '';
      return;
    }

    const totalPages = Math.ceil(total / TEMPLATE_PAGE_SIZE);
    if (currentTemplatePage > totalPages) {
      currentTemplatePage = totalPages;
    }

    let html = '';
    html += `<span class="pagination-total">共 ${total} 条</span>`;
    html += `<button type="button" class="btn btn-sm btn-ghost" data-page="${currentTemplatePage - 1}" ${currentTemplatePage === 1 ? 'disabled' : ''}>上一页</button>`;

    for (let i = 1; i <= totalPages; i++) {
      html += `<button type="button" class="btn btn-sm ${i === currentTemplatePage ? 'btn-primary' : 'btn-ghost'}" data-page="${i}">${i}</button>`;
    }

    html += `<button type="button" class="btn btn-sm btn-ghost" data-page="${currentTemplatePage + 1}" ${currentTemplatePage === totalPages ? 'disabled' : ''}>下一页</button>`;

    container.innerHTML = html;

    container.querySelectorAll('button[data-page]').forEach((btn) => {
      btn.addEventListener('click', function () {
        const target = Number(this.getAttribute('data-page'));
        if (!Number.isFinite(target)) return;
        if (target < 1 || target > totalPages || target === currentTemplatePage) return;
        currentTemplatePage = target;
        renderTemplatePage();
      });
    });
  }

  /**
   * 根据当前页码渲染模板列表与分页
   */
  function renderTemplatePage() {
    const total = filteredTemplates.length;
    const start = (currentTemplatePage - 1) * TEMPLATE_PAGE_SIZE;
    const pageList = filteredTemplates.slice(start, start + TEMPLATE_PAGE_SIZE);
    renderTemplateList(pageList);
    renderTemplatePagination(total);
  }

  /**
   * 应用状态与标签筛选并重绘列表（重置页码）
   */
  function applyFiltersAndRender() {
    const status = document.getElementById('filter-status').value;
    const tag = document.getElementById('filter-tag').value;
    let list = [...MOCK_TEMPLATES];
    if (status) {
      list = list.filter((t) => {
        if (status === 'published') return t.status === 'published' || t.status === 'pushed';
        return t.status === status;
      });
    }
    if (tag) list = list.filter((t) => (t.tags || []).includes(tag));
    filteredTemplates = list;
    currentTemplatePage = 1;
    renderTemplatePage();
  }

  /**
   * 全选/取消全选
   */
  function onRowCheckChange() {
    const checkAll = document.getElementById('check-all');
    const rowChecks = document.querySelectorAll('#template-tbody .row-check');
    selectedTemplateIds = Array.from(rowChecks).filter((c) => c.checked).map((c) => c.value);
    if (checkAll) {
      checkAll.checked = rowChecks.length > 0 && selectedTemplateIds.length === rowChecks.length;
      checkAll.indeterminate = selectedTemplateIds.length > 0 && selectedTemplateIds.length < rowChecks.length;
    }
    updateTemplateSelectionSummary();
  }

  /**
   * 打开新建模板弹窗
   */
  function openNewTemplateModal() {
    const modal = document.getElementById('modal-new-template');
    const copyWrap = document.getElementById('copy-source-wrap');
    const copySelect = document.getElementById('copy-template-select');
    const nameInput = document.getElementById('template-name');
    if (!modal || !copyWrap || !copySelect || !nameInput) return;

    nameInput.value = '';
    copyWrap.classList.add('hidden');
    copySelect.innerHTML = MOCK_TEMPLATES.map((t) => `<option value="${t.id}">${escapeHtml(t.name)}</option>`).join('');

    document.querySelectorAll('input[name="create-type"]').forEach((radio) => {
      radio.addEventListener('change', function () {
        copyWrap.classList.toggle('hidden', this.value !== 'copy');
      });
    });

    modal.classList.add('show');
  }

  /**
   * 确认新建模板（演示：跳转到编辑器或仅提示）
   */
  function confirmNewTemplate() {
    const type = document.querySelector('input[name="create-type"]:checked').value;
    const nameInput = document.getElementById('template-name');
    const name = (nameInput && nameInput.value.trim()) || '未命名模板';
    closeModal('modal-new-template');
    if (type === 'copy') {
      const copySelect = document.getElementById('copy-template-select');
      const srcId = copySelect && copySelect.value;
      alert('演示：将复制模板 ' + (srcId || '') + ' 并进入编辑。\n新建模板名称：' + name);
    } else {
      alert('演示：从空白创建模板「' + name + '」并进入编辑器。');
    }
    openEditor('new');
  }

  /**
   * 打开发布前预览弹窗
   * @param {string} id - 模板 ID
   */
  function openPublishPreview(id) {
    currentFlowTemplateId = id;
    const modal = document.getElementById('modal-publish-preview');
    const tabs = modal.querySelectorAll('.preview-tab');
    const frame = document.getElementById('preview-frame');
    if (!modal || !frame) return;

    tabs.forEach((tab) => {
      tab.addEventListener('click', function () {
        tabs.forEach((t) => t.classList.remove('active'));
        this.classList.add('active');
        frame.classList.remove('pc', 'mobile');
        frame.classList.add(this.dataset.device);
      });
    });

    modal.classList.add('show');
  }

  /**
   * 确认发布（模拟）
   */
  function confirmPublish() {
    if (!currentFlowTemplateId) return;
    alert('演示：模板已发布。实际会更新状态为「已发布」并记录审计日志。');
    closeModal('modal-publish-preview');
    currentFlowTemplateId = null;
    applyFiltersAndRender();
  }

  /**
   * 打开推送弹窗（可预填模板）
   * @param {string} [templateId] - 可选，预选模板 ID
   */
  function openPushModal(templateId) {
    const modal = document.getElementById('modal-push');
    const templateSelect = document.getElementById('push-template-select');
    const brandList = document.getElementById('push-brand-list');
    if (!modal || !templateSelect || !brandList) return;

    templateSelect.innerHTML = MOCK_TEMPLATES
      .filter((t) => t.status === 'published' || t.status === 'pushed')
      .map((t) => `<option value="${t.id}">${escapeHtml(t.name)}</option>`)
      .join('');
    if (templateId) templateSelect.value = templateId;

    brandList.innerHTML = MOCK_BRANDS.map(
      (b) => `<label><input type="checkbox" value="${b.id}" /> ${escapeHtml(b.name)}</label>`
    ).join('');

    modal.classList.add('show');
  }

  /**
   * 确认推送（模拟）
   */
  function confirmPush() {
    const templateSelect = document.getElementById('push-template-select');
    const pushType = document.querySelector('input[name="push-type"]:checked').value;
    const checked = document.querySelectorAll('#push-brand-list input:checked');
    const names = Array.from(checked).map((c) => c.value);
    if (names.length === 0) {
      alert('请至少选择一个品牌方。');
      return;
    }
    const templateName = templateSelect.options[templateSelect.selectedIndex].text;
    alert('演示：已将「' + templateName + '」以「' + (pushType === 'template-data' ? '模板+数据' : '仅模板') + '」方式推送给 ' + names.length + ' 个品牌。');
    closeModal('modal-push');
    renderPushRecord();
  }

  /**
   * 打开批量设置标签弹窗
   */
  function openBatchTagModal() {
    const modal = document.getElementById('modal-batch-tag');
    const countEl = document.getElementById('batch-count');
    if (!modal || !countEl) return;
    countEl.textContent = selectedTemplateIds.length;
    if (selectedTemplateIds.length === 0) {
      alert('请先勾选要操作的模板。');
      return;
    }
    document.getElementById('batch-system-tag').value = '';
    document.getElementById('batch-custom-tag').value = '';
    modal.classList.add('show');
  }

  /**
   * 确认批量设置标签（模拟）
   */
  function confirmBatchTag() {
    const sysTag = document.getElementById('batch-system-tag').value;
    const customTag = document.getElementById('batch-custom-tag').value.trim();
    alert('演示：已为选中的 ' + selectedTemplateIds.length + ' 个模板设置标签。' + (sysTag ? ' 系统标签：' + sysTag : '') + (customTag ? ' 自定义：' + customTag : ''));
    closeModal('modal-batch-tag');
    applyFiltersAndRender();
  }

  /**
   * 删除模板（模拟：仅提示）
   * @param {string} id - 模板 ID
   */
  function onDeleteTemplate(id) {
    const t = MOCK_TEMPLATES.find((x) => x.id === id);
    if (!t) return;
    if (t.status === 'pushed' && t.useCount > 0) {
      if (!confirm('该模板已推送给 ' + t.useCount + ' 个品牌，删除后品牌方将无法使用。是否确认删除？（演示中不会真正删除）')) return;
    }
    alert('演示：已删除模板「' + t.name + '」。（实际可为软删并通知下游）');
    applyFiltersAndRender();
  }

  /** 分类页模板 value -> 显示名称（用于编辑器标题） */
  const CATEGORY_TEMPLATE_NAMES = {
    level3: '三级分类页',
    level2: '二级分类页',
    'level2-list': '二级分类+商品列表页',
    'level1-tab': '一级分类+商品分类页（横向 Tab）',
    'level1-list': '一级分类+商品分类页（直接列表）',
    'level1-list-b': '一级分类+商品分类页（直接列表样式二）',
  };

  /**
   * 打开编辑器（演示：新开页或内嵌占位）
   * @param {string} id - 模板 ID 或 'new'
   * @param {Object} [options] - 可选，{ pageType, categoryTemplate, pageName }
   */
  function openEditor(id, options) {
    let name;
    if (id === 'new' && options && options.pageType === 'category' && options.categoryTemplate) {
      name = options.pageName || ('新建分类页 - ' + (CATEGORY_TEMPLATE_NAMES[options.categoryTemplate] || options.categoryTemplate));
    } else {
      name = id === 'new' ? '新建模板' : (MOCK_TEMPLATES.find((t) => t.id === id) || {}).name || id;
    }
    const url = new URL('editor.html', window.location.href);
    url.searchParams.set('id', id);
    url.searchParams.set('name', name);
    if (options && options.categoryTemplate) {
      url.searchParams.set('categoryTemplate', options.categoryTemplate);
    }
    window.open(url.toString(), 'editor', 'width=1200,height=800,scrollbars=yes');
  }

  /**
   * 打开「分类页选择模板」弹窗
   */
  function openCategoryTemplateModal() {
    const modal = document.getElementById('modal-category-template');
    if (!modal) return;
    const first = document.querySelector('#category-template-list input[name="category-template"]');
    if (first) first.checked = true;
    modal.classList.add('show');
  }

  /**
   * 确认所选分类页模板并进入编辑器
   */
  function confirmCategoryTemplate() {
    const radio = document.querySelector('#modal-category-template input[name="category-template"]:checked');
    if (!radio) {
      alert('请先选择一种分类页模板。');
      return;
    }
    const modal = document.getElementById('modal-category-template');
    if (modal) modal.classList.remove('show');
    const value = radio.value;
    const pageName = '新建分类页 - ' + (CATEGORY_TEMPLATE_NAMES[value] || value);
    openEditor('new', { pageType: 'category', categoryTemplate: value, pageName });
  }

  /**
   * 渲染某个模板下的页面列表，按当前选中的页面类型过滤
   * @param {string} templateId - 模板 ID
   */
  function renderTemplatePages(templateId) {
    const tbody = document.getElementById('template-pages-tbody');
    if (!tbody) return;
    const allPages = (MOCK_TEMPLATE_PAGES && MOCK_TEMPLATE_PAGES[templateId]) || [];
    const pages =
      currentTemplatePageType &&
      ['home', 'category', 'activity', 'mine', 'product-detail'].includes(currentTemplatePageType)
        ? allPages.filter((p) => p.type === currentTemplatePageType)
        : allPages;
    tbody.innerHTML = pages
      .map(
        (p, index) => `
        <tr data-id="${p.id}">
          <td>
            ${p.status === 'published' && index === 0 ? '<span class="page-ribbon">使用中</span>' : ''}
            ${escapeHtml(p.title)}
          </td>
          <td>${
            p.status === 'published'
              ? '<span class="page-status page-status-active">使用中</span>'
              : '<span class="page-status page-status-draft">草稿</span>'
          }</td>
          <td>${escapeHtml(p.updatedAt)}</td>
          <td>
            <button type="button" class="btn btn-sm btn-ghost btn-page-publish" data-id="${p.id}">投放</button>
            <button type="button" class="btn btn-sm btn-ghost btn-page-edit" data-id="${p.id}">编辑</button>
            <button type="button" class="btn btn-sm btn-ghost btn-page-copy" data-id="${p.id}">复制</button>
            <button type="button" class="btn btn-sm btn-danger btn-page-delete" data-id="${p.id}">删除</button>
          </td>
        </tr>
      `
      )
      .join('');

    tbody.querySelectorAll('.btn-page-edit').forEach((btn) => {
      btn.addEventListener('click', () => {
        const pageId = btn.dataset.id;
        openEditor(pageId || 'new');
      });
    });

    tbody.querySelectorAll('.btn-page-publish').forEach((btn) => {
      btn.addEventListener('click', () => {
        alert('演示：页面投放上线。');
      });
    });
    tbody.querySelectorAll('.btn-page-copy').forEach((btn) => {
      btn.addEventListener('click', () => {
        alert('演示：复制当前页面，生成一个新的草稿页面。');
      });
    });
    tbody.querySelectorAll('.btn-page-delete').forEach((btn) => {
      btn.addEventListener('click', () => {
        alert('演示：删除页面（实际项目中可做软删并校验依赖）。');
      });
    });

    const pagination = document.getElementById('template-pages-pagination');
    if (pagination) {
      if (!pages.length) {
        pagination.innerHTML = '<span class="pagination-total">暂无页面</span>';
      } else {
        pagination.innerHTML = `
          <span class="pagination-total">共 ${pages.length} 条</span>
          <div class="pagination-pages">
            <button type="button" class="pagination-page-btn active">1</button>
          </div>
          <div class="pagination-size">
            <select>
              <option>10 条/页</option>
            </select>
          </div>
        `;
      }
    }
  }

  /**
   * 进入某个模板的页面管理中间页
   * @param {string} templateId - 模板 ID
   */
  function openTemplatePages(templateId) {
    const tpl = MOCK_TEMPLATES.find((t) => t.id === templateId);
    currentTemplateForPages = tpl || null;
    currentTemplatePageType = 'home';
    const titleEl = document.getElementById('template-pages-title');
    if (titleEl) {
      titleEl.textContent = tpl ? `页面管理 - ${tpl.name}` : '页面管理';
    }
    const currentLabel = document.getElementById('template-pages-current-label');
    if (currentLabel) currentLabel.textContent = '当前：首页';
    // 重置左侧菜单选中状态
    document
      .querySelectorAll('#template-pages-menu .template-pages-menu-item')
      .forEach((item) => item.classList.toggle('active', item.dataset.type === 'home'));

    // 切换可见页面：隐藏所有 .page，仅展示 page-template-pages
    document.querySelectorAll('.page').forEach((p) => p.classList.remove('active'));
    const section = document.getElementById('page-template-pages');
    if (section) section.classList.add('active');
    renderTemplatePages(templateId);
  }

  /**
   * 关闭指定弹窗
   * @param {string} modalId - 弹窗元素 id
   */
  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('show');
  }

  /**
   * 渲染推送记录表
   */
  function renderPushRecord() {
    const tbody = document.getElementById('push-record-tbody');
    if (!tbody) return;
    tbody.innerHTML = MOCK_PUSH_RECORDS.map(
      (r) =>
        `<tr>
          <td>${escapeHtml(r.time)}</td>
          <td>${escapeHtml(r.templateName)}</td>
          <td>${escapeHtml(r.brands)}</td>
          <td>${escapeHtml(r.pushType)}</td>
          <td>${escapeHtml(r.operator)}</td>
          <td>${escapeHtml(r.brandStatus)}</td>
        </tr>`
    ).join('');
  }

  /** 商城列表搜索关键词（用于前端过滤） */
  let mallListSearchKeyword = '';

  /**
   * 获取当前展示的商城列表（按关键词过滤）
   * @returns {Array}
   */
  function getFilteredMalls() {
    const list = (typeof MOCK_MALLS !== 'undefined' && MOCK_MALLS) || [];
    if (!mallListSearchKeyword.trim()) return list;
    const kw = mallListSearchKeyword.trim().toLowerCase();
    return list.filter(
      (m) =>
        (m.name && m.name.toLowerCase().includes(kw)) ||
        (m.brandName && m.brandName.toLowerCase().includes(kw))
    );
  }

  /**
   * 渲染商城列表（支持搜索过滤）
   */
  function renderMallList() {
    const tbody = document.getElementById('mall-list-tbody');
    const paginationEl = document.getElementById('mall-list-pagination');
    if (!tbody) return;
    const list = getFilteredMalls();
    tbody.innerHTML = list
      .map(
        (m) => `
        <tr data-id="${m.id}">
          <td>${escapeHtml(m.name)}</td>
          <td>${escapeHtml(m.brandName)}</td>
          <td><span class="status-tag status-mall-${m.status}">${m.status === 'running' ? '运营中' : '已关闭'}</span></td>
          <td>${escapeHtml(m.createdAt)}</td>
          <td>
            <button type="button" class="btn btn-sm btn-ghost btn-mall-copy" data-id="${m.id}">一键复制</button>
          </td>
        </tr>
      `
      )
      .join('');

    tbody.querySelectorAll('.btn-mall-copy').forEach((btn) => {
      btn.addEventListener('click', () => onCopyMall(btn.dataset.id));
    });

    if (paginationEl) {
      paginationEl.innerHTML =
        list.length > 0
          ? `<span class="pagination-total">共 ${list.length} 条</span>`
          : '<span class="pagination-total">暂无数据</span>';
    }
  }

  /**
   * 一键复制商城（演示：复制配置生成新商城）
   * @param {string} mallId - 商城 ID
   */
  function onCopyMall(mallId) {
    const mall = (MOCK_MALLS || []).find((m) => m.id === mallId);
    if (!mall) return;
    alert('演示：一键复制商城「' + (mall.name || mallId) + '」，将复制其配置并生成新商城（实际会请求后端并刷新列表）。');
  }

  /**
   * 新建商城（演示）
   */
  function onNewMall() {
    alert('演示：新建商城。实际可跳转至商城创建向导或弹窗填写名称、关联品牌等。');
  }

  /**
   * 应用商城搜索并重新渲染
   */
  function applyMallSearch() {
    const input = document.getElementById('mall-search-input');
    if (input) mallListSearchKeyword = input.value || '';
    renderMallList();
  }

  function escapeHtml(str) {
    if (str == null) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // 页面切换
  document.querySelectorAll('.nav-item[data-page]').forEach((el) => {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      const page = this.dataset.page;
      document.querySelectorAll('.nav-item').forEach((n) => n.classList.remove('active'));
      this.classList.add('active');
      document.querySelectorAll('.page').forEach((p) => p.classList.remove('active'));
      const target = document.getElementById('page-' + page);
      if (target) target.classList.add('active');
    });
  });

  // 页面管理返回按钮
  document.getElementById('btn-back-to-templates')?.addEventListener('click', () => {
    document.querySelectorAll('.page').forEach((p) => p.classList.remove('active'));
    const templatesSection = document.getElementById('page-templates');
    if (templatesSection) templatesSection.classList.add('active');
  });

  // 页面管理左侧类型切换
  document.querySelectorAll('#template-pages-menu .template-pages-menu-item').forEach((btn) => {
    btn.addEventListener('click', function () {
      const type = this.dataset.type;
      if (!type || type === currentTemplatePageType) return;
      currentTemplatePageType = type;
      // 更新菜单选中样式
      document
        .querySelectorAll('#template-pages-menu .template-pages-menu-item')
        .forEach((item) => item.classList.toggle('active', item === this));
      const label = document.getElementById('template-pages-current-label');
      if (label) {
        const map = {
          home: '首页',
          category: '分类页',
          activity: '活动页',
          mine: '我的页面',
          'product-detail': '商品详情页',
        };
        label.textContent = '当前：' + (map[type] || '');
      }
      if (currentTemplateForPages) {
        renderTemplatePages(currentTemplateForPages.id);
      }
    });
  });

  // 全选
  const checkAll = document.getElementById('check-all');
  if (checkAll) {
    checkAll.addEventListener('change', function () {
      document.querySelectorAll('#template-tbody .row-check').forEach((c) => {
        c.checked = this.checked;
      });
      onRowCheckChange();
    });
  }

  // 筛选
  document.getElementById('filter-status')?.addEventListener('change', applyFiltersAndRender);
  document.getElementById('filter-tag')?.addEventListener('change', applyFiltersAndRender);

  // 按钮
  document.getElementById('btn-new-template')?.addEventListener('click', openNewTemplateModal);
  document.getElementById('btn-batch-tag')?.addEventListener('click', openBatchTagModal);
  document.getElementById('btn-confirm-new')?.addEventListener('click', confirmNewTemplate);
  document.getElementById('btn-confirm-publish')?.addEventListener('click', confirmPublish);
  document.getElementById('btn-confirm-push')?.addEventListener('click', confirmPush);
  document.getElementById('btn-confirm-batch-tag')?.addEventListener('click', confirmBatchTag);
  document.getElementById('btn-confirm-category-template')?.addEventListener('click', confirmCategoryTemplate);

  // 页面管理 - 新建页面（首页/海报/文章直接进编辑器，分类页先选模板）
  document.getElementById('btn-new-page')?.addEventListener('click', function () {
    if (currentTemplatePageType === 'category') {
      openCategoryTemplateModal();
    } else {
      openEditor('new');
    }
  });

  // 弹窗关闭
  document.querySelectorAll('.modal-close, .modal-cancel').forEach((btn) => {
    btn.addEventListener('click', function () {
      const modal = this.closest('.modal');
      if (modal) modal.classList.remove('show');
    });
  });

  document.querySelectorAll('.modal').forEach((modal) => {
    modal.addEventListener('click', function (e) {
      if (e.target === this) closeModal(this.id);
    });
  });

  // 商城列表：搜索、新建
  document.getElementById('btn-mall-search')?.addEventListener('click', applyMallSearch);
  document.getElementById('mall-search-input')?.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') applyMallSearch();
  });
  document.getElementById('btn-new-mall')?.addEventListener('click', onNewMall);

  // 初始化
  applyFiltersAndRender();
  renderPushRecord();
  renderMallList();
})();
