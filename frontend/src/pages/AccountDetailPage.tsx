import {
  ArrowLeftOutlined,
  EditOutlined,
  FileTextOutlined,
  MailOutlined,
  PhoneOutlined,
  PlusOutlined,
} from '@ant-design/icons'
import { Avatar, Button, Card, Col, Form, Input, Modal, Progress, Row, Select, Table, Tabs, Tag, Typography } from 'antd'
import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useGlobalMessage } from '../hooks/useGlobalMessage'
import { useI18n } from '../hooks/useI18n'
import {
  campaigns,
  contracts,
  flagForMarket,
  formatCurrency,
  getAccountById,
  getActivitiesByAccount,
  getContactsByAccount,
  getOpportunitiesByAccount,
  getOrdersByAccount,
  getPaymentsByAccount,
  getUserById,
  orders,
  payments,
  statusLabel,
  statusTone,
} from '../mocks/crmData'

const { Title, Text } = Typography

const tabKeys = [
  'overview',
  'contacts',
  'opportunities',
  'contracts',
  'orders',
  'payments',
  'activities',
  'campaigns',
  'documents',
]

export function AccountDetailPage() {
  const { id } = useParams<{ id: string }>()
  const account = getAccountById(id)
  const { t } = useI18n()
  const { success } = useGlobalMessage()
  const [activeTab, setActiveTab] = useState('overview')
  const [editOpen, setEditOpen] = useState(false)
  const [oppOpen, setOppOpen] = useState(false)

  if (!account) {
    return (
      <div className="crm-page">
        <Text>Account not found</Text>
        <Link to="/app/accounts">{t('accountDetail.back')}</Link>
      </div>
    )
  }

  const owner = getUserById(account.ownerId)
  const progress = Math.round((account.yearToDateUsd / account.annualTargetUsd) * 100)
  const totalRevenue = orders
    .filter((o) => o.accountId === account.id && o.status === '已完成')
    .reduce((s, o) => s + o.subtotalUsd, 0)
  const totalReceived = payments
    .filter((p) => p.accountId === account.id && p.status === '已确认')
    .reduce((s, p) => s + p.amountUsd, 0)
  const receivable = totalRevenue - totalReceived
  const activeOpps = getOpportunitiesByAccount(account.id)
  const wonOpps = activeOpps.filter((o) => o.stage === '已赢单')

  const stats = [
    { label: t('accountDetail.cumulativeSales'), value: formatCurrency(totalRevenue) },
    { label: t('accountDetail.cumulativeReceipts'), value: formatCurrency(totalReceived) },
    { label: t('accountDetail.receivable'), value: formatCurrency(receivable) },
    { label: t('accountDetail.activeOpps'), value: activeOpps.length.toString() },
    { label: t('accountDetail.won'), value: wonOpps.length.toString() },
    { label: t('accountDetail.creditLimit'), value: '-' },
  ]

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewTab account={account} progress={progress} owner={owner} stats={stats} />
      case 'contacts':
        return <ContactsTab accountId={account.id} />
      case 'opportunities':
        return <OpportunitiesTab accountId={account.id} />
      case 'contracts':
        return <ContractsTab accountId={account.id} />
      case 'orders':
        return <OrdersTab accountId={account.id} />
      case 'payments':
        return <PaymentsTab accountId={account.id} />
      case 'activities':
        return <ActivitiesTab accountId={account.id} />
      case 'campaigns':
        return <CampaignsTab />
      case 'documents':
        return <DocumentsTab />
      default:
        return null
    }
  }

  return (
    <div className="crm-page">
      <div className="crm-page-header">
        <div className="crm-page-header-left">
          <Link to="/app/accounts" className="back-link">
            <ArrowLeftOutlined /> {t('accountDetail.back')}
          </Link>
          <div className="crm-page-header-title" style={{ marginTop: 4 }}>
            {account.name}
            <Tag color={statusTone(account.contractStatus) === 'green' ? 'success' : statusTone(account.contractStatus) === 'amber' ? 'warning' : 'error'} style={{ marginLeft: 10 }}>
              {statusLabel(account.contractStatus)}
            </Tag>
          </div>
          <div className="crm-page-header-desc">
            <span className="flag">{flagForMarket(account.market)}</span>
            {account.market} · {account.code} · {t('accounts.owner')}: {owner?.name ?? '-'}
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <Button icon={<EditOutlined />} onClick={() => setEditOpen(true)}>{t('accountDetail.edit')}</Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={() => setOppOpen(true)}>{t('accountDetail.newOpp')}</Button>
        </div>
      </div>

      <Row gutter={[16, 16]}>
        {stats.map((s) => (
          <Col xs={12} md={8} lg={4} key={s.label}>
            <Card>
              <div className="metric-card-label">{s.label}</div>
              <div className="metric-card-value">{s.value}</div>
            </Card>
          </Col>
        ))}
      </Row>

      <Card>
        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          items={tabKeys.map((k) => ({ key: k, label: t(`accountDetail.tabs.${k}`) }))}
        />
        <div style={{ marginTop: 16 }}>{renderTabContent()}</div>
      </Card>

      <Modal
        title={t('accountDetail.edit')}
        open={editOpen}
        onCancel={() => setEditOpen(false)}
        onOk={() => { setEditOpen(false); success(t('common.successUpdate')) }}
        width={600}
      >
        <Form layout="vertical" initialValues={{ name: account.name, code: account.code, market: account.market, ownerId: account.ownerId }}>
          <Row gutter={16}>
            <Col span={12}><Form.Item label="客户名称" name="name"><Input /></Form.Item></Col>
            <Col span={12}><Form.Item label="客户代码" name="code"><Input /></Form.Item></Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}><Form.Item label="市场" name="market"><Select options={['SG','HK','MY','TH','ID','MO','US'].map(m => ({value:m, label:m}))} /></Form.Item></Col>
            <Col span={12}><Form.Item label="负责人" name="ownerId"><Select options={['u2','u3','u4','u5'].map(id => ({value:id, label:getUserById(id)?.name}))} /></Form.Item></Col>
          </Row>
          <Form.Item label="年度目标 (USD)" name="annualTarget"><Input prefix="$" /></Form.Item>
          <Form.Item label="商机深掘"><Input.TextArea rows={4} defaultValue={account.opportunityNotes} /></Form.Item>
        </Form>
      </Modal>

      <Modal
        title={t('accountDetail.newOpp')}
        open={oppOpen}
        onCancel={() => setOppOpen(false)}
        onOk={() => { setOppOpen(false); success(t('common.successCreate')) }}
        width={560}
      >
        <Form layout="vertical">
          <Form.Item label="商机名称"><Input placeholder="输入商机名称" /></Form.Item>
          <Row gutter={16}>
            <Col span={12}><Form.Item label="预计金额 (USD)"><Input prefix="$" /></Form.Item></Col>
            <Col span={12}><Form.Item label="赢率 (%)"><Select options={['20','40','60','80','100'].map(v => ({value:v, label:v+'%'}))} /></Form.Item></Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}><Form.Item label="阶段"><Select options={['初步接触','需求确认','方案报价','谈判中'].map(v => ({value:v, label:v}))} /></Form.Item></Col>
            <Col span={12}><Form.Item label="预计结单"><Input placeholder="2026-06-30" /></Form.Item></Col>
          </Row>
        </Form>
      </Modal>

      <style>{`
        .back-link { display: inline-flex; align-items: center; gap: 6px; color: var(--text-muted); font-size: 12px; text-decoration: none; }
        .back-link:hover { color: var(--angel-red); }
      `}</style>
    </div>
  )
}

