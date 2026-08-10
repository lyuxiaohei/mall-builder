/* mock-taxonomy.js — 品牌/标签/分类 Mock 数据。
 * 从 src/editor.html IIFE 内 const MOCK_BRANDS / MOCK_TAGS / MOCK_CATEGORIES
 * 外置(Phase 2), 挂到 MallBuilder.data.* (namespace.js 提供命名空间)。
 * editor.html 用 const 别名引用, 所有调用点保持不变。 */
MallBuilder.data.MOCK_BRANDS = [
  { id: 'brand-1', name: 'Apple', goodsCount: 156 },
  { id: 'brand-2', name: '华为', goodsCount: 234 },
  { id: 'brand-3', name: '小米', goodsCount: 189 },
  { id: 'brand-4', name: 'OPPO', goodsCount: 145 },
  { id: 'brand-5', name: 'vivo', goodsCount: 167 },
  { id: 'brand-6', name: '三星', goodsCount: 123 },
  { id: 'brand-7', name: '索尼', goodsCount: 89 },
  { id: 'brand-8', name: '联想', goodsCount: 112 },
  { id: 'brand-9', name: '戴尔', goodsCount: 78 },
  { id: 'brand-10', name: '惠普', goodsCount: 95 },
];

MallBuilder.data.MOCK_TAGS = [
  {
    id: 'tag-name-1', name: '性别', isGroup: true, children: [
      { id: 'tag-1-1', name: '男', goodsCount: 234 },
      { id: 'tag-1-2', name: '女', goodsCount: 567 },
      { id: 'tag-1-3', name: '中性', goodsCount: 89 },
    ]
  },
  {
    id: 'tag-name-2', name: '年龄段', isGroup: true, children: [
      { id: 'tag-2-1', name: '儿童', goodsCount: 145 },
      { id: 'tag-2-2', name: '青年', goodsCount: 345 },
      { id: 'tag-2-3', name: '中年', goodsCount: 278 },
      { id: 'tag-2-4', name: '老年', goodsCount: 123 },
    ]
  },
  {
    id: 'tag-name-3', name: '适用场景', isGroup: true, children: [
      { id: 'tag-3-1', name: '日常休闲', goodsCount: 456 },
      { id: 'tag-3-2', name: '商务办公', goodsCount: 234 },
      { id: 'tag-3-3', name: '运动健身', goodsCount: 189 },
      { id: 'tag-3-4', name: '户外旅行', goodsCount: 167 },
      { id: 'tag-3-5', name: '居家生活', goodsCount: 312 },
    ]
  },
  {
    id: 'tag-name-4', name: '风格', isGroup: true, children: [
      { id: 'tag-4-1', name: '简约', goodsCount: 234 },
      { id: 'tag-4-2', name: '时尚', goodsCount: 178 },
      { id: 'tag-4-3', name: '复古', goodsCount: 123 },
      { id: 'tag-4-4', name: '潮流', goodsCount: 89 },
    ]
  },
  {
    id: 'tag-name-5', name: '季节', isGroup: true, children: [
      { id: 'tag-5-1', name: '春季', goodsCount: 234 },
      { id: 'tag-5-2', name: '夏季', goodsCount: 189 },
      { id: 'tag-5-3', name: '秋季', goodsCount: 167 },
      { id: 'tag-5-4', name: '冬季', goodsCount: 145 },
    ]
  },
];

