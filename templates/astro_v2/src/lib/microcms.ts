import { createClient, type MicroCMSQueries } from 'microcms-js-sdk';

// ==========================================
// 1. 型定義 (News / Works)
// ==========================================

export interface NewsCategory {
  id: string;
  name: string;
}

export interface NewsItem {
  id: string;
  title: string;
  publishedAt?: string;
  createdAt?: string;
  date?: string; // 表示用（YYYY.MM.DD）
  category: string;
  content: string; // HTML文字列
  thumbnail?: {
    url: string;
    width?: number;
    height?: number;
  };
}

export interface WorkSlide {
  id?: number | string;
  title: string;
  image: string;
  caption: string;
}

export interface WorkSpec {
  label: string;
  value: string;
}

export interface WorkItem {
  id: string;
  title: string;
  subTitle?: string;
  location: string;
  type: string;
  tag: string;
  mainImage: string;
  publishedAt?: string;
  slides: WorkSlide[];
  specs: WorkSpec[];
  conceptTitle: string;
  conceptBody: string;
  comment: string;
  designer: string;
}

// ==========================================
// 2. フォールバック・モックデータ
// ==========================================

export const MOCK_NEWS: NewsItem[] = [
  {
    id: '2026-08-24-sample',
    title: '地方中小企業向け超高速Webエンジン「ArCraft」のサービス提供および無料診断を開始しました',
    date: '2026.09.20',
    category: 'サービス',
    content: `
      <p>この度、地方工務店・中小企業のための超高速Web制作・運用基盤「ArCraft（アルクラフト）」のサービス提供を開始いたしました。</p>
      <p>従来のWordPressサイトで頻発していた「プラグイン脆弱性」「バージョン更新崩れ」「表示速度の低下」を完全解決し、Google PageSpeed 95点以上の超高速表示と堅牢なセキュリティを実現します。</p>
      <div style="background-color: #f5f5f4; padding: 1.5rem; margin: 1.5rem 0; border: 1px solid #e7e5e4;">
        <h4 style="font-weight: 700; margin-bottom: 0.5rem; color: #1c1917;">無料サイト診断のご案内</h4>
        <p style="margin: 0; font-size: 0.875rem; color: #44403c;">貴社サイトの現状表示速度（LCP/CLS）やSEO基礎スコア、セキュリティリスクを無料で診断いたします。お気軽にお問い合わせください。</p>
      </div>
      <p>今後ともArCraftをよろしくお願いいたします。</p>
    `,
  },
  {
    id: 'news-02',
    title: 'microCMS連携による更新性強化とAstro Actionsによる高信頼フォーム対応を実装しました',
    date: '2026.09.15',
    category: '機能追加',
    content: '<p>microCMSによるヘッドレスCMS連携と、スパム耐性の高いサーバーサイドバリデーション対応フォームを標準搭載いたしました。</p>',
  },
  {
    id: 'news-03',
    title: '地方工務店・中小企業向けWebサイト無料診断の受付枠を拡大いたしました',
    date: '2026.09.01',
    category: 'お知らせ',
    content: '<p>大変ご好評をいただいておりますWebサイト無料診断につきまして、9月分の受付枠を10社限定で追加いたしました。</p>',
  }
];