function OverviewTab({ account, progress, owner }: any) {
  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} lg={16}>
        <Card title="商机深掘" style={{ marginBottom: 16 }}>
          <div className="opportunity-note-card" style={{ background: '#f8f7f4', borderRadius: 8, padding: 16, marginBottom: 16 }}>
            <Title level={5}>商用 (B2B) · 推进中</Title>
            <Text>{account.opportunityNotes}</Text>
          </div>
          <div style={{ marginBottom: 16 }}>
            <Text strong style={{ display: 'block', marginBottom: 6 }}>客户资源</Text>
            <Text className="text-secondary">{account.customerResources}</Text>
          </div>
          <div>
            <Text strong style={{ display: 'block', marginBottom: 6 }}>深化方向</Text>
            <Text className="text-secondary" style={{ whiteSpace: 'pre-line' }}>{account.nextDigDirections}</Text>
          </div>
        </Card>

        <Card title="年度目标进度">
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10 }}>
            <Text strong>年度目标</Text>
            <Text className="text-muted">{formatCurrency(account.yearToDateUsd)} / {formatCurrency(account.annualTargetUsd)} · {progress}%</Text>
          </div>
          <Progress percent={progress} strokeColor="#ee2737" trailColor="#ece6df" />
        </Card>
      </Col>

      <Col xs={24} lg={8}>
        <Card title="客户档案">
          <div className="profile-list">
            {[
              ['客户所在国家', flagForMarket(account.market) + ' ' + account.market],
              ['市场', account.market],
              ['归属公司', 'AHT Global Sales'],
              ['付款条款', 'Net 30'],
              ['信用额度', '-'],
              ['年度目标', formatCurrency(account.annualTargetUsd)],
              ['YTD 销售额', formatCurrency(account.yearToDateUsd)],
              ['负责人', owner?.name ?? '-'],
            ].map(([k, v]) => (
              <div className="profile-row" key={k}>
                <Text className="text-muted">{k}</Text>
                <Text strong>{v}</Text>
              </div>
            ))}
          </div>
        </Card>

        <Card title="主要联系人" style={{ marginTop: 16 }} extra={<Button type="text" icon={<PlusOutlined />}>添加</Button>}>
          {getContactsByAccount(account.id).slice(0, 2).map((c) => (
            <div key={c.id} className="contact-row">
              <Avatar size={36} style={{ background: '#0f172a' }}>{c.name.slice(0, 1)}</Avatar>
              <div>
                <Text strong>{c.name}</Text>
                <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{c.title}</div>
                <div style={{ fontSize: 12, display: 'flex', gap: 8, marginTop: 2 }}>
                  <span><PhoneOutlined /> {c.phone}</span>
                  <span><MailOutlined /> {c.email}</span>
                </div>
              </div>
            </div>
          ))}
        </Card>
      </Col>

      <style>{`
        .profile-list { display: flex; flex-direction: column; gap: 10px; }
        .profile-row { display: flex; justify-content: space-between; font-size: 13px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
        .profile-row:last-child { border-bottom: none; padding-bottom: 0; }
        .contact-row { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 12px; }
        .contact-row:last-child { margin-bottom: 0; }
      `}</style>
    </Row>
  )
}

