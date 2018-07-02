import React, { Component } from 'react';
import _ from 'lodash';
import logo from './logo.svg';
import './App.css';
import { Button, Alert, Select, Upload, Icon, Tooltip, Modal } from 'antd';
import demoGm from './gm_bg.jpg';
import rewardPic from './reward.jpg';

import Cell from './Cell';
import CellCornerModal from './CellCornerModal';

import {walkCells, cellsForWalk, formatColor, getPlanCells, getTopList, defaultCells} from './tool';
import combinatorics from './combinatorics';

const Option = Select.Option;

const initialPositions = _.fill(Array(9)).map((item, index) => index);

class App extends Component {
  state = {
    baseCells: [],
    showCellCornerModal: false,
    cellCornerModalProps: {},
    positions: initialPositions,
    topList: [],
    message: null,
    calcDisabled: false,
    grade: 60,
    sort: ['total', 'red'],
    uploadDisabled: false,
    showReward: false
  }

  async componentDidMount() {
    // const cells = await fetch('http://127.0.0.1:8080/cells2.json');
    this.setState({
      // baseCells: await cells.json(),
      baseCells: [], // JSON.parse(json),
      message: {
        type: 'info',
        content: <span>
          已大幅提升装备共鸣截图识别成功率，如还失败，可以切换到手动模式。
          欢迎到<a target="_blank" rel="noopener noreferrer" href="http://tieba.baidu.com/p/5768717398?pid=120516839719"> 贴吧 </a>
          讨论。<a target="_blank" rel="noopener noreferrer" href="https://github.com/homkai/lsqy-gm/"> GitHub </a>
          可以一起完善
        </span>
      }
    });
  }

  handleClickCellCorner = props => {
    this.setState({
      showCellCornerModal: true,
      cellCornerModalProps: props
    })
  }

  handleChangeCellCorner = ({baseCellsIndex}, colors) => {
    const baseCells = this.state.baseCells.map((item, index) => {
      return index !== baseCellsIndex ? item : {
        ...item,
        ...colors
      };
    });
    this.setState({
      baseCells,
      showCellCornerModal: false,
      cellCornerModalProps: {}
    });
  }

  handleWalk = () => {
    const {baseCells, grade, sort} = this.state;
    const liteCells = cellsForWalk(baseCells);
    if (liteCells.some(item => item.filter(test => test === null).length % 4)) {
      clearTimeout(this.clearError);
      this.setState({
        message: {
          type: 'error',
          content: '请补充完整装备四角颜色！'
        }
      });
      this.clearError = setTimeout(() => this.setState({
        message: null
      }), 3000);
      return;
    }
    this.setState({
      calcDisabled: true,
      message: {
        type: 'info',
        content: '正在计算，请耐心等待...'
      }
    });
    setTimeout(() => {
      const plans = []
      combinatorics.permutation(liteCells).forEach(cells => {
        plans.push(walkCells(cells, grade));
      });

      const topList = getTopList(plans, sort);
      this.setState({
        topList,
        positions: topList.length ? topList[0].positions : [],
        calcDisabled: false,
        message: {
          type: 'success',
          content: '点击方案，可查看装备排列方式'
        }
      });
      this.plans = plans;
    }, 100);
  }

  handleShowPlan = plan => {
    this.setState({positions: plan.positions});
  }

  handleSelectGrade = value => {
    this.setState({
      grade: value,
      positions: initialPositions,
      topList: [],
    });
  }

  handleSelectSort0 = value => {
    const sort = [value, this.state.sort[1]];
    if (!this.plans) {
      this.setState({sort});
      return;
    }
    const topList = getTopList(this.plans, sort);
    this.setState({
      sort,
      topList,
      positions: topList.length ? topList[0].positions : []
    });
  }

  handleSelectSort1 = value => {
    const sort = [this.state.sort[0], value];
    if (!this.plans) {
      this.setState({sort});
      return;
    }
    const topList = getTopList(this.plans, sort);
    this.setState({
      sort,
      topList,
      positions: topList.length ? topList[0].positions : []
    });
  }

  handleUploadEqp = ({file: {status, response}}) => {
    if (~['removed'].indexOf(status)) {
      this.setState({
        uploadDisabled: false
      });
    }
    else {
      this.setState({
        uploadDisabled: true
      });
      if (status === 'done') {
        this.setState({
          baseCells: response,
          message: {
            type: 'info',
            content: '请验证自动分析的结果是否匹配，点击装备四角可更改颜色。'
          }
        })
      }
    }
  }

  handleToggleRewardModal = () => {
    this.setState({
      showReward: !this.state.showReward
    })
  }

  handleSetDefaultCells = () => {
    this.setState({
      baseCells: JSON.parse(defaultCells),
      message: {
        type: 'warning',
        content: '请点击装备更改四角颜色'
      }
    })
  }



