import { ArrowRightOutlined, ContainerOutlined, DollarOutlined, ShoppingOutlined, TruckOutlined } from '@ant-design/icons'
import { Button, Card, Empty, Row, Space, Table, Tag, Typography } from 'antd'
import { useGlobalMessage } from '../hooks/useGlobalMessage'
import { useI18n } from '../hooks/useI18n'
import { formatCurrency, getAccountById, orders, payments, statusTone } from '../mocks/crmData'

const { Text, Title } = Typography

const collectionPlans = [
  { id: 'cp1', accountId: 'a1', dueDate: '2026-06-20', planAmountUsd: 42000, status: '即将到期' },
  { id: 'cp2', accountId: 'a2', dueDate: '2026-06-14', planAmountUsd: 18000, status: '已逾期' },
]

export function WorkQueuePage() {
  const { t } = useI18n()
  const { success } = useGlobalMessage()

  const orderOps = orders.filter((o) => o.status === '待开具 PI' || o.status === 'PI 已开具')
  const supply = orders.filter((o) => o.status === '已发货')
  const paymentVerification = payments.filter((p) => p.status === '待确认')

  const cards = [
    { key: 'orderOps', icon: <ShoppingOutlined />, value: orderOps.length },
    { key: 'supply', icon: <TruckOutlined />, value: supply.length },
    { key: 'finance', icon: <DollarOutlined />, value: paymentVerification.length + collectionPlans.length },
  ]

  const orderColumns = [
    { title: t('workqueue.table.orderNo'), dataIndex: 'orderNumber' },
    { title: t('workqueue.table.account'), dataIndex: 'accountId', render: (id: string) => getAccountById(id)?.name },
    { title: t('workqueue.table.subtotal'), dataIndex: 'subtotalUsd', render: (v: number) => formatCurrency(v) },
    { title: t('workqueue.table.status'), dataIndex: 'status', render: (v: string) => <Tag className={`pill pill-${statusTone(v)}`}>{v}</Tag> },
    { title: t('workqueue.table.action'), render: () => <Tag className="pill pill-amber">{t('workqueue.table.open')}</Tag> },
    { title: t('workqueue.table.createdAt'), dataIndex: 'createdAt' },
    {
      title: '',
      key: 'open',
      render: () => (
        <Button type="primary" size="small" icon={<ArrowRightOutlined />} onClick={() => success(t('common.confirm'))}>
          {t('workqueue.table.open')}
        </Button>
      ),
    },
  ]

  const paymentColumns = [
    { title: t('workqueue.table.receivedAt'), dataIndex: 'receivedAt' },
    { title: t('workqueue.table.account'), dataIndex: 'accountId', render: (id: string) => getAccountById(id)?.name },
    { title: t('workqueue.table.amount'), dataIndex: 'amountUsd', render: (v: number) => formatCurrency(v) },
    { title: t('workqueue.table.financeConfirm'), dataIndex: 'status', render: (v: string) => <Tag className={`pill pill-${statusTone(v)}`}>{v}</Tag> },
    { title: t('workqueue.table.action'), render: () => <Tag className="pill pill-amber">确认付款</Tag> },
    {
      title: '',
      key: 'open',
      render: () => (
        <Button type="primary" size="small" icon={<ArrowRightOutlined />} onClick={() => success(t('common.confirm'))}>
          {t('workqueue.table.open')}
        </Button>
      ),
    },
  ]

  const collectionColumns = [
    { title: t('workqueue.table.dueDate'), dataIndex: 'dueDate' },
    { title: t('workqueue.table.account'), dataIndex: 'accountId', render: (id: string) => getAccountById(id)?.name },
    { title: t('workqueue.table.planAmount'), dataIndex: 'planAmountUsd', render: (v: number) => formatCurrency(v) },
    { title: t('workqueue.table.status'), dataIndex: 'status', render: (v: string) => <Tag className={`pill pill-${statusTone(v)}`}>{v}</Tag> },
    { title: t('workqueue.table.action'), render: () => <Tag className="pill pill-amber">提醒客户</Tag> },
    {
      title: '',
      key: 'open',
      render: () => (
        <Button type="primary" size="small" icon={<ArrowRightOutlined />} onClick={() => success(t('common.confirm'))}>
          {t('workqueue.table.open')}
        </Button>
      ),
    },
  ]

  return (
    <div className="crm-page">
      <div className="crm-page-header">
        <div className="crm-page-header-left">
          <div className="crm-page-header-title">{t('workqueue.title')}</div>
          <div className="crm-page-header-desc">
            {t('workqueue.role')}: {t('pages.settings') === '设置' ? '系统管理员' : 'System Admin'}
          </div>
        </div>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        {cards.map((c) => (
          <div key={c.key} className="workqueue-kpi-card">
            <div className="workqueue-kpi-icon">{c.icon}</div>
            <div>
              <div className="workqueue-kpi-label">{t(`workqueue.cards.${c.key}`)}</div>
              <div className="workqueue-kpi-value" style={{ color: c.key === 'finance' ? '#ee2737' : c.key === 'supply' ? '#3b82f6' : '#f59e0b' }}>{c.value}</div>
            </div>
          </div>
        ))}
      </Row>

      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <SectionCard
          icon={<ShoppingOutlined />}
          title={t('workqueue.sections.orderOps')}
          desc={t('workqueue.sections.orderOpsDesc')}
          data={orderOps}
          columns={orderColumns}
          empty={t('workqueue.table.noData')}
        />
        <SectionCard
          icon={<TruckOutlined />}
          title={t('workqueue.sections.supply')}
          desc={t('workqueue.sections.supplyDesc')}
          data={supply}
          columns={orderColumns}
          empty={t('workqueue.table.noData')}
        />
        <SectionCard
          icon={<DollarOutlined />}
          title={t('workqueue.sections.paymentVerification')}
          desc={t('workqueue.sections.paymentVerificationDesc')}
          data={paymentVerification}
          columns={paymentColumns}
          empty={t('workqueue.table.noData')}
        />
        <SectionCard
          icon={<ContainerOutlined />}
          title={t('workqueue.sections.collectionTracking')}
          desc={t('workqueue.sections.collectionTrackingDesc')}
          data={collectionPlans}
          columns={collectionColumns}
          empty={t('workqueue.table.noData')}
        />
      </Space>

      <style>{`
        .workqueue-kpi-card { flex: 1; background: #fff; border: 1px solid var(--border); border-radius: 8px; padding: 16px; display: flex; align-items: center; gap: 14px; min-width: 200px; }
        .workqueue-kpi-icon { width: 40px; height: 40px; border-radius: 8px; background: #f8f7f4; display: grid; place-items: center; font-size: 18px; color: var(--angel-red); }
        .workqueue-kpi-label { font-size: 12px; font-weight: 600; color: var(--text-muted); }
        .workqueue-kpi-value { font-size: 28px; font-weight: 700; line-height: 1.2; }
        .workqueue-section-header { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
        .workqueue-section-title { font-size: 16px; font-weight: 700; margin: 0; }
        .workqueue-section-desc { color: var(--text-muted); font-size: 13px; }
      `}</style>
    </div>
  )
}

function SectionCard({ icon, title, desc, data, columns, empty }: any) {
  return (
    <Card>
      <div className="workqueue-section-header">
        {icon}
        <Title level={5} className="workqueue-section-title">{title}</Title>
      </div>
      <Text className="workqueue-section-desc" style={{ display: 'block', marginBottom: 16 }}>{desc}</Text>
      {data.length > 0 ? (
        <Table dataSource={data} rowKey="id" pagination={false} columns={columns} />
      ) : (
        <Empty description={empty} image={Empty.PRESENTED_IMAGE_SIMPLE} />
      )}
    </Card>
  )
}