function ContactsTab({ accountId }: { accountId: string }) {
  const data = getContactsByAccount(accountId)
  return (
    <Table
      dataSource={data}
      rowKey="id"
      pagination={false}
      columns={[
        { title: '姓名', dataIndex: 'name' },
        { title: '职位', dataIndex: 'title' },
        { title: '邮箱', dataIndex: 'email' },
        { title: '电话', dataIndex: 'phone' },
        { title: '主要联系人', dataIndex: 'isPrimary', render: (v) => v ? <Tag color="success">是</Tag> : '-' },
      ]}
    />
  )
}

function OpportunitiesTab({ accountId }: { accountId: string }) {
  const data = getOpportunitiesByAccount(accountId)
  return (
    <Table
      dataSource={data}
      rowKey="id"
      pagination={false}
      columns={[
        { title: '商机名称', dataIndex: 'name' },
        { title: '金额', dataIndex: 'amountUsd', render: (v) => formatCurrency(v) },
        { title: '阶段', dataIndex: 'stage' },
        { title: '赢率', dataIndex: 'probability', render: (v) => `${v}%` },
        { title: '预计结单', dataIndex: 'expectedCloseDate' },
      ]}
    />
  )
}

function ContractsTab({ accountId }: { accountId: string }) {
  const data = contracts.filter((c) => c.accountId === accountId)
  return (
    <Table
      dataSource={data}
      rowKey="id"
      pagination={false}
      columns={[
        { title: '合同编号', dataIndex: 'contractNumber' },
        { title: '名称', dataIndex: 'name' },
        { title: '类型', dataIndex: 'type' },
        { title: '状态', dataIndex: 'status' },
        { title: '金额', dataIndex: 'amountUsd', render: (v) => formatCurrency(v) },
        { title: '到期日', dataIndex: 'expiryDate' },
      ]}
    />
  )
}

