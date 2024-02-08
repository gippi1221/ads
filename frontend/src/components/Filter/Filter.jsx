import React, { useContext } from 'react'
import { Button, DatePicker, Form, Radio, Select, Space, Input } from 'antd'
import dayjs from 'dayjs'
import { Context } from '../..'
import { MinusCircleOutlined, PlusOutlined, FireOutlined } from '@ant-design/icons'
const Filter = () => {

  const { general } = useContext(Context)
  const [form] = Form.useForm()

  const onFinish = (values) => {
    const params = {
      granularity: values.granularity,
      groupBy: values.attributes ? values.attributes.join(',') : undefined,
      metrics: values.metrics ? values.metrics.join(',') : undefined,
    }

    if (values.date_range && values.date_range[0]) {
      params.startDate = dayjs(values.date_range[0]).format('YYYY-MM-DDTHH:mm:ss')
    }

    if (values.date_range && values.date_range[1]) {
      params.endDate = dayjs(values.date_range[1]).format('YYYY-MM-DDTHH:mm:ss')
    }

    if (values.filters && values.filters.length) {
      params.filters = JSON.stringify(values.filters)
    }

    general.setParams(params)
    
  }

  return (
    <Form
      name='filters'
      form={form}
      size='small'
      onFinish={onFinish}
      requiredMark='optional'
      labelCol={{
        span: 4,
      }}
    >
      <Form.Item
        name='granularity'
        initialValue='daily'
        label='Granularity'
        rules={[{required: true, message: 'Input value here'}]}
      >
        <Radio.Group optionType='button' buttonStyle='solid'>
          <Radio value='hourly'>Hourly</Radio>
          <Radio value='daily'>Daily</Radio>
        </Radio.Group>
      </Form.Item>

      <Form.Item
        name='date_range'
        label='Date Range'
      >
        <DatePicker.RangePicker showTime />
      </Form.Item>

      <Form.Item
        name='metrics'
        label='Metrics'
        rules={[{required: true, message: 'Input value here'}]}
        initialValue={['metric1','metric2']}
      >
        <Select
          mode="multiple"
          allowClear
          style={{ width: '100%' }}
          placeholder="Please select"
          options={[
            {value: 'metric1', label: 'metric1'},
            {value: 'metric2', label: 'metric2'},
          ]}
        />
      </Form.Item>

      <Form.Item
        name='attributes'
        label='Group By'
        rules={[{required: true, message: 'Input value here'}]}
        initialValue={['attribute1']}
      >
        <Select
          mode="multiple"
          allowClear
          style={{ width: '100%' }}
          placeholder="Please select"
          options={[
            {value: 'attribute1', label: 'attribute1'},
            {value: 'attribute2', label: 'attribute2'},
            {value: 'attribute3', label: 'attribute3'},
            {value: 'attribute4', label: 'attribute4'},
            {value: 'attribute5', label: 'attribute5'},
            {value: 'attribute6', label: 'attribute6'},
          ]}
        />
      </Form.Item>

      <Form.List name="filters">
        {(fields, { add, remove }) => (
          <>
            {fields.map(({ key, name, ...restField }) => (
              <div key={key} style={{ display: 'flex', marginBottom: 8, width: '100%', gap: 24, alignItems: 'center' }}>
                <Form.Item
                  {...restField}
                  name={[name, 'attribute']}
                  rules={[{ required: true, message: 'Input value here' }]}
                  style={{ flex: 1, marginBottom: 0 }}
                >
                  <Select
                    placeholder="Please select"
                    options={[
                      {value: 'attribute1', label: 'attribute1'},
                      {value: 'attribute2', label: 'attribute2'},
                      {value: 'attribute3', label: 'attribute3'},
                      {value: 'attribute4', label: 'attribute4'},
                      {value: 'attribute5', label: 'attribute5'},
                      {value: 'attribute6', label: 'attribute6'},
                    ]}
                  />
                </Form.Item>
                <Form.Item
                  {...restField}
                  name={[name, 'value']}
                  rules={[{ required: true, message: 'Input value here' }]}
                  style={{ flex: 1, marginBottom: 0 }}
                >
                  <Input placeholder="Value" />
                </Form.Item>
                <MinusCircleOutlined onClick={() => remove(name)} />
              </div>
            ))}
            <Form.Item>
              <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                Add field
              </Button>
            </Form.Item>
          </>
        )}
      </Form.List>

      <div>
        <Form.Item>
          <Button size='large' type='primary' icon={ <FireOutlined /> } htmlType='submit' style={{ width: '100%' }}>Apply</Button>
        </Form.Item>
      </div>
    </Form>
  )
}

export default Filter