  render() {
    const {baseCells, positions, showCellCornerModal, cellCornerModalProps, topList,
      message, calcDisabled, grade, sort, uploadDisabled, showReward} = this.state;
    const onClickCellCorner = this.handleClickCellCorner;
    const onChangeCellCorner = this.handleChangeCellCorner;
    const cells = baseCells.length ? getPlanCells(baseCells, positions, grade) : [];

    return (
      <div className="App">
        {showCellCornerModal && <CellCornerModal {...{...cellCornerModalProps, onChangeCellCorner}}/>}
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">欢迎使用灵山奇缘-装备共鸣模拟器</h1>
        </header>
        <main>
          {!!message && <Alert message={message.content} type={message.type} showIcon />}
          {
            !!cells.length ? <div className="gm-cells">
              <div className="gm-row gm-row-t">
                <Cell {...{...cells[0], onClickCellCorner}}/>
              </div>
              <div className="gm-row gm-row-td">
                <Cell {...{...cells[1], onClickCellCorner}}/>
                <Cell {...{...cells[2], onClickCellCorner}}/>
              </div>
              <div className="gm-row gm-row-m">
                <Cell {...{...cells[3], onClickCellCorner}}/>
                <Cell {...{...cells[4], onClickCellCorner}}/>
                <Cell {...{...cells[5], onClickCellCorner}}/>
              </div>
              <div className="gm-row gm-row-bd">
                <Cell {...{...cells[6], onClickCellCorner}}/>
                <Cell {...{...cells[7], onClickCellCorner}}/>
              </div>
              <div className="gm-row gm-row-b">
                <Cell {...{...cells[8], onClickCellCorner}}/>
              </div>
            </div> : <div className="gm-cells-empty">
              <h2>打开装备共鸣窗口，如下截图后，右侧上传 >></h2>
              <p><img width="300" src={demoGm} alt="示例截图"/></p>
              <Button onClick={this.handleSetDefaultCells}>手动录入模式</Button>
            </div>
          }
          <div className="gm-calc">
            <Upload {...{
              accept: '.jpg,.jpeg',
              action: 'http://api.homkai.com:8001/eqprecog/upload',
              listType: 'picture',
              defaultFileList: [],
              onChange: this.handleUploadEqp,
              withCredentials: true,
              disabled: uploadDisabled
            }}>
              <Tooltip placement="top" title={uploadDisabled ? '请先删除已上传的图片' : 'JPG格式100KB以内'}>
                <Button>
                  <Icon type="upload" /> 上传装备共鸣窗口截图
                </Button>
              </Tooltip>
            </Upload>
            <Select className="grade-select" value={grade} onChange={this.handleSelectGrade}>
              <Option value={50}>50级（解锁7个槽位）</Option>
              <Option value={60}>60级（解锁全部槽位）</Option>
            </Select>
            <br />
            <Button className="calc-btn" type="primary" disabled={calcDisabled || !cells.length} onClick={this.handleWalk}>
              计算最优解
            </Button>
            <br />
            <Select key={0} value={sort[0]} stype={{width: 100}} onChange={this.handleSelectSort0}>
              <Option value="total">优先：总数</Option>
              <Option value="red">优先：攻击</Option>
              <Option value="green">优先：防御</Option>
              <Option value="yellow">优先：速度</Option>
              <Option value="blue">优先：气血</Option>
            </Select>
            <Select key={1} value={sort[1]} stype={{width: 100}} onChange={this.handleSelectSort1}>
              <Option value="total">其次：总数</Option>
              <Option value="red">其次：攻击</Option>
              <Option value="green">其次：防御</Option>
              <Option value="yellow">其次：速度</Option>
              <Option value="blue">其次：气血</Option>
            </Select>
            {
              !!topList.length && <ul className="top-plan-list">
                {
                  topList.map(plan => <li title="点击查看方案" key={plan.positions} onClick={_.partial(this.handleShowPlan, plan)}>
                    <div><strong>总连线数：{plan.total}</strong></div>
                    <div className="line-count" style={{color: formatColor('red')}}>攻击：{plan.red}</div>
                    <div className="line-count" style={{color: formatColor('green')}}>防御：{plan.green}</div>
                    <div className="line-count" style={{color: formatColor('yellow')}}>速度：{plan.yellow}</div>
                    <div className="line-count" style={{color: formatColor('blue')}}>气血：{plan.blue}</div>
                  </li>)
                }
              </ul>
            }
            {
              !!topList.length && <div className="plan-btm"><a href="javascript:;" onClick={this.handleToggleRewardModal}>打赏支持一下</a></div>
            }
            {
              showReward && <Modal
                className="reward-modal"
                title="微信扫码打赏"
                visible={true}
                onCancel={this.handleToggleRewardModal}
                footer={null}
              >
                <img className="reward-pic" src={rewardPic} alt="微信打赏图片"/>
              </Modal>
            }
          </div>
        </main>
      </div>
    );
  }
}

export default App;