function OrdersTab({ accountId }: { accountId: string }) {
  const data = getOrdersByAccount(accountId)
  return (
    <Table
      dataSource={data}
      rowKey="id"
      pagination={false}
      columns={[
        { title: '订单号', dataIndex: 'orderNumber' },
        { title: 'PI 号', dataIndex: 'piNumber' },
        { title: '金额', dataIndex: 'subtotalUsd', render: (v) => formatCurrency(v) },
        { title: '类型', dataIndex: 'orderType' },
        { title: '状态', dataIndex: 'status' },
        { title: '创建时间', dataIndex: 'createdAt' },
      ]}
    />
  )
}

function PaymentsTab({ accountId }: { accountId: string }) {
  const data = getPaymentsByAccount(accountId)
  return (
    <Table
      dataSource={data}
      rowKey="id"
      pagination={false}
      columns={[
        { title: '到账时间', dataIndex: 'receivedAt' },
        { title: '金额', dataIndex: 'amountUsd', render: (v) => formatCurrency(v) },
        { title: '币种', dataIndex: 'currency' },
        { title: '方式', dataIndex: 'method' },
        { title: '状态', dataIndex: 'status' },
      ]}
    />
  )
}

function ActivitiesTab({ accountId }: { accountId: string }) {
  const data = getActivitiesByAccount(accountId)
  return (
    <Table
      dataSource={data}
      rowKey="id"
      pagination={false}
      columns={[
        { title: '时间', dataIndex: 'createdAt' },
        { title: '类型', dataIndex: 'type' },
        { title: '内容', dataIndex: 'content' },
        { title: '记录人', dataIndex: 'createdById', render: (id) => getUserById(id)?.name ?? id },
      ]}
    />
  )
}

function CampaignsTab() {
  return (
    <Table
      dataSource={campaigns}
      rowKey="id"
      pagination={false}
      columns={[
        { title: '活动编号', dataIndex: 'code' },
        { title: '活动名称', dataIndex: 'name' },
        { title: '状态', dataIndex: 'status' },
        { title: '转化金额', dataIndex: 'opportunityValueUsd', render: (v) => formatCurrency(v) },
      ]}
    />
  )
}

function DocumentsTab() {
  return (
    <Table
      dataSource={[
        { name: 'Raffles-PO-2026-05-08.pdf', type: '采购订单', date: '2026-05-30' },
        { name: 'AHT-Receipt-Raffles-001.pdf', type: '收款确认书', date: '2026-05-28' },
      ]}
      rowKey="name"
      pagination={false}
      columns={[
        { title: '文件名', dataIndex: 'name', render: (v) => <span><FileTextOutlined style={{ marginRight: 6 }} />{v}</span> },
        { title: '类型', dataIndex: 'type' },
        { title: '上传日期', dataIndex: 'date' },
      ]}
    />
  )
}
