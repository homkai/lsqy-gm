import React, { Component } from 'react';
import {formatColor, formatCornerName} from './tool';
import { Modal, Radio } from 'antd';
const RadioGroup = Radio.Group;


export default class extends Component {
  state = {value: null}

  handleOk = (e) => {
    const {cornerName, cellName, onChangeCellCorner} = this.props;
    onChangeCellCorner({cellName, cornerName}, this.state.value === 'gray' ? null : this.state.value);
  }

  handleCancel = (e) => {
    const {cornerName, color, cellName, onChangeCellCorner} = this.props;
    onChangeCellCorner({cellName, cornerName}, color);
  }

  handleChange = (e) => {
    this.setState({
      value: e.target.value
    });
  }

  render() {
    const {cornerName, color} = this.props;
    const value = this.state.value || color;

    return (
      <div>
        <Modal
          title="改变装备四角颜色"
          visible={true}
          onOk={this.handleOk}
          onCancel={this.handleCancel}
        >
          <p>你可以改变本装备{formatCornerName(cornerName)}颜色：</p>
          <div>
            <RadioGroup onChange={this.handleChange} value={value}>
              <Radio value={'red'}><span color={formatColor('red')}>红</span></Radio>
              <Radio value={'green'}><span color={formatColor('green')}>绿</span></Radio>
              <Radio value={'yellow'}><span color={formatColor('yellow')}>黄</span></Radio>
              <Radio value={'blue'}><span color={formatColor('blue')}>蓝</span></Radio>
              <Radio value={'gray'}><span color={formatColor('gray')}>放弃</span></Radio>
            </RadioGroup>
          </div>
        </Modal>
      </div>
    );
  }
}