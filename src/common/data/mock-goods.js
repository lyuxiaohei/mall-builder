/* mock-goods.js — 商品列表 Mock 数据(100个商品, 生成器) + 分页状态。
 * 从 src/editor.html IIFE 内 MOCK_GOODS_DATA / goodsPaginationState 外置(Phase 2)。
 * 生成器 helper (goodsNames 等) 为本文件局部, 仅用于生成。 */
MallBuilder.data.MOCK_GOODS_DATA = [];
const goodsNames = [
  '智能手表 Pro', '无线蓝牙耳机', '便携充电宝', '手机支架', '机械键盘',
  '游戏鼠标', '高清摄像头', '降噪耳麦', '固态硬盘', '内存条',
  '显示器支架', 'USB扩展坞', '移动硬盘', '路由器', '网络交换机',
  '智能音箱', '扫地机器人', '空气净化器', '加湿器', '台灯',
  '护眼灯', '电动牙刷', '剃须刀', '吹风机', '卷发棒',
  '电饭煲', '电磁炉', '微波炉', '破壁机', '咖啡机'
];
const goodsColors = ['黑色', '白色', '银色', '深空灰', '星空蓝', '玫瑰金', '香槟金', '极光绿'];
const goodsSpecs = ['标准版', '升级版', '尊享版', 'Pro版', 'Lite版', 'Max版'];
const goodsTags = ['热销', '新品', '特价', '限时', '爆款', ''];
const cornerTags = ['new', 'hot', 'sale', 'group', 'seckill', 'none'];

for (let i = 1; i <= 100; i++) {
  const nameIdx = (i - 1) % goodsNames.length;
  const colorIdx = (i - 1) % goodsColors.length;
  const specIdx = (i - 1) % goodsSpecs.length;
  const tagIdx = (i - 1) % goodsTags.length;
  const basePrice = 50 + Math.floor(Math.random() * 2000);
  const originalPrice = basePrice + Math.floor(Math.random() * 500);

  MallBuilder.data.MOCK_GOODS_DATA.push({
    id: 'goods-' + i,
    name: goodsNames[nameIdx] + ' ' + Math.ceil(i / 10) + '号',
    spec: goodsColors[colorIdx] + ' / ' + goodsSpecs[specIdx],
    price: basePrice.toString(),
    originalPrice: originalPrice.toString(),
    tag: goodsTags[tagIdx],
    cornerTag: cornerTags[(i - 1) % cornerTags.length],
    sales: Math.floor(Math.random() * 10000),
    comments: Math.floor(Math.random() * 5000),
    goodRate: (95 + Math.random() * 5).toFixed(1)
  });
}

// 商品列表分页状态
MallBuilder.data.goodsPaginationState = {
  currentPage: 1,
  pageSize: 10,
  loading: false,
  hasMore: true
};
