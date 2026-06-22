import { EditOutlined, PlusOutlined, SearchOutlined } from '@ant-design/icons'
import { Button, Checkbox, Form, Input, Modal, Select, Spin } from 'antd'
import { useEffect, useMemo, useState } from 'react'
import { listAccounts, type Account } from '../api/accounts'
import { createOpportunity, listOpportunities, updateOpportunity, type Opportunity, type OpportunityStage } from '../api/opportunities'
import { listUsers, type User } from '../api/users'
import { useGlobalMessage } from '../hooks/useGlobalMessage'
import { useI18n } from '../hooks/useI18n'

const stageOrder: OpportunityStage[] = ['prospect', 'qualify', 'proposal', 'negotiate', 'closedWon']

function parseAmount(amount: string): number {
  const normalized = amount.replace(/[$,]/g, '').toLowerCase()
  if (normalized.includes('m')) return parseFloat(normalized) * 1_000_000
  if (normalized.includes('k')) return parseFloat(normalized) * 1_000
  return parseFloat(normalized) || 0
}

function formatAmount(total: number): string {
  if (total >= 1_000_000) return `$${(total / 1_000_000).toFixed(2)}M`
  return `$${Math.round(total / 1_000)}k`
}

function accountRegionCode(account: Account): string {
  return `${account.market} · ${account.code}`
}