// 分类 Mock 数据（三级分类）
MallBuilder.data.MOCK_CATEGORIES = [
  {
    id: 'cat-1', name: '手机数码', isGroup: true, children: [
      {
        id: 'cat-1-1', name: '手机通讯', isGroup: true, children: [
          { id: 'cat-1-1-1', name: '智能手机', goodsCount: 456 },
          { id: 'cat-1-1-2', name: '老人机', goodsCount: 89 },
          { id: 'cat-1-1-3', name: '对讲机', goodsCount: 34 },
        ]
      },
      {
        id: 'cat-1-2', name: '手机配件', isGroup: true, children: [
          { id: 'cat-1-2-1', name: '手机壳', goodsCount: 234 },
          { id: 'cat-1-2-2', name: '充电器', goodsCount: 178 },
          { id: 'cat-1-2-3', name: '耳机', goodsCount: 145 },
        ]
      },
      {
        id: 'cat-1-3', name: '数码配件', isGroup: true, children: [
          { id: 'cat-1-3-1', name: '存储卡', goodsCount: 56 },
          { id: 'cat-1-3-2', name: '数据线', goodsCount: 89 },
        ]
      },
    ]
  },
  {
    id: 'cat-2', name: '电脑办公', isGroup: true, children: [
      {
        id: 'cat-2-1', name: '电脑整机', isGroup: true, children: [
          { id: 'cat-2-1-1', name: '笔记本', goodsCount: 234 },
          { id: 'cat-2-1-2', name: '台式机', goodsCount: 123 },
          { id: 'cat-2-1-3', name: '一体机', goodsCount: 45 },
        ]
      },
      {
        id: 'cat-2-2', name: '电脑配件', isGroup: true, children: [
          { id: 'cat-2-2-1', name: '显示器', goodsCount: 178 },
          { id: 'cat-2-2-2', name: '键盘鼠标', goodsCount: 156 },
          { id: 'cat-2-2-3', name: '硬盘', goodsCount: 89 },
        ]
      },
      {
        id: 'cat-2-3', name: '办公设备', isGroup: true, children: [
          { id: 'cat-2-3-1', name: '打印机', goodsCount: 67 },
          { id: 'cat-2-3-2', name: '投影仪', goodsCount: 34 },
        ]
      },
    ]
  },
  {
    id: 'cat-3', name: '家用电器', isGroup: true, children: [
      {
        id: 'cat-3-1', name: '大家电', isGroup: true, children: [
          { id: 'cat-3-1-1', name: '电视', goodsCount: 345 },
          { id: 'cat-3-1-2', name: '冰箱', goodsCount: 267 },
          { id: 'cat-3-1-3', name: '洗衣机', goodsCount: 234 },
        ]
      },
      {
        id: 'cat-3-2', name: '厨房电器', isGroup: true, children: [
          { id: 'cat-3-2-1', name: '电饭煲', goodsCount: 189 },
          { id: 'cat-3-2-2', name: '微波炉', goodsCount: 123 },
          { id: 'cat-3-2-3', name: '榨汁机', goodsCount: 98 },
        ]
      },
      {
        id: 'cat-3-3', name: '生活电器', isGroup: true, children: [
          { id: 'cat-3-3-1', name: '空调', goodsCount: 178 },
          { id: 'cat-3-3-2', name: '加湿器', goodsCount: 67 },
          { id: 'cat-3-3-3', name: '吸尘器', goodsCount: 89 },
        ]
      },
    ]
  },
  {
    id: 'cat-4', name: '服饰鞋包', isGroup: true, children: [
      {
        id: 'cat-4-1', name: '男装', isGroup: true, children: [
          { id: 'cat-4-1-1', name: 'T恤', goodsCount: 456 },
          { id: 'cat-4-1-2', name: '衬衫', goodsCount: 345 },
          { id: 'cat-4-1-3', name: '外套', goodsCount: 234 },
        ]
      },
      {
        id: 'cat-4-2', name: '女装', isGroup: true, children: [
          { id: 'cat-4-2-1', name: '连衣裙', goodsCount: 567 },
          { id: 'cat-4-2-2', name: '半身裙', goodsCount: 345 },
          { id: 'cat-4-2-3', name: '卫衣', goodsCount: 278 },
        ]
      },
      {
        id: 'cat-4-3', name: '鞋靴', isGroup: true, children: [
          { id: 'cat-4-3-1', name: '运动鞋', goodsCount: 389 },
          { id: 'cat-4-3-2', name: '皮鞋', goodsCount: 167 },
          { id: 'cat-4-3-3', name: '凉鞋', goodsCount: 123 },
        ]
      },
    ]
  },
  {
    id: 'cat-5', name: '美妆护肤', isGroup: true, children: [
      {
        id: 'cat-5-1', name: '面部护肤', isGroup: true, children: [
          { id: 'cat-5-1-1', name: '面膜', goodsCount: 234 },
          { id: 'cat-5-1-2', name: '乳液面霜', goodsCount: 178 },
          { id: 'cat-5-1-3', name: '精华', goodsCount: 145 },
        ]
      },
      {
        id: 'cat-5-2', name: '彩妆', isGroup: true, children: [
          { id: 'cat-5-2-1', name: '口红', goodsCount: 312 },
          { id: 'cat-5-2-2', name: '粉底', goodsCount: 189 },
          { id: 'cat-5-2-3', name: '眼影', goodsCount: 134 },
        ]
      },
    ]
  },
  {
    id: 'cat-6', name: '食品生鲜', isGroup: true, children: [
      {
        id: 'cat-6-1', name: '新鲜水果', isGroup: true, children: [
          { id: 'cat-6-1-1', name: '苹果', goodsCount: 234 },
          { id: 'cat-6-1-2', name: '橙子', goodsCount: 189 },
          { id: 'cat-6-1-3', name: '葡萄', goodsCount: 145 },
        ]
      },
      {
        id: 'cat-6-2', name: '休闲零食', isGroup: true, children: [
          { id: 'cat-6-2-1', name: '坚果', goodsCount: 267 },
          { id: 'cat-6-2-2', name: '饼干', goodsCount: 178 },
          { id: 'cat-6-2-3', name: '糖果', goodsCount: 123 },
        ]
      },
    ]
  },
  {
    id: 'cat-7', name: '母婴用品', isGroup: true, children: [
      {
        id: 'cat-7-1', name: '奶粉辅食', isGroup: true, children: [
          { id: 'cat-7-1-1', name: '婴儿奶粉', goodsCount: 189 },
          { id: 'cat-7-1-2', name: '宝宝零食', goodsCount: 123 },
          { id: 'cat-7-1-3', name: '营养辅食', goodsCount: 98 },
        ]
      },
      {
        id: 'cat-7-2', name: '婴童服饰', isGroup: true, children: [
          { id: 'cat-7-2-1', name: '连体衣', goodsCount: 156 },
          { id: 'cat-7-2-2', name: '婴童鞋', goodsCount: 89 },
        ]
      },
    ]
  },
  {
    id: 'cat-8', name: '家居家装', isGroup: true, children: [
      {
        id: 'cat-8-1', name: '家具', isGroup: true, children: [
          { id: 'cat-8-1-1', name: '沙发', goodsCount: 234 },
          { id: 'cat-8-1-2', name: '床', goodsCount: 178 },
          { id: 'cat-8-1-3', name: '衣柜', goodsCount: 145 },
        ]
      },
      {
        id: 'cat-8-2', name: '家纺', isGroup: true, children: [
          { id: 'cat-8-2-1', name: '四件套', goodsCount: 189 },
          { id: 'cat-8-2-2', name: '被子', goodsCount: 134 },
        ]
      },
    ]
  },
  {
    id: 'cat-9', name: '运动户外', isGroup: true, children: [
      {
        id: 'cat-9-1', name: '运动服饰', isGroup: true, children: [
          { id: 'cat-9-1-1', name: '运动T恤', goodsCount: 178 },
          { id: 'cat-9-1-2', name: '运动裤', goodsCount: 134 },
          { id: 'cat-9-1-3', name: '运动套装', goodsCount: 89 },
        ]
      },
      {
        id: 'cat-9-2', name: '户外装备', isGroup: true, children: [
          { id: 'cat-9-2-1', name: '帐篷', goodsCount: 67 },
          { id: 'cat-9-2-2', name: '登山杖', goodsCount: 45 },
        ]
      },
    ]
  },
  {
    id: 'cat-10', name: '图书文具', isGroup: true, children: [
      {
        id: 'cat-10-1', name: '图书', isGroup: true, children: [
          { id: 'cat-10-1-1', name: '文学小说', goodsCount: 189 },
          { id: 'cat-10-1-2', name: '教育考试', goodsCount: 145 },
          { id: 'cat-10-1-3', name: '童书绘本', goodsCount: 98 },
        ]
      },
      {
        id: 'cat-10-2', name: '文具', isGroup: true, children: [
          { id: 'cat-10-2-1', name: '笔类', goodsCount: 78 },
          { id: 'cat-10-2-2', name: '笔记本', goodsCount: 56 },
        ]
      },
    ]
  },
];
