import React, { Component } from 'react';
import {formatColor, formatCornerName} from './tool';
import { Modal, Radio } from 'antd';
import _ from 'lodash';

const RadioGroup = Radio.Group;

const GRAY = 'gray'


export default class extends Component {
  state = {values: null}

  handleOk = (e) => {
    const {baseCellsIndex, onChangeCellCorner} = this.props;
    onChangeCellCorner({baseCellsIndex}, _.mapValues(this.state.values, item => item === GRAY ? null : item));
  }

  handleCancel = (e) => {
    const {colors, baseCellsIndex, onChangeCellCorner} = this.props;
    onChangeCellCorner({baseCellsIndex}, colors);
  }

  handleChange = (cornerName, e) => {
    const values = this.state.values || this.props.colors;
    this.setState({
      values: {
        ...values,
        [cornerName]: e.target.value
      }
    });
  }

  render() {
    const {colors} = this.props;
    const values = this.state.values || colors;

    return (
      <div>
        <Modal
          title="改变装备四角颜色"
          visible={true}
          onOk={this.handleOk}
          onCancel={this.handleCancel}
          className="cell-conner-modal"
          width={810}
        >
          <p>你可以改变本装备四角颜色：</p>
          <div>
            {
              ['tl', 'tr', 'bl', 'br'].map(cornerName => <div className="control-row" key={cornerName}>
                <b className="label">{formatCornerName(cornerName)}</b>
                <RadioGroup className="control" onChange={_.partial(this.handleChange, cornerName)} value={values[cornerName] || GRAY}>
                  <Radio value={'red'}><span color={formatColor('red')}>红</span></Radio>
                  <Radio value={'green'}><span color={formatColor('green')}>绿</span></Radio>
                  <Radio value={'yellow'}><span color={formatColor('yellow')}>黄</span></Radio>
                  <Radio value={'blue'}><span color={formatColor('blue')}>蓝</span></Radio>
                  <Radio value={GRAY}><span color={formatColor('gray')}>放弃</span></Radio>
                </RadioGroup>
              </div>)
            }
          </div>
        </Modal>
      </div>
    );
  }
}