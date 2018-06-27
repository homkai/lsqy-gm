import React from 'react';
import _ from 'lodash';
import {formatColor} from './tool';

const CellCorner = ({cellName, cornerName, color, lls, lrs, onClickCellCorner}) => {
  return <div>
    <div
      className={'gm-cell-corner gm-cell-corner-' + cornerName}
      onClick={_.partial(onClickCellCorner, {cellName, cornerName, color})}
      style={{borderRightColor: formatColor(color)}}
    />
    {
      cornerName === 'bl' && lls && <div
        className="gm-cell-corner-line gm-cell-corner-line-l"
        style={{borderTopColor: formatColor(color)}}
      />
    }
    {
      cornerName === 'br' && lrs && <div
        className="gm-cell-corner-line gm-cell-corner-line-r"
        style={{borderTopColor: formatColor(color)}}
      />
    }
  </div>;
}

export default ({name, core, tl, tr, bl, br, lls, lrs, onClickCellCorner}) => {
  return <div className="gm-cell">
    <CellCorner {...{cellName: name, cornerName: 'tl', color: tl, lls, lrs, onClickCellCorner}}/>
    <CellCorner {...{cellName: name, cornerName: 'tr', color: tr, lls, lrs, onClickCellCorner}}/>
    <CellCorner {...{cellName: name, cornerName: 'bl', color: bl, lls, lrs, onClickCellCorner}}/>
    <CellCorner {...{cellName: name, cornerName: 'br', color: br, lls, lrs, onClickCellCorner}}/>
    <div className="gm-cell-core"
         style={{background: 'url(' + core + ') no-repeat'}}
    />
  </div>;
}