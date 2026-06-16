import { Card, Typography } from 'antd'
import { pageTitles } from '../mocks/crmData'

const { Text, Title } = Typography

export function PlaceholderPage({ title }: { title: string }) {
  return (
    <div className="crm-page">
      <div className="crm-page-header">
        <div className="crm-page-header-left">
          <div className="crm-page-header-title">{pageTitles[title as keyof typeof pageTitles] ?? title}</div>
          <div className="crm-page-header-desc">该页面正在持续完善中。</div>
        </div>
      </div>
      <Card>
        <Title level={5}>敬请期待</Title>
        <Text className="text-secondary">当前为高保真复刻过渡页，后续将补充完整交互与数据。</Text>
      </Card>
    </div>
  )
}
