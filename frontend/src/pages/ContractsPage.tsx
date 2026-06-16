import { EyeOutlined, PlusOutlined, WarningOutlined } from '@ant-design/icons'
import { Alert, Button, Card, DatePicker, Form, Input, Modal, Select, Table } from 'antd'
import { useMemo, useState } from 'react'
import { useAutoCreate } from '../hooks/useAutoCreate'
import { useGlobalMessage } from '../hooks/useGlobalMessage'
import { useI18n } from '../hooks/useI18n'
import { accounts, contracts, formatCurrency, getAccountById, statusTone } from '../mocks/crmData'

const contractTypes = ['框架合同', '单笔合同', '补充协议']
const contractStatuses = ['有效', '即将到期', '已到期']

export function ContractsPage() {
  const { t } = useI18n()
  const { success } = useGlobalMessage()
  const [createOpen, setCreateOpen] = useState(false)
  const clearCreateParam = useAutoCreate(setCreateOpen)
  const [detailOpen, setDetailOpen] = useState(false)
  const [selected, setSelected] = useState<typeof contracts[0] | null>(null)

  const expiringSoon = useMemo(() => contracts.filter((c) => c.status === '即将到期').length, [])

  return (
    <div className="crm-page">
      <div className="crm-page-header">
        <div className="crm-page-header-left">
          <div className="crm-page-header-title">{t('contracts.title')}</div>
          <div className="crm-page-header-desc">{t('contracts.subtitle')}</div>
        </div>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setCreateOpen(true)}>{t('contracts.create')}</Button>
      </div>

      <Alert
        message={t('contracts.alert').replace('{count}', String(expiringSoon))}
        type="warning"
        showIcon
        icon={<WarningOutlined />}
        style={{ marginBottom: 16 }}
      />

      <Card>
        <Table
          dataSource={contracts}
          rowKey="id"
          pagination={false}
          columns={[
            { title: t('contracts.code'), dataIndex: 'contractNumber' },
            { title: t('contracts.account'), dataIndex: 'accountId', render: (id) => getAccountById(id)?.name },
            { title: t('contracts.name'), dataIndex: 'name' },
            { title: t('contracts.type'), dataIndex: 'type' },
            { title: t('contracts.status'), dataIndex: 'status', render: (v) => <span className={`pill pill-${statusTone(v)}`}>{v}</span> },
            { title: t('contracts.entity'), dataIndex: 'signEntity' },
            { title: t('contracts.amount'), dataIndex: 'amountUsd', render: (v) => formatCurrency(v) },
            { title: t('contracts.collectionProgress'), dataIndex: 'paymentProgress' },
            { title: t('contracts.paymentStatus'), dataIndex: 'paymentStatus' },
            { title: t('contracts.expiry'), dataIndex: 'expiryDate' },
            {
              title: t('common.actions'),
              key: 'action',
              render: (_: any, record: typeof contracts[0]) => (
                <Button type="text" icon={<EyeOutlined />} onClick={() => { setSelected(record); setDetailOpen(true) }} />
              ),
            },
          ]}
        />
      </Card>

      <Modal
        title={t('contracts.create')}
        open={createOpen}
        onCancel={() => { setCreateOpen(false); clearCreateParam() }}
        onOk={() => { setCreateOpen(false); clearCreateParam(); success(t('common.successCreate')) }}
        width={560}
      >
        <Form layout="vertical">
          <Form.Item label={t('contracts.name')}><Input /></Form.Item>
          <Form.Item label={t('contracts.account')}>
            <Select options={accounts.map((a) => ({ value: a.id, label: a.name }))} />
          </Form.Item>
          <Form.Item label={t('contracts.type')}>
            <Select options={contractTypes.map((v) => ({ value: v, label: v }))} />
          </Form.Item>
          <Form.Item label={t('contracts.status')}>
            <Select options={contractStatuses.map((v) => ({ value: v, label: v }))} />
          </Form.Item>
          <Form.Item label={t('contracts.amount')}><Input prefix="$" /></Form.Item>
          <Form.Item label={t('contracts.expiry')}><DatePicker style={{ width: '100%' }} /></Form.Item>
        </Form>
      </Modal>

      <Modal
        title={t('contracts.detail')}
        open={detailOpen}
        onCancel={() => setDetailOpen(false)}
        footer={null}
        width={560}
      >
        {selected && (
          <Form layout="vertical">
            <Form.Item label={t('contracts.name')}><Input readOnly value={selected.name} /></Form.Item>
            <Form.Item label={t('contracts.account')}><Input readOnly value={getAccountById(selected.accountId)?.name} /></Form.Item>
            <Form.Item label={t('contracts.type')}><Input readOnly value={selected.type} /></Form.Item>
            <Form.Item label={t('contracts.status')}><Input readOnly value={selected.status} /></Form.Item>
            <Form.Item label={t('contracts.amount')}><Input readOnly value={formatCurrency(selected.amountUsd)} /></Form.Item>
            <Form.Item label={t('contracts.expiry')}><Input readOnly value={selected.expiryDate} /></Form.Item>
          </Form>
        )}
      </Modal>
    </div>
  )
}
