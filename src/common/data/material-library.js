/* material-library.js — 素材库图片分类/图片数据/选择器状态。
 * 从 src/editor.html IIFE 内 IMAGE_CATEGORIES / MATERIAL_LIBRARY / imagePickerState
 * 外置(Phase 2), 挂到 MallBuilder.data.*。MATERIAL_LIBRARY/imagePickerState 为 let,
 * editor.html 用 let 别名引用同一对象, 变更互通。 */
MallBuilder.data.IMAGE_CATEGORIES = [
  { id: 'default', name: '默认分类', icon: '📁' },
  { id: 'banner', name: 'Banner图', icon: '🖼️' },
  { id: 'product', name: '商品图', icon: '🛒' },
  { id: 'icon', name: '图标', icon: '⭐' },
  { id: 'background', name: '背景图', icon: '🎨' },
];

// 素材库图片数据（模拟）
MallBuilder.data.MATERIAL_LIBRARY = {
  images: [
    { id: 'img-1', name: 'Banner素材1', url: '../../assets/banner素材.jpg', categoryId: 'default', createTime: Date.now() - 86400000 },
    { id: 'img-2', name: 'Banner素材2', url: '../../assets/banner素材2.jpg', categoryId: 'default', createTime: Date.now() - 86400000 },
    { id: 'img-3', name: '促销活动图', url: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2ZmNzhjZSIvPjx0ZXh0IHg9IjEwMCIgeT0iMTAwIiBmb250LXNpemU9IjE0IiBmaWxsPSIjZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+5oql5ZGKPC90ZXh0Pjwvc3ZnPg==', categoryId: 'default', createTime: Date.now() - 72000000 },
    { id: 'img-4', name: '新品推荐', url: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzY3YjdmZiIvPjx0ZXh0IHg9IjEwMCIgeT0iMTAwIiBmb250LXNpemU9IjE0IiBmaWxsPSIjZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+5paw5Lqa5oql5ZGKPC90ZXh0Pjwvc3ZnPg==', categoryId: 'default', createTime: Date.now() - 36000000 },
    { id: 'img-5', name: '热销商品', url: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2ZmNGQ0ZiIvPjx0ZXh0IHg9IjEwMCIgeT0iMTAwIiBmb250LXNpemU9IjE0IiBmaWxsPSIjZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+54Ku5L2T5bel5Y2NPC90ZXh0Pjwvc3ZnPg==', categoryId: 'default', createTime: Date.now() - 18000000 },
  ],
  nextId: 6
};

// 图片选择器弹窗状态
MallBuilder.data.imagePickerState = {
  isOpen: false,
  selectedImages: [], // 多选模式时使用数组
  currentCategory: 'default',
  searchKeyword: '',
  currentPage: 1,
  pageSize: 15,
  onSelectCallback: null, // 选择回调
  multiSelect: false // 是否多选模式
};