export const MOCK_WORKS: WorkItem[] = [
  {
    id: 'sample-project',
    title: '中庭を囲む光のコートハウス',
    subTitle: 'Courtyard House in Setagaya',
    location: '東京都世田谷区',
    type: '新築注文住宅 / 木造2階',
    tag: '建築・施工事例',
    mainImage: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',
    slides: [
      { id: 1, title: '外観ファサード', image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80', caption: '1. 外観：杉板張りとガルバリウム鋼板が調和する端正なファサード' },
      { id: 2, title: 'リビング吹き抜け', image: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=80', caption: '2. リビング：天井高5.2mの大開口から自然光が降り注ぐLDK' },
      { id: 3, title: '階段・吹き抜け（縦構図）', image: 'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?auto=format&fit=crop&w=800&q=80', caption: '3. 階段・吹き抜け（縦構図写真）：2階へと視線が抜けるスケルトン階段とハイサイドライト' },
      { id: 4, title: 'ダイニング・キッチン', image: 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=80', caption: '4. ダイニング：モールテックス天板の特注アイランドキッチン' },
      { id: 5, title: '中庭コートヤード', image: 'https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80', caption: '5. 中庭：リビングとフラットに繋がるプライベートウッドデッキ' },
      { id: 6, title: '通り土間・坪庭（縦構図）', image: 'https://images.unsplash.com/photo-1507652313519-d4e9174996dd?auto=format&fit=crop&ar=2:3&w=800&q=80', caption: '6. 通り土間（縦構図写真）：視線が奥へと伸びる陰影豊かな縦長空間設計' },
      { id: 7, title: '主寝室', image: 'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1200&q=80', caption: '7. 主寝室：間接照明と珪藻土の塗り壁が演出する静寂の空間' },
      { id: 8, title: '造作洗面サニタリー', image: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=1200&q=80', caption: '8. サニタリー：大谷石と真鍮水栓をあしらったオリジナル造作洗面台' },
    ],
    specs: [
      { label: '所在地', value: '東京都世田谷区' },
      { label: '構造・規模', value: '木造軸組工法（SE構法） 地上2階建て' },
      { label: '敷地面積 / 延床面積', value: '165.20㎡ (49.97坪) / 128.45㎡ (38.85坪)' },
      { label: '断熱性能・省エネ', value: '断熱等級6 / HEAT20 G2グレード（Ua値: 0.38 W/㎡K）' },
      { label: '耐震性能', value: '耐震等級3（許容応力度計算による構造計算実施）' },
      { label: '竣工年月', value: '2026年3月' },
    ],
    conceptTitle: '都市の喧騒を忘れ、空と光を取り込む静謐の住まい',
    conceptBody: '住宅密集地にありながら、外部からの視線を遮りつつ自然光と風を最大限に取り込むため、建物の中央にロの字型の中庭（コートヤード）を配置。プライバシーを完全に守られたウッドデッキテラスは、第二のリビングとして機能します。内装にはオーク無垢床と珪藻土、真鍮の金物を採用し、経年とともに味わいを深める素材選びにこだわりました。',
    comment: '「クライアントが好まれる北欧のヴィンテージ家具と美しく調和するよう、床にはオーク三層無垢材、壁面には左官職人による大谷石調の塗り壁を施しました。光の陰影が時間とともに表情を変える、静謐で飽きのこない空間を目指しました。」',
    designer: '一級建築士 高山 潤一'
  }
];

// ==========================================
// 3. microCMS クライアント初期化
// ==========================================

const serviceDomain = import.meta.env.MICROCMS_SERVICE_DOMAIN;
const apiKey = import.meta.env.MICROCMS_API_KEY;

export const isMicroCMSConfigured = Boolean(serviceDomain && apiKey);

export const client = isMicroCMSConfigured
  ? createClient({
      serviceDomain: serviceDomain as string,
      apiKey: apiKey as string,
    })
  : null;

// rawデータの型（microCMSの実レスポンス柔軟対応）
interface MicroCMSNewsRaw {
  id: string;
  title: string;
  publishedAt?: string;
  createdAt?: string;
  date?: string;
  category?: string | { id?: string; name?: string };
  content: string;
  thumbnail?: { url: string; width?: number; height?: number };
  thambnail?: { url: string; width?: number; height?: number };
}

function formatNewsItem(item: MicroCMSNewsRaw): NewsItem {
  let categoryName = 'お知らせ';
  if (typeof item.category === 'object' && item.category !== null) {
    categoryName = item.category.name || 'お知らせ';
  } else if (typeof item.category === 'string' && item.category.trim() !== '') {
    categoryName = item.category;
  }

  const thumbnail = item.thumbnail || item.thambnail || undefined;

  return {
    id: item.id,
    title: item.title,
    publishedAt: item.publishedAt,
    createdAt: item.createdAt,
    date: item.publishedAt
      ? new Date(item.publishedAt).toISOString().split('T')[0].replace(/-/g, '.')
      : item.date || '2026.01.01',
    category: categoryName,
    content: item.content || '',
    thumbnail,
  };
}

// ==========================================
// 4. データ取得関数（フォールバック付き）
// ==========================================

export async function getNewsList(queries?: MicroCMSQueries): Promise<NewsItem[]> {
  if (!client) {
    return MOCK_NEWS;
  }

  try {
    const res = await client.getList<MicroCMSNewsRaw>({
      endpoint: 'news',
      queries: {
        orders: '-publishedAt',
        ...queries,
      },
    });

    return res.contents.map(formatNewsItem);
  } catch (error) {
    console.warn('[microCMS] news取得に失敗したためモックデータを使用します:', error);
    return MOCK_NEWS;
  }
}

export async function getNewsDetail(contentId: string, queries?: MicroCMSQueries): Promise<NewsItem | null> {
  if (!client) {
    return MOCK_NEWS.find((item) => item.id === contentId) || MOCK_NEWS[0];
  }

  try {
    const item = await client.getListDetail<MicroCMSNewsRaw>({
      endpoint: 'news',
      contentId,
      queries,
    });
    return formatNewsItem(item);
  } catch (error) {
    console.warn(`[microCMS] news/${contentId} 取得に失敗したためモックデータを使用します:`, error);
    return MOCK_NEWS.find((item) => item.id === contentId) || MOCK_NEWS[0];
  }
}

export async function getWorksList(queries?: MicroCMSQueries): Promise<WorkItem[]> {
  if (!client) {
    return MOCK_WORKS;
  }

  try {
    const res = await client.getList<WorkItem>({
      endpoint: 'works',
      queries: {
        orders: '-publishedAt',
        ...queries,
      },
    });
    return res.contents;
  } catch (error) {
    console.warn('[microCMS] works取得に失敗したためモックデータを使用します:', error);
    return MOCK_WORKS;
  }
}

export async function getWorksDetail(contentId: string, queries?: MicroCMSQueries): Promise<WorkItem | null> {
  if (!client) {
    return MOCK_WORKS.find((item) => item.id === contentId) || MOCK_WORKS[0];
  }

  try {
    const item = await client.getListDetail<WorkItem>({
      endpoint: 'works',
      contentId,
      queries,
    });
    return item;
  } catch (error) {
    console.warn(`[microCMS] works/${contentId} 取得に失敗したためモックデータを使用します:`, error);
    return MOCK_WORKS.find((item) => item.id === contentId) || MOCK_WORKS[0];
  }
}