export function PipelinePage() {
  const { t } = useI18n()
  const { success, error } = useGlobalMessage()
  const [loading, setLoading] = useState(true)
  const [cards, setCards] = useState<Opportunity[]>([])
  const [accounts, setAccounts] = useState<Account[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [search, setSearch] = useState('')
  const [region, setRegion] = useState<string>('ALL')
  const [createOpen, setCreateOpen] = useState(false)
  const [editing, setEditing] = useState<Opportunity | null>(null)
  const [createForm] = Form.useForm()
  const [editForm] = Form.useForm()

  const fetchData = async () => {
    try {
      setLoading(true)
      const [oppList, accountList, userList] = await Promise.all([
        listOpportunities(),
        listAccounts(),
        listUsers(),
      ])
      setCards(oppList)
      setAccounts(accountList)
      setUsers(userList)
    } catch (e) {
      error(t('common.loadError'))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const regions = useMemo(() => {
    const codes = Array.from(new Set(cards.map((c) => c.regionCode.split(' · ')[0]))).sort()
    return ['ALL', ...codes]
  }, [cards])

  const filtered = useMemo(() => {
    return cards.filter((c) => {
      const s = search.toLowerCase()
      const matchesSearch =
        c.companyName.toLowerCase().includes(s) || c.regionCode.toLowerCase().includes(s)
      const matchesRegion = region === 'ALL' || c.regionCode.startsWith(region)
      return matchesSearch && matchesRegion
    })
  }, [cards, search, region])

  const noFollowUpCount = cards.filter((c) => c.isNoFollowUp).length

  const handleCreate = async (values: Record<string, unknown>) => {
    const account = accounts.find((a) => a.id === values.accountId)
    if (!account) return
    const regionCode = (values.regionCode as string) || accountRegionCode(account)
    const payload = {
      accountId: account.id,
      companyName: (values.companyName as string) || account.name,
      regionCode,
      tags: (values.tags as string) || '',
      amount: (values.amount as string) || '',
      ownerName: (values.ownerName as string) || '',
      stage: (values.stage as OpportunityStage) || 'prospect',
      isNoFollowUp: Boolean(values.isNoFollowUp),
      winType: values.stage === 'closedWon' ? (values.winType as 'first' | 'reorder') : null,
    }
    try {
      await createOpportunity(payload)
      success(t('common.successCreate'))
      setCreateOpen(false)
      createForm.resetFields()
      await fetchData()
    } catch (e) {
      error(t('common.saveError'))
    }
  }

  const handleEdit = async (values: Record<string, unknown>) => {
    if (!editing) return
    const payload: Parameters<typeof updateOpportunity>[1] = {
      accountId: values.accountId as string,
      companyName: values.companyName as string,
      regionCode: values.regionCode as string,
      tags: values.tags as string,
      amount: values.amount as string,
      ownerName: values.ownerName as string,
      stage: values.stage as OpportunityStage,
      isNoFollowUp: Boolean(values.isNoFollowUp),
      winType: values.stage === 'closedWon' ? (values.winType as 'first' | 'reorder') : null,
    }
    try {
      await updateOpportunity(editing.id, payload)
      success(t('common.successUpdate'))
      setEditing(null)
      editForm.resetFields()
      await fetchData()
    } catch (e) {
      error(t('common.saveError'))
    }
  }

  const openEdit = (card: Opportunity) => {
    setEditing(card)
    editForm.setFieldsValue({
      accountId: card.accountId,
      companyName: card.companyName,
      regionCode: card.regionCode,
      tags: card.tags,
      amount: card.amount,
      ownerName: card.ownerName,
      stage: card.stage,
      isNoFollowUp: card.isNoFollowUp,
      winType: card.winType,
    })
  }

  const stageOptions = stageOrder.map((s) => ({ value: s, label: t(`labels.oppStage.${s}`) }))

  return (
    <div className="crm-page pipeline-page">
      <div className="pipeline-header">
        <div className="pipeline-title-wrap">
          <div className="crm-page-header-title">{t('pipeline.title')}</div>
          <span className="pipeline-badge">
            {noFollowUpCount} {t('pipeline.noFollowUp')}
          </span>
        </div>
      </div>

      <div className="pipeline-toolbar">
        <div className="pipeline-toolbar-left">
          <Input
            prefix={<SearchOutlined />}
            placeholder={t('pipeline.searchPlaceholder')}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pipeline-search"
          />
          <div className="region-chips">
            {regions.map((code) => (
              <button
                key={code}
                className={`region-chip ${region === code ? 'active' : ''}`}
                onClick={() => setRegion(code)}
              >
                {code === 'ALL' ? t('pipeline.regionAll') : code}
              </button>
            ))}
          </div>
        </div>
        <Button
          type="primary"
          className="pipeline-new-btn"
          icon={<PlusOutlined />}
          onClick={() => setCreateOpen(true)}
        >
          {t('pipeline.newOpp')}
        </Button>
      </div>

      {loading ? (
        <div className="pipeline-loading">
          <Spin size="large" />
        </div>
      ) : (
        <div className="pipeline-board">
          {stageOrder.map((stage) => (
            <KanbanColumn key={stage} stage={stage} cards={filtered.filter((c) => c.stage === stage)} onEdit={openEdit} />
          ))}
        </div>
      )}

      <Modal
        title={t('pipeline.newOpp')}
        open={createOpen}
        onCancel={() => { setCreateOpen(false); createForm.resetFields() }}
        onOk={() => createForm.submit()}
        width={560}
        destroyOnClose
      >
        <Form form={createForm} layout="vertical" onFinish={handleCreate}>
          <Form.Item label={t('accounts.formName')} name="accountId" rules={[{ required: true, message: t('common.required') }]}>
            <Select
              placeholder={t('common.selectAccount')}
              options={accounts.map((a) => ({ value: a.id, label: `${a.market} · ${a.code} · ${a.name}` }))}
              onChange={(id) => {
                const account = accounts.find((a) => a.id === id)
                if (account) {
                  createForm.setFieldsValue({
                    companyName: account.name,
                    regionCode: accountRegionCode(account),
                  })
                }
              }}
            />
          </Form.Item>
          <Form.Item label={t('leads.company')} name="companyName" rules={[{ required: true, message: t('common.required') }]}>
            <Input />
          </Form.Item>
          <Form.Item label={t('leads.market')} name="regionCode" rules={[{ required: true, message: t('common.required') }]}>
            <Input />
          </Form.Item>
          <Form.Item label={t('products.category')} name="tags">
            <Input placeholder="fnb · distributor" />
          </Form.Item>
          <Form.Item label={t('common.amount')} name="amount">
            <Input placeholder="$120k" />
          </Form.Item>
          <Form.Item label={t('leads.owner')} name="ownerName">
            <Select
              placeholder={t('common.selectOwner')}
              options={users.map((u) => ({ value: u.name, label: u.name }))}
            />
          </Form.Item>
          <Form.Item label={t('common.stage')} name="stage" initialValue="prospect" rules={[{ required: true }]}>
            <Select options={stageOptions} />
          </Form.Item>
          <Form.Item noStyle shouldUpdate={(prev, next) => prev.stage !== next.stage}>
            {({ getFieldValue }) =>
              getFieldValue('stage') === 'closedWon' ? (
                <Form.Item label={t('pipeline.winType')} name="winType" initialValue="first">
                  <Select
                    options={[
                      { value: 'first', label: t('pipeline.firstWin') },
                      { value: 'reorder', label: t('pipeline.reorder') },
                    ]}
                  />
                </Form.Item>
              ) : null
            }
          </Form.Item>
          <Form.Item name="isNoFollowUp" valuePropName="checked">
            <Checkbox>{t('pipeline.noFollowUp')}</Checkbox>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title={t('pipeline.editOpp')}
        open={!!editing}
        onCancel={() => { setEditing(null); editForm.resetFields() }}
        onOk={() => editForm.submit()}
        width={560}
        destroyOnClose
      >
        <Form form={editForm} layout="vertical" onFinish={handleEdit}>
          <Form.Item label={t('accounts.formName')} name="accountId" rules={[{ required: true, message: t('common.required') }]}>
            <Select
              options={accounts.map((a) => ({ value: a.id, label: `${a.market} · ${a.code} · ${a.name}` }))}
              onChange={(id) => {
                const account = accounts.find((a) => a.id === id)
                if (account) {
                  editForm.setFieldsValue({ companyName: account.name, regionCode: accountRegionCode(account) })
                }
              }}
            />
          </Form.Item>
          <Form.Item label={t('leads.company')} name="companyName" rules={[{ required: true, message: t('common.required') }]}>
            <Input />
          </Form.Item>
          <Form.Item label={t('leads.market')} name="regionCode" rules={[{ required: true, message: t('common.required') }]}>
            <Input />
          </Form.Item>
          <Form.Item label={t('products.category')} name="tags">
            <Input />
          </Form.Item>
          <Form.Item label={t('common.amount')} name="amount">
            <Input />
          </Form.Item>
          <Form.Item label={t('leads.owner')} name="ownerName">
            <Select options={users.map((u) => ({ value: u.name, label: u.name }))} />
          </Form.Item>
          <Form.Item label={t('common.stage')} name="stage" rules={[{ required: true }]}>
            <Select options={stageOptions} />
          </Form.Item>
          <Form.Item noStyle shouldUpdate={(prev, next) => prev.stage !== next.stage}>
            {({ getFieldValue }) =>
              getFieldValue('stage') === 'closedWon' ? (
                <Form.Item label={t('pipeline.winType')} name="winType">
                  <Select
                    options={[
                      { value: 'first', label: t('pipeline.firstWin') },
                      { value: 'reorder', label: t('pipeline.reorder') },
                    ]}
                  />
                </Form.Item>
              ) : null
            }
          </Form.Item>
          <Form.Item name="isNoFollowUp" valuePropName="checked">
            <Checkbox>{t('pipeline.noFollowUp')}</Checkbox>
          </Form.Item>
        </Form>
      </Modal>

      <style>{`
        .pipeline-page { --pipeline-border: #e8e4dd; }
        .pipeline-header { margin-bottom: 16px; }
        .pipeline-title-wrap { display: flex; align-items: center; gap: 12px; }
        .pipeline-badge {
          background: var(--angel-red, #ee2737);
          color: #fff;
          font-size: 12px;
          font-weight: 600;
          padding: 2px 10px;
          border-radius: 999px;
          line-height: 1.4;
        }
        .pipeline-toolbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 16px;
          margin-bottom: 20px;
          flex-wrap: wrap;
        }
        .pipeline-toolbar-left {
          display: flex;
          align-items: center;
          gap: 12px;
          flex-wrap: wrap;
        }
        .pipeline-search { width: 260px; }
        .region-chips { display: flex; gap: 8px; flex-wrap: wrap; }
        .region-chip {
          border: 1px solid var(--pipeline-border);
          background: #fff;
          color: #1f2024;
          font-weight: 700;
          font-size: 12px;
          padding: 5px 12px;
          border-radius: 6px;
          cursor: pointer;
          transition: all .15s ease;
        }
        .region-chip:hover { border-color: var(--angel-red, #ee2737); color: var(--angel-red, #ee2737); }
        .region-chip.active {
          background: var(--angel-red, #ee2737);
          border-color: var(--angel-red, #ee2737);
          color: #fff;
        }
        .pipeline-new-btn {
          background: var(--angel-red, #ee2737);
          border-color: var(--angel-red, #ee2737);
          font-weight: 600;
        }
        .pipeline-board {
          display: grid;
          grid-template-columns: repeat(5, minmax(260px, 1fr));
          gap: 16px;
          overflow-x: auto;
          padding-bottom: 8px;
        }
        .pipeline-loading { display: grid; place-items: center; min-height: 320px; }
        .pipeline-column { display: flex; flex-direction: column; gap: 12px; }
        .pipeline-column-header {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
        }
        .pipeline-column-name { font-weight: 700; font-size: 15px; color: #1f2024; }
        .pipeline-column-amount { font-size: 12px; color: var(--text-muted, #888); margin-top: 2px; }
        .pipeline-column-count {
          min-width: 24px;
          height: 24px;
          border-radius: 50%;
          background: #f0f0f0;
          color: #555;
          font-size: 12px;
          font-weight: 700;
          display: grid;
          place-items: center;
          padding: 0 6px;
        }
        .pipeline-column-cards { display: flex; flex-direction: column; gap: 10px; }
        .pipeline-subgroup { margin-bottom: 12px; }
        .pipeline-subgroup-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-size: 12px;
          color: var(--text-muted, #555);
          padding-bottom: 8px;
          border-bottom: 1px dashed var(--pipeline-border);
          margin-bottom: 10px;
        }
        .pipeline-subgroup-title { display: flex; align-items: center; gap: 6px; font-weight: 600; }
        .pipeline-subgroup-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--text-muted, #555); }
        .pipeline-card {
          background: #fff;
          border: 1px solid var(--pipeline-border);
          border-radius: 10px;
          padding: 12px;
          display: flex;
          flex-direction: column;
          gap: 6px;
          transition: box-shadow .15s ease;
        }
        .pipeline-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,.06); }
        .pipeline-card.no-follow { border-left: 3px solid var(--angel-red, #ee2737); }
        .pipeline-card-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 8px;
        }
        .pipeline-card-title { font-weight: 700; font-size: 14px; color: #1f2024; line-height: 1.3; }
        .pipeline-card-tag-red {
          background: var(--angel-red, #ee2737);
          color: #fff;
          font-size: 11px;
          font-weight: 600;
          padding: 1px 7px;
          border-radius: 4px;
          white-space: nowrap;
        }
        .pipeline-card-tag-orange {
          background: #f59e0b;
          color: #fff;
          font-size: 11px;
          font-weight: 600;
          padding: 1px 7px;
          border-radius: 4px;
          white-space: nowrap;
        }
        .pipeline-card-meta { font-size: 12px; color: var(--text-muted, #888); line-height: 1.3; }
        .pipeline-card-footer {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-top: 4px;
        }
        .pipeline-card-edit {
          width: 26px;
          height: 26px;
          border: 1px solid #ddd;
          border-radius: 6px;
          display: grid;
          place-items: center;
          color: #999;
          font-size: 12px;
          cursor: pointer;
        }
        .pipeline-card-right { display: flex; align-items: center; gap: 10px; }
        .owner-badge {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          min-width: 28px;
          height: 28px;
          border-radius: 999px;
          background: #1f2024;
          color: #fff;
          font-size: 11px;
          font-weight: 600;
          padding: 0 7px;
        }
        .pipeline-card-amount { font-weight: 700; font-size: 14px; color: #1f2024; }
        @media (max-width: 1400px) {
          .pipeline-board { grid-template-columns: repeat(5, 280px); }
        }
      `}</style>
    </div>
  )
}

function KanbanColumn({ stage, cards, onEdit }: { stage: OpportunityStage; cards: Opportunity[]; onEdit: (c: Opportunity) => void }) {
  const { t } = useI18n()
  const label = stage === 'closedWon' ? `${t('labels.oppStage.closedWon')}✓` : t(`labels.oppStage.${stage}`)
  const total = cards.reduce((sum, c) => sum + parseAmount(c.amount), 0)

  return (
    <div className="pipeline-column">
      <div className="pipeline-column-header">
        <div>
          <div className="pipeline-column-name">{label}</div>
          <div className="pipeline-column-amount">{formatAmount(total)}</div>
        </div>
        <div className="pipeline-column-count">{cards.length}</div>
      </div>
      <div className="pipeline-column-cards">
        {stage === 'closedWon' ? <ClosedWonGroups cards={cards} onEdit={onEdit} /> : cards.map((c) => <OppCard key={c.id} data={c} onEdit={onEdit} />)}
      </div>
    </div>
  )
}

function ClosedWonGroups({ cards, onEdit }: { cards: Opportunity[]; onEdit: (c: Opportunity) => void }) {
  const { t } = useI18n()
  const firstWins = cards.filter((c) => c.winType !== 'reorder')
  const reorders = cards.filter((c) => c.winType === 'reorder')

  const firstTotal = firstWins.reduce((sum, c) => sum + parseAmount(c.amount), 0)
  const reorderTotal = reorders.reduce((sum, c) => sum + parseAmount(c.amount), 0)

  return (
    <>
      {firstWins.length > 0 && (
        <div className="pipeline-subgroup">
          <div className="pipeline-subgroup-header">
            <span className="pipeline-subgroup-title">
              <span className="pipeline-subgroup-dot" />
              {t('pipeline.firstWinGroup')} · {firstWins.length}
            </span>
            <span>{formatAmount(firstTotal)}</span>
          </div>
          {firstWins.map((c) => <OppCard key={c.id} data={c} onEdit={onEdit} />)}
        </div>
      )}
      {reorders.length > 0 && (
        <div className="pipeline-subgroup">
          <div className="pipeline-subgroup-header">
            <span className="pipeline-subgroup-title">
              <span className="pipeline-subgroup-dot" style={{ background: '#f59e0b' }} />
              {t('pipeline.reorderGroup')} · {reorders.length}
            </span>
            <span>{formatAmount(reorderTotal)}</span>
          </div>
          {reorders.map((c) => <OppCard key={c.id} data={c} onEdit={onEdit} />)}
        </div>
      )}
    </>
  )
}

function OppCard({ data, onEdit }: { data: Opportunity; onEdit: (c: Opportunity) => void }) {
  const { t } = useI18n()
  return (
    <div className={`pipeline-card ${data.isNoFollowUp ? 'no-follow' : ''}`}>
      <div className="pipeline-card-row">
        <div className="pipeline-card-title">{data.companyName}</div>
        {data.isNoFollowUp && <span className="pipeline-card-tag-red">{t('pipeline.noFollowUp')}</span>}
        {data.winType === 'reorder' && <span className="pipeline-card-tag-orange">{t('pipeline.reorder')}</span>}
      </div>
      <div className="pipeline-card-meta">{data.regionCode}</div>
      <div className="pipeline-card-meta">{data.tags}</div>
      <div className="pipeline-card-footer">
        <span className="pipeline-card-edit" onClick={() => onEdit(data)}>
          <EditOutlined />
        </span>
        <div className="pipeline-card-right">
          <span className="owner-badge">{data.ownerName}</span>
          <span className="pipeline-card-amount">{data.amount}</span>
        </div>
      </div>
    </div>
  )
}
