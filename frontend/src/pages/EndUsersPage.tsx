import { Button, Card, Table } from 'antd'
import { useGlobalMessage } from '../hooks/useGlobalMessage'
import { useI18n } from '../hooks/useI18n'
import { endUsers, getAccountById } from '../mocks/crmData'

export function EndUsersPage() {
  const { t } = useI18n()
  const { info } = useGlobalMessage()
  return (
    <div className="crm-page">
      <div className="crm-page-header">
        <div className="crm-page-header-left">
          <div className="crm-page-header-title">{t('endUsers.title')}</div>
          <div className="crm-page-header-desc">{t('endUsers.subtitle')}</div>
        </div>
        <Button type="primary" onClick={() => info(t('common.devToast'))}>{t('endUsers.create')}</Button>
      </div>

      <Card>
        <Table
          dataSource={endUsers}
          rowKey="id"
          pagination={false}
          columns={[
            { title: t('endUsers.name'), dataIndex: 'name' },
            { title: t('endUsers.account'), dataIndex: 'accountId', render: (id) => getAccountById(id)?.name },
            { title: t('endUsers.location'), dataIndex: 'location' },
            { title: t('endUsers.installs'), dataIndex: 'units' },
            { title: t('endUsers.installDate'), dataIndex: 'installDate' },
            { title: t('endUsers.lastService'), dataIndex: 'lastService' },
          ]}
        />
      </Card>
    </div>
  )
}
